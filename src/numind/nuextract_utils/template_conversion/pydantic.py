"""Manipulation of input/output schema."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, create_model

from .utils import is_object_enum, is_object_multi_enum

from .json_schema import convert_json_schema_to_nuextract_template


def convert_nuextract_template_to_pydantic_model(
    template: dict[str, Any], class_name: str = "GeneratedModel"
) -> type[BaseModel]:
    """Convert JSON template to Pydantic model with recursive nested object support."""
    type_mapping = {
        "string": str,
        "verbatim-string": str,
        "integer": int,
        "float": float,
        "boolean": bool,
        "date-time": str,
    }

    description_mapping = {
        "verbatim-string": "Verbatim string as it appears in the document",
        "date-time": "Date-time in ISO 8601 format (e.g., '2023-12-25T10:30:00Z')",
    }

    # Store created nested models to avoid duplicates
    nested_models = {}

    def create_nested_model(
        nested_template: dict[str, Any], nested_name: str
    ) -> type[BaseModel]:
        """Recursively create nested models."""
        if nested_name in nested_models:
            return nested_models[nested_name]

        nested_fields = {}
        for field_name, field_value in nested_template.items():
            field_type = get_field_type(field_name, field_value, nested_name)
            description = get_field_description(field_value)
            nested_fields[field_name] = (
                field_type,
                Field(..., description=description),
            )

        model = create_model(nested_name, **nested_fields)
        nested_models[nested_name] = model
        return model

    def get_field_type(
        field_name: str,
        value: Any,  # noqa:ANN401
        parent_name: str = class_name,
    ) -> type:
        if isinstance(value, dict):
            # Nested object - create a new model (NOT nullable)
            nested_name = f"{parent_name}{field_name.title()}"
            return create_nested_model(value, nested_name)

        if isinstance(value, list):
            if len(value) == 1:
                inner_value = value[0]
                if isinstance(inner_value, dict):
                    # Array of nested objects: [{"name": "string"}] -> list[NestedModel]
                    # (NOT nullable)
                    nested_name = f"{parent_name}{field_name.title()}Item"
                    nested_model = create_nested_model(inner_value, nested_name)
                    return list[nested_model]
                if isinstance(inner_value, str):
                    # Single type array: ["string"] -> list[str] (NOT nullable)
                    inner_type = type_mapping.get(inner_value, str)
                    return list[inner_type]
                if is_object_multi_enum(value) and all(
                    isinstance(v, str) for v in inner_value
                ):
                    # Multi-value enum: [["English", "French"]]
                    # -> list[Literal["English", "French"]] (NOT nullable)
                    return list[Literal[tuple(inner_value)]]
                return list[Any]

            if is_object_enum(value) and all(isinstance(v, str) for v in value):
                # Enum: ["pop", "rock", "jazz"]
                # -> Literal["pop", "rock", "jazz"] | None (nullable)
                return Literal[tuple(value)] | None

            if is_object_enum(value) and all(isinstance(v, dict) for v in value):
                # This shouldn't happen in a template, but handle gracefully
                return list[Any]

        elif isinstance(value, str):
            # Primitive types are nullable: string -> str | None
            base_type = type_mapping.get(value, str)
            return base_type | type(None)

        return Any

    def get_field_description(original_value: Any) -> str | None:  # noqa:ANN401
        if isinstance(original_value, str) and original_value in description_mapping:
            return description_mapping[original_value]
        if isinstance(original_value, list):
            if is_object_multi_enum(original_value):
                values = "', '".join(original_value[0])
                return f"Multiple values allowed from: '{values}'"
            if is_object_enum(original_value) and all(
                isinstance(v, str) for v in original_value
            ):
                values = "', '".join(original_value)
                return f"Single choice from: '{values}' (or null if not applicable)"

        return None

    # Build field definitions for the main model
    field_definitions = {}

    for field_name, field_value in template.items():
        field_type = get_field_type(field_name, field_value)
        description = get_field_description(field_value)
        field_definitions[field_name] = (
            field_type,
            Field(..., description=description),
        )

    # Create and return the main model class
    main_model = create_model(class_name, **field_definitions)

    # Attach nested models as attributes for easy access
    for name, model in nested_models.items():
        setattr(main_model, name, model)

    return main_model


def convert_pydantic_model_to_nuextract_template(
    pydantic_model: type[BaseModel],
) -> dict[str, Any]:
    """
    Convert a Pydantic model class into a NuExtract template.

    Pydantic field constraints that cannot be represented by a NuExtract template,
    such as numeric bounds and required fields, are discarded by the JSON Schema
    conversion.

    :param pydantic_model: Pydantic model class to convert.
    :return: The corresponding NuExtract template.
    :raises KeyError: If a local JSON Schema reference cannot be resolved.
    :raises TypeError: If Pydantic produces an invalid JSON Schema node.
    :raises ValueError: If the model contains an unsupported JSON Schema construct.
    """
    template, _, _ = convert_json_schema_to_nuextract_template(
        pydantic_model.model_json_schema()
    )
    return template
