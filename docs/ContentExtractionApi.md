# numind.openapi_client.ContentExtractionApi

All URIs are relative to *https://nuextract.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_api_content_extraction_jobs_contentextractionjobid**](ContentExtractionApi.md#get_api_content_extraction_jobs_contentextractionjobid) | **GET** /api/content-extraction/jobs/{contentExtractionJobId} | 
[**post_api_content_extraction_jobs**](ContentExtractionApi.md#post_api_content_extraction_jobs) | **POST** /api/content-extraction/jobs | 


# **get_api_content_extraction_jobs_contentextractionjobid**
> ContentExtractionResponse get_api_content_extraction_jobs_contentextractionjobid(content_extraction_job_id, x_organization_id=x_organization_id)


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
from numind.models.content_extraction_response import ContentExtractionResponse
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

[**ContentExtractionResponse**](ContentExtractionResponse.md)

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
> JobIdResponse post_api_content_extraction_jobs(file, x_organization_id=x_organization_id, project_id=project_id, temperature=temperature, rasterization_dpi=rasterization_dpi, max_output_tokens=max_output_tokens, enable_thinking=enable_thinking, timeout=timeout)


 Extract content from the provided file in markdown format as an async job.
 The response contains extracted markdown together with the reasoning trace.
 The model only accepts images. Therefore, some files are converted to images -
 the **rasterizationDPI** parameter controls their resolution.
 Parameter resolution order:
 - `temperature`: request value -> project setting (when `projectId` is provided) -> platform default
 - `rasterizationDPI`: request value -> project setting (when `projectId` is provided) -> platform default
 - `maxOutputTokens`: request value -> project setting (when `projectId` is provided) -> platform default


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
    file = None # bytes | 
    x_organization_id = 'x_organization_id_example' # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)
    project_id = 'project_id_example' # str | Optional content project identifier. When provided, project settings are used as fallback for inference parameters; this identifier is also attached to usage and billing events. (optional)
    temperature = 3.4 # float | Model temperature (optional). Controls output diversity.  Ranges between 0 and 1. Resolution order: request `temperature` -> project setting (when `projectId` is provided) -> default 0.0. (optional)
    rasterization_dpi = 56 # int | Resolution used to convert formatted documents (PDFs, etc.) to images, in dot per inch (optional).   Ranges between 1 and 300. Resolution order: request `rasterizationDPI` -> project setting (when `projectId` is provided) -> default 170 dpi. (optional)
    max_output_tokens = 56 # int | Maximum number of output tokens (optional). Must be positive. Resolution order: request `maxOutputTokens` -> project setting (when `projectId` is provided) -> default 0. Set to 0 for no limit. (optional)
    enable_thinking = True # bool | Enable thinking/reasoning (optional). Resolution order: request `enableThinking` -> project setting (when `projectId` is provided) -> default true. (optional)
    timeout = 'timeout_example' # str | Max time to wait for the processing completion.   Format examples: 1000ms, 10s, 1m, 1h (optional)

    try:
        api_response = api_instance.post_api_content_extraction_jobs(file, x_organization_id=x_organization_id, project_id=project_id, temperature=temperature, rasterization_dpi=rasterization_dpi, max_output_tokens=max_output_tokens, enable_thinking=enable_thinking, timeout=timeout)
        print("The response of ContentExtractionApi->post_api_content_extraction_jobs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ContentExtractionApi->post_api_content_extraction_jobs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file** | **bytes**|  | 
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 
 **project_id** | **str**| Optional content project identifier. When provided, project settings are used as fallback for inference parameters; this identifier is also attached to usage and billing events. | [optional] 
 **temperature** | **float**| Model temperature (optional). Controls output diversity.  Ranges between 0 and 1. Resolution order: request &#x60;temperature&#x60; -&gt; project setting (when &#x60;projectId&#x60; is provided) -&gt; default 0.0. | [optional] 
 **rasterization_dpi** | **int**| Resolution used to convert formatted documents (PDFs, etc.) to images, in dot per inch (optional).   Ranges between 1 and 300. Resolution order: request &#x60;rasterizationDPI&#x60; -&gt; project setting (when &#x60;projectId&#x60; is provided) -&gt; default 170 dpi. | [optional] 
 **max_output_tokens** | **int**| Maximum number of output tokens (optional). Must be positive. Resolution order: request &#x60;maxOutputTokens&#x60; -&gt; project setting (when &#x60;projectId&#x60; is provided) -&gt; default 0. Set to 0 for no limit. | [optional] 
 **enable_thinking** | **bool**| Enable thinking/reasoning (optional). Resolution order: request &#x60;enableThinking&#x60; -&gt; project setting (when &#x60;projectId&#x60; is provided) -&gt; default true. | [optional] 
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
**400** | Invalid value for: query parameter temperature, Invalid value for: query parameter rasterizationDPI, Invalid value for: query parameter maxOutputTokens, Invalid value for: query parameter enableThinking, Invalid value for: body |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

