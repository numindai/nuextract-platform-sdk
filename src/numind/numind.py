"""NuMind API client."""

from __future__ import annotations

import asyncio
import json
import os
import time
from pathlib import Path

from pydantic import BaseModel, StrictStr

from .constants import NUMIND_API_KEY_ENV_VAR_NAME
from .models import (
    ContentExtractionResponse,
    ConvertRequest,
    CreateOrUpdateStructuredExampleRequest,
    JobStatusResponse,
    StructuredExtractionResponse,
    TextRequest,
)
from .openapi_client import (
    ApiClient,
    Configuration,
    ContentExtractionApi,
    ContentExtractionProjectManagementApi,
    DocumentsApi,
    FilesApi,
    InferenceApi,
    JobsApi,
    StructuredDataExtractionApi,
    StructuredExtractionExamplesApi,
    StructuredExtractionProjectManagementApi,
    TemplateGenerationApi,
)
from .openapi_client_async import (
    ApiClient as ApiClientAsync,
)
from .openapi_client_async import (
    ContentExtractionApi as ContentExtractionApiAsync,
)
from .openapi_client_async import (
    ContentExtractionProjectManagementApi as ContentExtractionProjectManagementApiAsync,
)
from .openapi_client_async import (
    DocumentsApi as DocumentsApiAsync,
)
from .openapi_client_async import (
    FilesApi as FilesApiAsync,
)
from .openapi_client_async import (
    InferenceApi as InferenceApiAsync,
)
from .openapi_client_async import (
    JobsApi as JobsApiAsync,
)
from .openapi_client_async import (
    StructuredDataExtractionApi as StructuredDataExtractionApiAsync,
)
from .openapi_client_async import (
    StructuredExtractionExamplesApi as StructuredExtractionExamplesApiAsync,
)
from .openapi_client_async import (
    StructuredExtractionProjectManagementApi as StructuredExtractionProjectManagementApiAsync,  # noqa: E501
)
from .openapi_client_async import (
    TemplateGenerationApi as TemplateGenerationApiAsync,
)

JOB_STATUS_COMPLETED = "completed"
JOB_POLLING_DELAY_SECONDS = 4
STRUCTURED_EXTRACTION_SETTING_NAMES = {
    "temperature": "temperature",
    "dpi": "rasterizationDPI",
    "max_output_tokens": "maxOutputTokens",
    "degraded_mode": "degradedMode",
    "max_example_token_number": "maxExampleTokenNumber",
    "max_example_number": "maxExampleNumber",
    "min_example_similarity": "minExampleSimilarity",
    "enable_thinking": "enableThinking",
    "random_seed": "randomSeed",
}


class FailedJobStatusResponse(JobStatusResponse):
    """Represent a terminal failed job together with its reported reason."""

    reason: str


class NuMind(
    DocumentsApi,
    StructuredExtractionExamplesApi,
    StructuredDataExtractionApi,
    ContentExtractionProjectManagementApi,
    TemplateGenerationApi,
    FilesApi,
    InferenceApi,
    JobsApi,
    ContentExtractionApi,
    StructuredExtractionProjectManagementApi,
):
    """NuMind API client."""

    def __init__(
        self,
        api_key: str | None = None,
        configuration: Configuration | None = None,
        client: ApiClient | None = None,
    ) -> None:
        if client is None:
            client = _prepare_client(api_key, configuration)
        super().__init__(client)

    def extract_structured_data(
        self,
        template: dict | BaseModel | str,
        instructions: str | None = None,
        input_text: str | None = None,
        input_file: Path | str | bytes | None = None,
        examples: list[tuple[str | Path | bytes, dict | BaseModel | str]] | None = None,
        convert_request: ConvertRequest | None = None,
        job_status_polling_delay: float = JOB_POLLING_DELAY_SECONDS,
        raise_on_job_fail: bool = True,
        **kwargs,
    ) -> StructuredExtractionResponse | FailedJobStatusResponse:
        """
        Extract structured data from an input document.

        Submit a projectless extraction job and wait for its result.

        :param template: template of the structured output describing the information to
            extract.
        :param instructions: instructions the model should follow when extracting
            structured data.
        :param input_text: text input as a string.
        :param input_file: input file, either as bytes or as a path (``str`` or
            ``pathlib.Path``) to the file to send to the API.
        :param examples: ICL (In-Context Learning) examples to add to the inference.
            Examples are pairs of inputs and expected outputs that aim to show practical
            use-cases and expected responses aiming to guide it to produce more accurate
            outputs. (default: ``None``)
        :param convert_request: ``ConvertRequest`` object holding the file conversion
            configuration, such as the DPI. If ``None`` is provided, the default API
            conversion configuration will be used. (default: ``None``)
        :param job_status_polling_delay: seconds to wait between job status requests.
        :param raise_on_job_fail: whether to raise when the job fails. If false, return
            the terminal job status and failure reason.
        :param kwargs: structured extraction settings, such as ``temperature``, and
            submission options such as ``timeout``.
        :return: extraction result, or failed job details when raising is disabled.
        :raises ValueError: if exactly one document input is not provided.
        :raises KeyError: if an unknown extraction setting is provided.
        :raises RuntimeError: if the extraction job fails and ``raise_on_job_fail`` is
            true.
        """
        job_timeout = kwargs.pop("timeout", None)
        extraction_request_json, document_bytes, example_files = (
            _prepare_structured_extraction_job(
                template,
                instructions,
                input_text,
                input_file,
                examples,
                convert_request,
                kwargs,
            )
        )
        job_id = self.post_api_structured_extraction_jobs(
            extraction_request_json,
            document_bytes,
            timeout=job_timeout,
            example_files=example_files or None,
        ).job_id

        job_status = self._poll_job_status(job_id, job_status_polling_delay)
        if job_status.status != JOB_STATUS_COMPLETED:
            failed_job_event_stream = self.get_api_jobs_jobid_stream(
                job_id,
                _headers={"Accept": "text/event-stream"},
            )
            return _raise_or_return_failed_job_response(
                job_status,
                failed_job_event_stream,
                raise_on_job_fail,
            )
        return self.get_api_structured_extraction_jobs_structuredextractionjobid(job_id)

    def _poll_job_status(
        self, job_id: str, job_status_polling_delay: float
    ) -> JobStatusResponse:
        """
        Poll a job until it reaches a terminal state.

        :param job_id: asynchronous job identifier.
        :param job_status_polling_delay: seconds between status requests.
        :return: terminal job status.
        """
        while True:
            job_status = self.get_api_jobs_jobid_status(job_id)
            if job_status.completed_at is not None:
                return job_status
            time.sleep(job_status_polling_delay)

    def add_examples_to_structured_extraction_project(
        self,
        project_id: str,
        examples: list[tuple[str | Path | bytes, dict | BaseModel | str]],
        convert_request: ConvertRequest | None = None,
    ) -> tuple[list[str | None], list[str]]:
        """
        Add ICL (In-Context Learning) examples to a project.

        :param project_id: id of the project to add examples to.
        :param examples: list of examples, to provided as a tuples of input and expected
            output. The inputs can be text (``str``) or files (``pathlib.Path`` or
            ``bytes``).
        :param convert_request: ``numind.models.ConvertRequest`` object holding the file
            conversion configuration, such as the DPI. If ``None`` is provided, the
            project's conversion configuration will be used. (default: ``None``)
        :return: file IDs (``None`` for text inputs) and document IDs.
        """
        file_ids, document_ids = [], []
        if convert_request is None:
            project_info = self.get_api_structured_extraction_structuredprojectid(
                project_id
            )
            convert_request = ConvertRequest(
                rasterizationDPI=project_info.settings.rasterization_dpi,
            )
        for example_input, example_output in examples:
            prepared_example_input, example_file_name, parsed_example_output = (
                _prepare_structured_example(example_input, example_output)
            )

            # Upload files or create text documents for the normalized input.
            if isinstance(prepared_example_input, bytes):
                file_id = self.post_api_files(
                    example_file_name, prepared_example_input
                ).file_id
                document_id = self.post_api_files_fileid_convert_to_document(
                    file_id, convert_request
                ).doc_info.actual_instance.document_id
            else:
                file_id = None
                document_id = self.post_api_documents_text(
                    TextRequest(text=prepared_example_input)
                ).doc_info.actual_instance.document_id
            file_ids.append(file_id)
            document_ids.append(document_id)

            # Add the example to the project
            self.post_api_structured_extraction_structuredprojectid_examples(
                project_id,
                CreateOrUpdateStructuredExampleRequest(
                    documentId=StrictStr(document_id), result=parsed_example_output
                ),
            )

        return file_ids, document_ids

    def extract_content(
        self,
        input_file: Path | str | bytes | None = None,
        job_status_polling_delay: float = JOB_POLLING_DELAY_SECONDS,
        raise_on_job_fail: bool = True,
        **kwargs,
    ) -> ContentExtractionResponse | FailedJobStatusResponse:
        """
        Extract Markdown content from an input file.

        :param input_file: input file to extract content from, provided as a
            ``pathlib.Path`` or string path, or bytes.
        :param job_status_polling_delay: seconds to wait between job status requests.
        :param raise_on_job_fail: whether to raise when the job fails. If false, return
            the terminal job status and failure reason.
        :param kwargs: keyword arguments to pass to the
            ``client.post_api_content_extraction_jobs`` method.
        :return: extraction result, or failed job details when raising is disabled.
        :raises RuntimeError: if the extraction job fails and ``raise_on_job_fail`` is
            true.
        """
        input_bytes, _ = _parse_input_file(input_file)
        job_id = self.post_api_content_extraction_jobs(input_bytes, **kwargs).job_id
        job_status = self._poll_job_status(job_id, job_status_polling_delay)
        if job_status.status != JOB_STATUS_COMPLETED:
            failed_job_event_stream = self.get_api_jobs_jobid_stream(
                job_id,
                _headers={"Accept": "text/event-stream"},
            )
            return _raise_or_return_failed_job_response(
                job_status,
                failed_job_event_stream,
                raise_on_job_fail,
            )
        return self.get_api_content_extraction_jobs_contentextractionjobid(job_id)


class NuMindAsync(
    DocumentsApiAsync,
    ContentExtractionProjectManagementApiAsync,
    TemplateGenerationApiAsync,
    StructuredExtractionExamplesApiAsync,
    StructuredDataExtractionApiAsync,
    FilesApiAsync,
    InferenceApiAsync,
    JobsApiAsync,
    ContentExtractionApiAsync,
    StructuredExtractionProjectManagementApiAsync,
):
    """NuMind API client."""

    def __init__(
        self,
        api_key: str | None = None,
        configuration: Configuration | None = None,
        client: ApiClientAsync | None = None,
    ) -> None:
        if client is None:
            client = _prepare_client(api_key, configuration, async_client=True)
        super().__init__(client)

    async def extract_structured_data(
        self,
        template: dict | BaseModel | str,
        instructions: str | None = None,
        input_text: str | None = None,
        input_file: Path | str | bytes | None = None,
        examples: list[tuple[str | Path | bytes, dict | BaseModel | str]] | None = None,
        convert_request: ConvertRequest | None = None,
        job_status_polling_delay: float = JOB_POLLING_DELAY_SECONDS,
        raise_on_job_fail: bool = True,
        **kwargs,
    ) -> StructuredExtractionResponse | FailedJobStatusResponse:
        """
        Extract structured data from an input document.

        Submit a projectless extraction job and wait for its result.

        :param template: template of the structured output describing the information to
            extract.
        :param instructions: instructions the model should follow when extracting
            structured data.
        :param input_text: text input as a string.
        :param input_file: input file, either as bytes or as a path (``str`` or
            ``pathlib.Path``) to the file to send to the API.
        :param examples: ICL (In-Context Learning) examples to add to the inference.
            Examples are pairs of inputs and expected outputs that aim to show practical
            use-cases and expected responses aiming to guide it to produce more accurate
            outputs. (default: ``None``)
        :param convert_request: ``ConvertRequest`` object holding the file conversion
            configuration, such as the DPI. If ``None`` is provided, the default API
            conversion configuration will be used. (default: ``None``)
        :param job_status_polling_delay: seconds to wait between job status requests.
        :param raise_on_job_fail: whether to raise when the job fails. If false, return
            the terminal job status and failure reason.
        :param kwargs: structured extraction settings, such as ``temperature``, and
            submission options such as ``timeout``.
        :return: extraction result, or failed job details when raising is disabled.
        :raises ValueError: if exactly one document input is not provided.
        :raises KeyError: if an unknown extraction setting is provided.
        :raises RuntimeError: if the extraction job fails and ``raise_on_job_fail`` is
            true.
        """
        job_timeout = kwargs.pop("timeout", None)
        extraction_request_json, document_bytes, example_files = (
            _prepare_structured_extraction_job(
                template,
                instructions,
                input_text,
                input_file,
                examples,
                convert_request,
                kwargs,
            )
        )
        job_id = (
            await self.post_api_structured_extraction_jobs(
                extraction_request_json,
                document_bytes,
                timeout=job_timeout,
                example_files=example_files or None,
            )
        ).job_id

        job_status = await self._poll_job_status(job_id, job_status_polling_delay)
        if job_status.status != JOB_STATUS_COMPLETED:
            failed_job_event_stream = await self.get_api_jobs_jobid_stream(
                job_id,
                _headers={"Accept": "text/event-stream"},
            )
            return _raise_or_return_failed_job_response(
                job_status,
                failed_job_event_stream,
                raise_on_job_fail,
            )
        return await self.get_api_structured_extraction_jobs_structuredextractionjobid(
            job_id
        )

    async def _poll_job_status(
        self, job_id: str, job_status_polling_delay: float
    ) -> JobStatusResponse:
        """
        Poll a job until it reaches a terminal state.

        :param job_id: asynchronous job identifier.
        :param job_status_polling_delay: seconds between status requests.
        :return: terminal job status.
        """
        while True:
            job_status = await self.get_api_jobs_jobid_status(job_id)
            if job_status.completed_at is not None:
                return job_status
            await asyncio.sleep(job_status_polling_delay)

    async def add_examples_to_structured_extraction_project(
        self,
        project_id: str,
        examples: list[tuple[str | Path | bytes, dict | BaseModel | str]],
        convert_request: ConvertRequest | None = None,
    ) -> tuple[list[str | None], list[str]]:
        """
        Add ICL (In-Context Learning) examples to a project.

        :param project_id: id of the project to add examples to.
        :param examples: list of examples, to provided as a tuples of input and expected
            output. The inputs can be text (``str``) or files (``pathlib.Path`` or
            ``bytes``).
        :param convert_request: ``numind.models.ConvertRequest`` object holding the file
            conversion configuration, such as the DPI. If ``None`` is provided, the
            project's conversion configuration will be used. (default: ``None``)
        :return: file IDs (``None`` for text inputs) and document IDs.
        """
        file_ids, document_ids = [], []
        if convert_request is None:
            project_info = await self.get_api_structured_extraction_structuredprojectid(
                project_id
            )
            convert_request = ConvertRequest(
                rasterizationDPI=project_info.settings.rasterization_dpi,
            )
        for example_input, example_output in examples:
            prepared_example_input, example_file_name, parsed_example_output = (
                _prepare_structured_example(example_input, example_output)
            )

            # Upload files or create text documents for the normalized input.
            if isinstance(prepared_example_input, bytes):
                file_id = (
                    await self.post_api_files(example_file_name, prepared_example_input)
                ).file_id
                document_id = (
                    await self.post_api_files_fileid_convert_to_document(
                        file_id, convert_request
                    )
                ).doc_info.actual_instance.document_id
            else:
                file_id = None
                document_id = (
                    await self.post_api_documents_text(
                        TextRequest(text=prepared_example_input)
                    )
                ).doc_info.actual_instance.document_id
            file_ids.append(file_id)
            document_ids.append(document_id)

            # Add the example to the project
            await self.post_api_structured_extraction_structuredprojectid_examples(
                project_id,
                CreateOrUpdateStructuredExampleRequest(
                    documentId=StrictStr(document_id), result=parsed_example_output
                ),
            )

        return file_ids, document_ids

    async def extract_content(
        self,
        input_file: Path | str | bytes | None = None,
        job_status_polling_delay: float = JOB_POLLING_DELAY_SECONDS,
        raise_on_job_fail: bool = True,
        **kwargs,
    ) -> ContentExtractionResponse | FailedJobStatusResponse:
        """
        Extract Markdown content from an input file.

        :param input_file: input file to extract content from, provided as a
            ``pathlib.Path`` or string path, or bytes.
        :param job_status_polling_delay: seconds to wait between job status requests.
        :param raise_on_job_fail: whether to raise when the job fails. If false, return
            the terminal job status and failure reason.
        :param kwargs: keyword arguments to pass to the
            ``client.post_api_content_extraction_jobs`` method.
        :return: extraction result, or failed job details when raising is disabled.
        :raises RuntimeError: if the extraction job fails and ``raise_on_job_fail`` is
            true.
        """
        input_bytes, _ = _parse_input_file(input_file)
        job_id = (
            await self.post_api_content_extraction_jobs(input_bytes, **kwargs)
        ).job_id
        job_status = await self._poll_job_status(job_id, job_status_polling_delay)
        if job_status.status != JOB_STATUS_COMPLETED:
            failed_job_event_stream = await self.get_api_jobs_jobid_stream(
                job_id,
                _headers={"Accept": "text/event-stream"},
            )
            return _raise_or_return_failed_job_response(
                job_status,
                failed_job_event_stream,
                raise_on_job_fail,
            )
        return await self.get_api_content_extraction_jobs_contentextractionjobid(job_id)


def _prepare_client(
    api_key: str, configuration: Configuration, async_client: bool = False
) -> ApiClient | ApiClientAsync:
    # Get api get from environment if argument is None
    if configuration is None:
        if api_key is None:
            api_key = os.getenv(NUMIND_API_KEY_ENV_VAR_NAME, None)
        if api_key is None:
            msg = (
                "The `NuMind` client must be initialized with either an"
                "`api_key`, a `Configuration`, by setting the "
                f"{NUMIND_API_KEY_ENV_VAR_NAME} environment variable or by "
                "providing a `client` (`numind.openapi_client.ApiClient` "
                "object)."
            )
            raise ValueError(msg)

    # Create configuration if required or make sure the api key attribute is non-None
    if configuration is None:
        configuration = Configuration(access_token=api_key)
    elif configuration.access_token is None:
        configuration.access_token = api_key

    return ApiClientAsync(configuration) if async_client else ApiClient(configuration)


def _prepare_structured_extraction_job(
    template: dict | BaseModel | str,
    instructions: str | None,
    input_text: str | None,
    input_file: Path | str | bytes | None,
    examples: list[tuple[str | Path | bytes, dict | BaseModel | str]] | None,
    convert_request: ConvertRequest | None,
    extraction_settings: dict,
) -> tuple[str, bytes, list[bytes | tuple[str, bytes]]]:
    """
    Build the manifest and multipart files for a projectless extraction job.

    :param template: structured output schema.
    :param instructions: optional extraction instructions.
    :param input_text: text document to extract from.
    :param input_file: file document to extract from.
    :param examples: optional input and expected-output pairs.
    :param convert_request: optional rasterization configuration.
    :param extraction_settings: inference settings using SDK argument names.
    :return: serialized manifest, document bytes, and ordered example files.
    :raises ValueError: if exactly one document input is not provided.
    :raises KeyError: if an unknown extraction setting is provided.
    """
    if bool(input_text is None) ^ bool(input_file is not None):
        msg = (
            "An input has to be provided with either the `input_text` or "
            "`input_file` argument."
        )
        raise ValueError(msg)

    document_bytes = (
        input_text.encode()
        if input_text is not None
        else _parse_input_file(input_file)[0]
    )

    request_settings = (
        convert_request.model_dump(by_alias=True) if convert_request is not None else {}
    )
    request_settings.update(
        {
            STRUCTURED_EXTRACTION_SETTING_NAMES[setting_name]: setting_value
            for setting_name, setting_value in extraction_settings.items()
            if setting_value is not None
        }
    )
    extraction_request = {
        "schema": _parse_template(template),
        "instructions": instructions or "",
        "settings": request_settings,
    }

    example_files = []
    if examples:
        parsed_example_results = []
        for example_input, example_output in examples:
            prepared_example_input, example_file_name, parsed_example_output = (
                _prepare_structured_example(example_input, example_output)
            )
            parsed_example_results.append({"result": parsed_example_output})
            if isinstance(prepared_example_input, bytes):
                example_files.append(
                    (example_file_name, prepared_example_input)
                    if example_file_name
                    else prepared_example_input
                )
            else:
                example_files.append(prepared_example_input.encode())
        extraction_request["examples"] = parsed_example_results

    return json.dumps(extraction_request), document_bytes, example_files


def _prepare_structured_example(
    example_input: str | Path | bytes,
    example_output: dict | BaseModel | str,
) -> tuple[str | bytes, str, dict]:
    """
    Normalize one structured extraction example.

    :param example_input: text, path, or bytes used as the example document.
    :param example_output: expected structured extraction output.
    :return: normalized input, file name when applicable, and parsed output.
    """
    parsed_example_output = _parse_template(example_output)
    if isinstance(example_input, (Path, bytes)):
        example_bytes, example_file_name = _parse_input_file(example_input)
        return example_bytes, example_file_name, parsed_example_output
    return example_input, "", parsed_example_output


def _parse_input_file(input_file: Path | str | bytes) -> tuple[bytes, str]:
    """Read an ``input_file`` argument provided in upstream methods."""
    file_name = ""
    if not isinstance(input_file, bytes):
        if not isinstance(input_file, Path):
            input_file = Path(input_file)
        file_name = input_file.name
        with input_file.open("rb") as file:
            input_file = file.read()
    return input_file, file_name


def _parse_template(template: dict | BaseModel | str) -> dict:
    """Read a ``template`` argument provided in upstream methods."""
    if not isinstance(template, dict):
        if isinstance(template, str):
            template = json.loads(template)
        else:
            template = template.model_dump()
    return template


def _raise_or_return_failed_job_response(
    job_status: JobStatusResponse,
    reason: str,
    raise_on_job_fail: bool,
) -> FailedJobStatusResponse:
    """
    Build a failed-job response and optionally raise it as a runtime error.

    :param job_status: terminal status returned by the jobs API.
    :param reason: error details returned by the job event stream.
    :param raise_on_job_fail: whether to raise instead of returning the response.
    :return: failed job details when raising is disabled.
    :raises RuntimeError: if ``raise_on_job_fail`` is true.
    """
    failed_job_status = FailedJobStatusResponse(
        **job_status.model_dump(),
        reason=reason,
    )
    if raise_on_job_fail:
        failed_job_error_message = (
            f"NuExtract job {failed_job_status.id} ended with status "
            f"{failed_job_status.status}:\n{failed_job_status.to_json()}"
        )
        raise RuntimeError(failed_job_error_message)
    return failed_job_status
