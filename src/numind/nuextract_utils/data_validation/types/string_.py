"""String type."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .base import SemanticType

if TYPE_CHECKING:
    from numind.nuextract_utils.data_validation.models import ErrorJson

ERR_LABEL_LEAF_VALUE_NULL_STRING_INSTEAD_OF_NULL = (
    'label leaf value is "null" string instead of plain null'
)
ERR_LABEL_LEAF_VALUE_IS_NOT_A_STRING = "label leaf value is not a string"
ERRORS_STRING = {
    ERR_LABEL_LEAF_VALUE_IS_NOT_A_STRING,
    ERR_LABEL_LEAF_VALUE_NULL_STRING_INSTEAD_OF_NULL,
}

NULL_STRINGS = {
    "",
    "null",
    "none",
    "not provided",
    "unspecified",
    "not specified",
    "undisclosed",
    "not disclosed",
    "undefined",
    "not defined",
    "unknown",
}


class String(SemanticType):
    """
    A string.

    It may be abstractive and may allow the model to return values deduced from
    knowledge or reasoning.

    :examples: `Hello World`, `any string`
    """

    @classmethod
    def coerce(
        cls,
        value: object,
        input_text: str | None = None,
        error: ErrorJson | None = None,
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
        if (
            value is None
            or error.error_message == ERR_LABEL_LEAF_VALUE_NULL_STRING_INSTEAD_OF_NULL
        ):
            return None
        if not isinstance(value, str):
            try:
                return str(value)
            except (ValueError, TypeError):
                return None
        return None

    @classmethod
    def validate(cls, value: object, _: str | None = None) -> str | None:
        """
        Check that a string is not considered "null" (and thus should be ``None``).

        :param value: string value to assess.
        :param _: placeholder for input text.
        :return: error message if the value should be ``None``, otherwise ``None``.
        """
        if not isinstance(value, str):
            return ERR_LABEL_LEAF_VALUE_IS_NOT_A_STRING
        if value.lower() in NULL_STRINGS:
            return ERR_LABEL_LEAF_VALUE_NULL_STRING_INSTEAD_OF_NULL
        return None
