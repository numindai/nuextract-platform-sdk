"""Currency type."""

from __future__ import annotations

import csv
import importlib.resources
from typing import TYPE_CHECKING, Literal

from ._utils import ClassCachedProperty, MappingInterface
from .base import SemanticType

if TYPE_CHECKING:
    from numind.nuextract_utils.data_validation.models import ErrorJson

ERR_LABEL_CURRENCY_CODE_NOT_ISO_4217_COMPLIANT = (
    "label currency code value is not ISO 4217 compliant"
)
ERR_LABEL_CURRENCY_ISO_4217_COMPLIANT_BUT_CASE_INSENSITIVE = (
    "label currency code/name value is ISO 4217 compliant but only case-insensitive"
)


CURRENCY_CODES, CURRENCY_NAMES = [], []
with (
    importlib.resources.files("numind.nuextract_utils._iso_data")
    .joinpath("ISO 4217 list-one.csv")
    .open(encoding="utf8") as _file
):
    reader_ = csv.reader(_file)
    next(reader_)
    for row in reader_:
        CURRENCY_CODES.append(row[2])
        CURRENCY_NAMES.append(row[1])
with (
    importlib.resources.files("numind.nuextract_utils._iso_data")
    .joinpath("ISO 4217 list-three.csv")
    .open(encoding="utf8") as _file
):
    reader_ = csv.reader(_file)
    next(reader_)
    for row in reader_:
        CURRENCY_CODES.append(row[2])
        CURRENCY_NAMES.append(row[1])
CURRENCIES_MAPPING = MappingInterface.from_data(
    names=CURRENCY_NAMES, codes_alpha3=CURRENCY_CODES
)


class Currency(SemanticType):
    """
    Uppercase 3-characters currency code following the ISO 4217 standard.

    It covers list 1 (currently used currencies) and list 3 (old unused currencies).

    :examples: `EUR` (euro), `USD` (US dollar), `DEM` (Deutsche Mark)
    """

    json_schema_format = ("currency-code-ISO_4217_3chars", "currency-code")
    iso_subset_type: Literal["names", "codes_alpha3"] = "codes_alpha3"
    # dictionaries to be used as ordered sets to build `country_data`

    mapping: MappingInterface = CURRENCIES_MAPPING
    names: set[str] = ClassCachedProperty(
        "mapping",
        lambda m: {
            g[m.group_names["names"]]
            for g in m._groups
            if g[m.group_names["names"]] is not None
        },
        "_names_cached",
    )  # Title case
    codes_alpha3: set[str] = ClassCachedProperty(
        "mapping",
        lambda m: {g[m.group_names["codes_alpha3"]] for g in m._groups},
        "_codes_alpha3_cached",
    )  # uppercase

    # Class-level cached properties that auto-invalidate when source changes
    names_lower = ClassCachedProperty(
        "names", lambda s: {code.lower(): code for code in s}, "_names_lower_cached"
    )
    codes_alpha3_lower = ClassCachedProperty(
        "codes_alpha3",
        lambda s: {code.lower(): code for code in s},
        "_codes_alpha3_lower_cached",
    )

    @classmethod
    def coerce(
        cls, value: str, input_text: str | None = None, error: ErrorJson | None = None
    ) -> str | None:
        """
        Try to fix a currency name or code.

        :param value: currency name/code to fix.
        :param input_text: input text.
        :param error: error associated to the value to convert. This argument
            can help to convert the value by targeting to the appropriate methods
            (default: ``None``).
        :return: a string corresponding to an ISO 4217 currency name or code, if the
            provided value can be converted, otherwise ``None``.
        """
        _ = input_text
        if not isinstance(value, str):
            return None

        # Correct case unsensitive errors
        if (
            error.error_message
            == ERR_LABEL_CURRENCY_ISO_4217_COMPLIANT_BUT_CASE_INSENSITIVE
            and cls.iso_subset_type == "codes_alpha3"
        ):
            return value.upper()

        # Try to correct based on groups
        group = cls.mapping.get_group(value.lower())
        if group is not None:
            idx_to_get = cls.mapping.group_names[cls.iso_subset_type]
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
                return ERR_LABEL_CURRENCY_ISO_4217_COMPLIANT_BUT_CASE_INSENSITIVE
            return ERR_LABEL_CURRENCY_CODE_NOT_ISO_4217_COMPLIANT
        return None

    @classmethod
    def _get_valid_set(cls) -> set[str]:
        if cls.iso_subset_type == "codes_alpha3":
            return cls.codes_alpha3
        return cls.names

    @classmethod
    def _get_valid_set_lowercase(cls) -> set[str]:
        if cls.iso_subset_type == "codes_alpha3":
            return cls.codes_alpha3_lower
        return cls.names_lower
