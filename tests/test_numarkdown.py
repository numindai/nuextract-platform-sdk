"""Test synchronous and asynchronous content extraction."""

from __future__ import annotations

from types import SimpleNamespace
from typing import TYPE_CHECKING
from unittest.mock import AsyncMock, Mock, call

import pytest

from numind import NuMind, NuMindAsync

from .conftest import TEST_CASES_NUMARKDOWN

if TYPE_CHECKING:
    from pathlib import Path


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


def test_extract_content_submits_polls_and_gets_result(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = NuMind(client=object())
    content_result = object()
    incomplete_job_status = SimpleNamespace(completed_at=None, status="running")
    completed_job_status = SimpleNamespace(completed_at="now", status="completed")
    submit_job = Mock(return_value=SimpleNamespace(job_id="job-id"))
    get_job_status = Mock(side_effect=[incomplete_job_status, completed_job_status])
    get_job_result = Mock(return_value=content_result)
    sleep = Mock()
    monkeypatch.setattr(client, "post_api_content_extraction_jobs", submit_job)
    monkeypatch.setattr(client, "get_api_jobs_jobid_status", get_job_status)
    monkeypatch.setattr(
        client,
        "get_api_content_extraction_jobs_contentextractionjobid",
        get_job_result,
    )
    monkeypatch.setattr("numind.numind.time.sleep", sleep)

    result = client.extract_content(
        b"document", job_status_polling_delay=0.25, timeout="10m"
    )

    submit_job.assert_called_once_with(b"document", timeout="10m")
    assert get_job_status.call_args_list == [call("job-id"), call("job-id")]
    sleep.assert_called_once_with(0.25)
    get_job_result.assert_called_once_with("job-id")
    assert result is content_result


@pytest.mark.asyncio
async def test_extract_content_async_returns_failed_status(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = NuMindAsync(client=object())
    incomplete_job_status = SimpleNamespace(completed_at=None, status="running")
    failed_job_status = SimpleNamespace(completed_at="now", status="failed")
    submit_job = AsyncMock(return_value=SimpleNamespace(job_id="job-id"))
    get_job_status = AsyncMock(side_effect=[incomplete_job_status, failed_job_status])
    get_job_result = AsyncMock()
    sleep = AsyncMock()
    monkeypatch.setattr(client, "post_api_content_extraction_jobs", submit_job)
    monkeypatch.setattr(client, "get_api_jobs_jobid_status", get_job_status)
    monkeypatch.setattr(
        client,
        "get_api_content_extraction_jobs_contentextractionjobid",
        get_job_result,
    )
    monkeypatch.setattr("numind.numind.asyncio.sleep", sleep)

    result = await client.extract_content(b"document", job_status_polling_delay=0.5)

    submit_job.assert_awaited_once_with(b"document")
    assert get_job_status.await_args_list == [call("job-id"), call("job-id")]
    sleep.assert_awaited_once_with(0.5)
    get_job_result.assert_not_awaited()
    assert result is failed_job_status
