"""Testing the creation, update and deletion of a project."""

from pathlib import Path

import pytest

from numind import NuMind
from numind.openapi_client.models import CreateProjectRequest, TextRequest

from .conftest import TEST_CASES


@pytest.fixture(params=TEST_CASES, ids=lambda tc: f"project_{tc[0]}", scope="session")
def test_case(
    numind_client: NuMind, request: pytest.FixtureRequest
) -> tuple[str, dict, list[str], list[Path]]:
    return request.param


@pytest.mark.dependency(name="create_project")
def test_create_project(
    numind_client: NuMind,
    test_case: tuple[str, dict, list[str], list[Path]],
    request: pytest.FixtureRequest,
) -> None:
    project_name, schema, string_list, file_paths_list = test_case
    project_id = numind_client.post_api_projects(
        CreateProjectRequest(name=project_name, description="", template=schema)
    ).id
    request.config.cache.set("project_id", project_id)
    request.config.cache.set("text_cases", string_list)
    request.config.cache.set(
        "file_cases", [str(file_path) for file_path in file_paths_list]
    )


@pytest.mark.dependency(depends=["create_project"])
def test_get_existing_projects(
    numind_client: NuMind, request: pytest.FixtureRequest
) -> None:
    project_id = request.config.cache.get("project_id", None)
    projects = numind_client.get_api_projects(shared=False)
    assert project_id in {project.id for project in projects}


@pytest.mark.dependency(name="infer_text", depends=["create_project"])
def test_infer_text(numind_client: NuMind, request: pytest.FixtureRequest) -> None:
    project_id = request.config.cache.get("project_id", None)
    text_cases = request.config.cache.get("text_cases", None)
    for input_text in text_cases:
        _ = numind_client.post_api_projects_projectid_infer_text(
            project_id, text_request=TextRequest(text=input_text)
        )


@pytest.mark.dependency(name="infer_file", depends=["create_project"])
def test_infer_file(numind_client: NuMind, request: pytest.FixtureRequest) -> None:
    project_id = request.config.cache.get("project_id", None)
    file_cases = request.config.cache.get("file_cases", None)
    for file_path in file_cases:
        file_path = Path(file_path)
        with file_path.open("rb") as file:
            intput_file = file.read()
        _ = numind_client.post_api_projects_projectid_infer_file(
            project_id, file_path.name, intput_file
        )


@pytest.mark.dependency(depends=["infer_text", "infer_file"])
def test_delete_project_and_has_been_deleted(
    numind_client: NuMind, request: pytest.FixtureRequest
) -> None:
    project_id = request.config.cache.get("project_id", None)
    numind_client.delete_api_projects_projectid(project_id)
    projects = numind_client.get_api_projects(shared=False)
    assert project_id not in {project.id for project in projects}
