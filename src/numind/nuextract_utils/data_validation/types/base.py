"""Base API for NuExtract semantic leaf types."""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Union

if TYPE_CHECKING:
    from numind.nuextract_utils.data_validation.models import ErrorJson

PrimitiveType = Union[type, tuple[type, ...]]


class SemanticType:
    """
    Common API for semantic types that coerce to primitive Python values.

    These classes are validators/coercers, not runtime wrapper instances. Their
    ``__new__`` methods return a primitive value such as ``str`` or ``int``.
    """

    primitive_type: ClassVar[PrimitiveType] = str

    def __new__(
        cls,
        value: object,
        input_text: str | None = None,
        error: ErrorJson | None = None,
    ) -> object:
        """Coerce ``value`` into the semantic type primitive representation."""
        return cls.coerce(value, input_text, error)

    @classmethod
    def coerce(
        cls,
        value: object,
        input_text: str | None = None,
        error: ErrorJson | None = None,
    ) -> object:
        """
        Convert a raw value into the semantic type primitive representation.

        :param value: value to create from.
        :param input_text: input text, used for verbatim-string assertion.
        :param error: error associated to the value to convert. This argument
            can help to convert the value by targeting to the appropriate methods
            (default: ``None``).
        :return: an int value if the provided value can be converted, otherwise
            ``None``.
        """
        raise NotImplementedError

    @classmethod
    def is_valid_primitive_instance(cls, value: object) -> bool:
        """Return whether ``value`` matches the primitive runtime type."""
        primitive_types = cls.primitive_type
        if not isinstance(primitive_types, tuple):
            primitive_types = (primitive_types,)

        value_type = type(value)
        for primitive_type in primitive_types:
            if primitive_type in {bool, int}:
                if value_type is primitive_type:
                    return True
                continue

            if isinstance(value, primitive_type):
                return True

        return False

    @classmethod
    def validate(
        cls,
        value: object,  # noqa: ARG003
        input_text: str | None = None,  # noqa: ARG003
    ) -> str | None:
        """Validate a primitive value against the semantic type."""
        return None
