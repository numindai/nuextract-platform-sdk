"""Testing the creation, update and deletion of a project."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from .conftest import TEST_CASES_NUMARKDOWN

if TYPE_CHECKING:
    from numind import NuMind, NuMindAsync


@pytest.mark.parametrize("file_path", TEST_CASES_NUMARKDOWN, ids=lambda p: p.name)
def test_numarkdown(numind_client: NuMind, file_path: Path) -> None:
    _ = numind_client.extract_content(file_path)


@pytest.mark.asyncio
@pytest.mark.parametrize("file_path", TEST_CASES_NUMARKDOWN, ids=lambda p: p.name)
async def test_numarkdown_async(
    numind_client_async: NuMindAsync,
    file_path: Path,
) -> None:
    _ = await numind_client_async.extract_content(file_path)
