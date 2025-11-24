# numind.openapi_client.ExtractionApi

All URIs are relative to *https://nuextract.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**post_api_projects_projectid_extract**](ExtractionApi.md#post_api_projects_projectid_extract) | **POST** /api/projects/{projectId}/extract | 
[**post_api_projects_projectid_extract_async**](ExtractionApi.md#post_api_projects_projectid_extract_async) | **POST** /api/projects/{projectId}/extract-async | 


# **post_api_projects_projectid_extract**
> ExtractionResponse post_api_projects_projectid_extract(project_id, body, temperature=temperature, rasterization_dpi=rasterization_dpi, max_output_tokens=max_output_tokens, degraded_mode=degraded_mode, max_tokens_smart_example=max_tokens_smart_example)


 Extract information from the provided text or file. Some files are converted to images - 
the **rasterizationDPI** parameter controls their resolution. When **temperature**, **rasterizationDPI**,
**maxOutputTokens**, **degradedMode** and **maxTokensSmartExample** parameters are not specified, 
they are set to their project-setting values.

#### Response:
Returns a JSON representing the extracted information.
 The ***result*** field is guaranteed to conform to the template via post-processing
 of the raw model output. In the event that the raw model output did not conform to the template,
 it is included in the ***rawResponse*** field, together with the corresponding error message,
 and an HTTP code 206 is returned.

#### Error Responses:
`404 Not Found` - If a **Project** with the specified `projectId` does not exist.

`403 Forbidden` - If the user does not have permission to run inference on this **Project** or if the user's billing quota is exceeded.
   

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.extraction_response import ExtractionResponse
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
    api_instance = numind.openapi_client.ExtractionApi(api_client)
    project_id = 'project_id_example' # str | Unique project identifier.
    body = None # bytearray | 
    temperature = 3.4 # float | Model temperature (optional). Controls output diversity.  When not specified, the project value is used.   Ranges between 0 and 1. (optional)
    rasterization_dpi = 56 # int | Resolution used to convert formatted documents (PDFs, etc.) to images, in dot per inch (optional).   Ranges between 1 and 300. (optional)
    max_output_tokens = 56 # int | Maximum number of output tokens (optional). Must be positive. Set to 0 for no limit. (optional)
    degraded_mode = 'degraded_mode_example' # str | Controls whether a response is returned when smart example is not functionning. Rejects by default. (optional)
    max_tokens_smart_example = 56 # int | Controls the maximum number of tokens that can be allocated to the examples.  Must be positive. Ranges in the context window of the model. (optional)

    try:
        api_response = api_instance.post_api_projects_projectid_extract(project_id, body, temperature=temperature, rasterization_dpi=rasterization_dpi, max_output_tokens=max_output_tokens, degraded_mode=degraded_mode, max_tokens_smart_example=max_tokens_smart_example)
        print("The response of ExtractionApi->post_api_projects_projectid_extract:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExtractionApi->post_api_projects_projectid_extract: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Unique project identifier. | 
 **body** | **bytearray**|  | 
 **temperature** | **float**| Model temperature (optional). Controls output diversity.  When not specified, the project value is used.   Ranges between 0 and 1. | [optional] 
 **rasterization_dpi** | **int**| Resolution used to convert formatted documents (PDFs, etc.) to images, in dot per inch (optional).   Ranges between 1 and 300. | [optional] 
 **max_output_tokens** | **int**| Maximum number of output tokens (optional). Must be positive. Set to 0 for no limit. | [optional] 
 **degraded_mode** | **str**| Controls whether a response is returned when smart example is not functionning. Rejects by default. | [optional] 
 **max_tokens_smart_example** | **int**| Controls the maximum number of tokens that can be allocated to the examples.  Must be positive. Ranges in the context window of the model. | [optional] 

### Return type

[**ExtractionResponse**](ExtractionResponse.md)

### Authorization

[oauth2Auth](../README.md#oauth2Auth)

### HTTP request headers

 - **Content-Type**: application/octet-stream
 - **Accept**: application/json, text/plain

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**400** | Invalid value for: query parameter temperature, Invalid value for: query parameter rasterizationDPI, Invalid value for: query parameter maxOutputTokens, Invalid value for: query parameter maxTokensSmartExample, Invalid value for: body |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_api_projects_projectid_extract_async**
> JobIdResponse post_api_projects_projectid_extract_async(project_id, body, temperature=temperature, dpi=dpi, max_output_tokens=max_output_tokens, degraded_mode=degraded_mode, max_tokens_smart_example=max_tokens_smart_example, timeout=timeout)


 Extract information from the provided text or file as an async job. Some files are converted to images -
 the **rasterizationDPI** parameter controls their resolution. When **temperature**, **rasterizationDPI**,
 **maxOutputTokens**, **degradedMode** and **maxTokensSmartExample** parameters are not specified,
 they are set to their project-setting values.

#### Response:
 Returns a JSON containing the job ID that can be used to retrieve the job status and results.

 If the job is completed successfully, the job's output data will contain a JSON representing the extracted information.
 The ***result*** field is guaranteed to conform to the template via post-processing
 of the raw model output. In the event that the raw model output did not conform to the template,
 it is included in the ***rawResponse*** field, together with the corresponding error message,
 and an HTTP code 206 is returned.

#### Error Responses:
`404 Not Found` - If a **Project** with the specified `projectId` does not exist.

`403 Forbidden` - If the user does not have permission to run inference on this **Project** or if the user's billing quota is exceeded.
   

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
    api_instance = numind.openapi_client.ExtractionApi(api_client)
    project_id = 'project_id_example' # str | Unique project identifier.
    body = None # bytearray | 
    temperature = 3.4 # float | Model temperature (optional). Controls output diversity.  When not specified, the project value is used.   Ranges between 0 and 1. (optional)
    dpi = 56 # int | DPI for file rasterization (optional).  When not specified, the project value is used.   If the file is already an image or a text, this parameter is ignored. (optional)
    max_output_tokens = 56 # int | Maximum number of output tokens (optional).  When not specified, the project value is used.   Use 0 to indicate no limit. (optional)
    degraded_mode = 'degraded_mode_example' # str | Controls whether a response is returned when smart example is not functionning. Rejects by default. (optional)
    max_tokens_smart_example = 56 # int | Controls the maximum number of tokens that can be allocated to the examples.  Must be positive. Ranges in the context window of the model. (optional)
    timeout = 'timeout_example' # str | Max time to wait for the processing completion.   Format examples: 1000ms, 10s, 1m, 1h (optional)

    try:
        api_response = api_instance.post_api_projects_projectid_extract_async(project_id, body, temperature=temperature, dpi=dpi, max_output_tokens=max_output_tokens, degraded_mode=degraded_mode, max_tokens_smart_example=max_tokens_smart_example, timeout=timeout)
        print("The response of ExtractionApi->post_api_projects_projectid_extract_async:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExtractionApi->post_api_projects_projectid_extract_async: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Unique project identifier. | 
 **body** | **bytearray**|  | 
 **temperature** | **float**| Model temperature (optional). Controls output diversity.  When not specified, the project value is used.   Ranges between 0 and 1. | [optional] 
 **dpi** | **int**| DPI for file rasterization (optional).  When not specified, the project value is used.   If the file is already an image or a text, this parameter is ignored. | [optional] 
 **max_output_tokens** | **int**| Maximum number of output tokens (optional).  When not specified, the project value is used.   Use 0 to indicate no limit. | [optional] 
 **degraded_mode** | **str**| Controls whether a response is returned when smart example is not functionning. Rejects by default. | [optional] 
 **max_tokens_smart_example** | **int**| Controls the maximum number of tokens that can be allocated to the examples.  Must be positive. Ranges in the context window of the model. | [optional] 
 **timeout** | **str**| Max time to wait for the processing completion.   Format examples: 1000ms, 10s, 1m, 1h | [optional] 

### Return type

[**JobIdResponse**](JobIdResponse.md)

### Authorization

[oauth2Auth](../README.md#oauth2Auth)

### HTTP request headers

 - **Content-Type**: application/octet-stream
 - **Accept**: application/json, text/plain

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**400** | Invalid value for: query parameter temperature, Invalid value for: query parameter dpi, Invalid value for: query parameter maxOutputTokens, Invalid value for: query parameter maxTokensSmartExample, Invalid value for: body |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

