# numind.openapi_client.JobsApi

All URIs are relative to *https://nuextract.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_api_jobs**](JobsApi.md#get_api_jobs) | **GET** /api/jobs | 
[**get_api_jobs_jobid_status**](JobsApi.md#get_api_jobs_jobid_status) | **GET** /api/jobs/{jobId}/status | 
[**get_api_jobs_jobid_stream**](JobsApi.md#get_api_jobs_jobid_stream) | **GET** /api/jobs/{jobId}/stream | 


# **get_api_jobs**
> PaginatedResponseJobResponse get_api_jobs(organization=organization, skip=skip, per_page=per_page)


 List all jobs for the authenticated user with pagination support.
 This endpoint returns a paginated list of all jobs owned by the current user.

 Each job object contains the same information as returned by the get job endpoint.
   

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.paginated_response_job_response import PaginatedResponseJobResponse
from numind.openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://nuextract.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = numind.openapi_client.Configuration(
    host = "https://nuextract.ai"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
with numind.openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = numind.openapi_client.JobsApi(api_client)
    organization = 'organization_example' # str |  (optional)
    skip = 56 # int | Number of jobs to skip. Min: 0. Default: 0. (optional)
    per_page = 56 # int | Number of jobs per page. Min: 1. Max: 100. Default: 30. (optional)

    try:
        api_response = api_instance.get_api_jobs(organization=organization, skip=skip, per_page=per_page)
        print("The response of JobsApi->get_api_jobs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling JobsApi->get_api_jobs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization** | **str**|  | [optional] 
 **skip** | **int**| Number of jobs to skip. Min: 0. Default: 0. | [optional] 
 **per_page** | **int**| Number of jobs per page. Min: 1. Max: 100. Default: 30. | [optional] 

### Return type

[**PaginatedResponseJobResponse**](PaginatedResponseJobResponse.md)

### Authorization

[oauth2Auth](../README.md#oauth2Auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, text/plain

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**400** | Invalid value for: query parameter skip, Invalid value for: query parameter perPage |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_api_jobs_jobid_status**
> JobStatusResponse get_api_jobs_jobid_status(job_id)


 Get details of a specific job by its unique identifier.
 This endpoint retrieves the metadata about an asynchronous job.

#### Error Responses:
`404 Not Found` - If a job with the specified ID does not exist.

`403 Forbidden` - If the user does not have permission to access this job.
   

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.job_status_response import JobStatusResponse
from numind.openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://nuextract.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = numind.openapi_client.Configuration(
    host = "https://nuextract.ai"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
with numind.openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = numind.openapi_client.JobsApi(api_client)
    job_id = 'job_id_example' # str | Unique job identifier.

    try:
        api_response = api_instance.get_api_jobs_jobid_status(job_id)
        print("The response of JobsApi->get_api_jobs_jobid_status:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling JobsApi->get_api_jobs_jobid_status: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **job_id** | **str**| Unique job identifier. | 

### Return type

[**JobStatusResponse**](JobStatusResponse.md)

### Authorization

[oauth2Auth](../README.md#oauth2Auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_api_jobs_jobid_stream**
> str get_api_jobs_jobid_stream(job_id)


 Stream job result via Server-Sent Events (SSE). This endpoint allows real-time monitoring of job progress and retrieval of results
 as soon as they become available.

 The endpoint uses the SSE protocol to maintain a persistent connection with the client. It will either:
 - Return the job result immediately if the job is already completed
 - Stream the job result when it completes. Send periodic ping events to keep the connection alive.

 The stream will timeout after the job execution timeout if the job doesn't complete within that timeframe.

#### SSE Event Types:
 - **result**: Contains the complete job response data when the job completes (either successfully, or with an error)
 - **ping**: Empty data events sent every 30 seconds to keep the connection alive
 - **error**: Sent when an error occurs (internal error or timeout)

#### Event Format:
 Each SSE event follows this format:
 ```
 event: <event_type>
 data: <JSON data>
 ```

 For **result** events, the data contains the complete JobResponse object (same as returned by the get job endpoint).
 For **error** events, the data contains an error object with code and message fields.
 For **ping** events, the data field is empty.

#### Timeout Behavior:
 If the job doesn't complete within the job execution timeout, the stream will end with an error event containing the code `JobTimeout`.

#### Error Responses:
`404 Not Found` - If a job with the specified ID does not exist.

`403 Forbidden` - If the user does not have permission to access this job or if the user's billing quota is exceeded.
   

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://nuextract.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = numind.openapi_client.Configuration(
    host = "https://nuextract.ai"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
with numind.openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = numind.openapi_client.JobsApi(api_client)
    job_id = 'job_id_example' # str | Unique job identifier.

    try:
        api_response = api_instance.get_api_jobs_jobid_stream(job_id)
        print("The response of JobsApi->get_api_jobs_jobid_stream:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling JobsApi->get_api_jobs_jobid_stream: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **job_id** | **str**| Unique job identifier. | 

### Return type

**str**

### Authorization

[oauth2Auth](../README.md#oauth2Auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/event-stream, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

