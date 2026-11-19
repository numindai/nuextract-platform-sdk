"""
NuExtract Platform

 NB: you can also interact with this API via the [Python SDK](https://github.com/numindai/nuextract-platform-sdk).  ## Extracting Information from Documents  Once your structured extraction project is ready, submit a document to the endpoint:  `https://nuextract.ai/api/structured-extraction/{structuredProjectId}/jobs`  To use it, you need:  - To create an API key in the [Account section](https://nuextract.ai/app/user?content=api) - To replace `{structuredProjectId}` by the project ID found in the API tab of the structured extraction project  This endpoint creates an asynchronous extraction job. Use the returned `jobId` to retrieve the result from:  `https://nuextract.ai/api/structured-extraction/jobs/{structuredExtractionJobId}`  You can test your extraction endpoint in your terminal using this command-line example with curl (make sure that you replace values of `STRUCTURED_PROJECT_ID` and `NUEXTRACT_API_KEY`):  ```bash NUEXTRACT_API_KEY=\"_your_api_key_here_\"; \\ STRUCTURED_PROJECT_ID=\"a24fd84a-44ab-4fd4-95a9-bebd46e4768b\"; \\ JOB_ID=$(curl \"https://nuextract.ai/api/structured-extraction/${STRUCTURED_PROJECT_ID}/jobs\" \\   -X POST \\   -H \"Authorization: Bearer ${NUEXTRACT_API_KEY}\" \\   -F \"file=@${FILE_NAME}\" | jq -r '.jobId')  curl \"https://nuextract.ai/api/structured-extraction/jobs/${JOB_ID}\" \\   -H \"Authorization: Bearer ${NUEXTRACT_API_KEY}\" ```  You can also use the [Python SDK](https://github.com/numindai/nuextract-platform-sdk#documentation), by replacing the `project_id`, `api_key` and request values in the following code:  ```python import asyncio from numind import NuMindAsync  client = NuMindAsync(api_key=api_key) requests = [{}]  async def main():     return [         await client.extract_structured_data(project_id, **request_kwargs)         for request_kwargs in requests     ]  responses = asyncio.run(main()) ```  ## Using the Platform via API  Everything you can do on the web platform can be done via API -  check the [user guide](https://www.notion.so/User-Guide-17c16b1df8c580d3a579ebfb24ddbea7?pvs=21) to learn about how the platform works.  This can be useful to create projects automatically, or to make your production more robust for example.  ### Main resources  - **Structured Extraction Project** - user project for structured extraction, identified by `structuredProjectId` - **Content Extraction Project** - user project for content extraction, identified by `contentProjectId` - **File** - uploaded file,  identified by `fileId`, stored up to two weeks if not tied to an **Example** - **Document** - internal representation of a document, identified by `documentId`, created from a File, stored up to two weeks if not tied to an Example - **Example** - document-extraction pair given to teach NuExtract, identified by `structuredExampleId`, created from a Document - **Job** - asynchronous extraction task, identified by `structuredExtractionJobId`  ### Most common API operations  #### Structured extraction  - Creating a **Structured Extraction Project** via `POST /api/structured-extraction` - Changing the template of a **Structured Extraction Project** via `PATCH /api/structured-extraction/{structuredProjectId}` - Changing settings of a **Structured Extraction Project** via `PATCH /api/structured-extraction/{structuredProjectId}/settings` - Uploading a file to a **File** via `POST /api/files` (up to 2 weeks storage) - Starting a structured extraction **Job** via `POST /api/structured-extraction/{structuredProjectId}/jobs` - Reading a structured extraction **Job** result via `GET /api/structured-extraction/jobs/{structuredExtractionJobId}` - Starting a localization **Job** from a completed structured extraction via `POST /api/localization/jobs/from-extraction/{sourceJobId}` - Starting a localization **Job** from a document and extraction JSON via `POST /api/localization/jobs/document/{documentId}` - Starting a localization **Job** from an uploaded file and extraction JSON via multipart `POST /api/localization/jobs` - Reading localization via `GET /api/localization/jobs/{localizationJobId}` (check progress with `GET /api/jobs/{localizationJobId}/status`) - Adding an **Example** to a **Structured Extraction Project** via `POST /api/structured-extraction/{structuredProjectId}/examples`  #### Content extraction  - Creating a **Content Extraction Project** via `POST /api/content-extraction` - Changing settings of a **Content Extraction Project** via `PATCH /api/content-extraction/{contentProjectId}/settings` - Uploading a file to a **File** via `POST /api/files` (up to 2 weeks storage) - Starting a content extraction **Job** via `POST /api/content-extraction/jobs` - Reading a content extraction **Job** result via `GET /api/content-extraction/jobs/{contentExtractionJobId}`  ## Testing with a temporary authorization  This documentation allows you to directly test the API. From the [platform API reference](https://nuextract.ai/doc), requests use your session automatically. Otherwise, click on \"Authorize\", then on \"Authorize\" under `oauth2Auth`, and sign in. You can then open an API endpoint, e.g. `POST /api/structured-extraction/{structuredProjectId}/jobs`, press “Try it out”, fill out the body, and press “Execute” to start a job.

The version of the OpenAPI document:
Generated by OpenAPI Generator (https://openapi-generator.tech)

Do not edit the class manually.
"""  # noqa: E501

from typing import Annotated, Any, Dict, List, Optional, Tuple, Union

from pydantic import (
    Field,
    StrictBool,
    StrictBytes,
    StrictFloat,
    StrictInt,
    StrictStr,
    validate_call,
)

from numind.api_response import ApiResponse
from numind.models.content_project_settings_response_image_width import (
    ContentProjectSettingsResponseImageWidth,
)
from numind.models.content_project_settings_response_rasterization_dpi import (
    ContentProjectSettingsResponseRasterizationDPI,
)
from numind.models.job_id_response import JobIdResponse
from numind.models.localization_response import LocalizationResponse
from numind.openapi_client_async.api_client import ApiClient, RequestSerialized
from numind.openapi_client_async.rest import RESTResponseType


class LocalizationApi:
    """
    NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client

    @validate_call
    async def get_api_localization_jobs_localizationjobid(
        self,
        localization_job_id: StrictStr,
        x_organization_id: Annotated[
            Optional[StrictStr],
            Field(
                description="Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key."
            ),
        ] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]
            ],
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> LocalizationResponse:
        """
        get_api_localization_jobs_localizationjobid

         Retrieve the result of a completed localization job.  The result follows the extraction's structure, with lists of `{page, bbox}` objects at leaves. `page` is a one-based document page number. `bbox` contains normalized `[x1, y1, x2, y2]` coordinates (0–1).  Returns `200 OK` for a complete result or `206 Partial Content` with all available boxes, `discardedLocalizationItems` and `diagnostics` explaining any partial result. `400 JobNotCompleted` if pending or running; `403 QuotaExceeded` if the job failed its quota check.

        :param localization_job_id: (required)
        :type localization_job_id: str
        :param x_organization_id: Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key.
        :type x_organization_id: str
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """  # noqa: E501
        _param = self._get_api_localization_jobs_localizationjobid_serialize(
            localization_job_id=localization_job_id,
            x_organization_id=x_organization_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

        _response_types_map: Dict[str, Optional[str]] = {
            "200": "LocalizationResponse",
            "206": "LocalizationResponse",
            "400": "Error",
            "401": "Error",
            "403": "Error",
            "404": "Error",
            "409": "Error",
            "429": "Error",
            "500": "Error",
        }
        response_data = await self.api_client.call_api(
            *_param, _request_timeout=_request_timeout
        )
        await response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        ).data

    @validate_call
    async def get_api_localization_jobs_localizationjobid_with_http_info(
        self,
        localization_job_id: StrictStr,
        x_organization_id: Annotated[
            Optional[StrictStr],
            Field(
                description="Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key."
            ),
        ] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]
            ],
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> ApiResponse[LocalizationResponse]:
        """
        get_api_localization_jobs_localizationjobid

         Retrieve the result of a completed localization job.  The result follows the extraction's structure, with lists of `{page, bbox}` objects at leaves. `page` is a one-based document page number. `bbox` contains normalized `[x1, y1, x2, y2]` coordinates (0–1).  Returns `200 OK` for a complete result or `206 Partial Content` with all available boxes, `discardedLocalizationItems` and `diagnostics` explaining any partial result. `400 JobNotCompleted` if pending or running; `403 QuotaExceeded` if the job failed its quota check.

        :param localization_job_id: (required)
        :type localization_job_id: str
        :param x_organization_id: Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key.
        :type x_organization_id: str
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """  # noqa: E501
        _param = self._get_api_localization_jobs_localizationjobid_serialize(
            localization_job_id=localization_job_id,
            x_organization_id=x_organization_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

        _response_types_map: Dict[str, Optional[str]] = {
            "200": "LocalizationResponse",
            "206": "LocalizationResponse",
            "400": "Error",
            "401": "Error",
            "403": "Error",
            "404": "Error",
            "409": "Error",
            "429": "Error",
            "500": "Error",
        }
        response_data = await self.api_client.call_api(
            *_param, _request_timeout=_request_timeout
        )
        await response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        )

    @validate_call
    async def get_api_localization_jobs_localizationjobid_without_preload_content(
        self,
        localization_job_id: StrictStr,
        x_organization_id: Annotated[
            Optional[StrictStr],
            Field(
                description="Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key."
            ),
        ] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]
            ],
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> RESTResponseType:
        """
        get_api_localization_jobs_localizationjobid

         Retrieve the result of a completed localization job.  The result follows the extraction's structure, with lists of `{page, bbox}` objects at leaves. `page` is a one-based document page number. `bbox` contains normalized `[x1, y1, x2, y2]` coordinates (0–1).  Returns `200 OK` for a complete result or `206 Partial Content` with all available boxes, `discardedLocalizationItems` and `diagnostics` explaining any partial result. `400 JobNotCompleted` if pending or running; `403 QuotaExceeded` if the job failed its quota check.

        :param localization_job_id: (required)
        :type localization_job_id: str
        :param x_organization_id: Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key.
        :type x_organization_id: str
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """  # noqa: E501
        _param = self._get_api_localization_jobs_localizationjobid_serialize(
            localization_job_id=localization_job_id,
            x_organization_id=x_organization_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

        _response_types_map: Dict[str, Optional[str]] = {
            "200": "LocalizationResponse",
            "206": "LocalizationResponse",
            "400": "Error",
            "401": "Error",
            "403": "Error",
            "404": "Error",
            "409": "Error",
            "429": "Error",
            "500": "Error",
        }
        response_data = await self.api_client.call_api(
            *_param, _request_timeout=_request_timeout
        )
        return response_data.response

    def _get_api_localization_jobs_localizationjobid_serialize(
        self,
        localization_job_id,
        x_organization_id,
        _request_auth,
        _content_type,
        _headers,
        _host_index,
    ) -> RequestSerialized:

        _host = None

        _collection_formats: Dict[str, str] = {}

        _path_params: Dict[str, str] = {}
        _query_params: List[Tuple[str, str]] = []
        _header_params: Dict[str, Any] = self.api_client._merge_headers(_headers)
        _form_params: List[Tuple[str, str]] = []
        _files: Dict[
            str, Union[str, bytes, List[str], List[bytes], List[Tuple[str, bytes]]]
        ] = {}
        _body_params: Optional[bytes] = None

        # process the path parameters
        if localization_job_id is not None:
            _path_params["localizationJobId"] = localization_job_id
        # process the query parameters
        # process the header parameters
        if x_organization_id is not None:
            self.api_client._set_header(
                _header_params, "x-organization-id", x_organization_id
            )
        # process the form parameters
        # process the body parameter

        # set the HTTP header `Accept`
        if not any(key.lower() == "accept" for key in _header_params):
            _header_params["Accept"] = self.api_client.select_header_accept(
                ["application/json"]
            )

        # authentication setting
        _auth_settings: List[str] = ["oauth2Auth"]

        return self.api_client.param_serialize(
            method="GET",
            resource_path="/api/localization/jobs/{localizationJobId}",
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            auth_settings=_auth_settings,
            collection_formats=_collection_formats,
            _host=_host,
            _request_auth=_request_auth,
        )

    @validate_call
    async def post_api_localization_jobs(
        self,
        file: Annotated[
            Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]],
            Field(description="File to convert into a document with image pages."),
        ],
        parameters: Annotated[
            Any,
            Field(
                description="JSON part containing a non-empty extraction object and optional localization settings."
            ),
        ],
        x_organization_id: Annotated[
            Optional[StrictStr],
            Field(
                description="Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key."
            ),
        ] = None,
        timeout: Annotated[
            Optional[StrictStr],
            Field(
                description="Execution timeout for the async inference job. If omitted, the server default of 60m is used.   If provided below the server-configured minimum (5m by default), the effective timeout is clamped to that minimum.   Format examples: 1000ms, 10s, 1m, 1h"
            ),
        ] = None,
        low_priority: Annotated[
            Optional[StrictBool],
            Field(
                description="Submit this job with lower scheduling priority in the job queue and inference engine."
            ),
        ] = None,
        rasterization_dpi: Optional[
            ContentProjectSettingsResponseRasterizationDPI
        ] = None,
        image_width: Optional[ContentProjectSettingsResponseImageWidth] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]
            ],
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> JobIdResponse:
        """
        post_api_localization_jobs

         Start an asynchronous localization job, without a project, from an uploaded file and a supplied extraction. The model locates each value of the extraction in the file pages and returns `{page, bbox}` boxes. The file is converted into a document with image pages before the response is returned.  This endpoint uses `multipart/form-data`. The multipart body must contain:   - `file`: the file to localize in  - `parameters`: a JSON part containing the extraction and optional localization settings described below  Optional multipart parts control the conversion: `rasterizationDPI` (default `automatic`) controls PDF/document rasterization: Resolution used to convert formatted documents (PDFs, etc.) to images, in dots per inch. Use 'automatic' or an integer between 1 and 600. Numeric strings are also accepted. Ignored for files that are already images or text. `imageWidth` (default `automatic`) controls standalone images: Original standalone images only (not PDF/TIFF or converted pages). Use automatic for a 1920 px short side, original to preserve the upload, or a positive integer for the upright image width in pixels. Aspect ratio is preserved; upscaling is allowed.  #### Request JSON: ```json {   \"extraction\": {     \"invoiceNumber\": \"INV-001\",     \"vendor\": \"ACME Corp\",     \"total\": \"120 €\"   },   \"settings\": {     \"temperature\": 0.2,     \"maxOutputTokens\": \"2048\",     \"loopDetection\": true,     \"randomSeed\": \"42\"   } } ```  #### Fields: `extraction` is required: a non-empty JSON object, usually the result of a structured extraction on the same document. An empty extraction is rejected with `400 Bad Request`.  `settings` is optional. Supported keys are `temperature`, `maxOutputTokens`, `loopDetection` and `randomSeed`. Omitted settings use the defaults: temperature 0.2, `maxOutputTokens` `\"120000\"` (`\"Unlimited\"` for no limit), loop detection enabled, and `randomSeed` `\"2022\"`. `randomSeed` must be a string containing a 64-bit integer or `\"random\"`.  #### cURL Example: ```bash curl -X POST \"$BASE_URL/api/localization/jobs\" \\   -H \"Authorization: Bearer $TOKEN\" \\   -F 'file=@invoice.pdf;type=application/pdf' \\   -F 'parameters=@parameters.json;type=application/json' \\   -F 'rasterizationDPI=200' \\   -F 'imageWidth=1600' ```  #### Error Responses: `400 Bad Request` - If the extraction is empty, the `parameters` part is not valid JSON, or the file cannot be converted into image pages.  `403 Forbidden` - If localization is disabled for this instance.  #### Response: Returns a JSON containing the job ID, for example `{\"jobId\": \"...\"}`. Poll GET `/api/jobs/{jobId}/status`, then retrieve the completed result with GET `/api/localization/jobs/{jobId}`. The billing quota is checked when the job runs, not when it is created.

        :param file: File to convert into a document with image pages. (required)
        :type file: bytes
        :param parameters: JSON part containing a non-empty extraction object and optional localization settings. (required)
        :type parameters: LocalizationParameters
        :param x_organization_id: Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key.
        :type x_organization_id: str
        :param timeout: Execution timeout for the async inference job. If omitted, the server default of 60m is used.   If provided below the server-configured minimum (5m by default), the effective timeout is clamped to that minimum.   Format examples: 1000ms, 10s, 1m, 1h
        :type timeout: str
        :param low_priority: Submit this job with lower scheduling priority in the job queue and inference engine.
        :type low_priority: bool
        :param rasterization_dpi:
        :type rasterization_dpi: ContentProjectSettingsResponseRasterizationDPI
        :param image_width:
        :type image_width: ContentProjectSettingsResponseImageWidth
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """  # noqa: E501
        _param = self._post_api_localization_jobs_serialize(
            file=file,
            parameters=parameters,
            x_organization_id=x_organization_id,
            timeout=timeout,
            low_priority=low_priority,
            rasterization_dpi=rasterization_dpi,
            image_width=image_width,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

        _response_types_map: Dict[str, Optional[str]] = {
            "200": "JobIdResponse",
            "400": "Error",
            "401": "Error",
            "403": "Error",
            "404": "Error",
            "500": "Error",
        }
        response_data = await self.api_client.call_api(
            *_param, _request_timeout=_request_timeout
        )
        await response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        ).data

    @validate_call
    async def post_api_localization_jobs_with_http_info(
        self,
        file: Annotated[
            Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]],
            Field(description="File to convert into a document with image pages."),
        ],
        parameters: Annotated[
            Any,
            Field(
                description="JSON part containing a non-empty extraction object and optional localization settings."
            ),
        ],
        x_organization_id: Annotated[
            Optional[StrictStr],
            Field(
                description="Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key."
            ),
        ] = None,
        timeout: Annotated[
            Optional[StrictStr],
            Field(
                description="Execution timeout for the async inference job. If omitted, the server default of 60m is used.   If provided below the server-configured minimum (5m by default), the effective timeout is clamped to that minimum.   Format examples: 1000ms, 10s, 1m, 1h"
            ),
        ] = None,
        low_priority: Annotated[
            Optional[StrictBool],
            Field(
                description="Submit this job with lower scheduling priority in the job queue and inference engine."
            ),
        ] = None,
        rasterization_dpi: Optional[
            ContentProjectSettingsResponseRasterizationDPI
        ] = None,
        image_width: Optional[ContentProjectSettingsResponseImageWidth] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]
            ],
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> ApiResponse[JobIdResponse]:
        """
        post_api_localization_jobs

         Start an asynchronous localization job, without a project, from an uploaded file and a supplied extraction. The model locates each value of the extraction in the file pages and returns `{page, bbox}` boxes. The file is converted into a document with image pages before the response is returned.  This endpoint uses `multipart/form-data`. The multipart body must contain:   - `file`: the file to localize in  - `parameters`: a JSON part containing the extraction and optional localization settings described below  Optional multipart parts control the conversion: `rasterizationDPI` (default `automatic`) controls PDF/document rasterization: Resolution used to convert formatted documents (PDFs, etc.) to images, in dots per inch. Use 'automatic' or an integer between 1 and 600. Numeric strings are also accepted. Ignored for files that are already images or text. `imageWidth` (default `automatic`) controls standalone images: Original standalone images only (not PDF/TIFF or converted pages). Use automatic for a 1920 px short side, original to preserve the upload, or a positive integer for the upright image width in pixels. Aspect ratio is preserved; upscaling is allowed.  #### Request JSON: ```json {   \"extraction\": {     \"invoiceNumber\": \"INV-001\",     \"vendor\": \"ACME Corp\",     \"total\": \"120 €\"   },   \"settings\": {     \"temperature\": 0.2,     \"maxOutputTokens\": \"2048\",     \"loopDetection\": true,     \"randomSeed\": \"42\"   } } ```  #### Fields: `extraction` is required: a non-empty JSON object, usually the result of a structured extraction on the same document. An empty extraction is rejected with `400 Bad Request`.  `settings` is optional. Supported keys are `temperature`, `maxOutputTokens`, `loopDetection` and `randomSeed`. Omitted settings use the defaults: temperature 0.2, `maxOutputTokens` `\"120000\"` (`\"Unlimited\"` for no limit), loop detection enabled, and `randomSeed` `\"2022\"`. `randomSeed` must be a string containing a 64-bit integer or `\"random\"`.  #### cURL Example: ```bash curl -X POST \"$BASE_URL/api/localization/jobs\" \\   -H \"Authorization: Bearer $TOKEN\" \\   -F 'file=@invoice.pdf;type=application/pdf' \\   -F 'parameters=@parameters.json;type=application/json' \\   -F 'rasterizationDPI=200' \\   -F 'imageWidth=1600' ```  #### Error Responses: `400 Bad Request` - If the extraction is empty, the `parameters` part is not valid JSON, or the file cannot be converted into image pages.  `403 Forbidden` - If localization is disabled for this instance.  #### Response: Returns a JSON containing the job ID, for example `{\"jobId\": \"...\"}`. Poll GET `/api/jobs/{jobId}/status`, then retrieve the completed result with GET `/api/localization/jobs/{jobId}`. The billing quota is checked when the job runs, not when it is created.

        :param file: File to convert into a document with image pages. (required)
        :type file: bytes
        :param parameters: JSON part containing a non-empty extraction object and optional localization settings. (required)
        :type parameters: LocalizationParameters
        :param x_organization_id: Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key.
        :type x_organization_id: str
        :param timeout: Execution timeout for the async inference job. If omitted, the server default of 60m is used.   If provided below the server-configured minimum (5m by default), the effective timeout is clamped to that minimum.   Format examples: 1000ms, 10s, 1m, 1h
        :type timeout: str
        :param low_priority: Submit this job with lower scheduling priority in the job queue and inference engine.
        :type low_priority: bool
        :param rasterization_dpi:
        :type rasterization_dpi: ContentProjectSettingsResponseRasterizationDPI
        :param image_width:
        :type image_width: ContentProjectSettingsResponseImageWidth
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """  # noqa: E501
        _param = self._post_api_localization_jobs_serialize(
            file=file,
            parameters=parameters,
            x_organization_id=x_organization_id,
            timeout=timeout,
            low_priority=low_priority,
            rasterization_dpi=rasterization_dpi,
            image_width=image_width,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

        _response_types_map: Dict[str, Optional[str]] = {
            "200": "JobIdResponse",
            "400": "Error",
            "401": "Error",
            "403": "Error",
            "404": "Error",
            "500": "Error",
        }
        response_data = await self.api_client.call_api(
            *_param, _request_timeout=_request_timeout
        )
        await response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        )

    @validate_call
    async def post_api_localization_jobs_without_preload_content(
        self,
        file: Annotated[
            Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]],
            Field(description="File to convert into a document with image pages."),
        ],
        parameters: Annotated[
            Any,
            Field(
                description="JSON part containing a non-empty extraction object and optional localization settings."
            ),
        ],
        x_organization_id: Annotated[
            Optional[StrictStr],
            Field(
                description="Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key."
            ),
        ] = None,
        timeout: Annotated[
            Optional[StrictStr],
            Field(
                description="Execution timeout for the async inference job. If omitted, the server default of 60m is used.   If provided below the server-configured minimum (5m by default), the effective timeout is clamped to that minimum.   Format examples: 1000ms, 10s, 1m, 1h"
            ),
        ] = None,
        low_priority: Annotated[
            Optional[StrictBool],
            Field(
                description="Submit this job with lower scheduling priority in the job queue and inference engine."
            ),
        ] = None,
        rasterization_dpi: Optional[
            ContentProjectSettingsResponseRasterizationDPI
        ] = None,
        image_width: Optional[ContentProjectSettingsResponseImageWidth] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]
            ],
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> RESTResponseType:
        """
        post_api_localization_jobs

         Start an asynchronous localization job, without a project, from an uploaded file and a supplied extraction. The model locates each value of the extraction in the file pages and returns `{page, bbox}` boxes. The file is converted into a document with image pages before the response is returned.  This endpoint uses `multipart/form-data`. The multipart body must contain:   - `file`: the file to localize in  - `parameters`: a JSON part containing the extraction and optional localization settings described below  Optional multipart parts control the conversion: `rasterizationDPI` (default `automatic`) controls PDF/document rasterization: Resolution used to convert formatted documents (PDFs, etc.) to images, in dots per inch. Use 'automatic' or an integer between 1 and 600. Numeric strings are also accepted. Ignored for files that are already images or text. `imageWidth` (default `automatic`) controls standalone images: Original standalone images only (not PDF/TIFF or converted pages). Use automatic for a 1920 px short side, original to preserve the upload, or a positive integer for the upright image width in pixels. Aspect ratio is preserved; upscaling is allowed.  #### Request JSON: ```json {   \"extraction\": {     \"invoiceNumber\": \"INV-001\",     \"vendor\": \"ACME Corp\",     \"total\": \"120 €\"   },   \"settings\": {     \"temperature\": 0.2,     \"maxOutputTokens\": \"2048\",     \"loopDetection\": true,     \"randomSeed\": \"42\"   } } ```  #### Fields: `extraction` is required: a non-empty JSON object, usually the result of a structured extraction on the same document. An empty extraction is rejected with `400 Bad Request`.  `settings` is optional. Supported keys are `temperature`, `maxOutputTokens`, `loopDetection` and `randomSeed`. Omitted settings use the defaults: temperature 0.2, `maxOutputTokens` `\"120000\"` (`\"Unlimited\"` for no limit), loop detection enabled, and `randomSeed` `\"2022\"`. `randomSeed` must be a string containing a 64-bit integer or `\"random\"`.  #### cURL Example: ```bash curl -X POST \"$BASE_URL/api/localization/jobs\" \\   -H \"Authorization: Bearer $TOKEN\" \\   -F 'file=@invoice.pdf;type=application/pdf' \\   -F 'parameters=@parameters.json;type=application/json' \\   -F 'rasterizationDPI=200' \\   -F 'imageWidth=1600' ```  #### Error Responses: `400 Bad Request` - If the extraction is empty, the `parameters` part is not valid JSON, or the file cannot be converted into image pages.  `403 Forbidden` - If localization is disabled for this instance.  #### Response: Returns a JSON containing the job ID, for example `{\"jobId\": \"...\"}`. Poll GET `/api/jobs/{jobId}/status`, then retrieve the completed result with GET `/api/localization/jobs/{jobId}`. The billing quota is checked when the job runs, not when it is created.

        :param file: File to convert into a document with image pages. (required)
        :type file: bytes
        :param parameters: JSON part containing a non-empty extraction object and optional localization settings. (required)
        :type parameters: LocalizationParameters
        :param x_organization_id: Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key.
        :type x_organization_id: str
        :param timeout: Execution timeout for the async inference job. If omitted, the server default of 60m is used.   If provided below the server-configured minimum (5m by default), the effective timeout is clamped to that minimum.   Format examples: 1000ms, 10s, 1m, 1h
        :type timeout: str
        :param low_priority: Submit this job with lower scheduling priority in the job queue and inference engine.
        :type low_priority: bool
        :param rasterization_dpi:
        :type rasterization_dpi: ContentProjectSettingsResponseRasterizationDPI
        :param image_width:
        :type image_width: ContentProjectSettingsResponseImageWidth
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """  # noqa: E501
        _param = self._post_api_localization_jobs_serialize(
            file=file,
            parameters=parameters,
            x_organization_id=x_organization_id,
            timeout=timeout,
            low_priority=low_priority,
            rasterization_dpi=rasterization_dpi,
            image_width=image_width,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

        _response_types_map: Dict[str, Optional[str]] = {
            "200": "JobIdResponse",
            "400": "Error",
            "401": "Error",
            "403": "Error",
            "404": "Error",
            "500": "Error",
        }
        response_data = await self.api_client.call_api(
            *_param, _request_timeout=_request_timeout
        )
        return response_data.response

    def _post_api_localization_jobs_serialize(
        self,
        file,
        parameters,
        x_organization_id,
        timeout,
        low_priority,
        rasterization_dpi,
        image_width,
        _request_auth,
        _content_type,
        _headers,
        _host_index,
    ) -> RequestSerialized:

        _host = None

        _collection_formats: Dict[str, str] = {}

        _path_params: Dict[str, str] = {}
        _query_params: List[Tuple[str, str]] = []
        _header_params: Dict[str, Any] = self.api_client._merge_headers(_headers)
        _form_params: List[Tuple[str, str]] = []
        _files: Dict[
            str, Union[str, bytes, List[str], List[bytes], List[Tuple[str, bytes]]]
        ] = {}
        _body_params: Optional[bytes] = None

        # process the path parameters
        # process the query parameters
        if timeout is not None:
            _query_params.append(("timeout", timeout))

        if low_priority is not None:
            _query_params.append(("lowPriority", low_priority))

        # process the header parameters
        if x_organization_id is not None:
            self.api_client._set_header(
                _header_params, "x-organization-id", x_organization_id
            )
        # process the form parameters
        if file is not None:
            _files["file"] = file
        if parameters is not None:
            _form_params.append(("parameters", parameters))
        if rasterization_dpi is not None:
            _form_params.append(("rasterizationDPI", rasterization_dpi))
        if image_width is not None:
            _form_params.append(("imageWidth", image_width))
        # process the body parameter

        # set the HTTP header `Accept`
        if not any(key.lower() == "accept" for key in _header_params):
            _header_params["Accept"] = self.api_client.select_header_accept(
                ["application/json"]
            )

        # set the HTTP header `Content-Type`
        if _content_type:
            self.api_client._set_header(_header_params, "Content-Type", _content_type)
        else:
            _default_content_type = self.api_client.select_header_content_type(
                ["multipart/form-data"]
            )
            if _default_content_type is not None:
                self.api_client._set_header(
                    _header_params, "Content-Type", _default_content_type
                )

        # authentication setting
        _auth_settings: List[str] = ["oauth2Auth"]

        return self.api_client.param_serialize(
            method="POST",
            resource_path="/api/localization/jobs",
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            auth_settings=_auth_settings,
            collection_formats=_collection_formats,
            _host=_host,
            _request_auth=_request_auth,
        )
