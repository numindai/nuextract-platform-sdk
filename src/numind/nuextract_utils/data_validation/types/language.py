"""
Language type.

ISO reference files:
* https://standards.iso.org/iso/639/ed-2/en/Access%20to%20the%20databases%20of%20the%20ISO%20639%20Language%20Code.pdf
* https://iso639-3.sil.org/code_tables/639/data
"""

from __future__ import annotations

import csv
import importlib.resources
from typing import TYPE_CHECKING, Literal

from ._utils import ClassCachedProperty, MappingInterface
from .base import SemanticType

if TYPE_CHECKING:
    from numind.nuextract_utils.data_validation.models import ErrorJson

ERR_LABEL_LANGUAGE_CODE_NOT_ISO_639_COMPLIANT = (
    "label language code value is not ISO 639-3 compliant"
)
ERR_LABEL_LANGUAGE_ISO_639_COMPLIANT_BUT_CASE_INSENSITIVE = (
    "label language code/name value is ISO 639-3 compliant but only case-insensitive"
)


# Not using retired ISO 639-3 codes
LANGUAGE_CODES3, LANGUAGE_CODES2, LANGUAGE_NAMES = [], [], []
with (
    importlib.resources.files("numind.nuextract_utils._iso_data")
    .joinpath("iso-639-3.tab")
    .open(encoding="utf8") as _file
):
    reader_ = csv.reader(_file, delimiter="\t")
    next(reader_)
    for row in reader_:
        LANGUAGE_CODES3.append(row[0])
        LANGUAGE_NAMES.append(row[6])
        if row[3] == "":
            LANGUAGE_CODES2.append(None)
        else:
            LANGUAGE_CODES2.append(row[3])

LANGUAGES_MAPPING = MappingInterface.from_data(
    names=LANGUAGE_NAMES, codes_alpha2=LANGUAGE_CODES2, codes_alpha3=LANGUAGE_CODES3
)


class Language(SemanticType):
    """
    Lowercase 3-character language code following the ISO 639-3 standard.

    Retired (depreciated) codes are not supported.

    :examples: `eng` (English), `fra` (French), `cos` (Corsican)
    """

    json_schema_format = ("language-code-ISO_639-3_3chars", "language-code")
    iso_subset_type: Literal["names", "codes_alpha2", "codes_alpha3"] = "codes_alpha3"
    mapping: MappingInterface = LANGUAGES_MAPPING
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
    )  # lowercase
    codes_alpha2: set[str] = ClassCachedProperty(
        "mapping",
        lambda m: {g[m.group_names["codes_alpha2"]] for g in m._groups},
        "_codes_alpha2_cached",
    )  # lowercase

    # Class-level cached properties that auto-invalidate when source changes
    names_lower = ClassCachedProperty(
        "names", lambda s: {code.lower(): code for code in s}, "_names_lower_cached"
    )

    @classmethod
    def coerce(
        cls, value: str, input_text: str | None = None, error: ErrorJson | None = None
    ) -> str | None:
        """
        Try to fix a language name or code.

        :param value: language name/code to fix.
        :param input_text: input text.
        :param error: error associated to the value to convert. This argument
            can help to convert the value by targeting to the appropriate methods
            (default: ``None``).
        :return: a string corresponding to an ISO 639-3 language name or code, if the
            provided value can be converted, otherwise ``None``.
        """
        _ = input_text
        if not isinstance(value, str):
            return None

        # Correct case unsensitive errors
        if (
            error.error_message
            == ERR_LABEL_LANGUAGE_ISO_639_COMPLIANT_BUT_CASE_INSENSITIVE
            and cls.iso_subset_type in {"codes_alpha2", "codes_alpha3"}
        ):
            return value.lower()

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
        valid_case_sensitive = value in cls._get_valid_set()
        if not valid_case_sensitive:
            if value.lower() in cls._get_valid_set_lowercase():
                return ERR_LABEL_LANGUAGE_ISO_639_COMPLIANT_BUT_CASE_INSENSITIVE
            return ERR_LABEL_LANGUAGE_CODE_NOT_ISO_639_COMPLIANT
        return None

    @classmethod
    def _get_valid_set(cls) -> set[str]:
        if cls.iso_subset_type == "codes_alpha3":
            return cls.codes_alpha3
        if cls.iso_subset_type == "codes_alpha2":
            return cls.codes_alpha2
        return cls.names

    @classmethod
    def _get_valid_set_lowercase(cls) -> set[str]:
        if cls.iso_subset_type == "codes_alpha3":
            return cls.codes_alpha3
        if cls.iso_subset_type == "codes_alpha2":
            return cls.codes_alpha2
        return cls.names_lower
