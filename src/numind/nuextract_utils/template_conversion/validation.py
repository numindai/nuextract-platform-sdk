"""
Validation of JSON schemas.

JSON Schema documentation:
* https://json-schema.org/draft/2020-12/json-schema-core
* https://json-schema.org/draft/2020-12/json-schema-validation
"""

from __future__ import annotations

from collections import deque
from collections.abc import Mapping
from json import JSONDecodeError
from typing import TYPE_CHECKING

import orjson
from jsonschema import Draft202012Validator, ValidationError

from .constants import (
    ERR_INPUT_LINT_DANGLING_DEPENDENCY,
    ERR_INPUT_SCHEMA_NOT_JSON_DESERIALIZABLE,
)

if TYPE_CHECKING:
    from collections.abc import Iterator

_JSON_SCHEMA_VALIDATOR_CLS = Draft202012Validator
_META_VALIDATOR = _JSON_SCHEMA_VALIDATOR_CLS(_JSON_SCHEMA_VALIDATOR_CLS.META_SCHEMA)


def _lint_schema_semantics(
    schema: dict, path: tuple | None = None
) -> Iterator[ValidationError]:
    """
    Recursively find and validate semantic rules and best practices.

    Currently checks for:
    - Dangling dependencies in 'dependentRequired'.
    """
    if not isinstance(schema, Mapping):
        return
    if path is None:
        path = ()

    # Check for dangling dependencies in 'dependentRequired'
    if "dependentRequired" in schema:
        defined_properties = schema.get("properties", {}).keys()
        for prop, required_list in schema["dependentRequired"].items():
            for i, required_prop in enumerate(required_list):
                if required_prop not in defined_properties:
                    error_path = deque((*path, "dependentRequired", prop, i))
                    yield ValidationError(
                        ERR_INPUT_LINT_DANGLING_DEPENDENCY + f": '{required_prop}'",
                        path=error_path,
                    )

    # Recurse into sub-schemas
    # Keywords that can contain sub-schemas
    schema_keywords = [
        "properties",
        "patternProperties",
        "additionalProperties",
        "items",
        "allOf",
        "anyOf",
        "oneOf",
        "not",
        "$defs",
        "dependentSchemas",
    ]
    for keyword in schema_keywords:
        if keyword in schema:
            sub_schema_container = schema[keyword]
            if isinstance(sub_schema_container, Mapping):
                # For keywords like 'properties', 'dependentSchemas', etc.
                for key, sub_schema in sub_schema_container.items():
                    yield from _lint_schema_semantics(sub_schema, (*path, keyword, key))
            elif isinstance(sub_schema_container, list):
                # For keywords like 'items' (tuple form), 'allOf', etc.
                for i, sub_schema in enumerate(sub_schema_container):
                    yield from _lint_schema_semantics(sub_schema, (*path, keyword, i))
            elif isinstance(
                sub_schema_container, (dict, list)
            ):  # Catches items obj, etc.
                yield from _lint_schema_semantics(
                    sub_schema_container,
                    (
                        *path,
                        keyword,
                    ),
                )


def _deduplicate_errors(errors: list[ValidationError]) -> list[ValidationError]:
    """
    Deduplicate a list of ValidationErrors based on their path and message.

    This is necessary because complex meta-schemas (using anyOf, etc.) can
    yield multiple nearly-identical errors for a single conceptual mistake.
    """
    unique_errors = []
    seen_keys = set()
    for error in errors:
        # A unique error is defined by its path in the instance and its message.
        # We convert the deque path to a tuple to make it hashable.
        key = (tuple(error.absolute_path), error.message)
        if key not in seen_keys:
            seen_keys.add(key)
            unique_errors.append(error)
    return unique_errors


def detect_errors_json_schema(schema: dict | list | str) -> list[ValidationError]:
    """
    Return the errors in a JSON schema.

    :param schema: JSON schema to validate.
    :return: list of ``jsonschema.ValidationError``s in the provided schema.
    """
    # 1. Deserialize if the schema is a string
    if isinstance(schema, str):
        try:
            schema = orjson.loads(schema)
        except JSONDecodeError as e:
            return [ValidationError(ERR_INPUT_SCHEMA_NOT_JSON_DESERIALIZABLE, cause=e)]

    # 2. Validate against the meta-schema (your original check)
    # This catches structural errors like `{"type": 123}`
    # If errors are caught here, we return them without checking the rest as it is very
    # likely that the JSON cannot be parsed reliably.
    errors = list(_META_VALIDATOR.iter_errors(schema))
    if len(errors) > 0:
        return _deduplicate_errors(errors)

    # 3. Semantic validation (linting)
    errors.extend(list(_lint_schema_semantics(schema)))

    # Return the collected errors
    return errors
