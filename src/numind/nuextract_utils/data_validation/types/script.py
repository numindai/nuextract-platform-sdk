"""Script type."""

from __future__ import annotations

import csv
import importlib.resources
from typing import TYPE_CHECKING, Literal

from ._utils import ClassCachedProperty, MappingInterface
from .base import SemanticType

if TYPE_CHECKING:
    from numind.nuextract_utils.data_validation.models import ErrorJson

ERR_LABEL_SCRIPT_CODE_NOT_ISO_15924_COMPLIANT = (
    "label script code value is not ISO 15924 compliant"
)
ERR_LABEL_SCRIPT_ISO_15924_COMPLIANT_BUT_CASE_INSENSITIVE = (
    "label script code/name value is ISO 15924 compliant but only case-insensitive"
)


SCRIPT_CODES, SCRIPT_NAMES = [], []
with (
    importlib.resources.files("numind.nuextract_utils._iso_data")
    .joinpath("ISO 15924.csv")
    .open(encoding="utf8") as _file
):
    reader_ = csv.reader(_file)
    next(reader_)
    for row in reader_:
        SCRIPT_CODES.append(row[0])
        SCRIPT_NAMES.append(row[2])
SCRIPTS_MAPPING = MappingInterface.from_data(
    names=SCRIPT_NAMES, codes_alpha=SCRIPT_CODES
)


class Script(SemanticType):
    """
    Titlecase 4-character script code following the ISO 15924 standard.

    :examples: `Latn` (Latin), `Kore` (Korean), `Deva` (Devanagari)
    """

    json_schema_format = ("script-code-ISO_15924-4chars", "script-code")
    iso_subset_type: Literal["names", "codes_alpha"] = "codes_alpha"
    # dictionaries to be used as ordered sets to build `country_data`
    mapping: MappingInterface = SCRIPTS_MAPPING

    names: set[str] = ClassCachedProperty(
        "mapping",
        lambda m: {
            g[m.group_names["names"]]
            for g in m._groups
            if g[m.group_names["names"]] is not None
        },
        "_names_cached",
    )  # Title case
    codes_alpha: set[str] = ClassCachedProperty(
        "mapping",
        lambda m: {g[m.group_names["codes_alpha"]] for g in m._groups},
        "_codes_alpha_cached",
    )  # Title case

    # Class-level cached properties that auto-invalidate when source changes
    names_lower = ClassCachedProperty(
        "names", lambda s: {code.lower(): code for code in s}, "_names_lower_cached"
    )
    codes_alpha_lower = ClassCachedProperty(
        "codes_alpha",
        lambda s: {code.lower(): code for code in s},
        "_codes_alpha_lower_cached",
    )

    @classmethod
    def coerce(
        cls, value: str, input_text: str | None = None, error: ErrorJson | None = None
    ) -> str | None:
        """
        Try to fix a script name or code.

        :param value: script name/code to fix.
        :param input_text: input text.
        :param error: error associated to the value to convert. This argument
            can help to convert the value by targeting to the appropriate methods
            (default: ``None``).
        :return: a string corresponding to an ISO 15924 script name or code, if the
            provided value can be converted, otherwise ``None``.
        """
        _ = input_text
        _ = error
        if value is None:
            return None

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
                return ERR_LABEL_SCRIPT_ISO_15924_COMPLIANT_BUT_CASE_INSENSITIVE
            return ERR_LABEL_SCRIPT_CODE_NOT_ISO_15924_COMPLIANT
        return None

    @classmethod
    def _get_valid_set(cls) -> set[str]:
        if cls.iso_subset_type == "codes_alpha":
            return cls.codes_alpha
        return cls.names

    @classmethod
    def _get_valid_set_lowercase(cls) -> set[str]:
        if cls.iso_subset_type == "codes_alpha":
            return cls.codes_alpha_lower
        return cls.names_lower
