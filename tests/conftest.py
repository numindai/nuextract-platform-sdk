"""
Pytest configuration file.

Doc: https://docs.pytest.org/en/latest/reference/reference.html.
"""

from __future__ import annotations

import asyncio
import csv
import json
import os
from pathlib import Path

import pytest
import pytest_asyncio

from numind import NuMind, NuMindAsync

NUMIND_API_KEY_TEST_ENV_VAR_NAME = "NUMIND_API_KEY_TESTS"
EXTRACT_KWARGS = {"temperature": 0.1, "max_output_tokens": 600}
TESTS_NAME_PREFIX = "tests-sdk"


def _read_test_case_examples(
    file_path: Path,
) -> list[tuple[str | Path, dict | str]]:
    with file_path.open() as file:
        reader = csv.reader(file)
        next(reader)  # skipping header
        examples = []
        for row in reader:
            input_text, input_file_path, output = row
            if input_text != "":
                examples.append((input_text, output))
            else:
                examples.append((file_path.parent / input_file_path, output))
    return examples


TEST_CASES_NUEXTRACT = []  # (test_name, schema, string_list, file_paths_list)
for dir_path in Path("tests", "test_cases").iterdir():
    if not dir_path.is_dir() or dir_path.name.startswith("."):
        continue
    with (dir_path / "schema.json").open() as file_:
        schema = json.load(file_)
    with (dir_path / "texts.csv").open(encoding="utf-8") as file_:
        reader_ = csv.reader(file_)
        texts = [line[0] for line in reader_]
    file_paths = [
        file_path
        for file_path in (dir_path / "files").iterdir()
        if not file_path.name.startswith(".")
    ]
    examples_ = _read_test_case_examples(dir_path / "examples.csv")
    TEST_CASES_NUEXTRACT.append(
        (f"{TESTS_NAME_PREFIX}-{dir_path.name}", schema, texts, file_paths, examples_)
    )


TEST_CASES_NUMARKDOWN = []  # (file_paths_list)
for dir_path in Path("tests", "test_cases").iterdir():
    if not dir_path.is_dir() or dir_path.name.startswith("."):
        continue
    TEST_CASES_NUMARKDOWN += [
        file_path
        for file_path in (dir_path / "files").iterdir()
        if not file_path.name.startswith(".")
    ]


@pytest.fixture(scope="session")
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
        raise OSError(msg)
    return api_key


@pytest.fixture(scope="session")
def numind_client(api_key: str) -> NuMind:
    """
    Get the NuMind api_key from the environment variable.

    If the variable is not set, the test using this fixture will be skipped.
    """
    return NuMind(api_key=api_key)


@pytest_asyncio.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def numind_client_async(api_key: str):
    """Get the NuMindAsync client."""
    client = NuMindAsync(api_key=api_key)
    yield client
    # If NuMindAsync has a close method, call it
    if hasattr(client, "close"):
        await client.close()
    elif hasattr(client, "aclose"):
        await client.aclose()
