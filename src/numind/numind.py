"""NuMind API client."""

from __future__ import annotations

import json
import os
from pathlib import Path

from pydantic import BaseModel, StrictStr

from .constants import NUMIND_API_KEY_ENV_VAR_NAME, TMP_PROJECT_NAME
from .openapi_client import (
    ApiClient,
    Configuration,
    ConvertRequest,
    CreateOrUpdateExampleRequest,
    CreateProjectRequest,
    DocumentsApi,
    ExamplesApi,
    ExtractionApi,
    ExtractionResponse,
    FilesApi,
    InferenceApi,
    JobsApi,
    MarkdownApi,
    OrganizationsApi,
    ProjectManagementApi,
    TextRequest,
)
from .openapi_client_async import (
    ApiClient as ApiClientAsync,
)
from .openapi_client_async import (
    DocumentsApi as DocumentsApiAsync,
)
from .openapi_client_async import (
    ExamplesApi as ExamplesApiAsync,
)
from .openapi_client_async import (
    ExtractionApi as ExtractionApiAsync,
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
    MarkdownApi as MarkdownApiAsync,
)
from .openapi_client_async import (
    OrganizationsApi as OrganizationsApiAsync,
)
from .openapi_client_async import (
    ProjectManagementApi as ProjectManagementApiAsync,
)

JOB_STATUS_COMPLETED = "completed"


class NuMind(
    DocumentsApi,
    ExamplesApi,
    ExtractionApi,
    FilesApi,
    InferenceApi,
    JobsApi,
    MarkdownApi,
    OrganizationsApi,
    ProjectManagementApi,
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

    def extract(
        self,
        project_id: str | None = None,
        template: dict | BaseModel | str | None = None,
        input_text: str | None = None,
        input_file: Path | str | bytes | None = None,
        examples: list[tuple[str | Path | bytes, dict | BaseModel | str]] | None = None,
        convert_request: ConvertRequest | None = None,
        **kwargs,
    ) -> ExtractionResponse:
        """
        Send an inference request to the API for either a text or a file input.

        Either the ``project_id`` or ``template`` argument has to be provided. The
        former references to an existing project to which a template and examples are
        associated. The latter allows to quickly infer from a template and input data
        on the fly.

        :param project_id: id of the associated project. (default: ``None``)
        :param template: template of the structured output describing the information to
            extract. (default: ``None``)
        :param input_text: text input as a string.
        :param input_file: input file, either as bytes or as a path (``str`` or
            ``pathlib.Path``) to the file to send to the API.
        :param examples: ICL (In-Context Learning) examples to add to the inference.
            This argument is only used when this method is used "on the fly" with no
            attached project, i.e. when ``project_id`` is not provided.
            Examples are pairs of inputs and expected outputs that aim to show practical
            use-cases and expected responses aiming to guide it to produce more accurate
            outputs. (default: ``None``)
        :param convert_request: ``ConvertRequest`` object holding the file conversion
            configuration, such as the DPI. If ``None`` is provided, the default API
            conversion configuration will be used. (default: ``None``)
        :param kwargs: additional keyword arguments to pass to the
            ``post_api_projects_projectid_extract`` method, such as ``temperature``.
        :return: the API response.
        """
        if bool(input_text is None) ^ bool(input_file is not None):
            msg = (
                "An input has to be provided with either the `input_text` or"
                "`input_file_path` argument."
            )
            raise ValueError(msg)

        # If the project_id argument wasn't provided, create a temporary project
        if not (project_id_provided := project_id is not None):
            if template is None:
                msg = "Either a `project_id` or `template` as to be provided."
                raise ValueError(msg)
            template = _parse_template(template)
            project_id = self.post_api_projects(
                CreateProjectRequest(
                    name=TMP_PROJECT_NAME, description="", template=template
                )
            ).id

            # Add examples to the project, only when project_id is not provided so to
            # prevent users from adding examples with this method.
            if examples is not None and len(examples) > 0:
                self.add_examples_to_project(project_id, examples, convert_request)

        # Determine input
        if input_text is not None:
            input_ = input_text.encode()
        else:
            input_, _ = _parse_input_file(input_file)

        # Call model using server sent events streaming
        job_id_response = self.post_api_projects_projectid_extract_async(
            project_id, input_, **kwargs
        )
        job_output = self.get_api_jobs_jobid_stream(
            job_id_response.job_id, _headers={"Accept": "text/event-stream"}
        )

        # Parsing the server's response
        messages = _parse_sse_string(job_output)
        if messages[-1]["event"] != JOB_STATUS_COMPLETED:
            raise ValueError(_ := f"Request couldn't be completed:\n{messages[-1]}")
        output = json.loads(json.loads(messages[-1]["data"])["outputData"])
        output = ExtractionResponse(**output)

        # Delete temporary project if necessary
        if not project_id_provided:
            self.delete_api_projects_projectid(project_id)

        return output

    def add_examples_to_project(
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
        :param convert_request: ``ConvertRequest`` object holding the file conversion
            configuration, such as the DPI. If ``None`` is provided, the project's
            conversion configuration will be used. (default: ``None``)
        """
        files_ids, documents_ids = [], []
        if convert_request is None:
            project_info = self.get_api_projects_projectid(project_id=project_id)
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
            self.post_api_projects_projectid_examples(
                project_id,
                CreateOrUpdateExampleRequest(
                    documentId=StrictStr(document_id), result=example_output
                ),
            )

        return files_ids, documents_ids

    def numarkdown(self, input_file: Path | str | bytes | None = None) -> str:
        input_, _ = _parse_input_file(input_file)
        job_id_response = self.post_api_markdown_infer_async(input_)
        job_output = self.get_api_jobs_jobid_stream(
            job_id_response.job_id, _headers={"Accept": "text/event-stream"}
        )
        messages = _parse_sse_string(job_output)
        if messages[-1]["event"] != JOB_STATUS_COMPLETED:
            raise ValueError(_ := f"Request couldn't be completed:\n{messages[-1]}")
        # output = json.loads(json.loads(messages[-1]["data"])["outputData"])
        return messages[-1]["data"]


class NuMindAsync(
    DocumentsApiAsync,
    ExamplesApiAsync,
    ExtractionApiAsync,
    FilesApiAsync,
    InferenceApiAsync,
    JobsApiAsync,
    MarkdownApiAsync,
    OrganizationsApiAsync,
    ProjectManagementApiAsync,
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

    async def extract(
        self,
        project_id: str | None = None,
        template: dict | BaseModel | str | None = None,
        input_text: str | None = None,
        input_file: Path | str | bytes | None = None,
        examples: list[tuple[str | Path | bytes, dict | BaseModel | str]] | None = None,
        convert_request: ConvertRequest | None = None,
        **kwargs,
    ) -> ExtractionResponse:
        """
        Send an inference request to the API for either a text or a file input.

        Either the ``project_id`` or ``template`` argument has to be provided. The
        former references to an existing project to which a template and examples are
        associated. The latter allows to quickly infer from a template and input data
        on the fly.

        :param project_id: id of the associated project. (default: ``None``)
        :param template: template of the structured output describing the information to
            extract. (default: ``None``)
        :param input_text: text input as a string.
        :param input_file: input file, either as bytes or as a path (``str`` or
            ``pathlib.Path``) to the file to send to the API.
        :param examples: ICL (In-Context Learning) examples to add to the inference.
            This argument is only used when this method is used "on the fly" with no
            attached project, i.e. when ``project_id`` is not provided.
            Examples are pairs of inputs and expected outputs that aim to show practical
            use-cases and expected responses aiming to guide it to produce more accurate
            outputs. (default: ``None``)
        :param convert_request: ``ConvertRequest`` object holding the file conversion
            configuration, such as the DPI. If ``None`` is provided, the default API
            conversion configuration will be used. (default: ``None``)
        :param kwargs: additional keyword arguments to pass to the
            ``post_api_projects_projectid_extract`` method, such as ``temperature``.
        :return: the API response.
        """
        if bool(input_text is None) ^ bool(input_file is not None):
            msg = (
                "An input has to be provided with either the `input_text` or"
                "`input_file_path` argument."
            )
            raise ValueError(msg)

        # If the project_id argument wasn't provided, create a temporary project
        if not (project_id_provided := project_id is not None):
            if template is None:
                msg = "Either a `project_id` or `template` as to be provided."
                raise ValueError(msg)
            template = _parse_template(template)
            project_id = await self.post_api_projects(
                CreateProjectRequest(
                    name=TMP_PROJECT_NAME, description="", template=template
                )
            ).id

            # Add examples to the project, only when project_id is not provided so to
            # prevent users from adding examples with this method.
            if examples is not None and len(examples) > 0:
                await self.add_examples_to_project(
                    project_id, examples, convert_request
                )

        # Determine input
        if input_text is not None:
            input_ = input_text.encode()
        else:
            input_, _ = _parse_input_file(input_file)

        # Call model using server sent events streaming
        job_id_response = await self.post_api_projects_projectid_extract_async(
            project_id, input_, **kwargs
        )
        job_output = await self.get_api_jobs_jobid_stream(
            job_id_response.job_id, _headers={"Accept": "text/event-stream"}
        )

        # Parsing the server's response
        messages = _parse_sse_string(job_output)
        if messages[-1]["event"] != JOB_STATUS_COMPLETED:
            raise ValueError(_ := f"Request couldn't be completed:\n{messages[-1]}")
        output = json.loads(json.loads(messages[-1]["data"])["outputData"])
        output = ExtractionResponse(**output)

        # Delete temporary project if necessary
        if not project_id_provided:
            await self.delete_api_projects_projectid(project_id)

        return output

    async def add_examples_to_project(
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
        :param convert_request: ``ConvertRequest`` object holding the file conversion
            configuration, such as the DPI. If ``None`` is provided, the project's
            conversion configuration will be used. (default: ``None``)
        """
        files_ids, documents_ids = [], []
        if convert_request is None:
            project_info = await self.get_api_projects_projectid(project_id=project_id)
            convert_request = ConvertRequest(
                rasterizationDPI=project_info.settings.rasterization_dpi,
            )
        for example_input, example_output in examples:
            # Prepare the example input and output, upload the input as file
            example_output = _parse_template(example_output)
            if isinstance(example_input, (Path, bytes)):
                example_input, file_name = _parse_input_file(example_input)
                file_id = await self.post_api_files(file_name, example_input).file_id
                document_id = await self.post_api_files_fileid_convert_to_document(
                    file_id, convert_request
                ).doc_info.actual_instance.document_id
            else:
                file_id = None
                document_id = await self.post_api_documents_text(
                    TextRequest(text=example_input)
                ).doc_info.actual_instance.document_id
            files_ids.append(file_id)
            documents_ids.append(document_id)

            # Add the example to the project
            await self.post_api_projects_projectid_examples(
                project_id,
                CreateOrUpdateExampleRequest(
                    documentId=StrictStr(document_id), result=example_output
                ),
            )

        return files_ids, documents_ids

    async def numarkdown(self, input_file: Path | str | bytes | None = None) -> str:
        input_, _ = _parse_input_file(input_file)
        job_id_response = await self.post_api_markdown_infer_async(input_)
        job_output = await self.get_api_jobs_jobid_stream(
            job_id_response.job_id, _headers={"Accept": "text/event-stream"}
        )
        messages = _parse_sse_string(job_output)
        if messages[-1]["event"] != JOB_STATUS_COMPLETED:
            raise ValueError(_ := f"Request couldn't be completed:\n{messages[-1]}")
        # output = json.loads(json.loads(messages[-1]["data"])["outputData"])
        # TODO add NuMarkdownResponse object when available
        return messages[-1]["data"]


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
            template = BaseModel().model_dump()
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
