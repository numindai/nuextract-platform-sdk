"""Date, time, and date-time formats."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from time import strptime
from typing import TYPE_CHECKING

from .base import SemanticType

if TYPE_CHECKING:
    from numind.nuextract_utils.data_validation.models import ErrorJson

_CURRENT_YEAR = datetime.now(timezone.utc).year
ERR_LABEL_DATE_VALUE_NOT_ISO_8601_COMPLIANT = "label date value not ISO 8601 compliant"
ERR_LABEL_TIME_VALUE_NOT_ISO_8601_COMPLIANT = "label time value not ISO 8601 compliant"
ERR_LABEL_DATETIME_VALUE_NOT_ISO_8601_COMPLIANT = (
    "label date-time value not ISO 8601 compliant"
)
ERR_LABEL_DATETIME_TIME_PART_ALL_ZEROS = "label date-time has time part with all zeros"

# Patterns for ISO 8601.
# A string has to strictly comply to one of them to be ISO 8601 compliant
TIMEZONE_REGEX = r"(?:(Z|[+-]\d{2}(?::?\d{2})?))?"
_DATETIME_PATTERNS = [
    (
        "YYYY-MM-DDThh:mm:ss.s",
        re.compile(
            rf"^(-?\d{{4}})-(\d{{2}})-(\d{{2}})T(\d{{2}}):(\d{{2}}):(\d{{2}})\.(\d+){TIMEZONE_REGEX}$"
        ),
        ["YYYY", "MM", "DD", "hh", "mm", "ss", "s", "TZ"],
    ),
    (
        "YYYY-Www-DThh:mm:ss.s",
        re.compile(
            rf"^(-?\d{{4}})-W(\d{{2}})-(\d)T(\d{{2}}):(\d{{2}}):(\d{{2}})\.(\d+){TIMEZONE_REGEX}$"
        ),
        ["YYYY", "Www", "D", "hh", "mm", "ss", "s", "TZ"],
    ),
    (
        "YYYY-MM-DDThh:mm:ss",
        re.compile(
            rf"^(-?\d{{4}})-(\d{{2}})-(\d{{2}})T(\d{{2}}):(\d{{2}}):(\d{{2}}){TIMEZONE_REGEX}$"
        ),
        ["YYYY", "MM", "DD", "hh", "mm", "ss", "TZ"],
    ),
    (
        "YYYY-Www-DThh:mm:ss",
        re.compile(
            rf"^(-?\d{{4}})-W(\d{{2}})-(\d)T(\d{{2}}):(\d{{2}}):(\d{{2}}){TIMEZONE_REGEX}$"
        ),
        ["YYYY", "Www", "D", "hh", "mm", "ss", "TZ"],
    ),
    (
        "YYYY-MM-DDThh:mm",
        re.compile(
            rf"^(-?\d{{4}})-(\d{{2}})-(\d{{2}})T(\d{{2}}):(\d{{2}}){TIMEZONE_REGEX}$"
        ),
        ["YYYY", "MM", "DD", "hh", "mm", "TZ"],
    ),
    (
        "YYYY-Www-DThh:mm",
        re.compile(
            rf"^(-?\d{{4}})-W(\d{{2}})-(\d)T(\d{{2}}):(\d{{2}}){TIMEZONE_REGEX}$"
        ),
        ["YYYY", "Www", "D", "hh", "mm", "TZ"],
    ),
    (
        "YYYY-MM-DDThh",
        re.compile(rf"^(-?\d{{4}})-(\d{{2}})-(\d{{2}})T(\d{{2}}){TIMEZONE_REGEX}$"),
        ["YYYY", "MM", "DD", "hh", "TZ"],
    ),
    (
        "YYYY-Www-DThh",
        re.compile(rf"^(-?\d{{4}})-W(\d{{2}})-(\d)T(\d{{2}}){TIMEZONE_REGEX}$"),
        ["YYYY", "Www", "D", "hh", "TZ"],
    ),
]

_DATE_PATTERNS = [
    ("YYYY-MM-DD", re.compile(r"^(-?\d{4})-(\d{2})-(\d{2})$"), ["YYYY", "MM", "DD"]),
    ("YYYY-MM", re.compile(r"^(-?\d{4})-(\d{2})$"), ["YYYY", "MM"]),
    ("YYYY-Www-D", re.compile(r"^(-?\d{4})-W(\d{2})-(\d)$"), ["YYYY", "Www", "D"]),
    ("YYYY-Www", re.compile(r"^(-?\d{4})-W(\d{2})$"), ["YYYY", "Www"]),
    ("YYYY", re.compile(r"^(-?\d{4})$"), ["YYYY"]),
    ("--MM-DD", re.compile(r"^--(\d{2})-(\d{2})$"), ["MM", "DD"]),
    ("--MM", re.compile(r"^--(\d{2})$"), ["MM"]),
    ("---DD", re.compile(r"^---(\d{2})$"), ["DD"]),
]

_TIME_PATTERNS = [
    (
        "hh:mm:ss.s",
        re.compile(rf"^(\d{{2}}):(\d{{2}}):(\d{{2}})\.(\d+){TIMEZONE_REGEX}$"),
        ["hh", "mm", "ss", "s", "TZ"],
    ),
    (
        "hh:mm:ss",
        re.compile(rf"^(\d{{2}}):(\d{{2}}):(\d{{2}}){TIMEZONE_REGEX}$"),
        ["hh", "mm", "ss", "TZ"],
    ),
    (
        "hh:mm",
        re.compile(rf"^(\d{{2}}):(\d{{2}}){TIMEZONE_REGEX}$"),
        ["hh", "mm", "TZ"],
    ),
    ("hh", re.compile(rf"^(\d{{2}}){TIMEZONE_REGEX}$"), ["hh", "TZ"]),
]
_time_components = {"hh", "mm", "ss", "s"}

_ALL_ISO_8601_PATTERNS = _DATETIME_PATTERNS + _DATE_PATTERNS + _TIME_PATTERNS

TIMEZONE_REGEX_NEAR = r"(?:(Z|[+-]\d{1,2}(?::?\d{1,2})?))?"
NEAR_ISO_8601_PATTERNS = [
    # Identical to valid ones but with varying numbers of digits for each component and
    # optional leading "T" char for time-only strings
    (
        "YYYY-MM-DDThh:mm:ss.s",
        re.compile(
            rf"^(-?\d{{1,4}})-(\d{{1,2}})-(\d{{1,2}})T(\d{{1,2}}):(\d{{1,2}}):(\d{{1,2}})\.(\d+){TIMEZONE_REGEX_NEAR}$"
        ),
        ["YYYY", "MM", "DD", "hh", "mm", "ss", "s", "TZ"],
    ),
    (
        "YYYY-Www-DThh:mm:ss.s",
        re.compile(
            rf"^(-?\d{{1,4}})-?W(\d{{1,2}})-(\d)T(\d{{1,2}}):(\d{{1,2}}):(\d{{1,2}})\.(\d+){TIMEZONE_REGEX_NEAR}$"
        ),
        ["YYYY", "Www", "D", "hh", "mm", "ss", "s", "TZ"],
    ),
    (
        "YYYY-MM-DDThh:mm:ss",
        re.compile(
            rf"^(-?\d{{1,4}})-(\d{{1,2}})-(\d{{1,2}})T(\d{{1,2}}):(\d{{1,2}}):(\d{{1,2}}){TIMEZONE_REGEX_NEAR}$"
        ),
        ["YYYY", "MM", "DD", "hh", "mm", "ss", "TZ"],
    ),
    (
        "YYYY-Www-DThh:mm:ss",
        re.compile(
            rf"^(-?\d{{1,4}})-?W(\d{{1,2}})-(\d)T(\d{{1,2}}):(\d{{1,2}}):(\d{{1,2}}){TIMEZONE_REGEX_NEAR}$"
        ),
        ["YYYY", "Www", "D", "hh", "mm", "ss", "TZ"],
    ),
    (
        "YYYY-MM-DDThh:mm",
        re.compile(
            rf"^(-?\d{{1,4}})-(\d{{1,2}})-(\d{{1,2}})T(\d{{1,2}}):(\d{{1,2}}){TIMEZONE_REGEX_NEAR}$"
        ),
        ["YYYY", "MM", "DD", "hh", "mm", "TZ"],
    ),
    (
        "YYYY-Www-DThh:mm",
        re.compile(
            rf"^(-?\d{{1,4}})-?W(\d{{1,2}})-(\d)T(\d{{1,2}}):(\d{{1,2}}){TIMEZONE_REGEX_NEAR}$"
        ),
        ["YYYY", "Www", "D", "hh", "mm", "TZ"],
    ),
    (
        "YYYY-MM-DDThh",
        re.compile(
            rf"^(-?\d{{1,4}})-(\d{{1,2}})-(\d{{1,2}})T(\d{{1,2}}){TIMEZONE_REGEX_NEAR}$"
        ),
        ["YYYY", "MM", "DD", "hh", "TZ"],
    ),
    (
        "YYYY-Www-DThh",
        re.compile(
            rf"^(-?\d{{1,4}})-?W(\d{{1,2}})-(\d)T(\d{{1,2}}){TIMEZONE_REGEX_NEAR}$"
        ),
        ["YYYY", "Www", "D", "hh", "TZ"],
    ),
    (
        "YYYY-MM-DD",
        re.compile(r"^(-?\d{1,4})-(\d{1,2})-(\d{1,2})$"),
        ["YYYY", "MM", "DD"],
    ),
    ("YYYY-Www-D", re.compile(r"^(-?\d{1,4})-?W(\d{1,2})-(\d)$"), ["YYYY", "Www", "D"]),
    ("YYYY-Www", re.compile(r"^(-?\d{1,4})-?W(\d{1,2})$"), ["YYYY", "Www"]),
    ("--MM-DD", re.compile(r"^--(\d{1,2})-(\d{1,2})$"), ["MM", "DD"]),
    ("--MMDD", re.compile(r"^--(\d{1,2})(\d{1,2})$"), ["MM", "DD"]),
    ("--MM", re.compile(r"^--(\d{1,2})$"), ["MM"]),
    ("---DD", re.compile(r"^---(\d{1,2})$"), ["DD"]),
    (
        "hh:mm:ss.s",
        re.compile(
            rf"^T?(\d{{1,2}}):(\d{{1,2}}):(\d{{1,2}})\.(\d+){TIMEZONE_REGEX_NEAR}$"
        ),
        ["hh", "mm", "ss", "s", "TZ"],
    ),
    (
        "hh:mm:ss",
        re.compile(rf"^T?(\d{{1,2}}):(\d{{1,2}}):(\d{{1,2}}){TIMEZONE_REGEX_NEAR}$"),
        ["hh", "mm", "ss", "TZ"],
    ),
    (
        "hh:mm",
        re.compile(rf"^T?(\d{{1,2}}):(\d{{1,2}}){TIMEZONE_REGEX_NEAR}$"),
        ["hh", "mm", "TZ"],
    ),
    (
        "Thh",  # with T specifically
        re.compile(rf"^T(\d{{1,2}}){TIMEZONE_REGEX_NEAR}$"),
        ["hh", "TZ"],
    ),
]

CHARS_REPLACEMENTS = {
    " ": ("T", "-", ":"),
    ".": ("-",),
    "/": ("-",),
    "z": ("Z",),
}


MAX_DAYS_IN_MONTH = {
    1: 31,  # January
    2: 29,  # February (accounting for leap years)
    3: 31,  # March
    4: 30,  # April
    5: 31,  # May
    6: 30,  # June
    7: 31,  # July
    8: 31,  # August
    9: 30,  # September
    10: 31,  # October
    11: 30,  # November
    12: 31,  # December
}


class DateTime(SemanticType):
    """
    An ISO 8601 compliant date-time string ("YYYY-MM-DDThh:mm:ss.s+hh-mm").

    It is composed of, either or both, a date and/or a time parts. It may feature
    "reduced accuracy", omitting certain components, on the date part if there is only
    a date part, or on the part if there is a time part.

    :examples: `2024-03-14T14:45:00`, `1999-11-03T02:12:78.845+02-00`, `2023-05-15T14`
    """

    ISO_NON_COMPLIANT_ERR = ERR_LABEL_DATETIME_VALUE_NOT_ISO_8601_COMPLIANT
    DATETIME_PATTERNS = _ALL_ISO_8601_PATTERNS
    REMOVE_TIME_0_WHEN_DATE_AND_TIME: bool = False
    primitive_type = str

    @classmethod
    def coerce(
        cls, value: str, input_text: str | None = None, error: ErrorJson | None = None
    ) -> str | None:
        """
        Try to correct a malformed datetime string to make it ISO compliant.

        :param value: string datetime to make ISO compliant.
        :param input_text: input text.
        :param error: error associated to the value to convert. This argument
            can help to convert the value by targeting to the appropriate methods
            (default: ``None``).
        :return: a string ISO 8601 compliant value if the provided value can be
            converted, otherwise ``None``.
        """
        _ = input_text
        _ = error
        # Convert int values to strings (e.g. year given as int)
        if isinstance(value, int):
            value = str(value)

        repaired_value = string_to_iso8601(value)
        if repaired_value is None:
            return None

        if (err := DateTime.validate(repaired_value)) is None:
            return repaired_value

        if err == ERR_LABEL_DATETIME_TIME_PART_ALL_ZEROS:
            return repaired_value.split("T")[0]

        return None

    @classmethod
    def validate(cls, value: str, _: str | None = None) -> str | None:
        """
        Check that a string complies to the ISO 8601 standard.

        :param value: date-time string to validate.
        :param _: placeholder for input text.
        :return: error message if the value is not ISO 8601 compliant, otherwise
            ``None``.
        """
        pattern_name, components = detect_precision_and_extract_components(
            value, cls.DATETIME_PATTERNS
        )
        if pattern_name is None:
            return cls.ISO_NON_COMPLIANT_ERR
        if (
            cls.REMOVE_TIME_0_WHEN_DATE_AND_TIME
            and "T" in pattern_name
            and all(components[c] == 0 for c in _time_components if c in components)
        ):
            return ERR_LABEL_DATETIME_TIME_PART_ALL_ZEROS
        return None


class Date(DateTime):
    """
    An ISO 8601 compliant date string.

    It may feature "reduced accuracy" and be of the form "YYYY-MM-DD", "YYYY-MM",
    "YYYY", "--MM-DD" (month and day with nullified year value), "YYYY-Www" (week date,
    the lowercase "w" characters are replaced with the week number) or "YYYY-Www-D"
    (week date with day number between 1 and 7).

    :examples: `2024-01-15`, `2024-01`, `2024`, `--12-25`
    """

    ISO_NON_COMPLIANT_ERR = ERR_LABEL_DATE_VALUE_NOT_ISO_8601_COMPLIANT
    DATETIME_PATTERNS = _DATE_PATTERNS

    @classmethod
    def coerce(
        cls, value: str, input_text: str | None = None, error: ErrorJson | None = None
    ) -> str | None:
        """
        Try to correct a malformed datetime string to make it ISO compliant.

        :param value: string datetime to make ISO compliant.
        :param input_text: input text.
        :param error: error associated to the value to convert. This argument
            can help to convert the value by targeting to the appropriate methods
            (default: ``None``).
        :return: a string ISO 8601 compliant value if the provided value can be
            converted, otherwise ``None``.
        """
        _ = input_text
        _ = error
        if isinstance(value, int):
            value = str(value)

        # 1. Check if the repaired string is already a valid Date.
        repaired_value = string_to_iso8601(value, allow_bare_month_day=True)
        if repaired_value is None:
            return None
        if cls.validate(repaired_value) is None:
            return repaired_value

        # 2. If not, check if it's a valid DateTime and extract the date part.
        if "T" in repaired_value and DateTime.validate(repaired_value) is None:
            return repaired_value.split("T")[0]

        return None


class Time(DateTime):
    """
    An ISO 8601 compliant time string.

    It may feature "reduced accuracy" and be of the
    form "hh:mm:ss.s", "hh:mm:ss", "hh:mm" or "hh". It may also include a timezone
    component of the form "+hh-mm", "-hh-mm", "+hh" or "-hh" appended to the former
    part.

    :examples: `14:30:57`, `18:01`, `14`, `14:30:45.123Z`
    """

    ISO_NON_COMPLIANT_ERR = ERR_LABEL_TIME_VALUE_NOT_ISO_8601_COMPLIANT
    DATETIME_PATTERNS = _TIME_PATTERNS

    @classmethod
    def coerce(
        cls, value: str, input_text: str | None = None, error: ErrorJson | None = None
    ) -> str | None:
        """
        Try to correct a malformed datetime string to make it ISO compliant.

        :param value: string datetime to make ISO compliant.
        :param input_text: input text.
        :param error: error associated to the value to convert. This argument
            can help to convert the value by targeting to the appropriate methods
            (default: ``None``).
        :return: a string ISO 8601 compliant value if the provided value can be
            converted, otherwise ``None``.
        """
        _ = input_text
        _ = error
        if isinstance(value, int):
            value = str(value)

        # 1. Check if the repaired string is already a valid Time.
        repaired_value = string_to_iso8601(value)
        if repaired_value is None:
            return None
        if cls.validate(repaired_value) is None:
            return repaired_value

        # 2. If not, check if it's a valid DateTime and extract the time part.
        if "T" in repaired_value and DateTime.validate(repaired_value) is None:
            return repaired_value.split("T")[1]

        return None


def detect_precision_and_extract_components(
    s: str, patterns: list[tuple], validate_values: bool = True
) -> tuple[str, dict[str, int]] | tuple[None, None]:
    """
    Detect the precision of a datetime string and extracts its components.

    The string has to be strictly ISO 8601 compliant to get matched to a precision
    pattern and parsed, otherwise the method returns ``None`` values. The values of the
    components are also checked to be sure that they are valid.

    :param s: datetime string to analyze.
    :param patterns: list of ISO 8601 patterns to check against.
    :param validate_values: verify the validity of the values of each component, and
        return them only if all of them are valid. For example, the month number is
        strictly within [1, 12], the hour number within [0,23]... (default: ``True``)
    :return: tuple holding the detected precision pattern and the components as a
        dictionary mapping the component name to its value (string).
    """
    # Detect precision and extract components
    pattern_name, components = None, None
    for name, pattern, keys in patterns:
        match = re.match(pattern, s)
        if match:
            values = match.groups()
            pattern_name = name
            components = {}
            for key, val in zip(keys, values):
                if val is None:
                    continue
                if key == "s":
                    # Normalize fractional seconds to microseconds
                    components[key] = int(val.ljust(6, "0")[:6])
                elif key == "TZ":
                    tz_hh, tz_mm = ("Z", None) if val == "Z" else parse_timezone(val)
                    components["tz_hh"] = tz_hh
                    if tz_mm is not None:
                        components["tz_mm"] = tz_mm
                else:
                    components[key] = int(val)
            break

    # Check for components value validity
    if (
        validate_values
        and components is not None
        and not _valid_time_components(**components)
    ):
        return None, None
    return pattern_name, components


def parse_timezone(tz: str) -> tuple[int, int | None] | None:
    """
    Parse a timezone string like '+02:30', '-0500', 'Z' into (hour, minute).

    :param tz: timezone string.
    :return: tuple holding the hours and minutes components.
    """
    if tz == "Z":
        return 0, None
    if not tz or not isinstance(tz, str):
        return None

    sign = -1 if tz.startswith("-") else 1
    tz_body = tz[1:]

    if ":" in tz_body:
        hours_str, minutes_str = tz_body.split(":")
    else:
        hours_str, minutes_str = tz_body[:2], tz_body[2:] if len(tz_body) > 2 else None

    try:
        return (
            sign * int(hours_str),
            sign * int(minutes_str) if minutes_str is not None else None,
        )
    except ValueError:
        return None


def _try_to_deduce_datetime_precision(
    date_str: str,
) -> tuple[str, dict[str, int]] | tuple[None, None]:
    """
    Detect the precision of a date string and normalize it.

    :param date_str: input date string
    :return: tuple holding the detected precision pattern and the components as a
        dictionary mapping the component name to its value (string).
    """
    date_str = date_str.strip()

    if not date_str:
        return None, None

    # Handle ambiguous ranges that should return None
    if _is_ambiguous_range(date_str):
        return None, None

    # Try to fix by replacing characters
    for char_to_replace, chars_replacing in CHARS_REPLACEMENTS.items():
        if char_to_replace not in date_str:
            continue
        for char_replacing in chars_replacing:
            date_str_alt = date_str.replace(char_to_replace, char_replacing)
            precision, components = detect_precision_and_extract_components(
                date_str_alt, _ALL_ISO_8601_PATTERNS, validate_values=False
            )
            if precision is not None:
                return precision, components

    # Tries "near ISO" regexes
    for precision, pattern, keys in NEAR_ISO_8601_PATTERNS:
        match = re.match(pattern, date_str)
        if match:
            values = match.groups()
            components = {}
            for key, val in zip(keys, values):
                if val is None:
                    continue
                if key == "s":
                    # Normalize fractional seconds to microseconds
                    components[key] = int(val.ljust(6, "0")[:6])
                elif key == "TZ":
                    tz_hh, tz_mm = parse_timezone(val)
                    components["tz_hh"] = tz_hh
                    components["tz_mm"] = tz_mm
                else:
                    components[key] = int(val)
            return precision, components

    # --- TEXTUAL FORMATS ---
    # Month-day without year formats like "December 5", "Jan 1st"
    textual_monthday_match = re.match(
        r"^([A-Za-z]+)\s+(\d{1,2})(?:st|nd|rd|th)?$", date_str
    )
    if textual_monthday_match:
        month_name, day = textual_monthday_match.groups()
        day = int(day)
        try:
            month_num = strptime(month_name, "%B").tm_mon
            return "--MM-DD", {"MM": month_num, "DD": day}
        except ValueError:
            try:
                month_num = strptime(month_name, "%b").tm_mon
                return "--MM-DD", {"MM": month_num, "DD": day}
            except ValueError:
                pass

    textual_month_year_match = re.match(r"^([A-Za-z]+)[,\s]+(\d{4})$", date_str)
    if textual_month_year_match:
        month_name, year = textual_month_year_match.groups()
        year = int(year)
        try:
            month_num = strptime(month_name, "%B").tm_mon
            return "YYYY-MM", {"YYYY": year, "MM": month_num}
        except ValueError:
            try:
                month_num = strptime(month_name, "%b").tm_mon
                return "YYYY-MM", {"YYYY": year, "MM": month_num}
            except ValueError:
                return None, None

    textual_full_match = re.match(r"^([A-Za-z]+)\s+(\d{1,2})[,\s]+(\d{4})$", date_str)
    if textual_full_match:
        month_name, day, year = textual_full_match.groups()
        day, year = int(day), int(year)
        try:
            month_num = strptime(month_name, "%B").tm_mon
            return "YYYY-MM-DD", {"YYYY": year, "MM": month_num, "DD": day}
        except ValueError:
            try:
                month_num = strptime(month_name, "%b").tm_mon
                return "YYYY-MM-DD", {"YYYY": year, "MM": month_num, "DD": day}
            except ValueError:
                return None, None

    # Month-only format like "December", "jan"
    # We use .title() to handle different casings like "december", "DECEMBER", "Dec".
    try:
        month_num = strptime(date_str.title(), "%B").tm_mon
        return "--MM", {"MM": month_num}
    except ValueError:
        try:
            month_num = strptime(date_str.title(), "%b").tm_mon
            return "--MM", {"MM": month_num}
        except ValueError:
            pass  # Not a standalone month name, continue.

    return None, None


def _is_ambiguous_range(date_str: str) -> bool:
    """Check if the date string represents an ambiguous range."""
    # Year ranges like "2022-2023"
    if re.match(r"^\d{4}-\d{4}$", date_str):
        return True

    # Date ranges with slash like "2013-09/2013-12"
    if "/" in date_str:
        return True

    # Time ranges like "08:30-09:00"
    if re.match(r"^\d{1,2}:\d{2}(?::\d{2})?-\d{1,2}:\d{2}(?::\d{2})?$", date_str):
        return True

    # Date ranges with explicit range indicators
    return bool(" to " in date_str.lower() or " - " in date_str)


def _valid_time_components(
    YYYY: int | None = None,  # noqa:N803
    MM: int | None = None,  # noqa:N803
    DD: int | None = None,  # noqa:N803
    Www: int | None = None,  # noqa:N803
    D: int | None = None,  # noqa:N803 used with YYYY-Www-D only
    hh: int | None = None,
    mm: int | None = None,
    ss: int | None = None,
    tz_hh: int | None = None,
    tz_mm: int | None = None,
    **_,
) -> bool:
    if MM is not None and not 1 <= MM <= 12:
        return False
    if DD is not None:
        if MM is not None:
            max_num_days_in_month = MAX_DAYS_IN_MONTH[MM]
            # For --MM-DD format without year, assume current year for leap year
            # calculation
            if MM == 2 and YYYY is None:
                if not _is_leap_year(_CURRENT_YEAR):
                    max_num_days_in_month = 28
            elif MM == 2 and YYYY is not None and not _is_leap_year(YYYY):
                max_num_days_in_month = 28
            if not 1 <= DD <= max_num_days_in_month:
                return False
        # Case for ---DD format, where month is not specified
        elif not 1 <= DD <= 31:
            return False
    if Www is not None and not 1 <= Www <= 53:
        return False
    if D is not None and not 1 <= D <= 7:
        return False
    if hh is not None and not 0 <= hh <= 23:
        return False
    if mm is not None and not 0 <= mm <= 59:
        return False
    if ss is not None and not 0 <= ss <= 59:
        return False
    if tz_hh is not None and tz_hh != "Z" and not -12 <= tz_hh <= 14:
        return False
    if tz_mm is not None:
        if (tz_hh == -12 or tz_hh == 14) and tz_mm != 0:
            return False
        if not 0 <= tz_mm <= 59:
            return False
    return True


def _is_leap_year(year: int) -> bool:
    """Check if a year is a leap year."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def string_to_iso8601(date_str: str, allow_bare_month_day: bool = False) -> str | None:
    """
    Try to convert a string to its closest ISO 8601 compliant equivalent.

    This function now handles fractional seconds and --MM-DD format.

    Examples:
        "2023-10-00" -> "2023-10"
        "2023-00-00" -> "2023"
        "May 2023" -> "2023-05"
        "2023-05-15T14:30:45.123Z" -> "2023-05-15T14:30:45.123Z"
        "2023-05-15T00:00:00.000" -> "2023-05-15"
        "2023-W52-1T14:30" -> "2023-W52-1T14:30"
        "2023-W52-1" -> "2023-W52-1"
        "2023-W05-0" -> "2023-W05"
        "2023-W05" -> "2023-W05"
        "2023W05" -> "2023-W05"
        "14:30:45.5" -> "14:30:45.5"
        "14:30" -> "14:30"
        "--01-01" -> "--01-01"
        "--12-25" -> "--12-25"
        "--0131" -> "--01-31"
        "December 5" -> "--12-05"
        "Jan 1st" -> "--01-01"
        "--05" -> "--05"
        "december" -> "--12"
        "---15" -> "---15"

    :param date_str: string to convert
    :param allow_bare_month_day: treat ``MM-DD`` inputs as ``--MM-DD`` instead of
        time values with a timezone.
    :return: the closest ISO 8601 compliant equivalent of the input string, or ``None``
        if no conversion can be performed.

    """
    if allow_bare_month_day:
        month_day_match = re.match(r"^(\d{1,2})-(\d{1,2})$", date_str.strip())
        if month_day_match:
            components = {
                "MM": int(month_day_match.group(1)),
                "DD": int(month_day_match.group(2)),
            }
            if _valid_time_components(**components):
                return convert_datetime_components_to_string(components)
            return None

    # First tries to extract the components from by matching the string to strict
    # regexes.
    precision, components = detect_precision_and_extract_components(
        date_str, _ALL_ISO_8601_PATTERNS, validate_values=False
    )

    # If no regex is matched, tries with a more permissive method "text-based"
    if components is None:
        precision, components = _try_to_deduce_datetime_precision(date_str)

    # Unable to parse the string
    if precision is None:
        return None

    # Reduce day/month/day-of-week if == 0 and no time component
    # If there is a time component and 0 values for month/day, it will be invalidated
    # in the following components validation
    # Skip this reduction for --MM-DD format since it doesn't have a year
    if "hh" not in components and "YYYY" in components:
        if "MM" in components and components["MM"] == 0:
            del components["MM"]
            if "DD" in components:
                del components["DD"]
        if "DD" in components and components["DD"] == 0:
            del components["DD"]
        if "D" in components and components["D"] == 0:
            del components["D"]

    # Final validation of the components
    if not _valid_time_components(**components):
        return None

    # Convert to string
    return convert_datetime_components_to_string(components)


def convert_datetime_components_to_string(components: dict[str, int]) -> str | None:
    """
    Format a dictionary of ISO 8601 components into an ISO 8601 compliant string.

    Supports reduced precision and only includes the parts that are present.
    Supports "--MM-DD", "--MM", and "---DD" formats.

    :param components: dictionary of components to format to an ISO 8601 string.
    :return: ISO 8601 compliant string of the provided components.
    """
    date = ""
    time = ""

    # Check if this is a --MM-DD format (month-day without year)
    if "MM" in components and "DD" in components and "YYYY" not in components:
        date = f"--{components['MM']:02d}-{components['DD']:02d}"
    # Check if this is a --MM format (month without year or day)
    elif "MM" in components and "YYYY" not in components and "DD" not in components:
        date = f"--{components['MM']:02d}"
    # Check if this is a ---DD format (day without year or month)
    elif "DD" in components and "YYYY" not in components and "MM" not in components:
        date = f"---{components['DD']:02d}"
    # Build week date part
    elif "Www" in components and "YYYY" in components:
        date = f"{components['YYYY']:04d}-W{components['Www']:02d}"
        if "D" in components:
            date += f"-{components['D']}"
    # Build regular date part
    elif "YYYY" in components:
        date = f"{components['YYYY']:04d}"
        if "MM" in components:
            date += f"-{components['MM']:02d}"
            if "DD" in components:
                date += f"-{components['DD']:02d}"

    # Build time part
    if "hh" in components:
        time = f"{components['hh']:02d}"
        if "mm" in components:
            time += f":{components['mm']:02d}"
            if "ss" in components:
                time += f":{components['ss']:02d}"
                if "s" in components:
                    # Fractional seconds (microseconds)
                    frac = (
                        f"{components['s']:06d}".rstrip("0")
                        if components["s"] != 0
                        else "0"
                    )
                    time += f".{frac}"
        # Timezone
        if "tz_hh" in components:
            # Catch the special case of Z
            if components["tz_hh"] == "Z":
                time += "Z"
            else:
                if components["tz_hh"] >= 0:
                    time += f"+{components['tz_hh']:02d}"
                else:
                    time += f"{components['tz_hh']:03d}"
                if "tz_mm" in components and components["tz_mm"] is not None:
                    time += f":{abs(components['tz_mm']):02d}"

    if date and time:
        return f"{date}T{time}"
    if date:
        return date
    if time:
        # When repairing a time-only string with a leading T, it gets stripped.
        # This is a bit of an edge case from _try_to_deduce...
        # Let's ensure time-only strings are valid without a date.
        return time.lstrip("T")
    return None
