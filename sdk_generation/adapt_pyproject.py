"""Collate the project and generated client pyproject.toml for the complete package."""  # noqa:INP001

from pathlib import Path

import toml

IGNORED_TOOLS = {"poetry"}


def collate_pyproject_files(
    project_pyproject_path: Path,
    client_pyproject_path: Path,
    client_requirements_path: Path,
    output_file_path: Path = Path("pyproject.toml"),
) -> None:
    """
    Collate the project and generated client pyproject.toml for the complete package.

    :param project_pyproject_path: path to the base project pyproject file.
    :param client_pyproject_path: path to generated client pyproject file.
    :param client_requirements_path: path to generated client "requirements.txt" file.
    :param output_file_path: path to the output pyproject.toml file.
        (default: ``pyproject.toml``)
    """
    with project_pyproject_path.open() as file:
        toml_project = toml.load(file)
    with client_pyproject_path.open() as file:
        toml_client = toml.load(file)

    # Merge tools
    for tool_name, tool_value in toml_client["tool"].items():
        if tool_name not in IGNORED_TOOLS and tool_name not in toml_project["tool"]:
            toml_project["tool"][tool_name] = tool_value

    # Merge dependencies
    with client_requirements_path.open() as file:
        client_dependencies = [line.rstrip() for line in file.readlines()]
    project_dependencies_names = {
        line.split()[0] for line in toml_project["project"]["dependencies"]
    }
    for client_dependency in client_dependencies:
        dependency_name = client_dependency.split()[0]
        if dependency_name not in project_dependencies_names:
            toml_project["project"]["dependencies"].append(client_dependency)

    # Write the collated pyproject file
    with output_file_path.open("w") as file:
        toml.dump(toml_project, file)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Dataset creation script")
    parser.add_argument("--project-pyproject-path", type=str, required=True)
    parser.add_argument("--client-pyproject-path", type=str, required=True)
    parser.add_argument("--client-requirements-path", type=str, required=True)
    args = vars(parser.parse_args())

    collate_pyproject_files(
        Path(args["project_pyproject_path"]),
        Path(args["client_pyproject_path"]),
        Path(args["client_requirements_path"]),
    )
