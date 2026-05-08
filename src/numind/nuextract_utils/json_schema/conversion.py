"""Conversion from NuExtract template to JSON Schema."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .constants import JSON_SCHEMA_PRIMITIVES, NUEXTRACT_TYPE_TO_JSON_SCHEMA_FORMAT

if TYPE_CHECKING:
    from collections.abc import Mapping
    from typing import Any


_TYPE_DESCRIPTION_KEYS = ("format", "description")
_OMIT_FROM_TEMPLATE = object()


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
        raise ValueError(
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


def _normalize_nullable_type_shorthand(node: Mapping[str, Any]) -> dict[str, Any]:
    """Normalize ``type: [T, "null"]`` nodes into their non-null leaf form."""
    node_type = node.get("type")
    if not isinstance(node_type, list):
        return dict(node)

    if not all(isinstance(type_name, str) for type_name in node_type):
        raise ValueError(_ := f"Invalid schema leaf: invalid list 'type'. Node: {node}")

    non_null_types = [type_name for type_name in node_type if type_name != "null"]
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
    custom_schema_dict: dict,
    objects_annotations: dict | None = None,
    set_all_properties_required: bool = False,
    set_type_in_description: bool = False,
) -> dict:
    """
    Convert a custom-formatted Python dictionary into a JSON Schema.

    This function recursively processes the input dictionary to build a
    JSON Schema. It handles:
    - Simple types (e.g., "integer", "string").
    - Custom types, which are mapped to {"type": "string", "format": "custom-type"}.
    - Lists, which are mapped to JSON Schema arrays.
    - Nested dictionaries, which are mapped to JSON Schema objects.

    :param custom_schema_dict: A dictionary following the custom format.
    :param objects_annotations: Additional annotations to add to each object.
        (default: ``None``)
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
            if len(value) > 1:
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

    return _build_node(custom_schema_dict)


def convert_json_schema_to_nuextract_template(
    schema: dict[str, Any],
    *,
    omit_unsupported_branches: bool = False,
) -> tuple[Any, list[dict[str, Any]]]:
    """
    Convert a JSON schema into a NuExtract template dictionary.

    This function recursively traverses a JSON schema and transforms it into a more
    compact representation. Objects are converted to dictionaries mapping property
    names to their types, and arrays are converted to lists containing their
    item's type.

    The function handles:
    - Simple types via the "type" key.
    - Optional types via the "anyOf" key.
    - Custom types defined in "$defs" via "$ref".
    - Nested objects and arrays.

    :param schema: A dictionary representing the JSON schema.
    :param omit_unsupported_branches: When ``True``, unsupported non-root schema
        branches are omitted from the output template instead of raising an error.
        If the root schema cannot produce a non-empty template, an error is still
        raised. (default: ``False``)
    :return: The simplified template and the list of dropped branch metadata.
    :raises TypeError: If the input ``schema`` is not a dictionary.
    :raises ValueError: If the schema is malformed or a ``$ref`` cannot be resolved.
    """
    if not isinstance(schema, dict):
        raise TypeError(_ := "Input schema must be a dictionary.")

    dropped_branches: list[dict[str, Any]] = []

    # The root of the schema is needed to resolve $ref pointers.
    converted = _process_node(
        schema,
        root_schema=schema,
        ref_stack=set(),
        omit_unsupported_branches=omit_unsupported_branches,
        dropped_branches=dropped_branches,
        path=[],
        is_root=True,
    )
    if converted is _OMIT_FROM_TEMPLATE:
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

    The resulting schema is intended to be consumable by
    :func:`convert_json_schema_to_nuextract_template` without requiring
    ``omit_unsupported_branches=True``.

    TODO rely on this method to first "clean" JSON schema and remove guardrails in
     convert_json_schema_to_nuextract_template/_process_node

    :param schema: A dictionary representing the JSON schema.
    :return: The sanitized JSON Schema and metadata about dropped branches.
    :raises TypeError: If the input ``schema`` is not a dictionary.
    :raises ValueError: If the root schema cannot produce a supported schema.
    """
    if not isinstance(schema, dict):
        raise TypeError(_ := "Input schema must be a dictionary.")

    dropped_branches: list[dict[str, Any]] = []
    converted = _sanitize_json_schema_node(
        schema,
        root_schema=schema,
        ref_stack=set(),
        dropped_branches=dropped_branches,
        path=[],
        is_root=True,
    )
    if converted is _OMIT_FROM_TEMPLATE or not isinstance(converted, dict):
        raise ValueError(
            _ := "Root schema is unsupported or contains no supported branches."
        )
    return converted, dropped_branches


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
        raise ValueError(
            _ := f"Resolved $ref does not point to an object node: '{ref_path}'"
        )
    return current_node


def _decode_json_pointer_part(part: str) -> str:
    """Decode a JSON Pointer path segment."""
    return part.replace("~1", "/").replace("~0", "~")


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
    """Merge sanitized object schemas produced from compatible ``allOf`` branches."""
    merged: dict[str, Any] = {"type": "object"}
    merged_properties: dict[str, Any] = {}
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

    kept_required = [key for key in merged_required if key in merged_properties]
    if kept_required:
        merged["required"] = kept_required

    if additional_properties_value is not None:
        merged["additionalProperties"] = additional_properties_value

    return merged


def _merge_template_object_fragments(fragments: list[dict[str, Any]]) -> dict[str, Any]:
    """Merge object-like template fragments extracted from ``allOf`` branches."""
    merged: dict[str, Any] = {}
    for fragment in fragments:
        merged.update(fragment)
    return merged


def _sanitize_json_schema_node(
    node: Any,  # noqa:ANN401
    root_schema: dict[str, Any],
    ref_stack: set[str],
    *,
    dropped_branches: list[dict[str, Any]] | None = None,
    path: list[str | int] | None = None,
    is_root: bool = False,
) -> Any:  # noqa:ANN401
    """
    Recursively sanitize a JSON Schema node to the NuExtract-compatible subset.

    Unsupported non-root branches are omitted and recorded in
    ``dropped_branches``.
    """
    if path is None:
        path = []

    try:
        if not isinstance(node, dict):
            raise ValueError(
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
                raise ValueError(
                    _ := "Unsupported enum node: single-value enums are omitted."
                )

            sanitized_node = _copy_supported_annotation_keys(
                node,
                include_schema_meta=is_root,
            )
            if isinstance(node.get("type"), str):
                sanitized_node["type"] = node["type"]
            sanitized_node["enum"] = enum_values
            return sanitized_node

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
                sanitized_inner = _sanitize_json_schema_node(
                    non_null_subschemas[0],
                    root_schema,
                    ref_stack,
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
            raise ValueError(
                _ := "Unsupported anyOf node. Only nullable unions of a single "
                f"non-null schema are supported. Node: {node}"
            )

        if "type" in node:
            node_type = node["type"]

            if node_type == "array":
                if "items" not in node:
                    raise ValueError(
                        _ := f"Unsupported array node without 'items'. Node: {node}"
                    )
                sanitized_items = _sanitize_json_schema_node(
                    node["items"],
                    root_schema,
                    ref_stack,
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
                        dropped_branches=dropped_branches,
                        path=[*path, "properties", key],
                    )
                    if processed_value is _OMIT_FROM_TEMPLATE:
                        continue
                    sanitized_properties[key] = processed_value
            if sanitized_properties:
                sanitized_node["properties"] = sanitized_properties

            additional_properties = node.get("additionalProperties")
            if additional_properties is True:
                sanitized_node["additionalProperties"] = True
            elif isinstance(additional_properties, dict):
                sanitized_additional_properties = _sanitize_json_schema_node(
                    additional_properties,
                    root_schema,
                    ref_stack,
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
    except (KeyError, ValueError) as exc:
        if not is_root:
            _record_dropped_branch(
                dropped_branches,
                path=path,
                error=_format_conversion_error(exc),
            )
            return _OMIT_FROM_TEMPLATE
        raise


def _process_node(
    node: Any,  # noqa:ANN401
    root_schema: dict[str, Any],
    ref_stack: set[str],
    *,
    omit_unsupported_branches: bool = False,
    dropped_branches: list[dict[str, Any]] | None = None,
    path: list[str | int] | None = None,
    is_root: bool = False,
) -> Any:  # noqa:ANN401
    """
    Recursively process a single schema node.

    This is the core worker function that handles the schema transformation logic
    based on the node's content (e.g., ``$ref``, ``anyOf``, ``type``).

    :param node: The current schema node (a dictionary) to process.
    :param root_schema: The complete root schema, needed to resolve ``$ref``s.
    :return: The simplified type representation of the node (str, dict, or list).
    :raises ValueError: If a schema segment is ambiguous or malformed.
    """
    if path is None:
        path = []

    try:
        if not isinstance(node, dict):
            return node

        node = _normalize_nullable_type_shorthand(node)

        # 1. Handle $ref: Highest priority. Resolve it and process the result.
        if "$ref" in node:
            ref_path = node["$ref"]
            if ref_path in ref_stack:
                raise ValueError(_ := f"Cyclic $ref detected: '{ref_path}'")

            referenced_node = _resolve_ref(ref_path, root_schema)
            merged_node = {
                **referenced_node,
                **{key: value for key, value in node.items() if key != "$ref"},
            }
            return _process_node(
                merged_node,
                root_schema,
                ref_stack | {ref_path},
                omit_unsupported_branches=omit_unsupported_branches,
                dropped_branches=dropped_branches,
                path=path,
            )

        if "enum" in node:
            enum_values = node["enum"]
            if isinstance(enum_values, list) and len(enum_values) == 1:
                _record_dropped_branch(
                    dropped_branches,
                    path=path,
                    error="Unsupported enum node: single-value enums are omitted.",
                )
                return _OMIT_FROM_TEMPLATE
            return _decode_leaf_type(node)

        # 2. Handle 'allOf' for object composition.
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
                if key in {"type", "properties", "additionalProperties"}
            }
            if sibling_object_keywords:
                branches_to_merge.append(sibling_object_keywords)

            processed_fragments: list[dict[str, Any]] = []
            for idx, branch in enumerate(branches_to_merge):
                processed_branch = _process_node(
                    branch,
                    root_schema,
                    ref_stack,
                    omit_unsupported_branches=omit_unsupported_branches,
                    dropped_branches=dropped_branches,
                    path=[*path, "allOf", idx],
                )
                if processed_branch is _OMIT_FROM_TEMPLATE:
                    continue
                if not isinstance(processed_branch, dict):
                    raise ValueError(
                        _ := "Unsupported allOf branch. Only object-compatible "
                        f"branches are supported. Node: {branch}"
                    )
                processed_fragments.append(processed_branch)

            if not processed_fragments:
                return _OMIT_FROM_TEMPLATE

            return _merge_template_object_fragments(processed_fragments)

        # 2. Handle 'anyOf' for optional types.
        if "anyOf" in node and isinstance(node["anyOf"], list):
            non_null_subschemas = [
                sub_schema
                for sub_schema in node["anyOf"]
                if not (
                    isinstance(sub_schema, dict) and sub_schema.get("type") == "null"
                )
            ]
            if len(non_null_subschemas) == 1 and len(non_null_subschemas) != len(
                node["anyOf"]
            ):
                return _process_node(
                    non_null_subschemas[0],
                    root_schema,
                    ref_stack,
                    omit_unsupported_branches=omit_unsupported_branches,
                    dropped_branches=dropped_branches,
                    path=[*path, "anyOf"],
                )
            if not non_null_subschemas:
                return "null"
            raise ValueError(
                _ := "Unsupported anyOf node. Only nullable unions of a single "
                f"non-null schema are supported. Node: {node}"
            )

        # 3. Handle explicit 'type' definitions.
        if "type" in node:
            node_type = node["type"]

            if node_type == "array":
                if "items" not in node:
                    raise ValueError(
                        _ := f"Unsupported array node without 'items'. Node: {node}"
                    )
                item_type = _process_node(
                    node["items"],
                    root_schema,
                    ref_stack,
                    omit_unsupported_branches=omit_unsupported_branches,
                    dropped_branches=dropped_branches,
                    path=[*path, "items"],
                )
                if item_type is _OMIT_FROM_TEMPLATE:
                    return _OMIT_FROM_TEMPLATE
                return [item_type]

            # Handle simple, primitive types
            if node_type != "object":
                return _decode_leaf_type(node)

        # 4. Handle object schemas, including nodes that omit an explicit
        # "type": "object".
        if (
            node.get("type") == "object"
            or "properties" in node
            or "additionalProperties" in node
        ):
            processed_properties = {}

            properties = node.get("properties")
            # ``properties`` is a direct field mapping, while
            # ``additionalProperties`` is a schema node that may resolve through
            # ``$ref`` and only merges if it converts to an object template.
            if isinstance(properties, dict):
                for key, value in properties.items():
                    processed_value = _process_node(
                        value,
                        root_schema,
                        ref_stack,
                        omit_unsupported_branches=omit_unsupported_branches,
                        dropped_branches=dropped_branches,
                        path=[*path, "properties", key],
                    )
                    if processed_value is _OMIT_FROM_TEMPLATE:
                        continue
                    processed_properties[key] = processed_value

            if (additional_properties := node.get("additionalProperties")) is True:
                return processed_properties or {}

            if isinstance(additional_properties, dict):
                if not additional_properties:
                    return processed_properties or {}

                processed_additional_properties = _process_node(
                    additional_properties,
                    root_schema,
                    ref_stack,
                    omit_unsupported_branches=omit_unsupported_branches,
                    dropped_branches=dropped_branches,
                    path=[*path, "additionalProperties"],
                )
                if (
                    processed_additional_properties is not _OMIT_FROM_TEMPLATE
                    and isinstance(processed_additional_properties, dict)
                ):
                    processed_properties.update(processed_additional_properties)
                    return processed_properties

            return processed_properties or _OMIT_FROM_TEMPLATE

        raise ValueError(
            _ := f"Invalid schema segment: Node does not contain '$ref', 'anyOf', "
            f"or 'type'. Node: {node}"
        )
    except (KeyError, ValueError) as exc:
        if omit_unsupported_branches and not is_root:
            _record_dropped_branch(
                dropped_branches,
                path=path,
                error=_format_conversion_error(exc),
            )
            return _OMIT_FROM_TEMPLATE
        raise


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


def _format_conversion_error(exc: KeyError | ValueError) -> str:
    """Return a stable human-readable error message for dropped branches."""
    if len(exc.args) == 1 and isinstance(exc.args[0], str):
        return exc.args[0]
    return str(exc)


def get_description_json_schema_nodes(schema: dict[str, Any]) -> str:
    """
    Parse a JSON schema for its descriptions field.

    This function recursively traverses a JSON schema and returns a string summarizing
    the description fields of its nodes.

    :param schema: A dictionary representing the JSON schema.
    :return: a string
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
            if properties is None:
                return
            if not isinstance(properties, dict):
                raise ValueError(
                    _ := f"Invalid object node: 'properties' must be a dictionary. "
                    f"Node: {node}"
                )
            for key, value in properties.items():
                _visit(value, path=f"{path}.{key}", ref_stack=ref_stack)
            return

        if node_type == "array":
            if "items" not in node:
                raise ValueError(
                    _ := f"Unsupported array node without 'items'. Node: {node}"
                )
            _visit(node["items"], path=f"{path}[]", ref_stack=ref_stack)

    _visit(schema, path="$", ref_stack=set())
    return "\n".join(description_lines)
