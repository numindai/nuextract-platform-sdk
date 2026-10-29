# numind.openapi_client.LocalizationApi

All URIs are relative to *https://nuextract.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_api_localization_jobs_localizationjobid**](LocalizationApi.md#get_api_localization_jobs_localizationjobid) | **GET** /api/localization/jobs/{localizationJobId} | 
[**post_api_localization_jobs_from_extraction_sourcejobid**](LocalizationApi.md#post_api_localization_jobs_from_extraction_sourcejobid) | **POST** /api/localization/jobs/from-extraction/{sourceJobId} | 


# **get_api_localization_jobs_localizationjobid**
> LocalizationResponse get_api_localization_jobs_localizationjobid(localization_job_id, x_organization_id=x_organization_id)


Retrieve the result of a completed localization job.

The result follows the extraction's structure, with lists of `{page, bbox}` objects at leaves.
`page` is a one-based document page number.
`bbox` contains normalized `[x1, y1, x2, y2]` coordinates (0–1).

Returns `200 OK` for a complete result or `206 Partial Content` with all available boxes,
`discardedLocalizations` and `diagnostics` explaining any partial result.
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

# **post_api_localization_jobs_from_extraction_sourcejobid**
> JobIdResponse post_api_localization_jobs_from_extraction_sourcejobid(source_job_id, x_organization_id=x_organization_id, low_priority=low_priority)


Start localization inference from a completed structured extraction job, with or without a project.
The extraction must have no partial error, and its document must contain image pages.
Uses the source job's temperature, maxOutputTokens, loopDetection and randomSeed settings.

Returns a `jobId`. Poll GET `/api/jobs/{jobId}/status`, then retrieve the completed result
with GET `/api/localization/jobs/{jobId}`.
    

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
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
    source_job_id = "source_job_id_example"  # str |
    x_organization_id = "x_organization_id_example"  # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)
    low_priority = False  # bool | Submit this job with lower scheduling priority in the job queue and inference engine. (optional) (default to False)

    try:
        api_response = (
            api_instance.post_api_localization_jobs_from_extraction_sourcejobid(
                source_job_id,
                x_organization_id=x_organization_id,
                low_priority=low_priority,
            )
        )
        print(
            "The response of LocalizationApi->post_api_localization_jobs_from_extraction_sourcejobid:\n"
        )
        pprint(api_response)
    except Exception as e:
        print(
            "Exception when calling LocalizationApi->post_api_localization_jobs_from_extraction_sourcejobid: %s\n"
            % e
        )
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **source_job_id** | **str**|  | 
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 
 **low_priority** | **bool**| Submit this job with lower scheduling priority in the job queue and inference engine. | [optional] [default to False]

### Return type

[**JobIdResponse**](JobIdResponse.md)

### Authorization

[oauth2Auth](../README.md#oauth2Auth)

### HTTP request headers

 - **Content-Type**: Not defined
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

