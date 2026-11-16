# numind.openapi_client.LocalizationApi

All URIs are relative to *https://nuextract.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_api_localization_jobs_localizationjobid**](LocalizationApi.md#get_api_localization_jobs_localizationjobid) | **GET** /api/localization/jobs/{localizationJobId} | 
[**post_api_localization_jobs**](LocalizationApi.md#post_api_localization_jobs) | **POST** /api/localization/jobs | 


# **get_api_localization_jobs_localizationjobid**
> LocalizationResponse get_api_localization_jobs_localizationjobid(localization_job_id, x_organization_id=x_organization_id)


Retrieve the result of a completed localization job.

The result follows the extraction's structure, with lists of `{page, bbox}` objects at leaves.
`page` is a one-based document page number.
`bbox` contains normalized `[x1, y1, x2, y2]` coordinates (0–1).

Returns `200 OK` for a complete result or `206 Partial Content` with all available boxes,
`discardedLocalizationItems` and `diagnostics` explaining any partial result.
`400 JobNotCompleted` if pending or running; `403 QuotaExceeded` if the job failed its quota check.
    

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.localization_response import LocalizationResponse
from numind.openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://nuextract.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = numind.openapi_client.Configuration(host="https://nuextract.ai")

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
with numind.openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = numind.openapi_client.LocalizationApi(api_client)
    localization_job_id = "localization_job_id_example"  # str |
    x_organization_id = "x_organization_id_example"  # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)

    try:
        api_response = api_instance.get_api_localization_jobs_localizationjobid(
            localization_job_id, x_organization_id=x_organization_id
        )
        print(
            "The response of LocalizationApi->get_api_localization_jobs_localizationjobid:\n"
        )
        pprint(api_response)
    except Exception as e:
        print(
            "Exception when calling LocalizationApi->get_api_localization_jobs_localizationjobid: %s\n"
            % e
        )
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **localization_job_id** | **str**|  | 
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 

### Return type

[**LocalizationResponse**](LocalizationResponse.md)

### Authorization

[oauth2Auth](../README.md#oauth2Auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Job completed successfully. |  -  |
**206** | Job completed with a partial result. |  -  |
**400** | Invalid request or job not completed (JobNotCompleted). |  -  |
**401** | Missing or invalid authentication. |  -  |
**403** | Localization is disabled, access is denied, or quota is exceeded (QuotaExceeded). |  -  |
**404** | Job, project or document not found in the active scope. |  -  |
**409** | Localization job canceled (JobCanceled). |  -  |
**429** | Localization job failed with a rate-limit error. |  -  |
**500** | Localization job failed or timed out (JobTimeout), or its stored result is unreadable. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_api_localization_jobs**
> JobIdResponse post_api_localization_jobs(file, parameters, x_organization_id=x_organization_id, timeout=timeout, low_priority=low_priority, rasterization_dpi=rasterization_dpi, image_width=image_width)


Start an asynchronous localization job, without a project, from an uploaded file and a supplied extraction.
The model locates each value of the extraction in the file pages and returns `{page, bbox}` boxes.
The file is converted into a document with image pages before the response is returned.

This endpoint uses `multipart/form-data`. The multipart body must contain:

 - `file`: the file to localize in
 - `parameters`: a JSON part containing the extraction and optional localization settings described below

Optional multipart parts control the conversion: `rasterizationDPI` (default `automatic`) controls PDF/document rasterization: Resolution used to convert formatted documents (PDFs, etc.) to images, in dots per inch. Use 'automatic' or an integer between 1 and 600. Numeric strings are also accepted. Ignored for files that are already images or text.
`imageWidth` (default `automatic`) controls standalone images: Original standalone images only (not PDF/TIFF or converted pages). Use automatic for a 1280 px short side, original to preserve the upload, or a positive integer for the upright image width in pixels. Aspect ratio is preserved; upscaling is allowed.

#### Request JSON:
```json
{
  "extraction": {
    "invoiceNumber": "INV-001",
    "vendor": "ACME Corp",
    "total": "120 €"
  },
  "settings": {
    "temperature": 0.2,
    "maxOutputTokens": "2048",
    "loopDetection": true,
    "randomSeed": "42"
  }
}
```

#### Fields:
`extraction` is required: a non-empty JSON object, usually the result of a structured extraction on the same document.
An empty extraction is rejected with `400 Bad Request`.

`settings` is optional. Supported keys are `temperature`, `maxOutputTokens`, `loopDetection` and `randomSeed`.
Omitted settings use the defaults: temperature 0.2, `maxOutputTokens` `"120000"`
(`"Unlimited"` for no limit), loop detection enabled, and `randomSeed` `"2022"`.
`randomSeed` must be a string containing a 64-bit integer or `"random"`.

#### cURL Example:
```bash
curl -X POST "$BASE_URL/api/localization/jobs" \
  -H "Authorization: Bearer $TOKEN" \
  -F 'file=@invoice.pdf;type=application/pdf' \
  -F 'parameters=@parameters.json;type=application/json' \
  -F 'rasterizationDPI=200' \
  -F 'imageWidth=1600'
```

#### Error Responses:
`400 Bad Request` - If the extraction is empty, the `parameters` part is not valid JSON, or the file cannot be converted into image pages.

`403 Forbidden` - If localization is disabled for this instance.

#### Response:
Returns a JSON containing the job ID, for example `{"jobId": "..."}`.
Poll GET `/api/jobs/{jobId}/status`, then retrieve the completed result with GET `/api/localization/jobs/{jobId}`.
The billing quota is checked when the job runs, not when it is created.


### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.content_project_settings_response_image_width import (
    ContentProjectSettingsResponseImageWidth,
)
from numind.models.content_project_settings_response_rasterization_dpi import (
    ContentProjectSettingsResponseRasterizationDPI,
)
from numind.models.job_id_response import JobIdResponse
from numind.openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://nuextract.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = numind.openapi_client.Configuration(host="https://nuextract.ai")

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
with numind.openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = numind.openapi_client.LocalizationApi(api_client)
    file = None  # bytes | File to convert into a document with image pages.
    parameters = numind.openapi_client.LocalizationParameters()  # LocalizationParameters | JSON part containing a non-empty extraction object and optional localization settings.
    x_organization_id = "x_organization_id_example"  # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)
    timeout = "timeout_example"  # str | Execution timeout for the async inference job. If omitted, the server default of 60m is used.   If provided below the server-configured minimum (5m by default), the effective timeout is clamped to that minimum.   Format examples: 1000ms, 10s, 1m, 1h (optional)
    low_priority = False  # bool | Submit this job with lower scheduling priority in the job queue and inference engine. (optional) (default to False)
    rasterization_dpi = (
        numind.openapi_client.ContentProjectSettingsResponseRasterizationDPI()
    )  # ContentProjectSettingsResponseRasterizationDPI |  (optional)
    image_width = (
        numind.openapi_client.ContentProjectSettingsResponseImageWidth()
    )  # ContentProjectSettingsResponseImageWidth |  (optional)

    try:
        api_response = api_instance.post_api_localization_jobs(
            file,
            parameters,
            x_organization_id=x_organization_id,
            timeout=timeout,
            low_priority=low_priority,
            rasterization_dpi=rasterization_dpi,
            image_width=image_width,
        )
        print("The response of LocalizationApi->post_api_localization_jobs:\n")
        pprint(api_response)
    except Exception as e:
        print(
            "Exception when calling LocalizationApi->post_api_localization_jobs: %s\n"
            % e
        )
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file** | **bytes**| File to convert into a document with image pages. | 
 **parameters** | [**LocalizationParameters**](LocalizationParameters.md)| JSON part containing a non-empty extraction object and optional localization settings. | 
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 
 **timeout** | **str**| Execution timeout for the async inference job. If omitted, the server default of 60m is used.   If provided below the server-configured minimum (5m by default), the effective timeout is clamped to that minimum.   Format examples: 1000ms, 10s, 1m, 1h | [optional] 
 **low_priority** | **bool**| Submit this job with lower scheduling priority in the job queue and inference engine. | [optional] [default to False]
 **rasterization_dpi** | [**ContentProjectSettingsResponseRasterizationDPI**](ContentProjectSettingsResponseRasterizationDPI.md)|  | [optional] 
 **image_width** | [**ContentProjectSettingsResponseImageWidth**](ContentProjectSettingsResponseImageWidth.md)|  | [optional] 

### Return type

[**JobIdResponse**](JobIdResponse.md)

### Authorization

[oauth2Auth](../README.md#oauth2Auth)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**400** | Invalid request or job not completed (JobNotCompleted). |  -  |
**401** | Missing or invalid authentication. |  -  |
**403** | Localization is disabled or access is denied. |  -  |
**404** | Job, project or document not found in the active scope. |  -  |
**500** | Invalid stored job data or internal error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

