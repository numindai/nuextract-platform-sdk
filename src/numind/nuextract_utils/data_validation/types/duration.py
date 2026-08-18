"""Duration class."""

from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation
from typing import TYPE_CHECKING

from .base import SemanticType

if TYPE_CHECKING:
    from numind.nuextract_utils.data_validation.models import ErrorJson

ERR_LABEL_DURATION_VALUE_NOT_ISO_8601_COMPLIANT = (
    "label duration value not ISO 8601 compliant"
)

# A comprehensive regex for the ISO 8601 duration format PnYnMnDTnHnMnS
# It uses named groups for clarity.
ISO_8601_DURATION_REGEX = re.compile(
    r"^P"
    r"(?:(?P<Y>\d+)Y)?"
    r"(?:(?P<M_date>\d+)M)?"
    r"(?:(?P<W>\d+)W)?"
    r"(?:(?P<D>\d+)D)?"
    r"(?:T"
    r"(?:(?P<H>\d+)H)?"
    r"(?:(?P<M_time>\d+)M)?"
    r"(?:(?P<S>\d+(?:[.,]\d+)?)S)?"
    r")?$"
)

# Mapping from full text component names to their ISO 8601 designators
TEXTUAL_DURATION_COMPONENTS = {
    "Y": ("year", "years"),
    "M_date": ("month", "months"),
    "W": ("week", "weeks"),
    "D": ("day", "days"),
    "H": ("hour", "hours"),
    "M_time": ("minute", "minutes"),
    "S": ("second", "seconds"),
}


# --- New Duration Class and Functions ---


class Duration(SemanticType):
    """
    An ISO 8601 compliant duration string ("PnYnMnDTnHnMnS" where "n" are integers).

    It contains a date and a time parts separated with a "T" character, which contain
    several components: "nY" for years, "nM" for months (in the date part), "nW" for
    weeks (cannot be combined with "Y"/"M"/"D" in the same string), "nD" for days, "T"
    is the separator before time components, "nH" for hours, "nM" for minutes (in the
    time part), "nS" for seconds (may include decimals, e.g. "PT0.5S").
    The duration string might feature "reduced accuracy" by combining the enumerated
    components in the same order, except the "PnW" component which cannot be mixed with
    teh other date components ("Y"/"M"/"D").

    :examples: `P2Y1M3D` (2 years, 1 month, 3 days), `PT1M30S` (1 minute, 30 seconds),
    `P3W` (3 weeks)
    """

    @classmethod
    def coerce(
        cls, value: str, input_text: str | None = None, error: ErrorJson | None = None
    ) -> str | None:
        """
        Try to correct a malformed duration string to make it ISO 8601 compliant.

        :param value: string duration to make ISO compliant.
        :param input_text: input text.
        :param error: error (not used here).
        :return: a string ISO 8601 compliant duration if the provided value can be
            converted, otherwise ``None``.
        """
        _ = input_text
        _ = error
        return string_to_iso8601_duration(value)

    @staticmethod
    def validate(value: str, _: str | None = None) -> str | None:
        """
        Check that a string complies to the ISO 8601 duration standard.

        :param value: duration string to validate.
        :param _: placeholder for input text.
        :return: error message if the value is not ISO 8601 compliant, otherwise
            ``None``.
        """
        if string_to_iso8601_duration(value) != value:
            return ERR_LABEL_DURATION_VALUE_NOT_ISO_8601_COMPLIANT
        return None


def detect_duration_components(s: str) -> dict[str, Decimal] | None:
    """
    Detect and extract components from a strictly compliant ISO 8601 duration string.

    The string must be strictly compliant to be parsed, otherwise the method returns
    ``None``. For example, 'P1Y' is valid, but '1Y' or 'P 1Y' are not.

    :param s: duration string to analyze.
    :return: A dictionary mapping the component name to its value (Decimal),
        or ``None`` if the string is not a valid ISO 8601 duration.
    """
    if not isinstance(s, str) or not s:
        return None

    match = ISO_8601_DURATION_REGEX.match(s)
    if not match:
        return None

    components = {
        # FIX: Replace comma with period before passing to Decimal constructor.
        key: Decimal(value.replace(",", "."))
        for key, value in match.groupdict().items()
        if value
    }

    # An empty duration 'P' or 'PT' is not valid. At least one component must be present
    if not components:
        return None

    return components


def _try_to_deduce_duration_components(s: str) -> dict[str, Decimal] | None:
    """
    Try to deduce duration components from a non-standard string.

    This version robustly parses textual and mixed-format duration strings.
    """
    if not isinstance(s, str):
        return None

    s_work = s.strip()
    if not s_work:
        return None

    components = {}

    try:
        # Step 1: Parse and remove all textual components first.
        text_to_designator = {}
        # Use temporary designators for Month/Minute to resolve ambiguity
        temp_map = {"M_date": "M_D", "M_time": "M_T"}
        for key, names in TEXTUAL_DURATION_COMPONENTS.items():
            designator = temp_map.get(key, key)
            for name in names:
                text_to_designator[name] = designator

        # Sort by length (desc) to match "seconds" before "second"
        sorted_units = sorted(text_to_designator.keys(), key=len, reverse=True)
        text_units_pattern = "|".join(re.escape(unit) for unit in sorted_units)
        text_pattern = re.compile(
            r"(\d+(?:[.,]\d+)?)\s*(" + text_units_pattern + r")\b", re.IGNORECASE
        )

        s_remaining = s_work
        # Use finditer and iterate backwards to safely remove matched parts
        matches = list(text_pattern.finditer(s_work))
        for match in reversed(matches):
            value_str, unit_text = match.groups()
            designator = text_to_designator[unit_text.lower()]

            current_val = components.get(designator, Decimal(0))
            components[designator] = current_val + Decimal(value_str.replace(",", "."))

            # Remove the matched part from the string
            s_remaining = s_remaining[: match.start()] + s_remaining[match.end() :]

        # Step 2: Translate temporary designators back to final ones
        if "M_D" in components:
            components["M_date"] = components.get(
                "M_date", Decimal(0)
            ) + components.pop("M_D")
        if "M_T" in components:
            components["M_time"] = components.get(
                "M_time", Decimal(0)
            ) + components.pop("M_T")

        # Step 3: Parse the remaining non-textual part of the string.
        s_remaining = "".join(s_remaining.split()).lower().lstrip("p")

        date_part_str = s_remaining
        time_part_str = ""
        if "t" in s_remaining:
            parts = s_remaining.split("t", 1)
            date_part_str, time_part_str = parts[0], parts[1]

        iso_pattern = re.compile(r"(\d+(?:[.,]\d+)?)([ymwdhs])")

        # Parse date part: 'm' is a month.
        for value, designator in iso_pattern.findall(date_part_str):
            key = None
            if designator == "y":
                key = "Y"
            elif designator == "w":
                key = "W"
            elif designator == "d":
                key = "D"
            elif designator == "m":
                key = "M_date"
            elif designator == "h":
                key = "H"
            elif designator == "s":
                key = "S"

            if key:
                current_val = components.get(key, Decimal(0))
                components[key] = current_val + Decimal(value.replace(",", "."))

        # Parse time part: 'm' is a minute.
        for value, designator in iso_pattern.findall(time_part_str):
            key = None
            if designator == "h":
                key = "H"
            elif designator == "s":
                key = "S"
            elif designator == "m":
                key = "M_time"

            if key:
                current_val = components.get(key, Decimal(0))
                components[key] = current_val + Decimal(value.replace(",", "."))

    except (InvalidOperation, TypeError):
        return None

    return components if components else None


def convert_duration_components_to_string(components: dict[str, Decimal]) -> str | None:
    """
    Format a dictionary of duration components into an ISO 8601 compliant string.

    This version correctly adds the 'T' separator and formats numbers robustly.
    """
    if not components:
        return None

    # Helper to format decimal values robustly.
    def format_decimal(d: Decimal) -> str:
        # If the number has no fractional part, format as a simple integer.
        # This avoids issues with f-string float formatting and rstrip on integers.
        if d == d.to_integral_value():
            return str(d.to_integral_value())
        # Otherwise, format as a float and remove unnecessary trailing zeros.
        return f"{d:f}".rstrip("0").rstrip(".")

    # Reorder components to be ISO 8601 compliant
    ordered_components = {
        k: components[k]
        for k in ["Y", "M_date", "W", "D", "H", "M_time", "S"]
        if k in components
    }

    # Check for invalid mixing of weeks with other date components
    has_week = "W" in ordered_components
    has_other_date = any(k in ordered_components for k in ["Y", "M_date", "D"])
    if has_week and has_other_date:
        return None  # ISO 8601 forbids mixing W with Y, M, D

    # Find the smallest unit to allow for fractional values
    smallest_unit = None
    for unit in reversed(["Y", "M_date", "W", "D", "H", "M_time", "S"]):
        if unit in ordered_components:
            smallest_unit = unit
            break

    def format_value(key: str, value: Decimal) -> str | None:
        # Only the smallest unit can have a fractional part
        if key != smallest_unit and value % 1 != 0:
            return None
        # Use the robust formatting helper
        return format_decimal(value)

    date_parts = []
    time_parts = []

    for key, value in ordered_components.items():
        formatted_val = format_value(key, value)
        if formatted_val is None:
            return None

        if key == "Y":
            date_parts.append(f"{formatted_val}Y")
        elif key == "M_date":
            date_parts.append(f"{formatted_val}M")
        elif key == "W":
            date_parts.append(f"{formatted_val}W")
        elif key == "D":
            date_parts.append(f"{formatted_val}D")
        elif key == "H":
            time_parts.append(f"{formatted_val}H")
        elif key == "M_time":
            time_parts.append(f"{formatted_val}M")
        elif key == "S":
            time_parts.append(f"{formatted_val}S")

    result = "P"
    result += "".join(date_parts)

    if time_parts:
        result += "T" + "".join(time_parts)

    # A valid duration must have at least one component, and not be just "P" or "PT"
    return result if len(result) > 1 and result != "PT" else None


def string_to_iso8601_duration(duration_str: str) -> str | None:
    """
    Try to convert a string to its closest ISO 8601 compliant duration equivalent.

    Examples:
        "P1Y2M3DT4H5M6S" -> "P1Y2M3DT4H5M6S"
        "PT1M30.5S" -> "PT1M30.5S"
        "p1y" -> "P1Y"
        "1Y 2M" -> "P1Y2M"
        "3 weeks" -> "P3W"
        "P1D 12H" -> "P1DT12H"
        "1 year 6 months" -> "P1Y6M"
        "PT100S" -> "PT100S"
        "Invalid" -> None

    :param duration_str: String to convert.
    :return: The closest ISO 8601 compliant equivalent of the input string, or ``None``
        if no conversion can be performed.

    """
    # First, try to parse with the strict method
    components = detect_duration_components(duration_str)

    # If parsing fails, try the more lenient deduction method
    if components is None:
        components = _try_to_deduce_duration_components(duration_str)

    # If components were successfully extracted by either method, format them
    if components:
        return convert_duration_components_to_string(components)

    return None
