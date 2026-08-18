"""Shared helpers for NuExtract template validation and correction."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence


def is_object_enum(value: object) -> bool:
    """Return whether a template value represents a single-choice enum."""
    return isinstance(value, list) and len(value) > 1


def is_object_multi_enum(value: object) -> bool:
    """Return whether a template value represents a multi-choice enum."""
    return isinstance(value, list) and len(value) == 1 and isinstance(value[0], list)


def group_identical_elements(
    items: Sequence[object],
) -> list[tuple[list[int], list[object]]]:
    """Group duplicate values with all their positions in ``items``."""
    duplicate_groups: list[tuple[list[int], list[object]]] = []
    for item_index, item in enumerate(items):
        for item_indices, identical_items in duplicate_groups:
            if item == identical_items[0]:
                item_indices.append(item_index)
                identical_items.append(item)
                break
        else:
            duplicate_groups.append(([item_index], [item]))
    return [group for group in duplicate_groups if len(group[0]) > 1]


def mock_schema(schema: dict | list | str) -> dict | list | None:
    """Build an empty output that follows a NuExtract template's structure."""

    def _mock_node(node: dict | list | str) -> dict | list | None:
        if isinstance(node, dict):
            return {key: _mock_node(value) for key, value in node.items()}
        if isinstance(node, list):
            return []
        return None

    return _mock_node(schema)
