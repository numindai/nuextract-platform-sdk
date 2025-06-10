"""Script removing problematic models from an OpenAPI specification file."""

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
    "VerbatimStr": None,
}
API_BASE_URL = "https://nuextract.ai"


def edit_problematic_leaves(data: dict | list) -> None:
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
                edit_problematic_leaves(item)
                if len(item) == 0:
                    del data[idx]
        return

    # Dictionary
    for key, value in data.copy().items():
        if key in MODELS_TO_DELETE:
            del data[key]
        elif isinstance(value, (dict | list)):
            edit_problematic_leaves(data[key])
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


def edit_openapi_file(openapi_file_path: Path, output_file_path: Path) -> None:
    """
    Edit an OpenAPI file to remove the models to delete.

    :param openapi_file_path: path to the OpenAPI file to edit.
    :param output_file_path: path to save the edited OpenAPI file.
    """
    with openapi_file_path.open() as file:
        content = yaml.full_load(file)

    edit_problematic_leaves(content["paths"])
    edit_problematic_leaves(content["components"])

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
