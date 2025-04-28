"""NuMind API client."""

import json
import os
from pathlib import Path

from pydantic import BaseModel

from .constants import NUMIND_API_KEY_ENV_VAR_NAME, TMP_PROJECT_NAME
from .openapi_client import (
    ApiClient,
    Configuration,
    CreateProjectRequest,
    DocumentsApi,
    ExamplesApi,
    InferenceApi,
    InferenceResponse,
    ProjectsApi,
    TextRequest,
)


class NuMind(DocumentsApi, ExamplesApi, InferenceApi, ProjectsApi):
    """NuMind API client."""

    def __init__(
        self,
        api_key: str | None = None,
        configuration: Configuration | None = None,
        client: ApiClient | None = None,
    ) -> None:
        if client is None:
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
                configuration = Configuration(access_token=api_key)
            client = ApiClient(configuration)

        super().__init__(client)

    def infer(
        self,
        project_id: str | None,
        template: dict | BaseModel | str,
        input_text: str | None = None,
        input_file: Path | str | bytes | None = None,
    ) -> InferenceResponse:
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
        :return: the API response.
        """
        if (input_text is None) ^ input_file is not None:
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
            if not isinstance(template, dict):
                if isinstance(template, str):
                    template = json.loads(template, ensure_ascii=False, indent=0)
                else:
                    template = BaseModel().model_dump()
            project_id = self.post_api_projects(
                CreateProjectRequest(
                    name=TMP_PROJECT_NAME, description="", template=template
                )
            ).id

        # Infer with text input
        if input_text is not None:
            output = self.post_api_projects_projectid_infer_text(
                project_id, TextRequest(text=input_text)
            )

        # Infer with file input
        else:
            if not isinstance(input_file, bytes):
                if not isinstance(input_file, Path):
                    input_file = Path(input_file)
                with input_file.open("rb") as file:
                    intput_file = file.read()
            output = self.post_api_projects_projectid_infer_file(
                project_id, input_file.name, intput_file
            )

        # Delete temporary project if necessary
        if not project_id_provided:
            self.delete_api_projects_projectid(project_id)

        return output
