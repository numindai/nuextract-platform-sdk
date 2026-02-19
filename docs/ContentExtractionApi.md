# numind.openapi_client.ContentExtractionApi

All URIs are relative to *https://nuextract.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_api_content_extraction_jobs_contentextractionjobid**](ContentExtractionApi.md#get_api_content_extraction_jobs_contentextractionjobid) | **GET** /api/content-extraction/jobs/{contentExtractionJobId} | 
[**post_api_content_extraction_jobs**](ContentExtractionApi.md#post_api_content_extraction_jobs) | **POST** /api/content-extraction/jobs | 


# **get_api_content_extraction_jobs_contentextractionjobid**
> MarkdownResponse get_api_content_extraction_jobs_contentextractionjobid(content_extraction_job_id, x_organization_id=x_organization_id)


 Get content extraction result of a specific job by its unique identifier.

#### Response:
 Returns a markdown string representing the extracted content.

#### Error Responses:
`404 Not Found` - If a content extraction job with the specified ID does not exist.

`403 Forbidden` - If the user does not have permission to access this job.
   

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.markdown_response import MarkdownResponse
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
    api_instance = numind.openapi_client.ContentExtractionApi(api_client)
    content_extraction_job_id = 'content_extraction_job_id_example' # str | Unique content extraction job identifier.
    x_organization_id = 'x_organization_id_example' # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)

    try:
        api_response = api_instance.get_api_content_extraction_jobs_contentextractionjobid(content_extraction_job_id, x_organization_id=x_organization_id)
        print("The response of ContentExtractionApi->get_api_content_extraction_jobs_contentextractionjobid:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ContentExtractionApi->get_api_content_extraction_jobs_contentextractionjobid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **content_extraction_job_id** | **str**| Unique content extraction job identifier. | 
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 

### Return type

[**MarkdownResponse**](MarkdownResponse.md)

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

# **post_api_content_extraction_jobs**
> JobIdResponse post_api_content_extraction_jobs(file, x_organization_id=x_organization_id, temperature=temperature, rasterization_dpi=rasterization_dpi, max_output_tokens=max_output_tokens, timeout=timeout)


 Extract markdown from the provided file using NuMarkdown model as an async job.
 The response contains an extracted markdown together with the reasoning trace.
 The model only accepts images. Therefore, some files are converted to images -
 the **rasterizationDPI** parameter controls their resolution.


#### Response:
 Returns a JSON containing the job ID that can be used to retrieve the job status and results.

 If the job is completed successfully, the job's output data will contain a JSON representing the inference result.
 The ***result*** field contains the extracted markdown. The ***thinking*** field contains the reasoning trace.
 If one of the fields ***result*** or ***thinking*** is empty, the ***rawResponse*** field contains the raw model output.
 and an HTTP code 206 is returned.
    

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.job_id_response import JobIdResponse
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
    api_instance = numind.openapi_client.ContentExtractionApi(api_client)
    file = None # bytearray | 
    x_organization_id = 'x_organization_id_example' # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)
    temperature = 3.4 # float | Model temperature (optional). Controls output diversity.  Ranges between 0 and 1. If not specified, the default value 0.0 is used. (optional)
    rasterization_dpi = 56 # int | Resolution used to convert formatted documents (PDFs, etc.) to images, in dot per inch (optional).   Ranges between 1 and 300. If not specified, the default value 170 dpi is used. (optional)
    max_output_tokens = 56 # int | Maximum number of output tokens (optional). Must be positive. Set to 0 for no limit by default. (optional)
    timeout = 'timeout_example' # str | Max time to wait for the processing completion.   Format examples: 1000ms, 10s, 1m, 1h (optional)

    try:
        api_response = api_instance.post_api_content_extraction_jobs(file, x_organization_id=x_organization_id, temperature=temperature, rasterization_dpi=rasterization_dpi, max_output_tokens=max_output_tokens, timeout=timeout)
        print("The response of ContentExtractionApi->post_api_content_extraction_jobs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ContentExtractionApi->post_api_content_extraction_jobs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file** | **bytearray**|  | 
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 
 **temperature** | **float**| Model temperature (optional). Controls output diversity.  Ranges between 0 and 1. If not specified, the default value 0.0 is used. | [optional] 
 **rasterization_dpi** | **int**| Resolution used to convert formatted documents (PDFs, etc.) to images, in dot per inch (optional).   Ranges between 1 and 300. If not specified, the default value 170 dpi is used. | [optional] 
 **max_output_tokens** | **int**| Maximum number of output tokens (optional). Must be positive. Set to 0 for no limit by default. | [optional] 
 **timeout** | **str**| Max time to wait for the processing completion.   Format examples: 1000ms, 10s, 1m, 1h | [optional] 

### Return type

[**JobIdResponse**](JobIdResponse.md)

### Authorization

[oauth2Auth](../README.md#oauth2Auth)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json, text/plain

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**400** | Invalid value for: query parameter temperature, Invalid value for: query parameter rasterizationDPI, Invalid value for: query parameter maxOutputTokens, Invalid value for: body |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

