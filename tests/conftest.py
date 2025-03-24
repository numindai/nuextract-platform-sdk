"""
Pytest configuration file.

Doc: https://docs.pytest.org/en/latest/reference/reference.html.
"""

from __future__ import annotations

import csv
import json
import os
from pathlib import Path

import pytest

from numind import NuMind

NUMIND_API_KEY_TEST_ENV_VAR_NAME = "NUMIND_API_KEY_TESTS"

TEST_CASES = []  # (test_name, schema, string_list, file_paths_list)
for dir_path in Path("tests", "test_cases").iterdir():
    with (dir_path / "schema.json").open() as file:
        schema = json.load(file)
    with (dir_path / "texts.csv").open() as file:
        reader = csv.reader(file)
        texts = [line[0] for line in reader]
    file_paths = [
        file_path for file_path in (dir_path / "files").iterdir()
        if not file_path.name.startswith(".")
    ]
    TEST_CASES.append((dir_path.name, schema, texts, file_paths))


@pytest.fixture()
def api_key() -> str:
    """
    Get the NuMind api_key from the environment variable.

    If the variable is not set, the test using this fixture will be skipped.
    """
    api_key = os.environ.get(NUMIND_API_KEY_TEST_ENV_VAR_NAME)
    if not api_key:
        msg = (
            f"The `{NUMIND_API_KEY_TEST_ENV_VAR_NAME}` environment variable is not set."
            f" It has to be set in order for the tests to be run to interact with the "
            f"API."
        )
        raise EnvironmentError(msg)
    return api_key


@pytest.fixture()
def numind_client(api_key: str) -> NuMind:
    """
    Get the NuMind api_key from the environment variable.

    If the variable is not set, the test using this fixture will be skipped.
    """
    return NuMind(api_key=api_key)
