"""Bounding-box type."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .base import SemanticType

if TYPE_CHECKING:
    from numind.nuextract_utils.data_validation.models import ErrorJson

ERR_LABEL_BBOX_VALUE_INVALID = "label bbox value is not a sequence of 5 integers"


class Bbox(SemanticType):
    """
    Bounding box containing the coordinates of a paired output leaf.

    Represented as ``[image_index, x_min, y_min, x_max, y_max]``,
    where x and y are integers taking values in [0, 1000].

    :examples: `[0, 122, 443, 545, 653]`
    """

    primitive_type = list
    json_schema_format = "bbox"

    @classmethod
    def coerce(
        cls,
        value: object,
        input_text: str | None = None,
        error: ErrorJson | None = None,
    ) -> list[int] | None:
        """
        Return ``value`` when it is a valid bounding box.

        :param value: value to filter.
        :param input_text: unused input text.
        :param error: unused validation error.
        :return: the valid bbox, or ``None`` when it has an invalid shape.
        """
        _ = input_text
        _ = error
        return value if cls.is_valid_bbox(value) else None

    @classmethod
    def validate(cls, value: object, input_text: str | None = None) -> str | None:
        """
        Validate the five-integer bbox output shape.

        :param value: bbox value to validate.
        :param input_text: unused input text.
        :return: error message if ``value`` is invalid, otherwise ``None``.
        """
        _ = input_text
        if cls.is_valid_bbox(value):
            return None
        return ERR_LABEL_BBOX_VALUE_INVALID

    @staticmethod
    def is_valid_bbox(value: object) -> bool:
        """
        Return whether ``value`` is one bbox encoded as five integers.

        :param value: bbox value to validate.
        :return: whether the bbox has the expected output shape.
        """
        return (
            isinstance(value, list)
            and len(value) == 5
            and all(type(coordinate) is int for coordinate in value)
        )
