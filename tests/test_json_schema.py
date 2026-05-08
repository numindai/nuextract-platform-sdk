"""Tests conversions between NuExtract template and JSON Schema."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from numind.nuextract_utils import (
    convert_json_schema_to_nuextract_template,
    convert_nuextract_template_to_json_schema,
)
from numind.nuextract_utils.json_schema import (
    convert_json_schema_to_nuextract_compatible_json_schema,
    detect_errors_json_schema,
)

# nuextract_template, json_schema
TEST_CASES_NUEXTRACT_TO_JSON_SCHEMA = [
    (
        {
            "test1": "string",
            "int1": "integer",
            "verbstr1": "verbatim-string",
            "date_time": "date-time",
            "date": "date",
            "time": "time",
            "duration": "duration",
            "choices": ["red", "amber", "green"],
            "multi-choices": [["red", "amber", "green"]],
            "countries": "country",
            "regions": "region:US",
            "currencies": "currency",
            "languages": "language",
            "scripts": "script",
            "language-tags": "language-tag",
            "urls": "url",
            "email-addresses": "email-address",
            "phone-numbers": "phone-number",
            "ibans": "iban",
            "bics": "bic",
            "bool": "boolean",
        },
        {
            "type": "object",
            "properties": {
                "test1": {"type": "string"},
                "int1": {"type": "integer"},
                "verbstr1": {"type": "string", "x-verbatim": True},
                "date_time": {"type": "string", "format": "date-time"},
                "date": {"type": "string", "format": "date"},
                "time": {"type": "string", "format": "time"},
                "duration": {"type": "string", "format": "duration"},
                "choices": {"enum": ["red", "amber", "green"]},
                "multi-choices": {
                    "items": {"enum": ["red", "amber", "green"]},
                    "type": "array",
                },
                "countries": {
                    "format": "country-code-ISO_3166-1_2chars",
                    "type": "string",
                },
                "regions": {"format": "region-code-ISO_3166-2:US", "type": "string"},
                "currencies": {
                    "format": "currency-code-ISO_4217_3chars",
                    "type": "string",
                },
                "languages": {
                    "format": "language-code-ISO_639-3_3chars",
                    "type": "string",
                },
                "scripts": {"format": "script-code-ISO_15924-4chars", "type": "string"},
                "language-tags": {
                    "format": "language-tag-IETF-BCP-47",
                    "type": "string",
                },
                "urls": {"format": "iri", "type": "string"},
                "email-addresses": {"format": "idn-email", "type": "string"},
                "phone-numbers": {"format": "phone-number-E.164", "type": "string"},
                "ibans": {"format": "iban-ISO_13616-1", "type": "string"},
                "bics": {"format": "bice-code-ISO_9362", "type": "string"},
                "bool": {"type": "boolean"},
            },
        },
    )
]


def _load_json_schema_to_template_cases() -> list[tuple[dict, dict]]:
    fixture_dir = Path(__file__).parent / "json_schema_test_cases"
    fixture_cases = []

    for path in sorted(fixture_dir.glob("*.json")):
        fixture = json.loads(path.read_text())
        fixture_cases.append(
            (
                fixture["json_schema"],
                _normalize_template_case(fixture["template"]),
            )
        )

    return [
        (
            {
                "type": "object",
                "$defs": {
                    "slash/name": {"type": "string", "format": "date-time"},
                },
                "properties": {
                    "status": {"enum": ["red", "amber", "green"]},
                    "multi_status": {
                        "type": "array",
                        "items": {"enum": ["red", "amber", "green"]},
                    },
                    "verbatim": {"type": "string", "x-verbatim": True},
                    "country": {
                        "anyOf": [
                            {
                                "type": "string",
                                "description": "country-code-ISO_3166-1_2chars",
                            },
                            {"type": "null"},
                        ]
                    },
                    "timestamp": {"$ref": "#/$defs/slash~1name"},
                },
            },
            {
                "status": ["red", "amber", "green"],
                "multi_status": [["red", "amber", "green"]],
                "verbatim": "verbatim-string",
                "country": "country",
                "timestamp": "date-time",
            },
        ),
        *fixture_cases,
    ]


def _normalize_template_case(template: object) -> object:
    if isinstance(template, dict):
        normalized = {
            key: _normalize_template_case(value) for key, value in template.items()
        }
        return {
            key: value
            for key, value in normalized.items()
            if not (key == "type" and value == ["text"])
        }

    if isinstance(template, list):
        return [_normalize_template_case(item) for item in template]

    return template


@pytest.mark.parametrize(
    ("nuextract_template", "json_schema_target"), TEST_CASES_NUEXTRACT_TO_JSON_SCHEMA
)
def test_json_schema_conversion(
    nuextract_template: dict,
    json_schema_target: dict,
) -> None:
    json_schema = convert_nuextract_template_to_json_schema(nuextract_template)
    json_schema_errors = detect_errors_json_schema(json_schema)
    assert len(json_schema_errors) == 0
    assert json_schema == json_schema_target


@pytest.mark.parametrize(
    "nuextract_template",
    [test_case[0] for test_case in TEST_CASES_NUEXTRACT_TO_JSON_SCHEMA],
)
def test_json_schema_round_trip(nuextract_template: dict) -> None:
    json_schema = convert_nuextract_template_to_json_schema(nuextract_template)

    template, dropped_branches = convert_json_schema_to_nuextract_template(json_schema)

    assert template == nuextract_template
    assert dropped_branches == []


@pytest.mark.parametrize(
    ("schema", "template_target"),
    _load_json_schema_to_template_cases(),
)
def test_json_schema_to_template_supports_description_refs_and_enums(
    schema: dict,
    template_target: dict,
) -> None:
    template, _ = convert_json_schema_to_nuextract_template(schema)

    assert template == template_target


@pytest.mark.parametrize("schema_format", ["iri", "uri", "url"])
def test_json_schema_to_template_supports_url_format_aliases(
    schema_format: str,
) -> None:
    schema = {
        "type": "object",
        "properties": {
            "link": {"type": "string", "format": schema_format},
        },
    }

    template, dropped_branches = convert_json_schema_to_nuextract_template(schema)

    assert template == {"link": "url"}
    assert dropped_branches == []


def test_json_schema_to_template_rejects_non_nullable_anyof() -> None:
    schema = {
        "anyOf": [
            {"type": "string"},
            {"type": "integer"},
        ]
    }

    with pytest.raises(ValueError, match="Only nullable unions"):
        convert_json_schema_to_nuextract_template(schema)


def test_json_schema_to_template_can_omit_unsupported_branches() -> None:
    schema = {
        "type": "object",
        "properties": {
            "valid": {"type": "string"},
            "invalid_union": {
                "anyOf": [
                    {"type": "string"},
                    {"type": "integer"},
                ]
            },
            "invalid_ref": {"$ref": "#/$defs/missing"},
            "empty_after_omit": {
                "type": "object",
                "properties": {
                    "singleton_enum": {"enum": ["fixed"]},
                    "invalid_union": {
                        "anyOf": [
                            {"type": "string"},
                            {"type": "integer"},
                        ]
                    },
                },
            },
            "nested": {
                "type": "object",
                "properties": {
                    "kept": {"type": "integer"},
                    "dropped": {"enum": ["constant"]},
                },
            },
        },
    }

    template, dropped_branches = convert_json_schema_to_nuextract_template(
        schema,
        omit_unsupported_branches=True,
    )

    assert template == {
        "valid": "string",
        "nested": {"kept": "integer"},
    }
    assert dropped_branches == [
        {
            "path": ["properties", "invalid_union"],
            "error": (
                "Unsupported anyOf node. Only nullable unions of a single non-null "
                "schema are supported. Node: {'anyOf': [{'type': 'string'}, "
                "{'type': 'integer'}]}"
            ),
        },
        {
            "path": ["properties", "invalid_ref"],
            "error": "Could not resolve $ref: '#/$defs/missing'",
        },
        {
            "path": ["properties", "empty_after_omit", "properties", "singleton_enum"],
            "error": "Unsupported enum node: single-value enums are omitted.",
        },
        {
            "path": ["properties", "empty_after_omit", "properties", "invalid_union"],
            "error": (
                "Unsupported anyOf node. Only nullable unions of a single non-null "
                "schema are supported. Node: {'anyOf': [{'type': 'string'}, "
                "{'type': 'integer'}]}"
            ),
        },
        {
            "path": ["properties", "nested", "properties", "dropped"],
            "error": "Unsupported enum node: single-value enums are omitted.",
        },
    ]


def test_json_schema_to_template_collects_dropped_branches() -> None:
    schema = {
        "type": "object",
        "properties": {
            "valid": {"type": "string"},
            "invalid_union": {
                "anyOf": [
                    {"type": "string"},
                    {"type": "integer"},
                ]
            },
            "invalid_ref": {"$ref": "#/$defs/missing"},
            "singleton_enum": {"enum": ["fixed"]},
        },
    }
    template, dropped_branches = convert_json_schema_to_nuextract_template(
        schema,
        omit_unsupported_branches=True,
    )

    assert template == {"valid": "string"}
    assert dropped_branches == [
        {
            "path": ["properties", "invalid_union"],
            "error": (
                "Unsupported anyOf node. Only nullable unions of a single non-null "
                "schema are supported. Node: {'anyOf': [{'type': 'string'}, "
                "{'type': 'integer'}]}"
            ),
        },
        {
            "path": ["properties", "invalid_ref"],
            "error": "Could not resolve $ref: '#/$defs/missing'",
        },
        {
            "path": ["properties", "singleton_enum"],
            "error": "Unsupported enum node: single-value enums are omitted.",
        },
    ]


def test_json_schema_to_nuextract_compatible_json_schema_drops_unsupported_nodes() -> (
    None
):
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": ["valid", "broken_union", "missing_array_items"],
        "properties": {
            "valid": {"type": "string", "description": "Kept"},
            "broken_union": {
                "anyOf": [
                    {"type": "string"},
                    {"type": "integer"},
                ]
            },
            "missing_array_items": {
                "type": "array",
            },
            "nested": {
                "type": "object",
                "required": ["kept", "dropped"],
                "properties": {
                    "kept": {"type": "integer"},
                    "dropped": {"enum": ["constant"]},
                },
            },
        },
    }

    compatible_schema, dropped_branches = (
        convert_json_schema_to_nuextract_compatible_json_schema(schema)
    )

    assert compatible_schema == {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "properties": {
            "valid": {"type": "string", "description": "Kept"},
            "nested": {
                "type": "object",
                "properties": {
                    "kept": {"type": "integer"},
                },
                "required": ["kept"],
            },
        },
        "required": ["valid"],
    }
    assert dropped_branches == [
        {
            "path": ["properties", "broken_union"],
            "error": (
                "Unsupported anyOf node. Only nullable unions of a single non-null "
                "schema are supported. Node: {'anyOf': [{'type': 'string'}, "
                "{'type': 'integer'}]}"
            ),
        },
        {
            "path": ["properties", "missing_array_items"],
            "error": "Unsupported array node without 'items'. Node: {'type': 'array'}",
        },
        {
            "path": ["properties", "nested", "properties", "dropped"],
            "error": "Unsupported enum node: single-value enums are omitted.",
        },
    ]
    assert detect_errors_json_schema(compatible_schema) == []

    template, template_dropped_branches = convert_json_schema_to_nuextract_template(
        compatible_schema
    )
    assert template == {
        "valid": "string",
        "nested": {"kept": "integer"},
    }
    assert template_dropped_branches == []


def test_json_schema_to_nuextract_compatible_json_schema_inlines_refs() -> None:
    schema = {
        "type": "object",
        "$defs": {
            "person": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "tags": {
                        "type": "array",
                        "items": {"enum": ["vip", "new"]},
                    },
                },
            }
        },
        "properties": {
            "person": {"$ref": "#/$defs/person"},
            "optional_person": {
                "anyOf": [
                    {"$ref": "#/$defs/person"},
                    {"type": "null"},
                ]
            },
        },
    }

    compatible_schema, dropped_branches = (
        convert_json_schema_to_nuextract_compatible_json_schema(schema)
    )

    assert compatible_schema == {
        "type": "object",
        "properties": {
            "person": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "tags": {
                        "type": "array",
                        "items": {"enum": ["vip", "new"]},
                    },
                },
            },
            "optional_person": {
                "anyOf": [
                    {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "tags": {
                                "type": "array",
                                "items": {"enum": ["vip", "new"]},
                            },
                        },
                    },
                    {"type": "null"},
                ]
            },
        },
    }
    assert dropped_branches == []

    template, template_dropped_branches = convert_json_schema_to_nuextract_template(
        compatible_schema
    )
    assert template == {
        "person": {
            "name": "string",
            "tags": [["vip", "new"]],
        },
        "optional_person": {
            "name": "string",
            "tags": [["vip", "new"]],
        },
    }
    assert template_dropped_branches == []


def test_json_schema_to_nuextract_compatible_json_schema_supports_allof_objects() -> (
    None
):
    schema = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "allOf": [
            {"$ref": "#/definitions/competency"},
            {
                "properties": {
                    "description": {"minLength": 1, "type": "string"},
                    "scale": {
                        "properties": {
                            "levels": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                            "name": {"type": "string"},
                        },
                        "required": ["name", "levels"],
                        "type": "object",
                    },
                },
                "required": ["description", "scale"],
            },
        ],
        "definitions": {
            "competency": {
                "allOf": [
                    {"$ref": "#/definitions/namedObject"},
                    {
                        "oneOf": [
                            {"type": "string"},
                            {"type": "integer"},
                        ]
                    },
                ]
            },
            "namedObject": {
                "properties": {
                    "name": {
                        "maxLength": 500,
                        "minLength": 1,
                        "type": "string",
                    }
                },
                "required": ["name"],
                "type": "object",
            },
        },
        "description": "Competency framework schema",
    }

    compatible_schema, dropped_branches = (
        convert_json_schema_to_nuextract_compatible_json_schema(schema)
    )

    assert compatible_schema == {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Competency framework schema",
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "description": {"type": "string"},
            "scale": {
                "type": "object",
                "properties": {
                    "levels": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "name": {"type": "string"},
                },
                "required": ["name", "levels"],
            },
        },
        "required": ["name", "description", "scale"],
    }
    assert dropped_branches == [
        {
            "path": ["allOf", 0, "allOf", 1],
            "error": (
                "Invalid schema segment: Node does not contain '$ref', 'anyOf', "
                "or 'type'. Node: {'oneOf': [{'type': 'string'}, "
                "{'type': 'integer'}]}"
            ),
        }
    ]
    assert detect_errors_json_schema(compatible_schema) == []

    template, template_dropped_branches = convert_json_schema_to_nuextract_template(
        compatible_schema
    )
    assert template == {
        "name": "string",
        "description": "string",
        "scale": {
            "levels": ["string"],
            "name": "string",
        },
    }
    assert template_dropped_branches == []


def test_json_schema_to_template_supports_allof_objects() -> None:
    schema = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "allOf": [
            {"$ref": "#/definitions/competency"},
            {
                "properties": {
                    "description": {"minLength": 1, "type": "string"},
                    "scale": {
                        "properties": {
                            "levels": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                            "name": {"type": "string"},
                        },
                        "required": ["name", "levels"],
                        "type": "object",
                    },
                },
                "required": ["description", "scale"],
            },
        ],
        "definitions": {
            "competency": {
                "allOf": [
                    {"$ref": "#/definitions/namedObject"},
                    {
                        "oneOf": [
                            {"type": "string"},
                            {"type": "integer"},
                        ]
                    },
                ]
            },
            "namedObject": {
                "properties": {
                    "name": {
                        "maxLength": 500,
                        "minLength": 1,
                        "type": "string",
                    }
                },
                "required": ["name"],
                "type": "object",
            },
        },
        "description": "Competency framework schema",
    }

    template, dropped_branches = convert_json_schema_to_nuextract_template(
        schema,
        omit_unsupported_branches=True,
    )

    assert template == {
        "name": "string",
        "description": "string",
        "scale": {
            "levels": ["string"],
            "name": "string",
        },
    }
    assert dropped_branches == [
        {
            "path": ["allOf", 0, "allOf", 1],
            "error": (
                "Invalid schema segment: Node does not contain '$ref', 'anyOf', "
                "or 'type'. Node: {'oneOf': [{'type': 'string'}, "
                "{'type': 'integer'}]}"
            ),
        }
    ]


def test_json_schema_to_template_supports_properties_without_object_type() -> None:
    schema = {
        "type": "object",
        "properties": {
            "nat": {
                "type": "array",
                "items": {
                    "properties": {
                        "season": {"type": "string"},
                        "data": {
                            "type": "array",
                            "items": {
                                "properties": {
                                    "value": {"type": "integer"},
                                }
                            },
                        },
                    }
                },
            }
        },
    }

    template, dropped_branches = convert_json_schema_to_nuextract_template(schema)

    assert template == {
        "nat": [
            {
                "season": "string",
                "data": [{"value": "integer"}],
            }
        ]
    }
    assert dropped_branches == []


def test_json_schema_to_template_prefers_explicit_array_type_over_properties() -> None:
    schema = {
        "type": "array",
        "properties": {},
        "items": {
            "type": "object",
            "properties": {
                "id": {"type": "string"},
                "categories": {
                    "type": "array",
                    "items": {"type": "number"},
                },
            },
        },
    }

    template, dropped_branches = convert_json_schema_to_nuextract_template(schema)

    assert template == [
        {
            "id": "string",
            "categories": ["number"],
        }
    ]
    assert dropped_branches == []


def test_json_schema_to_template_supports_nullable_type_shorthand() -> None:
    schema = {
        "type": "object",
        "properties": {
            "item_list_id": {"type": ["string", "null"]},
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "item_name": {"type": ["string", "null"]},
                        "price": {"type": ["number", "null"]},
                        "quantity": {"type": ["integer", "null"]},
                    },
                },
            },
        },
    }

    template, dropped_branches = convert_json_schema_to_nuextract_template(schema)

    assert template == {
        "item_list_id": "string",
        "items": [
            {
                "item_name": "string",
                "price": "number",
                "quantity": "integer",
            }
        ],
    }
    assert dropped_branches == []


def test_json_schema_to_template_supports_additional_properties_schema() -> None:
    schema = {
        "type": "object",
        "additionalProperties": {
            "type": "object",
            "additionalProperties": True,
            "properties": {
                "garnish": {"type": "string"},
                "glass": {
                    "type": "string",
                    "enum": ["martini", "cocktail"],
                },
                "ingredients": {"type": "object"},
                "profile": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["strong", "sweet"],
                    },
                },
                "variants": {
                    "type": "array",
                    "items": {"type": "string"},
                },
            },
        },
    }

    template, dropped_branches = convert_json_schema_to_nuextract_template(schema)

    assert template == {
        "garnish": "string",
        "glass": ["martini", "cocktail"],
        "profile": [["strong", "sweet"]],
        "variants": ["string"],
    }
    assert dropped_branches == []


def test_json_schema_to_template_merges_properties_and_additional_properties() -> None:
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "category": {"enum": ["classic", "modern"]},
        },
        "additionalProperties": {
            "type": "object",
            "properties": {
                "garnish": {"type": "string"},
                "profile": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["strong", "sweet"],
                    },
                },
            },
        },
    }

    template, dropped_branches = convert_json_schema_to_nuextract_template(schema)

    assert template == {
        "name": "string",
        "category": ["classic", "modern"],
        "garnish": "string",
        "profile": [["strong", "sweet"]],
    }
    assert dropped_branches == []


def test_json_schema_to_template_ignores_non_object_additional_properties() -> None:
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
        },
        "additionalProperties": {"type": "string"},
    }

    template, dropped_branches = convert_json_schema_to_nuextract_template(schema)

    assert template == {
        "name": "string",
    }
    assert dropped_branches == []


def test_json_schema_to_template_supports_ref_in_additional_properties() -> None:
    schema = {
        "type": "object",
        "$defs": {
            "extra_fields": {
                "type": "object",
                "properties": {
                    "garnish": {"type": "string"},
                    "profile": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": ["strong", "sweet"],
                        },
                    },
                },
            }
        },
        "properties": {
            "name": {"type": "string"},
        },
        "additionalProperties": {"$ref": "#/$defs/extra_fields"},
    }

    template, dropped_branches = convert_json_schema_to_nuextract_template(schema)

    assert template == {
        "name": "string",
        "garnish": "string",
        "profile": [["strong", "sweet"]],
    }
    assert dropped_branches == []


def test_json_schema_to_template_keeps_open_object_leaves() -> None:
    schema = {
        "type": "object",
        "properties": {
            "empty_object": {"type": "object"},
            "empty_additional_properties": {
                "type": "object",
                "additionalProperties": {},
            },
            "nested": {
                "type": "object",
                "properties": {
                    "kept": {"type": "string"},
                    "empty_object": {"type": "object"},
                },
            },
        },
    }

    template, dropped_branches = convert_json_schema_to_nuextract_template(schema)

    assert template == {
        "empty_additional_properties": {},
        "nested": {
            "kept": "string",
        },
    }
    assert dropped_branches == []


def test_json_schema_to_template_omit_unsupported_branches_still_rejects_root() -> None:
    schema = {
        "type": "object",
        "properties": {
            "only_invalid_union": {
                "anyOf": [
                    {"type": "string"},
                    {"type": "integer"},
                ]
            },
            "only_singleton_enum": {"enum": ["fixed"]},
        },
    }

    with pytest.raises(ValueError, match="Root schema is unsupported"):
        convert_json_schema_to_nuextract_template(
            schema,
            omit_unsupported_branches=True,
        )
