"""Conversions between NuExtract templates and JSON Schema."""

from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING

from jsonschema import SchemaError
from jsonschema.validators import validator_for

from numind.nuextract_utils.data_validation import (
    correct_output_json_and_input_template,
    detect_errors_in_output_json,
)
from numind.nuextract_utils.data_validation.utils import is_object_enum

from .constants import (
    JSON_SCHEMA_PRIMITIVES,
    NUEXTRACT_TYPE_TO_JSON_SCHEMA_FORMAT,
)

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping
    from typing import Any

    from jsonschema.exceptions import ValidationError

    from numind.nuextract_utils.data_validation.models import ErrorJson


_TYPE_DESCRIPTION_KEYS = ("format", "description")
_OMIT_FROM_TEMPLATE = object()
_INSTANCE_NOT_PROVIDED = object()
_COMPOSITION_DESCRIPTIONS_KEY = "x-nuextract-composition-descriptions"


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
        raise TypeError(
            _ := f"Invalid schema leaf: missing string 'type'. Node: {node}"
        )

    decoded_type = node_type
    if node_type == "string":
        for key in _TYPE_DESCRIPTION_KEYS:
            schema_value = node.get(key)
            if (
                isinstance(schema_value, str)
                and schema_value in JSON_SCHEMA_FORMAT_TO_NUEXTRACT_TYPE
            ):
                decoded_type = JSON_SCHEMA_FORMAT_TO_NUEXTRACT_TYPE[schema_value]
                break

    if node.get("x-verbatim") and decoded_type != "string":
        raise ValueError(
            _ := "The x-verbatim annotation is only supported for string leaves. "
            f"Node: {node}"
        )
    if node.get("x-verbatim"):
        return f"verbatim-{decoded_type}"

    return decoded_type


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
        raise ValueError(_ := f"Unsupported null-only schema node: {node}")

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


def adapt_json_to_nuextract_template(
    template: dict | list | str,
    json_instance: Any,  # noqa: ANN401
) -> tuple[Any, list[ErrorJson]]:
    """
    Adapt an output to a valid NuExtract template without fuzzy replacements.

    The correction only applies deterministic structural/type normalization and
    array deduplication. It does not rename keys or guess enum values.

    :param template: NuExtract template the output must follow.
    :param json_instance: Structured output to adapt.
    :return: The adapted output and any validation errors that remain.
    """
    # Wrapping gives root leaves and enums the same correction behavior as nested ones,
    # without treating their string values as serialized JSON documents.
    wrapped_template = {"value": template}
    _, wrapped_output, _, _ = correct_output_json_and_input_template(
        wrapped_template,
        {"value": deepcopy(json_instance)},
        None,
        indel_distance_output_enum=None,
        indel_distance_node_name=None,
        deduplicate_arrays_entries=True,
    )
    adapted_output = wrapped_output["value"]
    return adapted_output, detect_errors_in_output_json(template, adapted_output, None)


def convert_json_schema_to_nuextract_template(
    schema: dict[str, Any],
    *,
    omit_unsupported_branches: bool = False,
    instance: Any = _INSTANCE_NOT_PROVIDED,  # noqa:ANN401
) -> dict[str, Any]:
    """
    Convert a JSON Schema into a NuExtract template.

    The template keeps the schema's extraction shape, not all of its validation
    rules. When an ``instance`` is provided, it guides union selection and the method
    determines whether that instance already follows both representations. Otherwise,
    it applies deterministic NuExtract output corrections and only returns the adapted
    value when it remains valid against the original JSON Schema.

    Conversion follows these rules:

    - Primitive leaves become their JSON Schema type name. For example,
      ``{"type": "integer"}`` becomes ``"integer"``.
    - A recognized ``format`` or ``description`` turns a string leaf into the
      corresponding NuExtract semantic type. For example,
      ``{"type": "string", "format": "date-time"}`` becomes ``"date-time"``.
      Setting ``x-verbatim`` prefixes the result with ``"verbatim-"``.
    - An ``enum`` of two or more strings becomes a list of choices, such as
      ``{"enum": ["open", "closed"]}`` becoming ``["open", "closed"]``.
      A ``null`` choice is discarded because NuExtract templates do not retain
      nullability. If one string remains, the enum becomes a string leaf because a
      one-item template list represents an array rather than an enum.
    - An object becomes a dictionary whose keys come from ``properties``; an array
      becomes a one-item list describing every item. Thus, an array of enums becomes
      a nested list.
    - Local ``$ref`` values are resolved, including array indices in JSON Pointers,
      and sibling keywords are applied alongside the reference.
    - Compatible ``allOf`` branches are merged. Multi-branch ``anyOf`` and ``oneOf``
      nodes require an instance that selects exactly one alternative.
    - Nullable forms such as ``{"type": ["string", "null"]}`` or a union of one
      schema and ``{"type": "null"}`` become the non-null template. NuExtract
      templates do not retain whether a field is required or nullable.
    - Homogeneous ``prefixItems`` become a regular array item template. Heterogeneous
      tuples and dynamic-key schemas cannot be represented and are rejected or
      omitted according to ``omit_unsupported_branches``.

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
        conversion = convert_json_schema_to_nuextract_template(schema)
        assert conversion["template"] == {
            "name": "string",
            "created_at": "date-time",
            "status": ["open", "closed"],
            "tags": ["string"],
        }
        assert conversion["schema_status"] == "fully_converted"
        assert conversion["instance_status"] == "not_provided"
        assert conversion["adapted_instance"] is None
        assert conversion["incompatibilities"] == []
        assert conversion["descriptions"] == ["$.name: Customer name"]

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
        conversion = convert_json_schema_to_nuextract_template(schema)
        assert conversion["template"] == {"address": {"city": "string"}}

    :param schema: A dictionary representing the JSON schema.
    :param omit_unsupported_branches: When ``True``, unsupported non-root schema
        branches are omitted from the output template instead of raising an error.
        If the root schema cannot produce a template, ``template`` is ``None`` and
        ``schema_status`` is ``not_convertible``. (default: ``False``)
    :param instance: Optional JSON instance used to select the compatible alternative
        of otherwise unrepresentable unions. If values at one union path use multiple
        alternatives, that path is omitted instead of coercing values. (default: not
        provided) When no instance value exists at a union path, the converter cannot
        assume which alternative a future instance will use, so the ambiguous path is
        rejected or omitted. The input object is never modified.
    :return: A dictionary containing ``template``, ``adapted_instance``,
        ``schema_status``, ``instance_status``, ``incompatibilities``, and
        ``descriptions``. ``schema_status`` is ``fully_converted``,
        ``partially_converted``, or ``not_convertible``. ``instance_status`` is one of:

        - ``not_provided``: no instance was supplied;
        - ``valid_for_both``: the original instance follows both the JSON Schema and
          template;
        - ``adapted_valid_for_both``: deterministic correction produced the returned
          ``adapted_instance``, which follows both representations;
        - ``not_adaptable``: no corrected instance could satisfy both representations;
        - ``invalid_for_original_schema``: the supplied instance did not satisfy the
          source JSON Schema, so it was not adapted.

        Every incompatibility is a dictionary with ``kind``, ``schema_path``,
        ``instance_path``, and ``error``. Schema conversion failures use
        ``schema_node_not_convertible``. Instance failures use
        ``instance_node_not_adaptable`` or ``original_instance_invalid``. A path is
        ``None`` when that representation has no meaningful corresponding location;
        integer instance indices are collapsed to ``"*"`` so repeated array failures
        identify one logical location.
    :raises TypeError: If the input or one of its schema nodes has an invalid type.
    :raises KeyError: If a local ``$ref`` cannot be resolved.
    :raises ValueError: If the schema is malformed, unsupported, or contains a cyclic
        or non-local ``$ref``.
    """
    if not isinstance(schema, dict):
        raise TypeError(_ := "Input schema must be a dictionary.")

    # Validate before catching conversion errors so malformed schemas still fail fast.
    try:
        validator_for(schema).check_schema(schema)
    except SchemaError as exc:
        raise ValueError(_ := f"Invalid JSON Schema: {exc.message}") from exc

    original_schema_validator = validator_for(schema)(schema)
    dropped_branches: list[dict[str, Any]] = []
    template: Any = None
    descriptions: list[str] = []
    try:
        compatible_schema, dropped_branches = (
            _convert_json_schema_to_nuextract_compatible_json_schema(
                schema,
                omit_unsupported_branches=omit_unsupported_branches,
                root_instance=instance,
            )
        )
        descriptions = get_description_json_schema_nodes(compatible_schema)
        template = _process_json_schema_node(compatible_schema)
        if template is _OMIT_FROM_TEMPLATE:
            raise ValueError(
                _ := "Root schema is unsupported or contains no supported branches."
            )
    except (KeyError, TypeError, ValueError) as exc:
        if not omit_unsupported_branches:
            raise
        dropped_branches.append({"path": [], "error": _format_conversion_error(exc)})
        template = None
        descriptions = []

    incompatibilities = [
        {
            "kind": "schema_node_not_convertible",
            "schema_path": dropped_branch["path"],
            "instance_path": None,
            "error": dropped_branch["error"],
        }
        for dropped_branch in dropped_branches
    ]
    schema_status = (
        "not_convertible"
        if template is None
        else "partially_converted"
        if incompatibilities
        else "fully_converted"
    )

    adapted_instance = None
    if instance is _INSTANCE_NOT_PROVIDED:
        instance_status = "not_provided"
    else:
        original_instance_errors = list(original_schema_validator.iter_errors(instance))
        if original_instance_errors:
            instance_status = "invalid_for_original_schema"
            incompatibilities.extend(
                _validation_errors_to_incompatibilities(
                    original_instance_errors,
                    kind="original_instance_invalid",
                )
            )
        elif template is None:
            instance_status = "not_adaptable"
            incompatibilities.append(
                {
                    "kind": "instance_node_not_adaptable",
                    "schema_path": [],
                    "instance_path": [],
                    "error": "No NuExtract template was produced.",
                }
            )
        elif not detect_errors_in_output_json(template, instance, None):
            instance_status = "valid_for_both"
            adapted_instance = deepcopy(instance)
        else:
            candidate_instance, remaining_template_errors = (
                adapt_json_to_nuextract_template(template, instance)
            )
            if remaining_template_errors:
                instance_status = "not_adaptable"
                incompatibilities.extend(
                    {
                        "kind": "instance_node_not_adaptable",
                        "schema_path": None,
                        "instance_path": error.path,
                        "error": error.error_message,
                    }
                    for error in remaining_template_errors
                )
            else:
                adapted_original_schema_errors = list(
                    original_schema_validator.iter_errors(candidate_instance)
                )
                if adapted_original_schema_errors:
                    instance_status = "not_adaptable"
                    incompatibilities.extend(
                        _validation_errors_to_incompatibilities(
                            adapted_original_schema_errors,
                            kind="instance_node_not_adaptable",
                        )
                    )
                else:
                    instance_status = "adapted_valid_for_both"
                    adapted_instance = candidate_instance

    return {
        "template": template,
        "adapted_instance": adapted_instance,
        "schema_status": schema_status,
        "instance_status": instance_status,
        "incompatibilities": incompatibilities,
        "descriptions": descriptions,
    }


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

    # Reject malformed schemas before partial conversion can make them look valid.
    try:
        validator_for(schema).check_schema(schema)
    except SchemaError as exc:
        raise ValueError(_ := f"Invalid JSON Schema: {exc.message}") from exc

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
    *,
    instance: Any = _INSTANCE_NOT_PROVIDED,  # noqa:ANN401
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """
    Convert a JSON Schema into a NuExtract-compatible JSON Schema.

    Unsupported branches are omitted while supported branches are kept as JSON
    Schema nodes. This includes dropping ambiguous unions, heterogeneous tuples,
    dynamic-key schemas, and arrays that omit a representable item schema. Malformed
    input schemas are rejected before branches are sanitized.

    The resulting schema is consumable by
    :func:`convert_json_schema_to_nuextract_template`.

    :param schema: A dictionary representing the JSON schema.
    :param instance: Optional JSON instance used to select a single compatible union
        alternative. (default: not provided)
    :return: The sanitized JSON Schema and metadata about dropped branches.
    :raises TypeError: If the input ``schema`` is not a dictionary.
    :raises ValueError: If the root schema cannot produce a supported schema.
    """
    return _convert_json_schema_to_nuextract_compatible_json_schema(
        schema,
        omit_unsupported_branches=True,
        root_instance=instance,
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

    current_node: Any = root_schema
    for part in path_parts:
        if isinstance(current_node, dict) and part in current_node:
            current_node = current_node[part]
            continue
        if (
            isinstance(current_node, list)
            and part.isdigit()
            and int(part) < len(current_node)
        ):
            current_node = current_node[int(part)]
            continue
        raise KeyError(_ := f"Could not resolve $ref: '{ref_path}'")
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
) -> bool:
    """Return whether ``value`` fully validates against a schema node."""
    if not isinstance(node, dict):
        return False

    root_validator = validator_for(root_schema)(root_schema)
    return root_validator.evolve(schema=node).is_valid(value)


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
        _COMPOSITION_DESCRIPTIONS_KEY,
    }
    if include_schema_meta and "$schema" in node:
        supported_keys.add("$schema")
    return {key: value for key, value in node.items() if key in supported_keys}


def _merge_sanitized_schema_nodes(
    schemas: list[dict[str, Any]],
    *,
    include_schema_meta: bool = False,
) -> dict[str, Any]:
    """Merge schema nodes only when they produce one unambiguous template shape."""
    if not schemas:
        error = "Cannot merge an empty list of schema nodes."
        raise ValueError(error)

    if all(schema.get("type") == "object" for schema in schemas):
        merged = _merge_sanitized_object_schemas(
            schemas,
            include_schema_meta=include_schema_meta,
        )
    elif all(
        schema.get("type") == "array" and isinstance(schema.get("items"), dict)
        for schema in schemas
    ):
        merged = {
            "type": "array",
            "items": _merge_sanitized_schema_nodes(
                [schema["items"] for schema in schemas]
            ),
        }
        if include_schema_meta and "$schema" in schemas[0]:
            merged["$schema"] = schemas[0]["$schema"]
    else:
        template_nodes = [_process_json_schema_node(schema) for schema in schemas]
        if any(template_node != template_nodes[0] for template_node in template_nodes):
            raise ValueError(
                _ := "Composition contains incompatible schemas that cannot share "
                f"one NuExtract template node: {schemas}"
            )
        merged = deepcopy(schemas[0])

    composition_descriptions: list[str] = []
    for schema in schemas:
        description = schema.get("description")
        if isinstance(description, str) and description not in composition_descriptions:
            composition_descriptions.append(description)
        for branch_description in schema.get(_COMPOSITION_DESCRIPTIONS_KEY, []):
            if (
                isinstance(branch_description, str)
                and branch_description not in composition_descriptions
            ):
                composition_descriptions.append(branch_description)

    merged.pop("description", None)
    merged.pop(_COMPOSITION_DESCRIPTIONS_KEY, None)
    if composition_descriptions:
        merged[_COMPOSITION_DESCRIPTIONS_KEY] = composition_descriptions
    return merged


def _merge_sanitized_object_schemas(
    schemas: list[dict[str, Any]],
    *,
    include_schema_meta: bool = False,
) -> dict[str, Any]:
    """Merge object fields while rejecting incompatible property collisions."""
    merged: dict[str, Any] = {"type": "object"}
    merged_properties: dict[str, Any] = {}
    merged_required: list[str] = []

    for schema in schemas:
        if include_schema_meta and "$schema" in schema and "$schema" not in merged:
            merged["$schema"] = schema["$schema"]

        for key in ("title", "default", "examples"):
            if key in schema and key not in merged:
                merged[key] = schema[key]

        properties = schema.get("properties")
        if isinstance(properties, dict):
            for property_name, property_schema in properties.items():
                if property_name in merged_properties:
                    merged_properties[property_name] = _merge_sanitized_schema_nodes(
                        [merged_properties[property_name], property_schema]
                    )
                else:
                    merged_properties[property_name] = property_schema

        required = schema.get("required")
        if isinstance(required, list):
            for value in required:
                if isinstance(value, str) and value not in merged_required:
                    merged_required.append(value)

    if merged_properties:
        merged["properties"] = merged_properties

    kept_required = [key for key in merged_required if key in merged_properties]
    if kept_required:
        merged["required"] = kept_required

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
            sanitized_referenced_node = _sanitize_json_schema_node(
                referenced_node,
                root_schema,
                ref_stack | {ref_path},
                omit_unsupported_branches=omit_unsupported_branches,
                root_instance=root_instance,
                dropped_branches=dropped_branches,
                path=path,
                is_root=is_root,
            )
            if sanitized_referenced_node is _OMIT_FROM_TEMPLATE:
                return _OMIT_FROM_TEMPLATE

            structural_sibling_keys = {
                "type",
                "properties",
                "patternProperties",
                "additionalProperties",
                "required",
                "items",
                "prefixItems",
                "enum",
                "allOf",
                "anyOf",
                "oneOf",
            }
            structural_siblings = {
                key: value
                for key, value in node.items()
                if key in structural_sibling_keys
            }
            schemas_to_merge = [sanitized_referenced_node]
            if structural_siblings:
                if "type" not in structural_siblings:
                    structural_siblings["type"] = sanitized_referenced_node.get("type")
                sanitized_siblings = _sanitize_json_schema_node(
                    structural_siblings,
                    root_schema,
                    ref_stack | {ref_path},
                    omit_unsupported_branches=omit_unsupported_branches,
                    root_instance=root_instance,
                    dropped_branches=dropped_branches,
                    path=path,
                    is_root=is_root,
                )
                if sanitized_siblings is _OMIT_FROM_TEMPLATE:
                    return _OMIT_FROM_TEMPLATE
                schemas_to_merge.append(sanitized_siblings)

            merged_schema = _merge_sanitized_schema_nodes(
                schemas_to_merge,
                include_schema_meta=is_root,
            )
            return {
                **merged_schema,
                **_copy_supported_annotation_keys(
                    node,
                    include_schema_meta=is_root,
                ),
            }

        if "allOf" in node:
            all_of = node["allOf"]
            if not isinstance(all_of, list):
                raise ValueError(
                    _ := f"Invalid schema segment: 'allOf' must be a list. Node: {node}"
                )

            branches_to_merge = list(all_of)
            sibling_structural_keywords = {
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
                    "prefixItems",
                    "enum",
                }
            }
            if sibling_structural_keywords:
                branches_to_merge.append(sibling_structural_keywords)

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
                merged_schemas.append(sanitized_branch)

            if not merged_schemas:
                return _OMIT_FROM_TEMPLATE

            merged_schema = _merge_sanitized_schema_nodes(
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
                value is None or isinstance(value, str) for value in enum_values
            ):
                raise ValueError(_ := f"Unsupported enum node: {node}")
            non_null_enum_values = [value for value in enum_values if value is not None]
            if len(non_null_enum_values) == 1 and len(enum_values) > 1:
                sanitized_node = _copy_supported_annotation_keys(
                    node,
                    include_schema_meta=is_root,
                )
                sanitized_node["type"] = "string"
                return sanitized_node
            if len(non_null_enum_values) == 1:
                error = "Unsupported enum node: single-value enums are omitted."
                if is_root:
                    raise ValueError(error)
                _record_dropped_branch(
                    dropped_branches,
                    path=path,
                    error=error,
                )
                return _OMIT_FROM_TEMPLATE
            if not non_null_enum_values:
                raise ValueError(_ := f"Unsupported enum node: {node}")

            sanitized_node = _copy_supported_annotation_keys(
                node,
                include_schema_meta=is_root,
            )
            if isinstance(node.get("type"), str):
                sanitized_node["type"] = node["type"]
            sanitized_node["enum"] = non_null_enum_values
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
                    "prefixItems",
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
                    "prefixItems",
                }
            }
            non_null_subschemas = [
                (
                    {**structural_siblings, **sub_schema}
                    if structural_siblings.get("type") == "array"
                    and isinstance(sub_schema, dict)
                    else {"allOf": [structural_siblings, sub_schema]}
                    if structural_siblings
                    else sub_schema
                )
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
                raise ValueError(_ := f"Unsupported null-only union node: {node}")

            if root_instance is not _INSTANCE_NOT_PROVIDED:
                instance_values = [
                    value
                    for value in _get_instance_values_at_schema_path(
                        root_instance,
                        path,
                    )
                    if value is not None
                ]
                if instance_values:
                    matching_subschema_indices = {
                        idx
                        for idx, sub_schema in zip(
                            non_null_subschema_indices,
                            non_null_subschemas,
                        )
                        if all(
                            _json_schema_node_matches_value(
                                sub_schema,
                                value,
                                root_schema,
                            )
                            for value in instance_values
                        )
                    }
                    if len(matching_subschema_indices) != 1:
                        raise ValueError(
                            _ := "Union is ambiguous because the instance does not "
                            "select exactly one alternative."
                        )
                    selected_subschema_index = matching_subschema_indices.pop()
                    selected_subschema = non_null_subschemas[
                        non_null_subschema_indices.index(selected_subschema_index)
                    ]
                    selected_sub_schema = _sanitize_json_schema_node(
                        selected_subschema,
                        root_schema,
                        ref_stack,
                        omit_unsupported_branches=omit_unsupported_branches,
                        root_instance=root_instance,
                        dropped_branches=dropped_branches,
                        path=[*path, "anyOf", selected_subschema_index],
                    )
                    if selected_sub_schema is _OMIT_FROM_TEMPLATE:
                        return _OMIT_FROM_TEMPLATE
                    _record_dropped_branch(
                        dropped_branches,
                        path=path,
                        error=(
                            "Union requires instance-specific branch selection and "
                            "cannot be represented completely by one NuExtract "
                            "template."
                        ),
                    )
                    selected_sub_schema = _merge_sanitized_schema_nodes(
                        [selected_sub_schema],
                        include_schema_meta=is_root,
                    )
                    return {
                        **selected_sub_schema,
                        **_copy_supported_annotation_keys(
                            node,
                            include_schema_meta=is_root,
                        ),
                    }

            raise ValueError(
                _ := "Union is ambiguous because no instance value selects exactly "
                "one alternative."
            )

        if "type" in node:
            node_type = node["type"]

            if node_type == "null":
                raise ValueError(_ := f"Unsupported null-only schema node: {node}")

            if node_type == "array":
                prefix_items = node.get("prefixItems")
                if prefix_items is not None:
                    if not isinstance(prefix_items, list):
                        raise ValueError(
                            _ := "Invalid array node: 'prefixItems' must be a list. "
                            f"Node: {node}"
                        )

                    max_items = node.get("maxItems")
                    num_reachable_prefix_items = (
                        min(len(prefix_items), max_items)
                        if isinstance(max_items, int)
                        else len(prefix_items)
                    )
                    sanitized_item_schemas: list[dict[str, Any]] = []
                    for idx, prefix_item in enumerate(
                        prefix_items[:num_reachable_prefix_items]
                    ):
                        sanitized_prefix_item = _sanitize_json_schema_node(
                            prefix_item,
                            root_schema,
                            ref_stack,
                            omit_unsupported_branches=omit_unsupported_branches,
                            root_instance=root_instance,
                            dropped_branches=dropped_branches,
                            path=[*path, "prefixItems", idx],
                        )
                        if sanitized_prefix_item is _OMIT_FROM_TEMPLATE:
                            return _OMIT_FROM_TEMPLATE
                        sanitized_item_schemas.append(sanitized_prefix_item)

                    remaining_items = node.get("items", True)
                    trailing_items_are_reachable = not isinstance(
                        max_items, int
                    ) or max_items > len(prefix_items)
                    if (
                        isinstance(remaining_items, dict)
                        and trailing_items_are_reachable
                    ):
                        sanitized_remaining_items = _sanitize_json_schema_node(
                            remaining_items,
                            root_schema,
                            ref_stack,
                            omit_unsupported_branches=omit_unsupported_branches,
                            root_instance=root_instance,
                            dropped_branches=dropped_branches,
                            path=[*path, "items"],
                        )
                        if sanitized_remaining_items is _OMIT_FROM_TEMPLATE:
                            return _OMIT_FROM_TEMPLATE
                        sanitized_item_schemas.append(sanitized_remaining_items)
                    elif remaining_items is not False and trailing_items_are_reachable:
                        raise ValueError(
                            _ := "Unsupported tuple with unconstrained trailing "
                            f"items. Node: {node}"
                        )

                    if not sanitized_item_schemas:
                        raise ValueError(_ := f"Unsupported empty tuple node: {node}")

                    sanitized_node = _copy_supported_annotation_keys(
                        node,
                        include_schema_meta=is_root,
                    )
                    sanitized_node["type"] = "array"
                    sanitized_node["items"] = _merge_sanitized_schema_nodes(
                        sanitized_item_schemas
                    )
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

            pattern_properties = node.get("patternProperties")
            if isinstance(pattern_properties, dict):
                for pattern in pattern_properties:
                    error = (
                        "Dynamic object keys cannot be represented by a NuExtract "
                        "template."
                    )
                    if not omit_unsupported_branches:
                        raise ValueError(error)
                    _record_dropped_branch(
                        dropped_branches,
                        path=[*path, "patternProperties", pattern],
                        error=error,
                    )

            additional_properties = node.get("additionalProperties")
            if isinstance(additional_properties, dict):
                error = (
                    "Dynamic object keys cannot be represented by a NuExtract template."
                )
                if not omit_unsupported_branches:
                    raise ValueError(error)
                _record_dropped_branch(
                    dropped_branches,
                    path=[*path, "additionalProperties"],
                    error=error,
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


def _validation_errors_to_incompatibilities(
    validation_errors: Iterable[ValidationError],
    *,
    kind: str,
) -> list[dict[str, Any]]:
    """Convert JSON Schema errors into deduplicated logical incompatibilities."""
    incompatibilities: list[dict[str, Any]] = []
    recorded_locations: set[tuple[tuple[str | int, ...], tuple[str, ...]]] = set()
    for validation_error in validation_errors:
        schema_path = list(validation_error.absolute_schema_path)
        if schema_path and schema_path[-1] == validation_error.validator:
            schema_path.pop()
        instance_path = [
            "*" if isinstance(path_part, int) else path_part
            for path_part in validation_error.absolute_path
        ]
        location = (tuple(schema_path), tuple(instance_path))
        if location in recorded_locations:
            continue
        recorded_locations.add(location)
        incompatibilities.append(
            {
                "kind": kind,
                "schema_path": schema_path,
                "instance_path": instance_path,
                "error": validation_error.message,
            }
        )
    return incompatibilities


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
        descriptions_at_path: list[str] = []
        if isinstance(description, str):
            descriptions_at_path.append(description)
        for composition_description in node.get(
            _COMPOSITION_DESCRIPTIONS_KEY,
            [],
        ):
            if (
                isinstance(composition_description, str)
                and composition_description not in descriptions_at_path
            ):
                descriptions_at_path.append(composition_description)
        description_lines.extend(
            f"{path}: {description_at_path}"
            for description_at_path in descriptions_at_path
        )

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
            if "items" not in node:
                raise ValueError(
                    _ := f"Unsupported array node without 'items'. Node: {node}"
                )
            _visit(node["items"], path=f"{path}[]", ref_stack=ref_stack)

    _visit(schema, path="$", ref_stack=set())
    return description_lines
