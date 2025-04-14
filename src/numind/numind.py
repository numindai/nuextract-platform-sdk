"""NuMind API client."""

import os
from pathlib import Path

from .constants import NUMIND_API_KEY_ENV_VAR_NAME
from .openapi_client import (
    ApiClient,
    Configuration,
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
        project_id: str,
        input_text: str | None = None,
        input_file_path: Path | str | None = None,
    ) -> InferenceResponse:
        """
        Send an inference request to the API for either a text or a file input.

        TODO offer some way to infer by creating a project and deleting it on the fly?

        :param project_id: id of the associated project.
        :param input_text: text input as a string.
        :param input_file_path: path to the file to send to the API.
        :return: the API response.
        """
        if (input_text is None) ^ input_file_path is not None:
            msg = (
                "An input has to be provided with either the `input_text` or"
                "`input_file_path` argument."
            )
            raise ValueError(msg)

        # Infer with text input
        if input_text is not None:
            return self.post_api_projects_projectid_infer_text(
                project_id, TextRequest(text=input_text)
            )

        # Infer with file input
        if not isinstance(input_file_path, Path):
            input_file_path = Path(input_file_path)
        with input_file_path.open("rb") as file:
            intput_file = file.read()
        return self.post_api_projects_projectid_infer_file(
            project_id, input_file_path.name, intput_file
        )
