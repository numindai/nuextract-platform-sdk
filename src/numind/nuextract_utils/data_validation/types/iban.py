"""IBAN (International Bank Account Number) type."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

try:
    import schwifty
except ImportError:
    schwifty = None

from .base import SemanticType

if TYPE_CHECKING:
    from numind.nuextract_utils.data_validation.models import ErrorJson

ERR_LABEL_LEAF_VALUE_IBAN_IS_NOT_STRING = "label leaf value IBAN is not a string"
ERR_LABEL_LEAF_VALUE_IS_NOT_A_VALID_IBAN = "label leaf value is not a valid IBAN"
ERR_LABEL_LEAF_VALUE_IS_VALID_IBAN_BUT_IS_MESSY_STRING = (
    "label leaf value is a valid IBAN but is a messy string"
)
ERR_LABEL_LEAF_VALUE_IBAN_CANNOT_BE_PARSED = "label leaf value IBAN cannot be parsed"

ALPHANUMERIC_RE = re.compile(r"[^A-Za-z0-9]")


class IBAN(SemanticType):
    """
    International Bank Account Number complying to the ISO 13616-1 standard.

    An IBAN consists of a two-letter ISO 3166-1 country code, two check digits, and up
    to thirty alphanumeric characters for the domestic bank account number (BBAN).
    The exact length and structure depend on the issuing country.

    :examples: `DE89370400440532013000` (Germany), `FR7630006000011234567890189`
    (France)
    """

    json_schema_format = "iban-ISO_13616-1"

    @classmethod
    def coerce(
        cls, value: str, input_text: str | None = None, error: ErrorJson | None = None
    ) -> str | None:
        """
        Try to convert a value to its string type.

        :param value: value to convert to string if it can, otherwise ``None``.
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
        if not isinstance(value, str):
            return None
        if schwifty is None:
            return value
        if error.error_message in {
            ERR_LABEL_LEAF_VALUE_IBAN_CANNOT_BE_PARSED,
            ERR_LABEL_LEAF_VALUE_IS_NOT_A_VALID_IBAN,
        }:
            return None

        # Try to clean messy string
        iban = schwifty.IBAN(value)
        return str(iban)

    @classmethod
    def validate(cls, value: object, _: str | None = None) -> str | None:
        """
        Check that a string is a valid IBAN.

        :param value: string value to assess.
        :param _: placeholder for input text.
        :return: error message if the value should be ``None``, otherwise ``None``.
        """
        if not isinstance(value, str):
            return ERR_LABEL_LEAF_VALUE_IBAN_IS_NOT_STRING
        if schwifty is None:
            return None
        try:
            iban = schwifty.IBAN(value)
            if not iban.validate(validate_bban=True):
                return ERR_LABEL_LEAF_VALUE_IS_NOT_A_VALID_IBAN
            if str(iban) != value:
                return ERR_LABEL_LEAF_VALUE_IS_VALID_IBAN_BUT_IS_MESSY_STRING

        except schwifty.exceptions.SchwiftyException:
            return ERR_LABEL_LEAF_VALUE_IBAN_CANNOT_BE_PARSED
        return None
