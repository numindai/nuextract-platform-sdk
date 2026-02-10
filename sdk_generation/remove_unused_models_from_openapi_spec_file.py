"""Script removing problematic models from an OpenAPI specification file."""  # noqa:INP001

from __future__ import annotations

from pathlib import Path

import yaml

MODELS_TO_DELETE = {
    "Obj": None,
    "Obj1": None,
    "SchemaNode": None,
    "ValidSchema": None,
    "InvalidSchema": None,
    "MultiEnum": None,
    "Enum": None,
    "Arr": None,
    "Arr1": None,
    "Bool": None,
    "Bool1": None,
    "Null": None,
    "Num": None,
    "Num1": None,
    "Str": None,
    "Str1": None,
    "Integer": None,
    "InfoNode": None,
}
PATHS_TO_DELETE = {
    f"/api/{path}" for path in (
        "jobs/{jobId}",
        "projects/{projectId}/extract",
        "projects/{projectId}/extract-async",
    )
}
TAGS_PATHS_TO_DELETE = {
    "Structured Extraction Playground",
    "Content Extraction Playground",
    "Authentication",
    "Organization Management",
    "Billing",
    "Project Management (Deprecated)",
    "Examples (Deprecated)",
    "Playground (Deprecated)",
    "Inference (Deprecated)",
}
API_BASE_URL = "https://nuextract.ai"


def remove_unwanted_models(data: dict | list) -> None:
    """
    Recursively remove models to delete from a dictionary or list, inplace.

    :param data: dictionary or list from an OpenAPI specification file.
    """
    # List --> recursively call the method, delete empty processed items
    if isinstance(data, list):
        for idx, item in reversed(list(enumerate(data.copy()))):
            if isinstance(item, (dict | list)):
                # Handles cases of "oneOf"
                if isinstance(item, dict) and len(item) == 1:
                    key, value = next(iter(item.items()))
                    if (
                        key == "$ref"
                        and isinstance(value, str)
                        and any(value.endswith(model) for model in MODELS_TO_DELETE)
                    ):
                        del data[idx]
                        continue
                remove_unwanted_models(item)
                if len(item) == 0:
                    del data[idx]
        return

    # Dictionary
    for key, value in data.copy().items():
        if key in MODELS_TO_DELETE:
            del data[key]
        elif isinstance(value, (dict | list)):
            remove_unwanted_models(data[key])
            if isinstance(value, list) and len(data[key]) == 0:
                del data[key]
                data["type"] = "object"
        # Replace references to model to delete by a simple "object" type
        elif key == "$ref":
            for model in MODELS_TO_DELETE:
                if value.endswith(model):
                    del data[key]
                    if MODELS_TO_DELETE[model] is None:
                        data["type"] = "object"
                    else:
                        data.update(MODELS_TO_DELETE[model])
                    break


def remove_unwanted_paths(paths: dict[str, dict]) -> None:
    """
    Remove paths from an OpenAPI paths dictionary.

    :param paths: dictionary of paths of OpenAPI specifications.
    """
    for path, path_details in paths.copy().items():
        # endpoints to delete based on their path
        # TODO remove this step, should only be handled by tags
        if path in PATHS_TO_DELETE:
            del paths[path]
            continue
        # Delete endpoints based on their tags
        for method, details in path_details.copy().items():
            if any(tag in TAGS_PATHS_TO_DELETE for tag in details["tags"]):
                del paths[path][method]
        if len(paths[path]) == 0:
            del paths[path]


def remove_unused_models(content: dict[str, dict | list]) -> None:
    """
    Remove paths from an OpenAPI paths dictionary.

    :param content: openapi specifications.
    """
    models_in_paths = get_models_in_endpoints(content["paths"])

    for model_name in content["components"]["schemas"].copy():
        if model_name not in models_in_paths:
            del content["components"]["schemas"][model_name]


def get_models_in_endpoints(data: dict | list) -> set[str]:
    """
    Recursively returns the model names present in an OpenAPI paths dictionary.

    :param data: dictionary or list from an OpenAPI specification file.
    :return: set of model names referenced in the paths
    """
    models = set()

    # List --> recursively call the method on each item
    if isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                models.update(get_models_in_endpoints(item))
        return models

    # Dictionary
    if isinstance(data, dict):
        for key, value in data.items():
            # Check for $ref keys that point to models
            if key == "$ref" and isinstance(value, str):
                # Extract model name from reference like #/components/schemas/ModelName
                if "/schemas/" in value:
                    model_name = value.split("/")[-1]
                    models.add(model_name)
            elif isinstance(value, (dict, list)):
                models.update(get_models_in_endpoints(value))

    return models


def edit_openapi_file(openapi_file_path: Path, output_file_path: Path) -> None:
    """
    Edit an OpenAPI file to remove the models to delete.

    :param openapi_file_path: path to the OpenAPI file to edit.
    :param output_file_path: path to save the edited OpenAPI file.
    """
    with openapi_file_path.open() as file:
        content = yaml.full_load(file)

    # Filter out paths with unwanted tags
    remove_unwanted_paths(content["paths"])
    for idx in reversed(range(len(content["tags"]))):
        if content["tags"][idx]["name"] in TAGS_PATHS_TO_DELETE:
            del content["tags"][idx]

    # Remove unwanted models from paths
    remove_unwanted_models(content["paths"])

    # Remove models from components that aren't found in paths
    remove_unused_models(content)

    # add server entry
    content["servers"] = [{"url": API_BASE_URL}]

    with output_file_path.open("w") as file:
        yaml.dump(content, file, allow_unicode=True, line_break=True, sort_keys=False)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Dataset creation script")
    parser.add_argument("--openapi-file-path", type=str, required=True)
    parser.add_argument("--output-file-path", type=str, required=True)
    args = vars(parser.parse_args())

    edit_openapi_file(Path(args["openapi_file_path"]), Path(args["output_file_path"]))
