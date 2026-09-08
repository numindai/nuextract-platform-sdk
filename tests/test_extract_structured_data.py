"""Tests for projectless structured extraction convenience methods."""

from __future__ import annotations

import json
from types import SimpleNamespace
from typing import TYPE_CHECKING
from unittest.mock import AsyncMock, Mock, call

import pytest

from numind import NuMind, NuMindAsync
from numind.models import ConvertRequest
from numind.numind import FailedJobStatusResponse

if TYPE_CHECKING:
    from pathlib import Path

    from numind.models import JobStatusResponse


def test_extract_structured_data_submits_and_polls(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    example_path = tmp_path / "example.txt"
    example_path.write_bytes(b"file example")
    client = NuMind(client=object())
    extraction_result = object()
    incomplete_job_status = SimpleNamespace(completed_at=None, status="running")
    completed_job_status = SimpleNamespace(completed_at="now", status="completed")

    submit_job = Mock(return_value=SimpleNamespace(job_id="job-id"))
    get_job_status = Mock(side_effect=[incomplete_job_status, completed_job_status])
    get_job_result = Mock(return_value=extraction_result)
    sleep = Mock()
    monkeypatch.setattr(client, "post_api_structured_extraction_jobs", submit_job)
    monkeypatch.setattr(client, "get_api_jobs_jobid_status", get_job_status)
    monkeypatch.setattr(
        client,
        "get_api_structured_extraction_jobs_structuredextractionjobid",
        get_job_result,
    )
    monkeypatch.setattr("numind.numind.time.sleep", sleep)

    result = client.extract_structured_data(
        template='{"value": "string"}',
        instructions="Extract the value.",
        input_file=b"target document",
        examples=[
            ("text example", '{"value": "first"}'),
            (example_path, {"value": "second"}),
        ],
        convert_request=ConvertRequest(rasterizationDPI=200),
        job_status_polling_delay=0.25,
        max_output_tokens=500,
        timeout="10m",
    )

    extraction_request_json, document_bytes = submit_job.call_args.args
    assert json.loads(extraction_request_json) == {
        "schema": {"value": "string"},
        "instructions": "Extract the value.",
        "settings": {"rasterizationDPI": 200, "maxOutputTokens": 500},
        "examples": [
            {"result": {"value": "first"}},
            {"result": {"value": "second"}},
        ],
    }
    assert document_bytes == b"target document"
    assert submit_job.call_args.kwargs == {
        "timeout": "10m",
        "example_files": [
            b"text example",
            ("example.txt", b"file example"),
        ],
    }
    assert get_job_status.call_args_list == [call("job-id"), call("job-id")]
    sleep.assert_called_once_with(0.25)
    get_job_result.assert_called_once_with("job-id")
    assert result is extraction_result


def test_extract_structured_data_reports_failed_job_event_stream(
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
    monkeypatch.setattr(client, "post_api_structured_extraction_jobs", submit_job)
    monkeypatch.setattr(client, "get_api_jobs_jobid_status", get_job_status)
    monkeypatch.setattr(
        client,
        "get_api_structured_extraction_jobs_structuredextractionjobid",
        get_job_result,
    )
    monkeypatch.setattr(client, "get_api_jobs_jobid_stream", get_job_event_stream)

    with pytest.raises(RuntimeError) as raised_error:
        client.extract_structured_data(
            template={"value": "string"}, input_text="target document"
        )

    get_job_result.assert_not_called()
    get_job_event_stream.assert_called_once_with(
        "job-id",
        _headers={"Accept": "text/event-stream"},
    )
    expected_failed_job_status = FailedJobStatusResponse(
        **failed_job_status_response.model_dump(),
        reason=failed_job_event_stream,
    )
    assert str(raised_error.value) == (
        "NuExtract job job-id ended with status failed:\n"
        f"{expected_failed_job_status.to_json()}"
    )


@pytest.mark.asyncio
async def test_extract_structured_data_async_returns_failed_job_status(
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
    monkeypatch.setattr(client, "post_api_structured_extraction_jobs", submit_job)
    monkeypatch.setattr(client, "get_api_jobs_jobid_status", get_job_status)
    monkeypatch.setattr(
        client,
        "get_api_structured_extraction_jobs_structuredextractionjobid",
        get_job_result,
    )
    monkeypatch.setattr(client, "get_api_jobs_jobid_stream", get_job_event_stream)
    monkeypatch.setattr("numind.numind.asyncio.sleep", sleep)

    result = await client.extract_structured_data(
        template={"value": "string"},
        input_text="target document",
        job_status_polling_delay=0.5,
        raise_on_job_fail=False,
    )

    submit_job.assert_awaited_once_with(
        json.dumps(
            {
                "schema": {"value": "string"},
                "instructions": "",
                "settings": {},
            }
        ),
        b"target document",
        timeout=None,
        example_files=None,
    )
    assert get_job_status.await_args_list == [
        call("job-id"),
        call("job-id"),
    ]
    sleep.assert_awaited_once_with(0.5)
    get_job_result.assert_not_awaited()
    get_job_event_stream.assert_awaited_once_with(
        "job-id",
        _headers={"Accept": "text/event-stream"},
    )
    assert result == FailedJobStatusResponse(
        **failed_job_status_response.model_dump(),
        reason=failed_job_event_stream,
    )
