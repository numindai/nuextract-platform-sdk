"""Tests for description extraction from JSON Schema."""

from __future__ import annotations

import pytest

from numind.nuextract_utils.json_schema import get_description_json_schema_nodes

TEST_CASES = [
    (
        {
            "type": "object",
            "description": "Root description",
            "properties": {
                "name": {"type": "string", "description": "Customer name"},
                "tags": {
                    "type": "array",
                    "description": "Applied tags",
                    "items": {"type": "string", "description": "Single tag"},
                },
                "address": {
                    "type": "object",
                    "description": "Postal address",
                    "properties": {
                        "city": {"type": "string", "description": "City name"},
                    },
                },
            },
        },
        "\n".join(
            [
                "$: Root description",
                "$.name: Customer name",
                "$.tags: Applied tags",
                "$.tags[]: Single tag",
                "$.address: Postal address",
                "$.address.city: City name",
            ]
        ),
        None,
    ),
    (
        {
            "type": "object",
            "$defs": {
                "person": {
                    "type": "object",
                    "description": "A person entry",
                    "properties": {
                        "country": {
                            "anyOf": [
                                {"type": "string", "description": "Country code"},
                                {"type": "null"},
                            ]
                        }
                    },
                }
            },
            "properties": {
                "owner": {"$ref": "#/$defs/person"},
            },
        },
        "\n".join(
            [
                "$.owner: A person entry",
                "$.owner.country: Country code",
            ]
        ),
        None,
    ),
    (
        {
            "anyOf": [
                {"type": "string", "description": "A"},
                {"type": "integer", "description": "B"},
            ]
        },
        None,
        "Only nullable unions",
    ),
]


@pytest.mark.parametrize(
    ("schema", "expected", "error_match"),
    TEST_CASES,
)
def test_get_description_json_schema_nodes(
    schema: dict,
    expected: str | None,
    error_match: str | None,
) -> None:
    if error_match is not None:
        with pytest.raises(ValueError, match=error_match):
            get_description_json_schema_nodes(schema)
        return

    assert get_description_json_schema_nodes(schema) == expected
