"""BIC (Bank Identifier Code) type."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

import schwifty
from schwifty.exceptions import SchwiftyException

from .base import SemanticType

if TYPE_CHECKING:
    from numind.nuextract_utils.data_validation.models import ErrorJson

ERR_LABEL_LEAF_VALUE_BIC_IS_NOT_STRING = "label leaf value BIC is not a string"
ERR_LABEL_LEAF_VALUE_IS_NOT_A_VALID_BIC = "label leaf value is not a valid BIC"
ERR_LABEL_LEAF_VALUE_IS_VALID_BIC_BUT_IS_MESSY_STRING = (
    "label leaf value is a valid BIC but is a messy string"
)
ERR_LABEL_LEAF_VALUE_BIC_CANNOT_BE_PARSED = "label leaf value BIC cannot be parsed"

ALPHANUMERIC_RE = re.compile(r"[^A-Za-z0-9]")


class BIC(SemanticType):
    """
    Business Identifier Code complying to the ISO 9362 standard.

    The first four characters are the business code, the next two ones the business's
    ISO 3166-1 country code, the next two ones the location code and the last three ones
    the agency/branch code (optional, "XXX" by default).

    :examples: `BNPAFRPPXXX` (BNP Paribas France), `DEUTDEDBFRA` (Deutsche Bank
    Frankfurt)
    """

    json_schema_format = "bice-code-ISO_9362"

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
        if not isinstance(value, str) or error.error_message in {
            ERR_LABEL_LEAF_VALUE_BIC_CANNOT_BE_PARSED,
            ERR_LABEL_LEAF_VALUE_IS_NOT_A_VALID_BIC,
        }:
            return None

        # Try to clean messy string
        bic = schwifty.BIC(value)
        return str(bic)

    @classmethod
    def validate(cls, value: object, _: str | None = None) -> str | None:
        """
        Check that a string is a valid BIC.

        :param value: string value to assess.
        :param _: placeholder for input text.
        :return: error message if the value should be ``None``, otherwise ``None``.
        """
        if not isinstance(value, str):
            return ERR_LABEL_LEAF_VALUE_BIC_IS_NOT_STRING
        try:
            bic = schwifty.BIC(value)
            if not bic.validate(enforce_swift_compliance=True):
                return ERR_LABEL_LEAF_VALUE_IS_NOT_A_VALID_BIC
            if str(bic) != value:
                return ERR_LABEL_LEAF_VALUE_IS_VALID_BIC_BUT_IS_MESSY_STRING

        except SchwiftyException:
            return ERR_LABEL_LEAF_VALUE_BIC_CANNOT_BE_PARSED
        return None
