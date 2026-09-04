"""Number type."""

from __future__ import annotations

from contextlib import suppress
from tokenize import TokenError
from typing import TYPE_CHECKING

try:
    from sympy import sympify
except ImportError:
    sympify = None

from .base import SemanticType

if TYPE_CHECKING:
    from numind.nuextract_utils.data_validation.models import ErrorJson


class Number(SemanticType):
    """
    Any number, that may be a floating point number or an integer.

    :examples: `3.14`, `-9.1`, `0`
    """

    primitive_type = (int, float)

    @classmethod
    def coerce(
        cls,
        value: float | str | None = None,
        input_text: str | None = None,
        error: ErrorJson | None = None,
    ) -> float | None:
        """
        Create a float variable while handling more cases than the builtin float.

        :param value: value to create a float from.
        :param input_text: input text.
        :param error: error associated to the value to convert. This argument
            can help to convert the value by targeting to the appropriate methods
            (default: ``None``).
        :return: a float value if the provided value can be converted, otherwise
            ``None``.
        """
        _ = input_text
        _ = error
        if isinstance(value, (float, int)):
            return value
        if isinstance(value, str):
            if sympify is not None:
                try:
                    math_express_result = sympify(value).evalf()
                    return float(math_express_result)
                except (TokenError, SyntaxError, TypeError):
                    pass
            return cls.convert_str_to_float(value)
        return None

    @staticmethod
    def convert_str_to_float(value: str) -> float | None:
        """
        Convert a string representation of a number to a float.

        :param value: string representation of a number.
        :return: float number.
        """
        # Try direct conversion first
        with suppress(ValueError):
            return float(value)

        # Clean the string
        value = value.strip()

        # Handle comma as decimal separator (European format)
        with suppress(ValueError):
            # Replace the last comma with a period
            modified_value = value.replace(",", ".", 1)
            return float(modified_value)

        # Handle thousands separators
        with suppress(ValueError):
            # Remove all commas, assuming they're thousands separators
            modified_value = value.replace(",", "")
            return float(modified_value)

        # Handle European format with both thousand separators and decimal
        with suppress(ValueError):
            # Space or period as thousands separator, comma as decimal
            if "." in value and "," in value and value.rindex(",") > value.rindex("."):
                modified_value = value.replace(".", "").replace(",", ".")
                return float(modified_value)

        # Handle percentage
        with suppress(ValueError):
            if "%" in value:
                modified_value = value.replace("%", "")
                return float(modified_value)

        # Nothing worked, returning None
        return None
