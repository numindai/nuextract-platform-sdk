"""Country type."""

from __future__ import annotations

import csv
import importlib.resources
from typing import TYPE_CHECKING, Literal

from ._utils import AssociativeMapping, ClassCachedProperty
from .base import SemanticType

if TYPE_CHECKING:
    from numind.nuextract_utils.data_validation.models import ErrorJson

ERR_LABEL_COUNTRY_NOT_ISO_3166_COMPLIANT = (
    "label country code/name value is not ISO 3166 compliant"
)
ERR_LABEL_COUNTRY_ISO_3166_COMPLIANT_BUT_CASE_INSENSITIVE = (
    "label country code/name value is ISO 3166 compliant but only case-insensitive"
)

COUNTRY_NAMES, COUNTRY_CODES2, COUNTRY_CODES3 = {}, {}, {}
with (
    importlib.resources.files("numind.nuextract_utils._iso_data")
    .joinpath("ISO 3166-1.csv")
    .open(encoding="utf8") as _file
):
    reader_ = csv.reader(_file)
    next(reader_)
    for row in reader_:
        COUNTRY_NAMES[row[0]] = None
        COUNTRY_CODES2[row[1]] = None
        COUNTRY_CODES3[row[2]] = None


class Country(SemanticType):
    """
    Uppercase 2-characters country code following the ISO 3166-1 standard.

    :examples: `FR` (France), `SG` (Singapore), `KR` (South Korea, "Korea, Republic of")
    """

    json_schema_format = ("country-code-ISO_3166-1_2chars", "country-code")
    iso_subset_type: Literal["names", "codes_alpha2", "codes_alpha3"] = "codes_alpha2"
    # dictionaries to be used as ordered sets to build `country_data`
    names: dict[str, None] = COUNTRY_NAMES  # Title case
    codes_alpha2: dict[str, None] = COUNTRY_CODES2  # uppercase
    codes_alpha3: dict[str, None] = COUNTRY_CODES3  # uppercase

    # Class-level cached properties that auto-invalidate when source changes
    names_lower = ClassCachedProperty(
        "names", lambda s: {code.lower(): code for code in s}
    )
    codes_alpha2_lower = ClassCachedProperty(
        "codes_alpha2", lambda s: {code.lower(): code for code in s}
    )
    codes_alpha3_lower = ClassCachedProperty(
        "codes_alpha3", lambda s: {code.lower(): code for code in s}
    )
    country_data = AssociativeMapping("names", "codes_alpha2", "codes_alpha3")

    @classmethod
    def coerce(
        cls, value: str, input_text: str | None = None, error: ErrorJson | None = None
    ) -> str | None:
        """
        Try to fix a country name or code.

        :param value: country name/code to fix.
        :param input_text: input text.
        :param error: error associated to the value to convert. This argument
            can help to convert the value by targeting to the appropriate methods
            (default: ``None``).
        :return: a string corresponding to an ISO 3166-1 country name or code, if the
            provided value can be converted, otherwise ``None``.
        """
        _ = input_text
        if not isinstance(value, str):
            return None

        # Correct case unsensitive errors
        if (
            error.error_message
            == ERR_LABEL_COUNTRY_ISO_3166_COMPLIANT_BUT_CASE_INSENSITIVE
        ):
            return cls._get_valid_set_lowercase()[value.lower()]

        # Try to correct based on groups
        group = cls.country_data.get_group(value.lower())
        if group is not None:
            idx_to_get = cls.country_data.group_names[cls.iso_subset_type]
            return group[idx_to_get]

        return None

    @classmethod
    def validate(cls, value: str, _: str | None = None) -> str | None:
        """
        Check that a string is not considered "null" (and thus should be ``None``).

        :param value: string value to assess.
        :param _: placeholder for input text.
        :return: error message if the value should be ``None``, otherwise ``None``.
        """
        if value not in cls._get_valid_set():
            if value.lower() in cls._get_valid_set_lowercase():
                return ERR_LABEL_COUNTRY_ISO_3166_COMPLIANT_BUT_CASE_INSENSITIVE
            return ERR_LABEL_COUNTRY_NOT_ISO_3166_COMPLIANT
        return None

    @classmethod
    def _get_valid_set(cls) -> dict[str, None]:
        if cls.iso_subset_type == "codes_alpha2":
            return cls.codes_alpha2
        if cls.iso_subset_type == "codes_alpha3":
            return cls.codes_alpha3
        return cls.names

    @classmethod
    def _get_valid_set_lowercase(cls) -> dict[str, str]:
        if cls.iso_subset_type == "codes_alpha2":
            return cls.codes_alpha2_lower
        if cls.iso_subset_type == "codes_alpha3":
            return cls.codes_alpha3_lower
        return cls.names_lower
