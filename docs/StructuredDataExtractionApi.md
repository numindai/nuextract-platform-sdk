# numind.openapi_client.StructuredDataExtractionApi

All URIs are relative to *https://nuextract.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_api_structured_extraction_jobs_structuredextractionjobid**](StructuredDataExtractionApi.md#get_api_structured_extraction_jobs_structuredextractionjobid) | **GET** /api/structured-extraction/jobs/{structuredExtractionJobId} | 
[**post_api_structured_extraction_structuredextractionprojectid_jobs**](StructuredDataExtractionApi.md#post_api_structured_extraction_structuredextractionprojectid_jobs) | **POST** /api/structured-extraction/{structuredExtractionProjectId}/jobs | 


# **get_api_structured_extraction_jobs_structuredextractionjobid**
> ExtractionResponse get_api_structured_extraction_jobs_structuredextractionjobid(structured_extraction_job_id)


 Get structured extraction result of a specific job by its unique identifier.

#### Response:
 Returns a JSON representing the extracted information.
 In case the extraction fails, an empty template is returned.

#### Error Responses:
`404 Not Found` - If an extraction job with the specified ID does not exist.

`403 Forbidden` - If the user does not have permission to access this job.
   

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
    api_instance = numind.openapi_client.StructuredDataExtractionApi(api_client)
    structured_extraction_job_id = 'structured_extraction_job_id_example' # str | Unique structured extraction job identifier.

    try:
        api_response = api_instance.get_api_structured_extraction_jobs_structuredextractionjobid(structured_extraction_job_id)
        print("The response of StructuredDataExtractionApi->get_api_structured_extraction_jobs_structuredextractionjobid:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StructuredDataExtractionApi->get_api_structured_extraction_jobs_structuredextractionjobid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **structured_extraction_job_id** | **str**| Unique structured extraction job identifier. | 

### Return type

[**ExtractionResponse**](ExtractionResponse.md)

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

# **post_api_structured_extraction_structuredextractionprojectid_jobs**
> JobIdResponse post_api_structured_extraction_structuredextractionprojectid_jobs(structured_extraction_project_id, body, temperature=temperature, dpi=dpi, max_output_tokens=max_output_tokens, max_example_token_number=max_example_token_number, max_example_number=max_example_number, min_example_similarity=min_example_similarity, timeout=timeout)


 Extract information from the provided text or file as an async job. Some files are converted to images -
 the **rasterizationDPI** parameter controls their resolution. When **temperature**, **rasterizationDPI**,
 **maxOutputTokens** and **maxExampleTokenNumber** parameters are not specified,
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
    api_instance = numind.openapi_client.StructuredDataExtractionApi(api_client)
    structured_extraction_project_id = 'structured_extraction_project_id_example' # str | Unique structured extraction project identifier.
    body = None # bytearray | 
    temperature = 3.4 # float | Model temperature (optional). Controls output diversity.  When not specified, the project value is used.   Ranges between 0 and 1. (optional)
    dpi = 56 # int | DPI for file rasterization (optional).  When not specified, the project value is used.   If the file is already an image or a text, this parameter is ignored. (optional)
    max_output_tokens = 56 # int | Maximum number of output tokens (optional).  When not specified, the project value is used.   Use 0 to indicate no limit. (optional)
    max_example_token_number = 56 # int | Controls the maximum number of tokens that can be allocated to the examples.  Must be positive. Ranges in the context window of the model. (optional)
    max_example_number = 56 # int | Controls the maximum number of examples to use.  Must be positive. Set to 0 for no limit. (optional)
    min_example_similarity = 3.4 # float | Controls the minimum similarity between the document and the examples.  Must be between 0 and 1. Set to 0 for any similarity and 1 for exact match. (optional)
    timeout = 'timeout_example' # str | Max time to wait for the processing completion.   Format examples: 1000ms, 10s, 1m, 1h (optional)

    try:
        api_response = api_instance.post_api_structured_extraction_structuredextractionprojectid_jobs(structured_extraction_project_id, body, temperature=temperature, dpi=dpi, max_output_tokens=max_output_tokens, max_example_token_number=max_example_token_number, max_example_number=max_example_number, min_example_similarity=min_example_similarity, timeout=timeout)
        print("The response of StructuredDataExtractionApi->post_api_structured_extraction_structuredextractionprojectid_jobs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StructuredDataExtractionApi->post_api_structured_extraction_structuredextractionprojectid_jobs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **structured_extraction_project_id** | **str**| Unique structured extraction project identifier. | 
 **body** | **bytearray**|  | 
 **temperature** | **float**| Model temperature (optional). Controls output diversity.  When not specified, the project value is used.   Ranges between 0 and 1. | [optional] 
 **dpi** | **int**| DPI for file rasterization (optional).  When not specified, the project value is used.   If the file is already an image or a text, this parameter is ignored. | [optional] 
 **max_output_tokens** | **int**| Maximum number of output tokens (optional).  When not specified, the project value is used.   Use 0 to indicate no limit. | [optional] 
 **max_example_token_number** | **int**| Controls the maximum number of tokens that can be allocated to the examples.  Must be positive. Ranges in the context window of the model. | [optional] 
 **max_example_number** | **int**| Controls the maximum number of examples to use.  Must be positive. Set to 0 for no limit. | [optional] 
 **min_example_similarity** | **float**| Controls the minimum similarity between the document and the examples.  Must be between 0 and 1. Set to 0 for any similarity and 1 for exact match. | [optional] 
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
**400** | Invalid value for: query parameter temperature, Invalid value for: query parameter dpi, Invalid value for: query parameter maxOutputTokens, Invalid value for: query parameter maxExampleTokenNumber, Invalid value for: query parameter maxExampleNumber, Invalid value for: query parameter minExampleSimilarity, Invalid value for: body |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

