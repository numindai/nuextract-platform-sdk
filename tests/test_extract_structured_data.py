"""Tests for projectless structured extraction convenience methods."""

from __future__ import annotations

import json
from types import SimpleNamespace
from typing import TYPE_CHECKING
from unittest.mock import AsyncMock, Mock, call

import pytest

from numind import NuMind, NuMindAsync
from numind.models import ConvertRequest

if TYPE_CHECKING:
    from pathlib import Path


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
    sleep.assert_called_once_with(1)
    get_job_result.assert_called_once_with("job-id")
    assert result is extraction_result


@pytest.mark.asyncio
async def test_extract_structured_data_async_returns_failed_status(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = NuMindAsync(client=object())
    incomplete_job_status = SimpleNamespace(completed_at=None, status="running")
    failed_job_status = SimpleNamespace(completed_at="now", status="failed")

    submit_job = AsyncMock(return_value=SimpleNamespace(job_id="job-id"))
    get_job_status = AsyncMock(side_effect=[incomplete_job_status, failed_job_status])
    get_job_result = AsyncMock()
    sleep = AsyncMock()
    monkeypatch.setattr(client, "post_api_structured_extraction_jobs", submit_job)
    monkeypatch.setattr(client, "get_api_jobs_jobid_status", get_job_status)
    monkeypatch.setattr(
        client,
        "get_api_structured_extraction_jobs_structuredextractionjobid",
        get_job_result,
    )
    monkeypatch.setattr("numind.numind.asyncio.sleep", sleep)

    result = await client.extract_structured_data(
        template={"value": "string"}, input_text="target document"
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
    sleep.assert_awaited_once_with(1)
    get_job_result.assert_not_awaited()
    assert result is failed_job_status
