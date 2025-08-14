# numind.openapi_client.JobsApi

All URIs are relative to *https://nuextract.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_api_jobs**](JobsApi.md#get_api_jobs) | **GET** /api/jobs | 
[**get_api_jobs_jobid**](JobsApi.md#get_api_jobs_jobid) | **GET** /api/jobs/{jobId} | 
[**get_api_jobs_jobid_stream**](JobsApi.md#get_api_jobs_jobid_stream) | **GET** /api/jobs/{jobId}/stream | 


# **get_api_jobs**
> List[JobResponse] get_api_jobs(organization=organization)

List all jobs for the authenticated user

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.job_response import JobResponse
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

    try:
        api_response = api_instance.get_api_jobs(organization=organization)
        print("The response of JobsApi->get_api_jobs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling JobsApi->get_api_jobs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization** | **str**|  | [optional] 

### Return type

[**List[JobResponse]**](JobResponse.md)

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

# **get_api_jobs_jobid**
> JobResponse get_api_jobs_jobid(job_id)

Get details of a specific job

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.job_response import JobResponse
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
        api_response = api_instance.get_api_jobs_jobid(job_id)
        print("The response of JobsApi->get_api_jobs_jobid:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling JobsApi->get_api_jobs_jobid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **job_id** | **str**| Unique job identifier. | 

### Return type

[**JobResponse**](JobResponse.md)

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

Stream job result via Server-Sent Events

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

