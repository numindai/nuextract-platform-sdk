"""NuMind client object"""

import os

from .constants import NUMIND_API_KEY_ENV_VAR_NAME
from .openapi_client import ApiClient, Configuration, ReferenceApi


class NuMind(ReferenceApi):
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

    # TODO easy method to auto-route text/image/document to the write method
