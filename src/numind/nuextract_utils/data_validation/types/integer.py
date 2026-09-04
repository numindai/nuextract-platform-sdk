"""Integer type."""

from __future__ import annotations

from tokenize import TokenError
from typing import TYPE_CHECKING

try:
    from sympy import sympify
except ImportError:
    sympify = None

from .base import SemanticType

if TYPE_CHECKING:
    from numind.nuextract_utils.data_validation.models import ErrorJson


class Integer(SemanticType):
    """
    An integer number.

    :examples: `12`, `0`, `-4`
    """

    primitive_type = int
    epsilon = 1e-3

    @classmethod
    def coerce(
        cls,
        value: int | str | None = None,
        input_text: str | None = None,
        error: ErrorJson | None = None,
    ) -> int | None:
        """
        Create an int variable.

        :param value: value to create a float from.
        :param input_text: input text.
        :param error: error associated to the value to convert. This argument
            can help to convert the value by targeting to the appropriate methods
            (default: ``None``).
        :return: an int value if the provided value can be converted, otherwise
            ``None``.
        """
        _ = input_text
        _ = error
        if isinstance(value, int):
            return value
        if isinstance(value, str):
            # Try to convert str to int first
            if (int_val := cls.convert_str_to_int(value)) is not None:
                return int_val

            # Try to evaluate mathematical expression, rounding the result
            if sympify is not None:
                try:
                    return int(sympify(value).evalf().round())
                except (TokenError, SyntaxError, TypeError):
                    pass

        # Nothing worked, returning None
        return None

    @classmethod
    def convert_str_to_int(cls, value: str) -> int | None:
        """
        Try to convert a string to an ``int``.

        :param value: string value to convert to an ``int``.
        :return: int value if the provided value can be converted, otherwise ``None``.
        """
        try:
            int_val = int(value)
        except ValueError:
            return None

        # Return the converted value if its float-converted value is close to the
        # int-converted value
        if abs(int_val - float(value)) <= cls.epsilon:
            return int_val

        return None
