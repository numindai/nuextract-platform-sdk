"""Testing the creation, update and deletion of a project."""

import pytest
from pathlib import Path

from numind import NuMind
from numind.openapi_client.models import CreateOrUpdateProjectRequest, TextRequest

from .conftest import TEST_CASES


@pytest.fixture(params=TEST_CASES, ids=lambda tc: f"project_{tc}")
def test_create_project(
    numind_client: NuMind, request: pytest.FixtureRequest
) -> tuple[str, list[str], list[Path]]:
    project_name, schema, string_list, file_paths_list = request.param
    project_id = numind_client.post_api_reference_projects(
        CreateOrUpdateProjectRequest(name=project_name, description="", template=schema)
    ).id
    return project_id, string_list, file_paths_list


def test_get_existing_projects(numind_client: NuMind, test_create_project) -> None:
    projects = numind_client.get_api_reference_projects(shared=False)
    assert test_create_project[0] in {project.id for project in projects}


def test_infer_text(numind_client: NuMind, test_create_project) -> None:
    for input_text in test_create_project[1]:
        _ = numind_client.post_api_reference_projects_projectid_infer_text(
            test_create_project[0], text_request=TextRequest(text=input_text)
        )


def test_infer_file(numind_client: NuMind, test_create_project) -> None:
    for file_path in test_create_project[2]:
        with file_path.open("rb") as file:
            intput_file = file.read()
        _ = numind_client.post_api_reference_projects_projectid_infer_file(
            test_create_project[0], file_path.name, intput_file
        )


@pytest.fixture()
def test_delete_project(numind_client: NuMind, test_create_project) -> str:
    numind_client.delete_api_reference_projects_projectid(test_create_project[0])
    return test_create_project[0]


def test_project_has_been_deleted(numind_client: NuMind, test_delete_project) -> None:
    projects = numind_client.get_api_reference_projects(shared=False)
    assert test_delete_project not in {project.id for project in projects}
