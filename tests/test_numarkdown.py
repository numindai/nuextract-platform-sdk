"""Test synchronous and asynchronous content extraction."""

from __future__ import annotations

from types import SimpleNamespace
from typing import TYPE_CHECKING
from unittest.mock import AsyncMock, Mock, call

import pytest

from numind import NuMind, NuMindAsync
from numind.numind import FailedJobStatusResponse

from .conftest import TEST_CASES_NUMARKDOWN

if TYPE_CHECKING:
    from pathlib import Path

    from numind.models import JobStatusResponse


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


def test_extract_content_reports_failed_job_event_stream(
    monkeypatch: pytest.MonkeyPatch,
    failed_job_status_response: JobStatusResponse,
) -> None:
    client = NuMind(client=object())
    submit_job = Mock(return_value=SimpleNamespace(job_id="job-id"))
    get_job_status = Mock(return_value=failed_job_status_response)
    get_job_result = Mock()
    failed_job_event_stream = (
        'event: result\ndata: {"code":413,"message":"Request Entity Too Large"}'
    )
    get_job_event_stream = Mock(return_value=failed_job_event_stream)
    monkeypatch.setattr(client, "post_api_content_extraction_jobs", submit_job)
    monkeypatch.setattr(client, "get_api_jobs_jobid_status", get_job_status)
    monkeypatch.setattr(
        client,
        "get_api_content_extraction_jobs_contentextractionjobid",
        get_job_result,
    )
    monkeypatch.setattr(client, "get_api_jobs_jobid_stream", get_job_event_stream)

    with pytest.raises(RuntimeError) as raised_error:
        client.extract_content(b"document")

    get_job_result.assert_not_called()
    get_job_event_stream.assert_called_once_with("job-id")
    expected_failed_job_status = FailedJobStatusResponse(
        **failed_job_status_response.model_dump(),
        reason=failed_job_event_stream,
    )
    assert str(raised_error.value) == (
        "NuExtract job job-id ended with status failed:\n"
        f"{expected_failed_job_status.to_json()}"
    )


@pytest.mark.asyncio
async def test_extract_content_async_returns_failed_job_status(
    monkeypatch: pytest.MonkeyPatch,
    failed_job_status_response: JobStatusResponse,
) -> None:
    client = NuMindAsync(client=object())
    incomplete_job_status = SimpleNamespace(completed_at=None, status="running")
    submit_job = AsyncMock(return_value=SimpleNamespace(job_id="job-id"))
    get_job_status = AsyncMock(
        side_effect=[incomplete_job_status, failed_job_status_response]
    )
    get_job_result = AsyncMock()
    failed_job_event_stream = (
        'event: result\ndata: {"code":413,"message":"Request Entity Too Large"}'
    )
    get_job_event_stream = AsyncMock(return_value=failed_job_event_stream)
    sleep = AsyncMock()
    monkeypatch.setattr(client, "post_api_content_extraction_jobs", submit_job)
    monkeypatch.setattr(client, "get_api_jobs_jobid_status", get_job_status)
    monkeypatch.setattr(
        client,
        "get_api_content_extraction_jobs_contentextractionjobid",
        get_job_result,
    )
    monkeypatch.setattr(client, "get_api_jobs_jobid_stream", get_job_event_stream)
    monkeypatch.setattr("numind.numind.asyncio.sleep", sleep)

    result = await client.extract_content(
        b"document",
        job_status_polling_delay=0.5,
        raise_on_job_fail=False,
    )

    submit_job.assert_awaited_once_with(b"document")
    assert get_job_status.await_args_list == [call("job-id"), call("job-id")]
    sleep.assert_awaited_once_with(0.5)
    get_job_result.assert_not_awaited()
    get_job_event_stream.assert_awaited_once_with("job-id")
    assert result == FailedJobStatusResponse(
        **failed_job_status_response.model_dump(),
        reason=failed_job_event_stream,
    )
