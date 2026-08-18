"""Geolocation type."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, ClassVar

from .base import SemanticType

if TYPE_CHECKING:
    from numind.nuextract_utils.data_validation.models import ErrorJson

# --- Error Messages ---
ERR_LABEL_LEAF_VALUE_IS_GEOLOCATION_BUT_IN_MESSY_STRING = (
    "label leaf value is a geolocation but in messy string"
)
ERR_LABEL_LEAF_VALUE_IS_NOT_A_GEOLOCATION = "label leaf value is not a geolocation"
ERR_LABEL_LEAF_INVALID_COORDINATE_VALUES = (
    "string has valid format but invalid coordinate values"
)

# --- ISO 6709 Compliant Regexes for Different Formats ---
ISO_DECIMAL_PATTERN = (
    r"(?P<lat_dec>[+-]\d{2,}(?:\.\d+)?)"
    r"(?P<lon_dec>[+-]\d{3,}(?:\.\d+)?)"
)
ISO_DM_PATTERN = (
    r"(?P<lat_sign_dm>[+-])(?P<lat_deg_dm>\d{2})(?P<lat_min_dm>\d{2}(?:\.\d+)?)"
    r"(?P<lon_sign_dm>[+-])(?P<lon_deg_dm>\d{3})(?P<lon_min_dm>\d{2}(?:\.\d+)?)"
)
ISO_DMS_PATTERN = (
    r"(?P<lat_sign_dms>[+-])(?P<lat_deg_dms>\d{2})(?P<lat_min_dms>\d{2})(?P<lat_sec_dms>\d{2}(?:\.\d+)?)"
    r"(?P<lon_sign_dms>[+-])(?P<lon_deg_dms>\d{3})(?P<lon_min_dms>\d{2})(?P<lon_sec_dms>\d{2}(?:\.\d+)?)"
)

GEOLOCATION_REGEX_STRICT = re.compile(
    rf"""
    ^
    (?:{ISO_DMS_PATTERN}|{ISO_DM_PATTERN}|{ISO_DECIMAL_PATTERN})
    (?P<alt>[+-]\d+(?:\.\d+)?)?
    (?:/(?P<crs>.*))?
    $
    """,
    re.VERBOSE,
)


class Geolocation(SemanticType):
    """
    Geolocation coordinates (latitude/longitude/altitude/CRS).

    It is a string following the ISO 6709 standard (rev 2022). The latitude and
    longitude can be expressed with degrees, minutes and seconds.

    :examples: `-17.0228-149.5958` (latitude of -17 degrees and a longitude of -149.6
    degrees), `+404246.00-0740021.00` (equivalent of "40° 42' 46" N, 74° 0' 21" W")
    """

    _DECIMAL_PRECISION: ClassVar[int] = 6
    _FIND_NUMBERS_REGEX: ClassVar[re.Pattern] = re.compile(r"[+-]?\d+(?:\.\d+)?")
    _HUMAN_DMS_REGEX: ClassVar[re.Pattern] = re.compile(
        r"""
                # Case 1: Numbers first, then cardinal direction (d, m, s, card)
                (\d+(?:\.\d+)?)\s*(?:°|d|deg)?\s*
                (?:(\d+(?:\.\d+)?)\s*(?:'|min|m|’)?\s*)?
                (?:(\d+(?:\.\d+)?)\s*(?:"|sec|s|”)?\s*)?
                \s*(?<![a-zA-Z])([NSEW])(?![a-zA-Z])
                | # OR
                # Case 2: Cardinal direction first, then numbers (card, d, m, s)
                (?<![a-zA-Z])([NSEW])(?![a-zA-Z])\s*
                (\d+(?:\.\d+)?)\s*(?:°|d|deg)?\s*
                (?:(\d+(?:\.\d+)?)\s*(?:'|min|m|’)?\s*)?
                (?:(\d+(?:\.\d+)?)\s*(?:"|sec|s|”)?\s*)?
                """,
        re.IGNORECASE | re.VERBOSE,
    )

    @classmethod
    def coerce(
        cls,
        value: object,
        input_text: str | None = None,
        error: ErrorJson | None = None,
    ) -> str | None:
        """
        Try to convert a string to its ISO 6709 compliant equivalent.

        :param value: value to convert to an ISO 6709 compliant string if it can be,
            otherwise ``None``.
        :param input_text: input text.
        :param error: error associated to the value to convert. This argument
            can help to convert the value by targeting to the appropriate methods
            (default: ``None``).
        :return: a string value if the provided value can be converted, otherwise
            ``None``.
        """
        _ = input_text
        if error is None:
            return value
        if not isinstance(value, str) or not value.strip():
            return None
        if (
            error.error_message
            == ERR_LABEL_LEAF_VALUE_IS_GEOLOCATION_BUT_IN_MESSY_STRING
        ):
            return cls._parse_messy_string(value)
        if error.error_message is not None:
            return None
        validation_result = cls.validate(value)
        if validation_result is None:
            return value
        if validation_result == ERR_LABEL_LEAF_VALUE_IS_GEOLOCATION_BUT_IN_MESSY_STRING:
            return cls._parse_messy_string(value)
        return None

    @classmethod
    def validate(cls, value: str, _: str | None = None) -> str | None:
        """
        Check that a string is strictly ISO 6709 compliant.

        :param value: string value to assess.
        :param _: placeholder for input text.
        :return: error message if the value should be ``None``, otherwise ``None``.
        """
        match = GEOLOCATION_REGEX_STRICT.fullmatch(value)
        if match:
            g = match.groupdict()
            try:
                if g.get("lat_deg_dms"):
                    lat = cls._dms_to_dd(
                        g["lat_deg_dms"], g["lat_min_dms"], g["lat_sec_dms"]
                    ) * (-1 if g["lat_sign_dms"] == "-" else 1)
                    lon = cls._dms_to_dd(
                        g["lon_deg_dms"], g["lon_min_dms"], g["lon_sec_dms"]
                    ) * (-1 if g["lon_sign_dms"] == "-" else 1)
                elif g.get("lat_deg_dm"):
                    lat = cls._dms_to_dd(g["lat_deg_dm"], g["lat_min_dm"]) * (
                        -1 if g["lat_sign_dm"] == "-" else 1
                    )
                    lon = cls._dms_to_dd(g["lon_deg_dm"], g["lon_min_dm"]) * (
                        -1 if g["lon_sign_dm"] == "-" else 1
                    )
                elif g.get("lat_dec"):
                    lat = float(g["lat_dec"])
                    lon = float(g["lon_dec"])
                else:
                    return ERR_LABEL_LEAF_VALUE_IS_NOT_A_GEOLOCATION
                if not cls._validate_coordinate_ranges(lat, lon):
                    return ERR_LABEL_LEAF_INVALID_COORDINATE_VALUES
            except (ValueError, IndexError, TypeError):
                return ERR_LABEL_LEAF_INVALID_COORDINATE_VALUES
            return None
        if cls._parse_messy_string(value) is not None:
            return ERR_LABEL_LEAF_VALUE_IS_GEOLOCATION_BUT_IN_MESSY_STRING
        return ERR_LABEL_LEAF_VALUE_IS_NOT_A_GEOLOCATION

    @staticmethod
    def _validate_coordinate_ranges(latitude: float, longitude: float) -> bool:
        return -90.0 <= latitude <= 90.0 and -180.0 <= longitude <= 180.0

    @staticmethod
    def _dms_to_dd(d: str, m: str | None = None, s: str | None = None) -> float:
        d_val, m_val, s_val = float(d), float(m) if m else 0.0, float(s) if s else 0.0
        if not (0 <= m_val < 60 and 0 <= s_val < 60):
            raise ValueError(_ := "Minutes or seconds are out of the [0, 60) range.")
        return d_val + m_val / 60 + s_val / 3600

    @classmethod
    def _parse_messy_string(cls, value: str) -> str | None:
        lat, lon, alt = None, None, None
        detected_format = "decimal"

        try:
            # Strategy 1: Attempt to parse using cardinal directions (N,S,E,W).
            dms_matches = cls._HUMAN_DMS_REGEX.findall(value)

            if dms_matches:
                # If cardinal directions are present, the format MUST be a valid pair.
                # No fallback to number-only parsing is allowed if this block fails.
                if len(dms_matches) != 2:
                    return None  # Must be exactly one lat and one lon component.

                temp_lat, temp_lon, is_dms, is_dm = None, None, False, False
                dms_numbers_used = []
                for d1, m1, s1, card1, card2, d2, m2, s2 in dms_matches:
                    d, m, s, card = (d1 or d2), (m1 or m2), (s1 or s2), (card1 or card2)

                    if s:
                        is_dms = True
                    if m and not s:
                        is_dm = True
                    dd = cls._dms_to_dd(d, m, s) * (-1 if card.upper() in "SW" else 1)
                    dms_numbers_used.extend(filter(None, [d, m, s]))

                    if card.upper() in "NS":
                        if temp_lat is not None:
                            return None  # Duplicate latitude found, invalid.
                        temp_lat = dd
                    else:  # EW
                        if temp_lon is not None:
                            return None  # Duplicate longitude found, invalid.
                        temp_lon = dd

                if temp_lat is None or temp_lon is None:
                    return None  # Failed to find a valid lat/lon pair.

                lat, lon = temp_lat, temp_lon
                if is_dms:
                    detected_format = "dms"
                elif is_dm:
                    detected_format = "dm"
                all_numbers = cls._FIND_NUMBERS_REGEX.findall(value)
                alt_candidates = [n for n in all_numbers if n not in dms_numbers_used]
                if len(alt_candidates) == 1:
                    alt = float(alt_candidates[0])
            else:
                # Strategy 2: Fallback for strings with NO cardinal directions.
                # Heuristic: check for other standalone letters that aren't NSEW (e.g.,
                # X, Y)
                text_without_numbers = re.sub(r"[+-]?\d+(?:\.\d+)?", " ", value)
                if re.search(r"\b[A-Z]\b", text_without_numbers, re.IGNORECASE):
                    return (
                        None  # Found a standalone letter; likely an invalid cardinal.
                    )

                numbers = cls._FIND_NUMBERS_REGEX.findall(value)
                if len(numbers) in [2, 3]:
                    lat = float(numbers[0])
                    lon = float(numbers[1])
                    alt = float(numbers[2]) if len(numbers) == 3 else None
                else:
                    return None  # Not enough numbers to form a coordinate
        except (ValueError, IndexError):
            return None

        if lat is None or lon is None or not cls._validate_coordinate_ranges(lat, lon):
            return None

        if detected_format == "dms":
            return cls._format_to_iso_dms(lat, lon, alt)
        if detected_format == "dm":
            return cls._format_to_iso_dm(lat, lon, alt)
        return cls._format_to_iso_decimal(lat, lon, alt)

    @classmethod
    def _format_to_iso_decimal(cls, lat: float, lon: float, alt: float | None) -> str:
        lat_str = f"{lat:+.{cls._DECIMAL_PRECISION}f}"
        if abs(lat) < 10:
            lat_str = f"{lat_str[0]}0{lat_str[1:]}"
        lon_str = f"{lon:+.{cls._DECIMAL_PRECISION}f}"
        sign, num_part = lon_str[0], lon_str[1:]
        integer_part, frac_part = num_part.split(".")
        lon_str = f"{sign}{integer_part.zfill(3)}.{frac_part}"
        alt_str = f"{alt:+.{cls._DECIMAL_PRECISION}f}" if alt is not None else ""
        return f"{lat_str}{lon_str}{alt_str}"

    @classmethod
    def _format_to_iso_dm(cls, lat: float, lon: float, alt: float | None) -> str:
        lat_sign, lon_sign = ("+" if lat >= 0 else "-"), ("+" if lon >= 0 else "-")
        lat_d, lat_m = cls._dd_to_dm(lat)
        lon_d, lon_m = cls._dd_to_dm(lon)
        lat_str = f"{lat_sign}{lat_d:02}{lat_m:07.4f}"
        lon_str = f"{lon_sign}{lon_d:03}{lon_m:07.4f}"
        alt_str = f"{alt:+.{cls._DECIMAL_PRECISION}f}" if alt is not None else ""
        return f"{lat_str}{lon_str}{alt_str}"

    @classmethod
    def _format_to_iso_dms(cls, lat: float, lon: float, alt: float | None) -> str:
        lat_sign, lon_sign = ("+" if lat >= 0 else "-"), ("+" if lon >= 0 else "-")
        lat_d, lat_m, lat_s = cls._dd_to_dms(lat)
        lon_d, lon_m, lon_s = cls._dd_to_dms(lon)
        lat_str = f"{lat_sign}{lat_d:02}{lat_m:02}{lat_s:05.2f}"
        lon_str = f"{lon_sign}{lon_d:03}{lon_m:02}{lon_s:05.2f}"
        alt_str = f"{alt:+.{cls._DECIMAL_PRECISION}f}" if alt is not None else ""
        return f"{lat_str}{lon_str}{alt_str}"

    @staticmethod
    def _dd_to_dms(dd: float) -> tuple[int, int, float]:
        dd = abs(dd)
        minutes, seconds = divmod(dd * 3600, 60)
        degrees, minutes = divmod(minutes, 60)
        return int(degrees), int(minutes), seconds

    @staticmethod
    def _dd_to_dm(dd: float) -> tuple[int, float]:
        dd = abs(dd)
        degrees = int(dd)
        minutes = (dd - degrees) * 60
        return degrees, minutes
