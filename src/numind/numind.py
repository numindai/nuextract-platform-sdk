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

MESSAGE_STATUS_COMPLETED = "result"
JOB_STATUS_COMPLETED = "completed"
JOB_POLLING_DELAY_SECONDS = 1
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
        **kwargs,
    ) -> StructuredExtractionResponse | JobStatusResponse:
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
        :param kwargs: structured extraction settings, such as ``temperature``, and
            submission options such as ``timeout``.
        :return: the API response.
        :raises ValueError: if exactly one document input is not provided.
        :raises KeyError: if an unknown extraction setting is provided.
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

        # Wait until the job reaches a terminal state before requesting its result.
        while True:
            job_status = self.get_api_jobs_jobid_status(job_id)
            if job_status.completed_at is not None:
                break
            time.sleep(JOB_POLLING_DELAY_SECONDS)

        if job_status.status != JOB_STATUS_COMPLETED:
            return job_status
        return self.get_api_structured_extraction_jobs_structuredextractionjobid(job_id)

    def add_examples_to_structured_extraction_project(
        self,
        project_id: str,
        examples: list[tuple[str | Path | bytes, dict | BaseModel | str]],
        convert_request: ConvertRequest | None = None,
    ) -> tuple[list[str], list[str]]:
        """
        Add ICL (In-Context Learning) examples to a project.

        :param project_id: id of the project to add examples to.
        :param examples: list of examples, to provided as a tuples of input and expected
            output. The inputs can be text (``str``) or files (``pathlib.Path`` or
            ``bytes``).
        :param convert_request: ``numind.models.ConvertRequest`` object holding the file
            conversion configuration, such as the DPI. If ``None`` is provided, the
            project's conversion configuration will be used. (default: ``None``)
        """
        files_ids, documents_ids = [], []
        if convert_request is None:
            project_info = self.get_api_structured_extraction_structuredprojectid(
                project_id
            )
            convert_request = ConvertRequest(
                rasterizationDPI=project_info.settings.rasterization_dpi,
            )
        for example_input, example_output in examples:
            # Prepare the example input and output, upload the input as file
            example_output = _parse_template(example_output)
            if isinstance(example_input, (Path, bytes)):
                example_input, file_name = _parse_input_file(example_input)
                file_id = self.post_api_files(file_name, example_input).file_id
                document_id = self.post_api_files_fileid_convert_to_document(
                    file_id, convert_request
                ).doc_info.actual_instance.document_id
            else:
                file_id = None
                document_id = self.post_api_documents_text(
                    TextRequest(text=example_input)
                ).doc_info.actual_instance.document_id
            files_ids.append(file_id)
            documents_ids.append(document_id)

            # Add the example to the project
            self.post_api_structured_extraction_structuredprojectid_examples(
                project_id,
                CreateOrUpdateStructuredExampleRequest(
                    documentId=StrictStr(document_id), result=example_output
                ),
            )

        return files_ids, documents_ids

    def extract_content(
        self, input_file: Path | str | bytes | None = None, **kwargs
    ) -> ContentExtractionResponse:
        """
        Extract Markdown content from an input file.

        :param input_file: input file to extract content from, provided as a
            ``pathlib.Path`` or string path, or bytes.
        :param kwargs: keyword arguments to pass to the
            ``client.post_api_content_extraction_jobs`` method.
        :return: ``numind.models.ContentExtractionResponse`` object.
        """
        input_, _ = _parse_input_file(input_file)
        job_id_response = self.post_api_content_extraction_jobs(input_, **kwargs)
        job_output = self.get_api_jobs_jobid_stream(
            job_id_response.job_id, _headers={"Accept": "text/event-stream"}
        )
        messages = _parse_sse_string(job_output)
        if messages[-1]["event"] != MESSAGE_STATUS_COMPLETED:
            raise ValueError(_ := f"Request couldn't be completed:\n{messages[-1]}")
        return ContentExtractionResponse(
            **json.loads(json.loads(messages[-1]["data"])["outputData"])
        )


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
        **kwargs,
    ) -> StructuredExtractionResponse | JobStatusResponse:
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
        :param kwargs: structured extraction settings, such as ``temperature``, and
            submission options such as ``timeout``.
        :return: the API response.
        :raises ValueError: if exactly one document input is not provided.
        :raises KeyError: if an unknown extraction setting is provided.
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

        # Wait until the job reaches a terminal state before requesting its result.
        while True:
            job_status = await self.get_api_jobs_jobid_status(job_id)
            if job_status.completed_at is not None:
                break
            await asyncio.sleep(JOB_POLLING_DELAY_SECONDS)

        if job_status.status != JOB_STATUS_COMPLETED:
            return job_status
        return await self.get_api_structured_extraction_jobs_structuredextractionjobid(
            job_id
        )

    async def add_examples_to_structured_extraction_project(
        self,
        project_id: str,
        examples: list[tuple[str | Path | bytes, dict | BaseModel | str]],
        convert_request: ConvertRequest | None = None,
    ) -> tuple[list[str], list[str]]:
        """
        Add ICL (In-Context Learning) examples to a project.

        :param project_id: id of the project to add examples to.
        :param examples: list of examples, to provided as a tuples of input and expected
            output. The inputs can be text (``str``) or files (``pathlib.Path`` or
            ``bytes``).
        :param convert_request: ``numind.models.ConvertRequest`` object holding the file
            conversion configuration, such as the DPI. If ``None`` is provided, the
            project's conversion configuration will be used. (default: ``None``)
        """
        files_ids, documents_ids = [], []
        if convert_request is None:
            project_info = await self.get_api_structured_extraction_structuredprojectid(
                project_id
            )
            convert_request = ConvertRequest(
                rasterizationDPI=project_info.settings.rasterization_dpi,
            )
        for example_input, example_output in examples:
            # Prepare the example input and output, upload the input as file
            example_output = _parse_template(example_output)
            if isinstance(example_input, (Path, bytes)):
                example_input, file_name = _parse_input_file(example_input)
                file_id = (await self.post_api_files(file_name, example_input)).file_id
                document_id = (
                    await self.post_api_files_fileid_convert_to_document(
                        file_id, convert_request
                    )
                ).doc_info.actual_instance.document_id
            else:
                file_id = None
                document_id = (
                    await self.post_api_documents_text(TextRequest(text=example_input))
                ).doc_info.actual_instance.document_id
            files_ids.append(file_id)
            documents_ids.append(document_id)

            # Add the example to the project
            await self.post_api_structured_extraction_structuredprojectid_examples(
                project_id,
                CreateOrUpdateStructuredExampleRequest(
                    documentId=StrictStr(document_id), result=example_output
                ),
            )

        return files_ids, documents_ids

    async def extract_content(
        self, input_file: Path | str | bytes | None = None, **kwargs
    ) -> ContentExtractionResponse:
        """
        Extract Markdown content from an input file.

        :param input_file: input file to extract content from, provided as a
            ``pathlib.Path`` or string path, or bytes.
        :param kwargs: keyword arguments to pass to the
            ``client.post_api_content_extraction_jobs`` method.
        :return: ``numind.models.ContentExtractionResponse`` object.
        """
        input_, _ = _parse_input_file(input_file)
        job_id_response = await self.post_api_content_extraction_jobs(input_, **kwargs)
        job_output = await self.get_api_jobs_jobid_stream(
            job_id_response.job_id, _headers={"Accept": "text/event-stream"}
        )
        messages = _parse_sse_string(job_output)
        if messages[-1]["event"] != MESSAGE_STATUS_COMPLETED:
            raise ValueError(_ := f"Request couldn't be completed:\n{messages[-1]}")
        return ContentExtractionResponse(
            **json.loads(json.loads(messages[-1]["data"])["outputData"])
        )


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
        extraction_request["examples"] = [
            {"result": _parse_template(example_output)}
            for _, example_output in examples
        ]
        for example_input, _ in examples:
            if isinstance(example_input, (Path, bytes)):
                example_bytes, example_file_name = _parse_input_file(example_input)
                example_files.append(
                    (example_file_name, example_bytes)
                    if example_file_name
                    else example_bytes
                )
            else:
                example_files.append(example_input.encode())

    return json.dumps(extraction_request), document_bytes, example_files


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


def _parse_sse_string(raw: str) -> list[dict[str, str]]:
    messages = []
    msg = {}
    data_buf = []
    for line in raw.splitlines():
        if not line.strip():  # blank line = end of message
            if data_buf or msg:
                msg["data"] = "\n".join(data_buf)
                messages.append(msg)
                msg, data_buf = {}, []
            continue

        if line.startswith(":"):  # comment line
            continue

        field, _, value = line.partition(":")
        value = value.lstrip(" ")
        if field == "data":
            data_buf.append(value)
        else:
            msg[field] = value

    # handle final pending message
    if data_buf or msg:
        msg["data"] = "\n".join(data_buf)
        messages.append(msg)

    return messages
