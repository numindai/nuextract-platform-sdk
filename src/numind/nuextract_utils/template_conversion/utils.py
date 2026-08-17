"""Generic useful methods."""

from __future__ import annotations


def is_object_enum(value: object) -> bool:
    """Return whether ``value`` is a NuExtract enum template node."""
    return isinstance(value, list) and len(value) > 1


def is_object_multi_enum(value: object) -> bool:
    """Return whether ``value`` is a NuExtract multi-enum template node."""
    return isinstance(value, list) and len(value) == 1 and isinstance(value[0], list)
