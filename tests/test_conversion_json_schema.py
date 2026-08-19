"""Tests conversions between NuExtract template and JSON Schema."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from numind.nuextract_utils.template_conversion import (
    convert_json_schema_to_nuextract_template,
    convert_nuextract_template_to_json_schema,
    detect_errors_json_schema,
)
from numind.nuextract_utils.template_conversion.json_schema import (
    adapt_json_to_nuextract_template,
    convert_json_schema_to_nuextract_compatible_json_schema,
)

_AMBIGUOUS_UNION_ERROR = (
    "Union is ambiguous because no instance value selects exactly one alternative."
)
_INSTANCE_SELECTED_UNION_ERROR = (
    "Union requires instance-specific branch selection and cannot be represented "
    "completely by one NuExtract template."
)
_DYNAMIC_OBJECT_ERROR = (
    "Dynamic object keys cannot be represented by a NuExtract template."
)


def _convert_json_schema_to_nuextract_template_values(
    schema: dict,
    **kwargs: object,
) -> tuple[object, list[dict], list[str]]:
    conversion = convert_json_schema_to_nuextract_template(schema, **kwargs)
    schema_incompatibilities = [
        {
            "path": incompatibility["schema_path"],
            "error": incompatibility["error"],
        }
        for incompatibility in conversion["incompatibilities"]
        if incompatibility["kind"] == "schema_node_not_convertible"
    ]
    return (
        conversion["template"],
        schema_incompatibilities,
        conversion["descriptions"],
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

    template, dropped_branches, descriptions = (
        _convert_json_schema_to_nuextract_template_values(json_schema)
    )

    assert template == nuextract_template
    assert dropped_branches == []
    assert descriptions == []


def test_json_schema_conversion_applies_object_annotations_to_every_object() -> None:
    json_schema = convert_nuextract_template_to_json_schema(
        {
            "name": "string",
            "address": {"city": "string"},
        },
        objects_annotations={"additionalProperties": False},
    )

    assert json_schema == {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "address": {
                "type": "object",
                "properties": {"city": {"type": "string"}},
                "additionalProperties": False,
            },
        },
        "additionalProperties": False,
    }


def test_json_schema_conversion_applies_leaf_schema_overrides() -> None:
    bbox_json_schema = {
        "type": "object",
        "properties": {
            "image_index": {"type": "integer"},
            "bbox_2d": {
                "type": "array",
                "items": {"type": "integer"},
                "minItems": 4,
                "maxItems": 4,
            },
        },
        "required": ["image_index", "bbox_2d"],
        "additionalProperties": False,
    }

    json_schema = convert_nuextract_template_to_json_schema(
        {"name": "string", "name_bboxes": ["bbox"]},
        leaf_schema_overrides={"bbox": bbox_json_schema},
    )

    assert json_schema == {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "name_bboxes": {
                "type": "array",
                "items": bbox_json_schema,
            },
        },
    }


@pytest.mark.parametrize(
    ("schema", "template_target"),
    _load_json_schema_to_template_cases(),
)
def test_json_schema_to_template_supports_description_refs_and_enums(
    schema: dict,
    template_target: dict,
) -> None:
    template, _, _ = _convert_json_schema_to_nuextract_template_values(
        schema,
        omit_unsupported_branches=True,
    )

    assert template == template_target


def test_json_schema_to_template_supports_nullable_enums() -> None:
    schema = {
        "type": "object",
        "properties": {
            "status": {
                "type": ["string", "null"],
                "enum": ["open", "closed", None],
            },
            "classification": {
                "type": "string",
                "enum": ["xbrl", None],
            },
        },
    }

    template, dropped_branches, _ = _convert_json_schema_to_nuextract_template_values(
        schema
    )

    assert template == {
        "status": ["open", "closed"],
        "classification": "string",
    }
    assert dropped_branches == []


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

    template, dropped_branches, _ = _convert_json_schema_to_nuextract_template_values(
        schema
    )

    assert template == {"link": "url"}
    assert dropped_branches == []


def test_json_schema_to_template_rejects_non_nullable_anyof() -> None:
    schema = {
        "anyOf": [
            {"type": "string"},
            {"type": "integer"},
        ]
    }

    with pytest.raises(ValueError, match="ambiguous"):
        _convert_json_schema_to_nuextract_template_values(schema)


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

    template, dropped_branches, descriptions = (
        _convert_json_schema_to_nuextract_template_values(
            schema,
            omit_unsupported_branches=True,
        )
    )

    assert template == {
        "valid": "string",
        "nested": {"kept": "integer"},
    }
    assert dropped_branches == [
        {
            "path": ["properties", "invalid_union"],
            "error": _AMBIGUOUS_UNION_ERROR,
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
            "error": _AMBIGUOUS_UNION_ERROR,
        },
        {
            "path": ["properties", "nested", "properties", "dropped"],
            "error": "Unsupported enum node: single-value enums are omitted.",
        },
    ]
    assert descriptions == []


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
    template, dropped_branches, _ = _convert_json_schema_to_nuextract_template_values(
        schema,
        omit_unsupported_branches=True,
    )

    assert template == {"valid": "string"}
    assert dropped_branches == [
        {
            "path": ["properties", "invalid_union"],
            "error": _AMBIGUOUS_UNION_ERROR,
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
            "error": _AMBIGUOUS_UNION_ERROR,
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

    template, template_dropped_branches, _ = (
        _convert_json_schema_to_nuextract_template_values(compatible_schema)
    )
    assert template == {
        "valid": "string",
        "nested": {"kept": "integer"},
    }
    assert template_dropped_branches == []


def test_json_schema_to_template_drops_array_with_empty_converted_items() -> None:
    schema = {
        "type": "object",
        "properties": {
            "valid": {"type": "string"},
            "invalid_array": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "invalid_nested_array": {
                            "type": "array",
                            "items": {},
                        }
                    },
                },
            },
        },
    }

    template, dropped_branches, _ = _convert_json_schema_to_nuextract_template_values(
        schema,
        omit_unsupported_branches=True,
    )

    assert template == {"valid": "string"}
    assert dropped_branches == [
        {
            "path": [
                "properties",
                "invalid_array",
                "items",
                "properties",
                "invalid_nested_array",
                "items",
            ],
            "error": (
                "Invalid schema segment: Node does not contain '$ref', 'anyOf', "
                "or 'type'. Node: {}"
            ),
        }
    ]


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

    template, template_dropped_branches, _ = (
        _convert_json_schema_to_nuextract_template_values(compatible_schema)
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
            "error": _AMBIGUOUS_UNION_ERROR,
        }
    ]
    assert detect_errors_json_schema(compatible_schema) == []

    template, template_dropped_branches, _ = (
        _convert_json_schema_to_nuextract_template_values(compatible_schema)
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

    template, dropped_branches, descriptions = (
        _convert_json_schema_to_nuextract_template_values(
            schema,
            omit_unsupported_branches=True,
        )
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
            "error": _AMBIGUOUS_UNION_ERROR,
        }
    ]
    assert descriptions == ["$: Competency framework schema"]


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

    template, dropped_branches, _ = _convert_json_schema_to_nuextract_template_values(
        schema
    )

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

    template, dropped_branches, _ = _convert_json_schema_to_nuextract_template_values(
        schema
    )

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

    template, dropped_branches, _ = _convert_json_schema_to_nuextract_template_values(
        schema
    )

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


def test_json_schema_to_template_supports_single_item_type_list() -> None:
    schema = {
        "type": ["object"],
        "properties": {"name": {"type": ["string"]}},
    }

    template, dropped_branches, _ = _convert_json_schema_to_nuextract_template_values(
        schema
    )

    assert template == {"name": "string"}
    assert dropped_branches == []


def test_json_schema_to_template_selects_one_object_any_of_branch() -> None:
    schema = {
        "type": "object",
        "anyOf": [
            {
                "type": "object",
                "properties": {
                    "shared": {"type": "string"},
                    "left": {"type": "integer"},
                },
                "required": ["left"],
            },
            {
                "type": "object",
                "properties": {
                    "shared": {"type": "string"},
                    "right": {"type": "number"},
                },
                "required": ["right"],
            },
        ],
    }

    template, dropped_branches, _ = _convert_json_schema_to_nuextract_template_values(
        schema,
        omit_unsupported_branches=True,
        instance={"shared": "value", "left": 1},
    )

    assert template == {
        "shared": "string",
        "left": "integer",
    }
    assert dropped_branches == [
        {
            "path": [],
            "error": _INSTANCE_SELECTED_UNION_ERROR,
        }
    ]


def test_json_schema_to_template_selects_one_oneof_array_item_object() -> None:
    schema = {
        "type": "array",
        "oneOf": [
            {
                "items": {
                    "type": "object",
                    "properties": {"name": {"type": "string"}},
                    "required": ["name"],
                }
            },
            {
                "items": {
                    "type": "object",
                    "properties": {"size": {"type": "integer"}},
                    "required": ["size"],
                }
            },
        ],
    }

    template, dropped_branches, _ = _convert_json_schema_to_nuextract_template_values(
        schema,
        omit_unsupported_branches=True,
        instance=[{"name": "value"}],
    )

    assert template == [{"name": "string"}]
    assert dropped_branches == [
        {
            "path": [],
            "error": _INSTANCE_SELECTED_UNION_ERROR,
        }
    ]


def test_json_schema_to_template_rejects_dynamic_pattern_properties() -> None:
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "projects": {
                "type": "object",
                "patternProperties": {
                    "^[a-z]+$": {
                        "type": "object",
                        "properties": {"title": {"type": "string"}},
                    }
                },
            },
        },
    }

    with pytest.raises(ValueError, match="Dynamic object keys"):
        _convert_json_schema_to_nuextract_template_values(schema)

    template, dropped_branches, _ = _convert_json_schema_to_nuextract_template_values(
        schema,
        omit_unsupported_branches=True,
    )

    assert template == {"name": "string"}
    assert dropped_branches == [
        {
            "path": [
                "properties",
                "projects",
                "patternProperties",
                "^[a-z]+$",
            ],
            "error": _DYNAMIC_OBJECT_ERROR,
        }
    ]


def test_json_schema_to_template_drops_schema_additional_properties() -> None:
    schema = {
        "type": "object",
        "properties": {
            "x": {"type": "string"},
        },
        "additionalProperties": {
            "type": "object",
            "properties": {
                "x": {"type": "integer"},
            },
        },
    }

    with pytest.raises(ValueError, match="Dynamic object keys"):
        _convert_json_schema_to_nuextract_template_values(schema)

    template, dropped_branches, _ = _convert_json_schema_to_nuextract_template_values(
        schema,
        omit_unsupported_branches=True,
    )

    assert template == {"x": "string"}
    assert dropped_branches == [
        {
            "path": ["additionalProperties"],
            "error": _DYNAMIC_OBJECT_ERROR,
        }
    ]


def test_json_schema_to_template_applies_ref_siblings() -> None:
    schema = {
        "$defs": {
            "base": {
                "type": "object",
                "properties": {"a": {"type": "string"}},
            }
        },
        "type": "object",
        "properties": {
            "value": {
                "$ref": "#/$defs/base",
                "properties": {"b": {"type": "integer"}},
            }
        },
    }

    template, dropped_branches, _ = _convert_json_schema_to_nuextract_template_values(
        schema
    )

    assert template == {"value": {"a": "string", "b": "integer"}}
    assert dropped_branches == []


@pytest.mark.parametrize("composition_keyword", ["allOf", "anyOf", "oneOf"])
def test_json_schema_to_template_rejects_composition_property_collisions(
    composition_keyword: str,
) -> None:
    schema = {
        "type": "object",
        "properties": {
            "kept": {"type": "boolean"},
            "value": {
                composition_keyword: [
                    {
                        "type": "object",
                        "properties": {"x": {"type": "string"}},
                    },
                    {
                        "type": "object",
                        "properties": {"x": {"type": "integer"}},
                    },
                ]
            },
        },
    }

    with pytest.raises(ValueError, match=r"incompatible schemas|ambiguous"):
        _convert_json_schema_to_nuextract_template_values(schema)

    template, dropped_branches, _ = _convert_json_schema_to_nuextract_template_values(
        schema,
        omit_unsupported_branches=True,
    )

    assert template == {"kept": "boolean"}
    assert dropped_branches


def test_json_schema_to_template_selects_array_union_from_items() -> None:
    schema = {
        "type": "object",
        "properties": {
            "values": {
                "anyOf": [
                    {"type": "array", "items": {"type": "string"}},
                    {"type": "array", "items": {"type": "integer"}},
                ]
            }
        },
    }

    template, dropped_branches, _ = _convert_json_schema_to_nuextract_template_values(
        schema,
        omit_unsupported_branches=True,
        instance={"values": [1, 2]},
    )

    assert template == {"values": ["integer"]}
    assert dropped_branches == [
        {
            "path": ["properties", "values"],
            "error": _INSTANCE_SELECTED_UNION_ERROR,
        }
    ]


def test_json_schema_to_template_does_not_select_absent_union_value() -> None:
    schema = {
        "type": "object",
        "properties": {
            "values": {
                "anyOf": [
                    {"type": "array", "items": {"type": "string"}},
                    {"type": "array", "items": {"type": "integer"}},
                ]
            },
            "kept": {"type": "boolean"},
        },
    }

    template, dropped_branches, _ = _convert_json_schema_to_nuextract_template_values(
        schema,
        omit_unsupported_branches=True,
        instance={"kept": True},
    )

    assert template == {"kept": "boolean"}
    assert dropped_branches[0]["path"] == ["properties", "values"]


def test_json_schema_to_template_rejects_heterogeneous_prefix_items() -> None:
    schema = {
        "type": "object",
        "properties": {
            "tuple": {
                "type": "array",
                "prefixItems": [{"type": "string"}],
                "items": {"type": "number"},
            },
            "kept": {"type": "string"},
        },
    }

    with pytest.raises(ValueError, match="incompatible schemas"):
        _convert_json_schema_to_nuextract_template_values(schema)

    template, dropped_branches, _ = _convert_json_schema_to_nuextract_template_values(
        schema,
        omit_unsupported_branches=True,
    )

    assert template == {"kept": "string"}
    assert dropped_branches[0]["path"] == ["properties", "tuple"]


def test_json_schema_to_template_ignores_unreachable_trailing_items() -> None:
    schema = {
        "type": "array",
        "prefixItems": [{"type": "string"}],
        "items": {"type": "integer"},
        "maxItems": 1,
    }

    template, dropped_branches, _ = _convert_json_schema_to_nuextract_template_values(
        schema
    )

    assert template == ["string"]
    assert dropped_branches == []


def test_json_schema_to_template_ignores_semantic_formats_on_non_strings() -> None:
    schema = {
        "type": "object",
        "properties": {
            "amount": {"type": "number", "format": "email"},
            "enabled": {"type": "boolean", "description": "date"},
        },
    }

    template, _, _ = _convert_json_schema_to_nuextract_template_values(schema)

    assert template == {"amount": "number", "enabled": "boolean"}


def test_json_schema_to_template_collects_composition_descriptions() -> None:
    schema = {
        "allOf": [
            {
                "type": "object",
                "description": "First branch",
                "properties": {"a": {"type": "string"}},
            },
            {
                "type": "object",
                "description": "Second branch",
                "properties": {"b": {"type": "integer"}},
            },
        ]
    }

    template, _, descriptions = _convert_json_schema_to_nuextract_template_values(
        schema
    )

    assert template == {"a": "string", "b": "integer"}
    assert descriptions == ["$: First branch", "$: Second branch"]


def test_json_schema_to_template_resolves_array_json_pointer_segments() -> None:
    schema = {
        "$defs": {
            "choices": {
                "anyOf": [
                    {"type": "string"},
                    {"type": "integer"},
                ]
            }
        },
        "$ref": "#/$defs/choices/anyOf/0",
    }

    template, dropped_branches, _ = _convert_json_schema_to_nuextract_template_values(
        schema
    )

    assert template == "string"
    assert dropped_branches == []


@pytest.mark.parametrize(
    "schema",
    [
        {"type": "money"},
        {"type": []},
    ],
)
def test_json_schema_to_template_rejects_invalid_schemas(schema: dict) -> None:
    with pytest.raises(ValueError, match="Invalid JSON Schema"):
        _convert_json_schema_to_nuextract_template_values(
            schema,
            omit_unsupported_branches=True,
        )


def test_json_schema_to_template_drops_null_only_properties() -> None:
    schema = {
        "type": "object",
        "properties": {
            "nothing": {"type": "null"},
            "kept": {"type": "string"},
        },
    }

    with pytest.raises(ValueError, match="null-only"):
        _convert_json_schema_to_nuextract_template_values(schema)

    template, dropped_branches, _ = _convert_json_schema_to_nuextract_template_values(
        schema,
        omit_unsupported_branches=True,
    )

    assert template == {"kept": "string"}
    assert dropped_branches == [
        {
            "path": ["properties", "nothing"],
            "error": "Unsupported null-only schema node: {'type': 'null'}",
        }
    ]


def test_json_schema_to_template_reports_an_unconvertible_root() -> None:
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

    conversion = convert_json_schema_to_nuextract_template(
        schema,
        omit_unsupported_branches=True,
    )

    assert conversion["template"] is None
    assert conversion["schema_status"] == "not_convertible"
    assert conversion["instance_status"] == "not_provided"
    assert conversion["adapted_instance"] is None
    assert conversion["incompatibilities"][-1]["schema_path"] == []


def test_json_schema_to_template_selects_union_branch_from_instance() -> None:
    schema = {
        "type": "object",
        "properties": {
            "enabled": {
                "anyOf": [
                    {"type": "boolean"},
                    {"type": "string", "enum": ["yes", "no"]},
                ]
            }
        },
    }

    template, dropped_branches, _ = _convert_json_schema_to_nuextract_template_values(
        schema,
        omit_unsupported_branches=True,
        instance={"enabled": "no"},
    )

    assert template == {"enabled": ["yes", "no"]}
    assert dropped_branches == [
        {
            "path": ["properties", "enabled"],
            "error": _INSTANCE_SELECTED_UNION_ERROR,
        }
    ]


def test_json_schema_to_template_keeps_anyof_structural_siblings() -> None:
    schema = {
        "type": "object",
        "properties": {"common": {"type": "string"}},
        "required": ["common"],
        "anyOf": [
            {
                "type": "object",
                "properties": {"a": {"type": "integer"}},
                "required": ["a"],
            },
            {
                "type": "object",
                "properties": {"b": {"type": "integer"}},
                "required": ["b"],
            },
        ],
    }

    conversion = convert_json_schema_to_nuextract_template(
        schema,
        omit_unsupported_branches=True,
        instance={"common": "value", "a": 1},
    )

    assert conversion["template"] == {"common": "string", "a": "integer"}
    assert conversion["schema_status"] == "partially_converted"
    assert conversion["instance_status"] == "valid_for_both"


def test_json_schema_to_template_keeps_nullable_anyof_structural_siblings() -> None:
    schema = {
        "type": "object",
        "properties": {"common": {"type": "string"}},
        "required": ["common"],
        "anyOf": [
            {
                "type": "object",
                "properties": {"optional": {"type": "integer"}},
            },
            {"type": "null"},
        ],
    }

    conversion = convert_json_schema_to_nuextract_template(
        schema,
        instance={"common": "value", "optional": 1},
    )

    assert conversion["template"] == {
        "common": "string",
        "optional": "integer",
    }
    assert conversion["schema_status"] == "fully_converted"
    assert conversion["instance_status"] == "valid_for_both"


def test_json_schema_to_template_drops_union_used_with_multiple_types() -> None:
    schema = {
        "type": "object",
        "properties": {
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "label": {"type": "string"},
                        "value": {
                            "anyOf": [
                                {"type": "boolean"},
                                {"type": "integer"},
                            ]
                        },
                    },
                },
            }
        },
    }

    template, dropped_branches, _ = _convert_json_schema_to_nuextract_template_values(
        schema,
        omit_unsupported_branches=True,
        instance={
            "items": [
                {"label": "first", "value": False},
                {"label": "second", "value": 70},
            ]
        },
    )

    assert template == {"items": [{"label": "string"}]}
    assert dropped_branches == [
        {
            "path": ["properties", "items", "items", "properties", "value"],
            "error": (
                "Union is ambiguous because the instance does not select exactly "
                "one alternative."
            ),
        }
    ]


def test_json_schema_to_template_reports_an_instance_valid_for_both() -> None:
    schema = {
        "type": "object",
        "properties": {"count": {"type": "integer"}},
        "required": ["count"],
    }
    instance = {"count": 3}

    conversion = convert_json_schema_to_nuextract_template(
        schema,
        instance=instance,
    )

    assert conversion == {
        "template": {"count": "integer"},
        "adapted_instance": {"count": 3},
        "schema_status": "fully_converted",
        "instance_status": "valid_for_both",
        "incompatibilities": [],
        "descriptions": [],
    }
    assert conversion["adapted_instance"] is not instance


def test_json_schema_to_template_adapts_an_instance_valid_for_both() -> None:
    schema = {
        "type": "object",
        "properties": {"count": {"type": "integer"}},
        "required": ["count"],
    }
    instance = {"count": 3, "extra": "remove"}

    conversion = convert_json_schema_to_nuextract_template(schema, instance=instance)

    assert conversion["instance_status"] == "adapted_valid_for_both"
    assert conversion["adapted_instance"] == {"count": 3}
    assert conversion["incompatibilities"] == []
    assert instance == {"count": 3, "extra": "remove"}


def test_json_schema_to_template_adapts_a_root_semantic_value() -> None:
    conversion = convert_json_schema_to_nuextract_template(
        {"type": "string", "format": "url"},
        instance="google.com",
    )

    assert conversion["instance_status"] == "adapted_valid_for_both"
    assert conversion["adapted_instance"] == "https://google.com"
    assert conversion["incompatibilities"] == []


def test_adapt_json_to_nuextract_template_preserves_a_root_enum() -> None:
    adapted_instance, remaining_errors = adapt_json_to_nuextract_template(
        ["open", "closed"],
        "open",
    )

    assert adapted_instance == "open"
    assert remaining_errors == []


def test_adapt_json_to_nuextract_template_deduplicates_a_root_array() -> None:
    adapted_instance, remaining_errors = adapt_json_to_nuextract_template(
        ["integer"],
        [1, 1],
    )

    assert adapted_instance == [1]
    assert remaining_errors == []


def test_json_schema_to_template_reports_an_instance_that_cannot_be_adapted() -> None:
    schema = {
        "type": "object",
        "properties": {
            "kept": {"type": "string"},
            "fixed": {"enum": ["only"]},
        },
        "required": ["kept", "fixed"],
    }

    conversion = convert_json_schema_to_nuextract_template(
        schema,
        omit_unsupported_branches=True,
        instance={"kept": "yes", "fixed": "only"},
    )

    assert conversion["instance_status"] == "not_adaptable"
    assert conversion["adapted_instance"] is None
    assert conversion["incompatibilities"][-1] == {
        "kind": "instance_node_not_adaptable",
        "schema_path": [],
        "instance_path": [],
        "error": "'fixed' is a required property",
    }


def test_json_schema_to_template_reports_an_originally_invalid_instance() -> None:
    schema = {
        "type": "object",
        "properties": {
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {"count": {"type": "integer"}},
                    "required": ["count"],
                },
            }
        },
        "required": ["items"],
    }

    conversion = convert_json_schema_to_nuextract_template(
        schema,
        instance={"items": [{"count": "first"}, {"count": "second"}]},
    )

    assert conversion["instance_status"] == "invalid_for_original_schema"
    assert conversion["adapted_instance"] is None
    assert conversion["incompatibilities"] == [
        {
            "kind": "original_instance_invalid",
            "schema_path": [
                "properties",
                "items",
                "items",
                "properties",
                "count",
            ],
            "instance_path": ["items", "*", "count"],
            "error": "'first' is not of type 'integer'",
        }
    ]


def test_json_schema_to_template_rejects_verbatim_on_non_string_types() -> None:
    schema = {"type": "integer", "x-verbatim": True}

    with pytest.raises(ValueError, match="only supported for string leaves"):
        convert_json_schema_to_nuextract_template(schema)
