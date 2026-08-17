"""Conversion from NuExtract template to JSON Schema."""

from __future__ import annotations

from collections.abc import Mapping
from copy import deepcopy
from typing import TYPE_CHECKING

from .constants import (
    BBOX_TYPE_NAME,
    JSON_SCHEMA_PRIMITIVES,
    NUEXTRACT_TYPE_TO_JSON_SCHEMA_FORMAT,
)
from .utils import is_object_enum

if TYPE_CHECKING:
    from typing import Any


_TYPE_DESCRIPTION_KEYS = ("format", "description")
_OMIT_FROM_TEMPLATE = object()
_INSTANCE_NOT_PROVIDED = object()
_BBOX_JSON_SCHEMA = {
    "type": "array",
    "prefixItems": [{"type": "integer"}] * 5,
    "minItems": 5,
    "maxItems": 5,
}


def _iter_custom_type_schema_values(type_name: str) -> tuple[str, ...]:
    """Return all JSON Schema metadata values used to represent a custom type."""
    schema_values = NUEXTRACT_TYPE_TO_JSON_SCHEMA_FORMAT.get(type_name, type_name)
    if isinstance(schema_values, str):
        return (schema_values,)
    return tuple(schema_values)


JSON_SCHEMA_FORMAT_TO_NUEXTRACT_TYPE = {
    schema_value: type_name
    for type_name in NUEXTRACT_TYPE_TO_JSON_SCHEMA_FORMAT
    for schema_value in _iter_custom_type_schema_values(type_name)
}


def _build_leaf_schema(
    type_name: str,
    *,
    set_type_in_description: bool = False,
) -> dict[str, Any]:
    """Convert a NuExtract leaf type name into a JSON Schema leaf node."""
    if type_name == BBOX_TYPE_NAME:
        return deepcopy(_BBOX_JSON_SCHEMA)

    leaf: dict[str, Any] = {}
    normalized_type_name = type_name

    if type_name.startswith("verbatim-"):
        leaf["x-verbatim"] = True
        normalized_type_name = type_name[len("verbatim-") :]

    if normalized_type_name.lower() in JSON_SCHEMA_PRIMITIVES:
        leaf["type"] = normalized_type_name.lower()
        return leaf

    leaf["type"] = "string"
    format_key = "description" if set_type_in_description else "format"
    leaf[format_key] = _iter_custom_type_schema_values(normalized_type_name)[0]
    return leaf


def _decode_leaf_type(node: Mapping[str, Any]) -> str | list[str]:
    """Convert a JSON Schema leaf node into a NuExtract leaf representation."""
    if "enum" in node:
        enum_values = node["enum"]
        if not isinstance(enum_values, list) or not all(
            isinstance(value, str) for value in enum_values
        ):
            raise ValueError(_ := f"Unsupported enum node: {node}")
        return enum_values

    node_type = node.get("type")
    if not isinstance(node_type, str):
        raise TypeError(
            _ := f"Invalid schema leaf: missing string 'type'. Node: {node}"
        )

    decoded_type = node_type
    for key in _TYPE_DESCRIPTION_KEYS:
        schema_value = node.get(key)
        if (
            isinstance(schema_value, str)
            and schema_value in JSON_SCHEMA_FORMAT_TO_NUEXTRACT_TYPE
        ):
            decoded_type = JSON_SCHEMA_FORMAT_TO_NUEXTRACT_TYPE[schema_value]
            break

    if node.get("x-verbatim"):
        return f"verbatim-{decoded_type}"

    return decoded_type


def _is_bbox_json_schema(node: Mapping[str, Any]) -> bool:
    """Return whether ``node`` represents the NuExtract bbox output shape."""
    if node.get("type") != "array":
        return False

    prefix_items = node.get("prefixItems")
    return (
        isinstance(prefix_items, list)
        and len(prefix_items) == 5
        and node.get("minItems") == 5
        and node.get("maxItems") == 5
        and all(
            isinstance(prefix_item, Mapping) and prefix_item.get("type") == "integer"
            for prefix_item in prefix_items
        )
    )


def _normalize_nullable_type_shorthand(node: Mapping[str, Any]) -> dict[str, Any]:
    """Normalize singleton and nullable ``type`` lists into one supported type."""
    node_type = node.get("type")
    if not isinstance(node_type, list):
        return dict(node)

    if not all(isinstance(type_name, str) for type_name in node_type):
        raise ValueError(_ := f"Invalid schema leaf: invalid list 'type'. Node: {node}")

    non_null_types = [type_name for type_name in node_type if type_name != "null"]
    if len(node_type) == 1:
        normalized_node = dict(node)
        normalized_node["type"] = node_type[0]
        return normalized_node
    if len(non_null_types) == 1 and len(non_null_types) != len(node_type):
        normalized_node = dict(node)
        normalized_node["type"] = non_null_types[0]
        return normalized_node

    if not non_null_types:
        normalized_node = dict(node)
        normalized_node["type"] = "null"
        return normalized_node

    raise ValueError(
        _ := "Unsupported type union. Only nullable unions of a single non-null "
        f"schema are supported. Node: {node}"
    )


def convert_nuextract_template_to_json_schema(
    nuextract_template: dict,
    objects_annotations: dict | None = None,
    set_all_properties_required: bool = False,
    set_type_in_description: bool = False,
) -> dict:
    """
    Convert a NuExtract template into a JSON Schema.

    This function recursively processes the input dictionary to build a
    JSON Schema. It handles:
    - Simple types (e.g., "integer", "string").
    - Custom types, which are mapped to {"type": "string", "format": "custom-type"}.
    - Lists, which are mapped to JSON Schema arrays.
    - Nested dictionaries, which are mapped to JSON Schema objects.

    :param nuextract_template: A dictionary following the custom format.
    :param objects_annotations: A flat mapping merged into every generated object
        schema. It is independent of the template structure; its keys override the
        generated object keys. (default: ``None``)
    :param set_all_properties_required: Whether to set all properties required.
    :param set_type_in_description: Whether to set type in ``description`` instead of
        ``format``. (default: ``False``)
    :return: A dictionary representing the equivalent JSON Schema.
    :raise TypeError: If the input contains unsupported types.
    """

    def _build_node(value: Any) -> dict[str, Any]:  # noqa:ANN401
        """Recursively build a schema node based on the value's type."""
        # Case 1: The value is a string (e.g., "string", "integer", "quantity")
        if isinstance(value, str):
            return _build_leaf_schema(
                value,
                set_type_in_description=set_type_in_description,
            )

        # Case 2: The value is a list (e.g., ["word"]) -> JSON Schema "array"
        if isinstance(value, list):
            if not value:
                # Handle empty list by defining an array with no item constraints
                raise ValueError(_ := "Empty list in input template")
            # Enum / Classification
            if is_object_enum(value):
                return {"enum": value}
            # Multiclassification is handled as an array of enums, returned by the
            # following recursive call, which also handles arrays of primitives.
            # Recursively call _build_node on the first element to define item schema
            item_schema = _build_node(value[0])
            return {"type": "array", "items": item_schema}

        # Case 3: The value is a dictionary -> JSON Schema "object"
        if isinstance(value, dict):
            properties = {}
            for key, sub_value in value.items():
                # Recursively call _build_node for each property in the nested object
                properties[key] = _build_node(sub_value)
            # "$schema": "https://json-schema.org/draft/2020-12/schema",
            object_ = {"type": "object", "properties": properties}
            if objects_annotations is not None:
                object_.update(objects_annotations)
            if set_all_properties_required:
                object_["required"] = list(object_["properties"].keys())
            return object_

        # Handle unsupported types
        raise TypeError(
            _ := f"Unsupported type in custom schema definition: {type(value)}"
        )

    return _build_node(nuextract_template)


def convert_json_schema_to_nuextract_template(
    schema: dict[str, Any],
    *,
    omit_unsupported_branches: bool = False,
    instance: Any = _INSTANCE_NOT_PROVIDED,  # noqa:ANN401
) -> tuple[Any, list[dict[str, Any]], list[str]]:
    """
    Convert a JSON Schema into a NuExtract template.

    The template keeps the schema's extraction shape, not all of its validation
    rules. Conversion follows these rules:

    - Primitive leaves become their JSON Schema type name. For example,
      ``{"type": "integer"}`` becomes ``"integer"``.
    - A recognized ``format`` or ``description`` turns a string leaf into the
      corresponding NuExtract semantic type. For example,
      ``{"type": "string", "format": "date-time"}`` becomes ``"date-time"``.
      Setting ``x-verbatim`` prefixes the result with ``"verbatim-"``.
    - An ``enum`` of two or more strings becomes a list of choices, such as
      ``{"enum": ["open", "closed"]}`` becoming ``["open", "closed"]``.
    - An object becomes a dictionary whose keys come from ``properties``; an array
      becomes a one-item list describing every item. Thus, an array of enums becomes
      a nested list. The fixed five-integer bounding-box schema becomes ``"bbox"``.
    - Local ``$ref`` values are resolved. Object-compatible ``allOf`` branches and
      object alternatives in ``anyOf`` or ``oneOf`` are merged.
    - Nullable forms such as ``{"type": ["string", "null"]}`` or a union of one
      schema and ``{"type": "null"}`` become the non-null template. NuExtract
      templates do not retain whether a field is required or nullable.
    - Object-valued ``patternProperties`` and ``additionalProperties`` schemas are
      flattened into the surrounding template because dynamic keys cannot be
      represented directly.

    Keywords that only constrain validation, including ``required``, numeric bounds,
    and string lengths, do not appear in the template.

    For example, nested leaves, enums, and arrays are converted as follows::

        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Customer name"},
                "created_at": {"type": "string", "format": "date-time"},
                "status": {"enum": ["open", "closed"]},
                "tags": {"type": "array", "items": {"type": "string"}},
            },
        }
        template, dropped_branches, descriptions = (
            convert_json_schema_to_nuextract_template(schema)
        )
        assert template == {
            "name": "string",
            "created_at": "date-time",
            "status": ["open", "closed"],
            "tags": ["string"],
        }
        assert dropped_branches == []
        assert descriptions == ["$.name: Customer name"]

    A nullable local reference is resolved and then has its null alternative removed::

        schema = {
            "$defs": {
                "address": {
                    "type": "object",
                    "properties": {"city": {"type": "string"}},
                }
            },
            "type": "object",
            "properties": {
                "address": {
                    "anyOf": [
                        {"$ref": "#/$defs/address"},
                        {"type": "null"},
                    ]
                }
            },
        }
        template, _, _ = convert_json_schema_to_nuextract_template(schema)
        assert template == {"address": {"city": "string"}}

    :param schema: A dictionary representing the JSON schema.
    :param omit_unsupported_branches: When ``True``, unsupported non-root schema
        branches are omitted from the output template instead of raising an error.
        If the root schema cannot produce a non-empty template, an error is still
        raised. (default: ``False``)
    :param instance: Optional JSON instance used to select the compatible alternative
        of otherwise unrepresentable unions. If values at one union path use multiple
        alternatives, that path is omitted instead of coercing values. (default: not
        provided)
    :return: A tuple containing the converted template, one ``path`` and ``error``
        dictionary per omitted branch, and descriptions prefixed by their template
        paths.
    :raises TypeError: If the input or one of its schema nodes has an invalid type.
    :raises KeyError: If a local ``$ref`` cannot be resolved.
    :raises ValueError: If the schema is malformed, unsupported, or contains a cyclic
        or non-local ``$ref``.
    """
    if omit_unsupported_branches:
        compatible_schema, dropped_branches = (
            _convert_json_schema_to_nuextract_compatible_json_schema(
                schema,
                omit_unsupported_branches=True,
                root_instance=instance,
            )
        )
    else:
        compatible_schema, dropped_branches = (
            _convert_json_schema_to_nuextract_compatible_json_schema(
                schema,
                omit_unsupported_branches=False,
            )
        )
    descriptions = get_description_json_schema_nodes(compatible_schema)
    converted = _process_json_schema_node(compatible_schema)
    if converted is _OMIT_FROM_TEMPLATE:
        raise ValueError(
            _ := "Root schema is unsupported or contains no supported branches."
        )
    return converted, dropped_branches, descriptions


def _convert_json_schema_to_nuextract_compatible_json_schema(
    schema: dict[str, Any],
    *,
    omit_unsupported_branches: bool,
    root_instance: Any = _INSTANCE_NOT_PROVIDED,  # noqa:ANN401
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """
    Sanitize a JSON Schema using strict or branch-omitting behavior.

    :param schema: The JSON Schema to sanitize.
    :param omit_unsupported_branches: Whether to drop unsupported non-root branches.
    :param root_instance: Optional instance used to select union alternatives.
    :return: The compatible schema and dropped-branch metadata.
    """
    if not isinstance(schema, dict):
        raise TypeError(_ := "Input schema must be a dictionary.")

    dropped_branches: list[dict[str, Any]] = []
    converted = _sanitize_json_schema_node(
        schema,
        root_schema=schema,
        ref_stack=set(),
        omit_unsupported_branches=omit_unsupported_branches,
        root_instance=root_instance,
        dropped_branches=dropped_branches,
        path=[],
        is_root=True,
    )
    if converted is _OMIT_FROM_TEMPLATE or not isinstance(converted, dict):
        raise ValueError(
            _ := "Root schema is unsupported or contains no supported branches."
        )
    return converted, dropped_branches


def convert_json_schema_to_nuextract_compatible_json_schema(
    schema: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """
    Convert a JSON Schema into a NuExtract-compatible JSON Schema.

    Unsupported branches are omitted while supported branches are kept as JSON
    Schema nodes. This includes dropping unsupported unions such as
    ``anyOf: [{"type": "string"}, {"type": "integer"}]`` and invalid arrays
    that omit their ``items`` schema.

    The resulting schema is consumable by
    :func:`convert_json_schema_to_nuextract_template`.

    :param schema: A dictionary representing the JSON schema.
    :return: The sanitized JSON Schema and metadata about dropped branches.
    :raises TypeError: If the input ``schema`` is not a dictionary.
    :raises ValueError: If the root schema cannot produce a supported schema.
    """
    return _convert_json_schema_to_nuextract_compatible_json_schema(
        schema,
        omit_unsupported_branches=True,
    )


def _resolve_ref(ref_path: str, root_schema: dict[str, Any]) -> dict[str, Any]:
    """
    Resolve a local ``$ref`` pointer to its definition within the root schema.

    :param ref_path: The ``$ref`` string (e.g., "#/$defs/address").
    :param root_schema: The complete root schema dictionary to search within.
    :return: The dictionary node that the ``$ref`` points to.
    :raises ValueError: If the ``$ref`` format is unsupported (not a local '#/...'
        path).
    :raises KeyError: If a part of the path does not exist in the schema.
    """
    if not ref_path.startswith("#/"):
        raise ValueError(
            _ := f"Unsupported $ref format: {ref_path}. Only local refs are supported."
        )

    path_parts = [_decode_json_pointer_part(part) for part in ref_path.split("/")[1:]]

    current_node = root_schema
    try:
        for part in path_parts:
            current_node = current_node[part]
    except KeyError as e:
        raise KeyError(_ := f"Could not resolve $ref: '{ref_path}'") from e
    if not isinstance(current_node, dict):
        raise TypeError(
            _ := f"Resolved $ref does not point to an object node: '{ref_path}'"
        )
    return current_node


def _decode_json_pointer_part(part: str) -> str:
    """Decode a JSON Pointer path segment."""
    return part.replace("~1", "/").replace("~0", "~")


def _get_instance_values_at_schema_path(
    instance: Any,  # noqa:ANN401
    path: list[str | int],
) -> list[Any]:
    """Return instance values reached by an object/array JSON Schema path."""
    values = [instance]
    path_index = 0
    while path_index < len(path):
        path_part = path[path_index]
        if path_part == "properties":
            property_name = path[path_index + 1]
            values = [
                value[property_name]
                for value in values
                if isinstance(value, dict) and property_name in value
            ]
            path_index += 2
            continue
        if path_part == "items":
            values = [
                item for value in values if isinstance(value, list) for item in value
            ]
            path_index += 1
            continue
        if path_part in {"patternProperties", "additionalProperties"}:
            values = [
                item
                for value in values
                if isinstance(value, dict)
                for item in value.values()
            ]
            path_index += 2 if path_part == "patternProperties" else 1
            continue
        if path_part in {"allOf", "anyOf", "oneOf"}:
            path_index += 2
            continue
        path_index += 1
    return values


def _json_schema_node_matches_value(
    node: Any,  # noqa:ANN401
    value: Any,  # noqa:ANN401
    root_schema: dict[str, Any],
    ref_stack: set[str] | None = None,
) -> bool:
    """Return whether ``value`` matches the structural type of a schema node."""
    if not isinstance(node, dict):
        return False
    if ref_stack is None:
        ref_stack = set()

    if "$ref" in node:
        ref_path = node["$ref"]
        if not isinstance(ref_path, str) or ref_path in ref_stack:
            return False
        referenced_node = _resolve_ref(ref_path, root_schema)
        node = {
            **referenced_node,
            **{key: item for key, item in node.items() if key != "$ref"},
        }
        ref_stack = ref_stack | {ref_path}

    if "allOf" in node:
        return all(
            _json_schema_node_matches_value(branch, value, root_schema, ref_stack)
            for branch in node["allOf"]
        )
    if "anyOf" in node:
        return any(
            _json_schema_node_matches_value(branch, value, root_schema, ref_stack)
            for branch in node["anyOf"]
        )
    if "oneOf" in node:
        return (
            sum(
                _json_schema_node_matches_value(
                    branch,
                    value,
                    root_schema,
                    ref_stack,
                )
                for branch in node["oneOf"]
            )
            == 1
        )
    if "enum" in node:
        return value in node["enum"]

    node_type = node.get("type")
    if isinstance(node_type, list):
        return any(
            _json_schema_node_matches_value(
                {**node, "type": type_name},
                value,
                root_schema,
                ref_stack,
            )
            for type_name in node_type
        )
    if node_type == "null":
        return value is None
    if node_type == "boolean":
        return type(value) is bool
    if node_type == "integer":
        return type(value) is int
    if node_type == "number":
        return type(value) in {int, float}
    if node_type == "string":
        return isinstance(value, str)
    if node_type == "array":
        return isinstance(value, list)
    if node_type == "object" or "properties" in node or "patternProperties" in node:
        return isinstance(value, dict)
    return True


def _copy_supported_annotation_keys(
    node: Mapping[str, Any],
    *,
    include_schema_meta: bool = False,
) -> dict[str, Any]:
    """Copy non-structural keys that remain useful after sanitization."""
    supported_keys = {
        "title",
        "description",
        "default",
        "examples",
        "format",
        "x-verbatim",
    }
    if include_schema_meta and "$schema" in node:
        supported_keys.add("$schema")
    return {key: value for key, value in node.items() if key in supported_keys}


def _merge_sanitized_object_schemas(
    schemas: list[dict[str, Any]],
    *,
    include_schema_meta: bool = False,
) -> dict[str, Any]:
    """Merge sanitized object schemas produced from compatible union branches."""
    merged: dict[str, Any] = {"type": "object"}
    merged_properties: dict[str, Any] = {}
    merged_pattern_properties: dict[str, Any] = {}
    merged_required: list[str] = []
    additional_properties_value: bool | dict[str, Any] | None = None

    for schema in schemas:
        if include_schema_meta and "$schema" in schema and "$schema" not in merged:
            merged["$schema"] = schema["$schema"]

        for key in ("title", "description", "default", "examples"):
            if key in schema and key not in merged:
                merged[key] = schema[key]

        properties = schema.get("properties")
        if isinstance(properties, dict):
            merged_properties.update(properties)

        pattern_properties = schema.get("patternProperties")
        if isinstance(pattern_properties, dict):
            merged_pattern_properties.update(pattern_properties)

        required = schema.get("required")
        if isinstance(required, list):
            for value in required:
                if isinstance(value, str) and value not in merged_required:
                    merged_required.append(value)

        if schema.get("additionalProperties") is True:
            additional_properties_value = True
        elif (
            isinstance(schema.get("additionalProperties"), dict)
            and additional_properties_value is not True
        ):
            additional_properties_value = schema["additionalProperties"]

    if merged_properties:
        merged["properties"] = merged_properties
    if merged_pattern_properties:
        merged["patternProperties"] = merged_pattern_properties

    kept_required = [key for key in merged_required if key in merged_properties]
    if kept_required:
        merged["required"] = kept_required

    if additional_properties_value is not None:
        merged["additionalProperties"] = additional_properties_value

    return merged


def _sanitize_json_schema_node(
    node: Any,  # noqa:ANN401
    root_schema: dict[str, Any],
    ref_stack: set[str],
    *,
    omit_unsupported_branches: bool,
    root_instance: Any = _INSTANCE_NOT_PROVIDED,  # noqa:ANN401
    dropped_branches: list[dict[str, Any]] | None = None,
    path: list[str | int] | None = None,
    is_root: bool = False,
) -> Any:  # noqa:ANN401
    """
    Recursively sanitize a JSON Schema node to the NuExtract-compatible subset.

    Unsupported non-root branches are either omitted and recorded or raised,
    according to ``omit_unsupported_branches``.

    :param node: The current JSON Schema node.
    :param root_schema: The complete schema used to resolve local references.
    :param ref_stack: References already followed in the current branch.
    :param omit_unsupported_branches: Whether to drop unsupported non-root branches.
    :param root_instance: Optional instance used to select union alternatives.
    :param dropped_branches: Collector for dropped-branch metadata.
    :param path: Path of the current node in the input schema.
    :param is_root: Whether ``node`` is the schema root.
    :return: A compatible node or the omission sentinel.
    """
    if path is None:
        path = []

    try:
        if not isinstance(node, dict):
            raise TypeError(
                _ := f"Invalid schema segment: expected object node. Node: {node}"
            )

        node = _normalize_nullable_type_shorthand(node)

        if "$ref" in node:
            ref_path = node["$ref"]
            if not isinstance(ref_path, str):
                raise ValueError(_ := f"Invalid $ref value: {ref_path}")
            if ref_path in ref_stack:
                raise ValueError(_ := f"Cyclic $ref detected: '{ref_path}'")

            referenced_node = _resolve_ref(ref_path, root_schema)
            merged_node = {
                **referenced_node,
                **{key: value for key, value in node.items() if key != "$ref"},
            }
            return _sanitize_json_schema_node(
                merged_node,
                root_schema,
                ref_stack | {ref_path},
                omit_unsupported_branches=omit_unsupported_branches,
                root_instance=root_instance,
                dropped_branches=dropped_branches,
                path=path,
                is_root=is_root,
            )

        if "allOf" in node:
            all_of = node["allOf"]
            if not isinstance(all_of, list):
                raise ValueError(
                    _ := f"Invalid schema segment: 'allOf' must be a list. Node: {node}"
                )

            branches_to_merge = list(all_of)
            sibling_object_keywords = {
                key: value
                for key, value in node.items()
                if key in {"type", "properties", "additionalProperties", "required"}
            }
            if sibling_object_keywords:
                branches_to_merge.append(sibling_object_keywords)

            merged_schemas: list[dict[str, Any]] = []
            for idx, branch in enumerate(branches_to_merge):
                sanitized_branch = _sanitize_json_schema_node(
                    branch,
                    root_schema,
                    ref_stack,
                    omit_unsupported_branches=omit_unsupported_branches,
                    root_instance=root_instance,
                    dropped_branches=dropped_branches,
                    path=[*path, "allOf", idx],
                )
                if sanitized_branch is _OMIT_FROM_TEMPLATE:
                    continue
                if not (
                    isinstance(sanitized_branch, dict)
                    and (
                        sanitized_branch.get("type") == "object"
                        or "properties" in sanitized_branch
                        or "additionalProperties" in sanitized_branch
                    )
                ):
                    if omit_unsupported_branches:
                        _record_dropped_branch(
                            dropped_branches,
                            path=[*path, "allOf", idx],
                            error=(
                                "Unsupported allOf branch. Only object-compatible "
                                f"branches are supported. Node: {branch}"
                            ),
                        )
                        continue
                    raise ValueError(
                        _ := "Unsupported allOf branch. Only object-compatible "
                        f"branches are supported. Node: {branch}"
                    )
                merged_schemas.append(sanitized_branch)

            if not merged_schemas:
                return _OMIT_FROM_TEMPLATE

            merged_schema = _merge_sanitized_object_schemas(
                merged_schemas,
                include_schema_meta=is_root,
            )
            annotations = _copy_supported_annotation_keys(
                node,
                include_schema_meta=is_root,
            )
            if merged_schema.get("type") == "object":
                annotations.pop("format", None)
                annotations.pop("x-verbatim", None)
            return {
                **merged_schema,
                **annotations,
            }

        if "enum" in node:
            enum_values = node["enum"]
            if not isinstance(enum_values, list) or not all(
                isinstance(value, str) for value in enum_values
            ):
                raise ValueError(_ := f"Unsupported enum node: {node}")
            if len(enum_values) == 1:
                error = "Unsupported enum node: single-value enums are omitted."
                if is_root:
                    raise ValueError(error)
                _record_dropped_branch(
                    dropped_branches,
                    path=path,
                    error=error,
                )
                return _OMIT_FROM_TEMPLATE

            sanitized_node = _copy_supported_annotation_keys(
                node,
                include_schema_meta=is_root,
            )
            if isinstance(node.get("type"), str):
                sanitized_node["type"] = node["type"]
            sanitized_node["enum"] = enum_values
            return sanitized_node

        if "oneOf" in node:
            one_of = node["oneOf"]
            if not isinstance(one_of, list):
                raise ValueError(
                    _ := f"Invalid schema segment: 'oneOf' must be a list. Node: {node}"
                )

            # Apply oneOf alongside its structural sibling keywords before handling
            # it with the same representational rules as anyOf.
            structural_siblings = {
                key: value
                for key, value in node.items()
                if key
                in {
                    "type",
                    "properties",
                    "patternProperties",
                    "additionalProperties",
                    "required",
                    "items",
                }
            }
            normalized_node = _copy_supported_annotation_keys(
                node,
                include_schema_meta=is_root,
            )
            normalized_node["anyOf"] = [
                (
                    {**structural_siblings, **branch}
                    if structural_siblings.get("type") == "array"
                    else {"allOf": [structural_siblings, branch]}
                    if structural_siblings
                    else branch
                )
                for branch in one_of
            ]
            return _sanitize_json_schema_node(
                normalized_node,
                root_schema,
                ref_stack,
                omit_unsupported_branches=omit_unsupported_branches,
                root_instance=root_instance,
                dropped_branches=dropped_branches,
                path=path,
                is_root=is_root,
            )

        if "anyOf" in node:
            any_of = node["anyOf"]
            if not isinstance(any_of, list):
                raise ValueError(
                    _ := f"Invalid schema segment: 'anyOf' must be a list. Node: {node}"
                )
            non_null_subschemas = [
                sub_schema
                for sub_schema in any_of
                if not (
                    isinstance(sub_schema, dict) and sub_schema.get("type") == "null"
                )
            ]
            non_null_subschema_indices = [
                idx
                for idx, sub_schema in enumerate(any_of)
                if not (
                    isinstance(sub_schema, dict) and sub_schema.get("type") == "null"
                )
            ]
            if len(non_null_subschemas) == 1 and len(non_null_subschemas) != len(
                any_of
            ):
                sanitized_inner = _sanitize_json_schema_node(
                    non_null_subschemas[0],
                    root_schema,
                    ref_stack,
                    omit_unsupported_branches=omit_unsupported_branches,
                    root_instance=root_instance,
                    dropped_branches=dropped_branches,
                    path=[*path, "anyOf"],
                )
                if sanitized_inner is _OMIT_FROM_TEMPLATE:
                    return _OMIT_FROM_TEMPLATE

                sanitized_node = _copy_supported_annotation_keys(
                    node,
                    include_schema_meta=is_root,
                )
                sanitized_node["anyOf"] = [
                    sanitized_inner,
                    {"type": "null"},
                ]
                return sanitized_node
            if not non_null_subschemas:
                sanitized_node = _copy_supported_annotation_keys(
                    node,
                    include_schema_meta=is_root,
                )
                sanitized_node["type"] = "null"
                return sanitized_node

            sanitized_sub_schemas: list[tuple[int, dict[str, Any]]] = []
            for idx, sub_schema in zip(
                non_null_subschema_indices,
                non_null_subschemas,
                strict=True,
            ):
                sanitized_sub_schema = _sanitize_json_schema_node(
                    sub_schema,
                    root_schema,
                    ref_stack,
                    omit_unsupported_branches=omit_unsupported_branches,
                    root_instance=root_instance,
                    dropped_branches=dropped_branches,
                    path=[*path, "anyOf", idx],
                )
                if sanitized_sub_schema is _OMIT_FROM_TEMPLATE:
                    continue
                sanitized_sub_schemas.append((idx, sanitized_sub_schema))

            if sanitized_sub_schemas and all(
                sub_schema.get("type") == "object"
                for _, sub_schema in sanitized_sub_schemas
            ):
                merged_schema = _merge_sanitized_object_schemas(
                    [sub_schema for _, sub_schema in sanitized_sub_schemas],
                    include_schema_meta=is_root,
                )
                return {
                    **merged_schema,
                    **_copy_supported_annotation_keys(
                        node,
                        include_schema_meta=is_root,
                    ),
                }

            if sanitized_sub_schemas and all(
                sub_schema.get("type") == "array"
                and isinstance(sub_schema.get("items"), dict)
                and sub_schema["items"].get("type") == "object"
                for _, sub_schema in sanitized_sub_schemas
            ):
                merged_items_schema = _merge_sanitized_object_schemas(
                    [sub_schema["items"] for _, sub_schema in sanitized_sub_schemas]
                )
                return {
                    "type": "array",
                    "items": merged_items_schema,
                    **_copy_supported_annotation_keys(
                        node,
                        include_schema_meta=is_root,
                    ),
                }

            if (
                omit_unsupported_branches
                and sanitized_sub_schemas
                and root_instance is not _INSTANCE_NOT_PROVIDED
            ):
                instance_values = [
                    value
                    for value in _get_instance_values_at_schema_path(
                        root_instance,
                        path,
                    )
                    if value is not None
                ]
                matching_subschema_indices = {
                    idx
                    for idx, sub_schema in zip(
                        non_null_subschema_indices,
                        non_null_subschemas,
                        strict=True,
                    )
                    if not instance_values
                    or all(
                        _json_schema_node_matches_value(
                            sub_schema,
                            value,
                            root_schema,
                        )
                        for value in instance_values
                    )
                }
                matching_sanitized_sub_schemas = [
                    (idx, sub_schema)
                    for idx, sub_schema in sanitized_sub_schemas
                    if idx in matching_subschema_indices
                ]
                if not matching_sanitized_sub_schemas:
                    _record_dropped_branch(
                        dropped_branches,
                        path=path,
                        error=(
                            "Union omitted because no single alternative matches all "
                            "instance values."
                        ),
                    )
                    return _OMIT_FROM_TEMPLATE

                selected_subschema_index, selected_sub_schema = (
                    matching_sanitized_sub_schemas[0]
                )
                for idx, _ in sanitized_sub_schemas:
                    if idx == selected_subschema_index:
                        continue
                    _record_dropped_branch(
                        dropped_branches,
                        path=[*path, "anyOf", idx],
                        error="Union alternative omitted from the NuExtract template.",
                    )
                return {
                    **selected_sub_schema,
                    **_copy_supported_annotation_keys(
                        node,
                        include_schema_meta=is_root,
                    ),
                }

            if omit_unsupported_branches:
                error = (
                    "Unsupported anyOf node. Only nullable unions of a single "
                    f"non-null schema or object unions are supported. Node: {node}"
                )
                if is_root:
                    raise ValueError(error)
                _record_dropped_branch(
                    dropped_branches,
                    path=path,
                    error=error,
                )
                return _OMIT_FROM_TEMPLATE
            raise ValueError(
                _ := "Unsupported anyOf node. Only nullable unions of a single "
                f"non-null schema or object unions are supported. Node: {node}"
            )

        if "type" in node:
            node_type = node["type"]

            if node_type == "array":
                if _is_bbox_json_schema(node):
                    sanitized_node = _copy_supported_annotation_keys(
                        node,
                        include_schema_meta=is_root,
                    )
                    sanitized_node.update(deepcopy(_BBOX_JSON_SCHEMA))
                    return sanitized_node

                if "items" not in node:
                    raise ValueError(
                        _ := f"Unsupported array node without 'items'. Node: {node}"
                    )
                sanitized_items = _sanitize_json_schema_node(
                    node["items"],
                    root_schema,
                    ref_stack,
                    omit_unsupported_branches=omit_unsupported_branches,
                    root_instance=root_instance,
                    dropped_branches=dropped_branches,
                    path=[*path, "items"],
                )
                if sanitized_items is _OMIT_FROM_TEMPLATE:
                    return _OMIT_FROM_TEMPLATE

                sanitized_node = _copy_supported_annotation_keys(
                    node,
                    include_schema_meta=is_root,
                )
                sanitized_node["type"] = "array"
                sanitized_node["items"] = sanitized_items
                return sanitized_node

            if node_type != "object":
                _decode_leaf_type(node)
                sanitized_node = _copy_supported_annotation_keys(
                    node,
                    include_schema_meta=is_root,
                )
                sanitized_node["type"] = node_type
                return sanitized_node

        if (
            node.get("type") == "object"
            or "properties" in node
            or "patternProperties" in node
            or "additionalProperties" in node
        ):
            sanitized_node = _copy_supported_annotation_keys(
                node,
                include_schema_meta=is_root,
            )
            sanitized_node["type"] = "object"

            sanitized_properties: dict[str, Any] = {}
            properties = node.get("properties")
            if isinstance(properties, dict):
                for key, value in properties.items():
                    processed_value = _sanitize_json_schema_node(
                        value,
                        root_schema,
                        ref_stack,
                        omit_unsupported_branches=omit_unsupported_branches,
                        root_instance=root_instance,
                        dropped_branches=dropped_branches,
                        path=[*path, "properties", key],
                    )
                    if processed_value is _OMIT_FROM_TEMPLATE:
                        continue
                    sanitized_properties[key] = processed_value
            if sanitized_properties:
                sanitized_node["properties"] = sanitized_properties

            # Retain dynamic object schemas so their representable fields can be
            # flattened into the NuExtract template.
            pattern_properties = node.get("patternProperties")
            if isinstance(pattern_properties, dict):
                sanitized_pattern_properties: dict[str, Any] = {}
                for key, value in pattern_properties.items():
                    processed_value = _sanitize_json_schema_node(
                        value,
                        root_schema,
                        ref_stack,
                        omit_unsupported_branches=omit_unsupported_branches,
                        root_instance=root_instance,
                        dropped_branches=dropped_branches,
                        path=[*path, "patternProperties", key],
                    )
                    if processed_value is not _OMIT_FROM_TEMPLATE:
                        sanitized_pattern_properties[key] = processed_value
                if sanitized_pattern_properties:
                    sanitized_node["patternProperties"] = sanitized_pattern_properties

            additional_properties = node.get("additionalProperties")
            if additional_properties is True:
                sanitized_node["additionalProperties"] = True
            elif additional_properties == {}:
                sanitized_node["additionalProperties"] = {}
            elif isinstance(additional_properties, dict):
                sanitized_additional_properties = _sanitize_json_schema_node(
                    additional_properties,
                    root_schema,
                    ref_stack,
                    omit_unsupported_branches=omit_unsupported_branches,
                    root_instance=root_instance,
                    dropped_branches=dropped_branches,
                    path=[*path, "additionalProperties"],
                )
                if sanitized_additional_properties is not _OMIT_FROM_TEMPLATE:
                    sanitized_node["additionalProperties"] = (
                        sanitized_additional_properties
                    )

            required = node.get("required")
            if isinstance(required, list) and sanitized_properties:
                kept_required = [
                    key
                    for key in required
                    if isinstance(key, str) and key in sanitized_properties
                ]
                if kept_required:
                    sanitized_node["required"] = kept_required

            return sanitized_node

        raise ValueError(
            _ := f"Invalid schema segment: Node does not contain '$ref', 'anyOf', "
            f"or 'type'. Node: {node}"
        )
    except (KeyError, TypeError, ValueError) as exc:
        if omit_unsupported_branches and not is_root:
            _record_dropped_branch(
                dropped_branches,
                path=path,
                error=_format_conversion_error(exc),
            )
            return _OMIT_FROM_TEMPLATE
        raise


def _process_json_schema_node(
    node: dict[str, Any],
) -> Any:  # noqa:ANN401
    """
    Convert a NuExtract-compatible JSON Schema node into a template node.

    :param node: A node produced by the JSON Schema sanitizer.
    :return: The simplified type representation of the node (str, dict, or list).
    """
    if "enum" in node:
        return _decode_leaf_type(node)

    if "anyOf" in node:
        non_null_schema = next(
            branch for branch in node["anyOf"] if branch.get("type") != "null"
        )
        return _process_json_schema_node(non_null_schema)

    node_type = node["type"]
    if node_type == "array":
        if _is_bbox_json_schema(node):
            return BBOX_TYPE_NAME
        processed_items = _process_json_schema_node(node["items"])
        if processed_items is _OMIT_FROM_TEMPLATE:
            return _OMIT_FROM_TEMPLATE
        return [processed_items]

    if node_type != "object":
        return _decode_leaf_type(node)

    processed_properties = {}
    for key, value in node.get("properties", {}).items():
        processed_value = _process_json_schema_node(value)
        if processed_value is not _OMIT_FROM_TEMPLATE:
            processed_properties[key] = processed_value

    pattern_properties = node.get("patternProperties", {})
    for value in pattern_properties.values():
        processed_value = _process_json_schema_node(value)
        if isinstance(processed_value, dict):
            processed_properties.update(processed_value)

    # A dynamic map of primitives has no fixed NuExtract keys, but remains a valid
    # open object instead of making its entire parent unsupported.
    if pattern_properties and not processed_properties:
        return {}

    additional_properties = node.get("additionalProperties")
    if additional_properties is True or additional_properties == {}:
        return processed_properties
    if isinstance(additional_properties, dict):
        processed_additional_properties = _process_json_schema_node(
            additional_properties
        )
        if isinstance(processed_additional_properties, dict):
            processed_properties.update(processed_additional_properties)

    return processed_properties or _OMIT_FROM_TEMPLATE


def _record_dropped_branch(
    dropped_branches: list[dict[str, Any]] | None,
    *,
    path: list[str | int],
    error: str,
) -> None:
    """Append dropped-branch metadata to the optional collector."""
    if dropped_branches is None:
        return
    dropped_branches.append({"path": path.copy(), "error": error})


def _format_conversion_error(exc: KeyError | TypeError | ValueError) -> str:
    """Return a stable human-readable error message for dropped branches."""
    if len(exc.args) == 1 and isinstance(exc.args[0], str):
        return exc.args[0]
    return str(exc)


def get_description_json_schema_nodes(schema: dict[str, Any]) -> list[str]:
    """
    Parse a JSON schema for its descriptions field.

    This function recursively traverses a JSON schema and returns its description
    fields with their template paths.

    :param schema: A dictionary representing the JSON schema.
    :return: Description lines prefixed with their template paths.
    :raises TypeError: If ``schema`` is not a dictionary.
    :raises ValueError: If the schema is malformed or a ``$ref`` cannot be resolved.
    """
    if not isinstance(schema, dict):
        raise TypeError(_ := "Input schema must be a dictionary.")

    schema = convert_json_schema_to_nuextract_compatible_json_schema(schema)[0]

    description_lines: list[str] = []

    def _visit(
        node: Any,  # noqa:ANN401
        *,
        path: str,
        ref_stack: set[str],
    ) -> None:
        if not isinstance(node, dict):
            return

        description = node.get("description")
        if isinstance(description, str):
            description_lines.append(f"{path}: {description}")

        if "$ref" in node:
            ref_path = node["$ref"]
            if not isinstance(ref_path, str):
                raise ValueError(_ := f"Invalid $ref value: {ref_path}")
            if ref_path in ref_stack:
                raise ValueError(_ := f"Cyclic $ref detected: '{ref_path}'")

            referenced_node = _resolve_ref(ref_path, schema)
            merged_node = {
                **referenced_node,
                **{key: value for key, value in node.items() if key != "$ref"},
            }
            _visit(merged_node, path=path, ref_stack=ref_stack | {ref_path})
            return

        if "anyOf" in node:
            any_of = node["anyOf"]
            if not isinstance(any_of, list):
                raise ValueError(
                    _ := f"Invalid schema segment: 'anyOf' must be a list. Node: {node}"
                )
            non_null_subschemas = [
                sub_schema
                for sub_schema in any_of
                if not (
                    isinstance(sub_schema, dict) and sub_schema.get("type") == "null"
                )
            ]
            if len(non_null_subschemas) == 1 and len(non_null_subschemas) != len(
                any_of
            ):
                _visit(non_null_subschemas[0], path=path, ref_stack=ref_stack)
                return
            if not non_null_subschemas:
                return
            raise ValueError(
                _
                := "Unsupported anyOf node. Only nullable unions of a single non-null "
                f"schema are supported. Node: {node}"
            )

        node_type = node.get("type")
        if node_type == "object":
            properties = node.get("properties")
            if properties is not None and not isinstance(properties, dict):
                raise ValueError(
                    _ := f"Invalid object node: 'properties' must be a dictionary. "
                    f"Node: {node}"
                )
            for key, value in (properties or {}).items():
                _visit(value, path=f"{path}.{key}", ref_stack=ref_stack)

            pattern_properties = node.get("patternProperties")
            if pattern_properties is not None and not isinstance(
                pattern_properties, dict
            ):
                raise ValueError(
                    _ := "Invalid object node: 'patternProperties' must be a "
                    f"dictionary. Node: {node}"
                )
            for value in (pattern_properties or {}).values():
                _visit(value, path=path, ref_stack=ref_stack)

            additional_properties = node.get("additionalProperties")
            if isinstance(additional_properties, dict):
                _visit(additional_properties, path=path, ref_stack=ref_stack)
            return

        if node_type == "array":
            if _is_bbox_json_schema(node):
                return
            if "items" not in node:
                raise ValueError(
                    _ := f"Unsupported array node without 'items'. Node: {node}"
                )
            _visit(node["items"], path=f"{path}[]", ref_stack=ref_stack)

    _visit(schema, path="$", ref_stack=set())
    return description_lines
