# numind.openapi_client.TemplateGenerationApi

All URIs are relative to *https://nuextract.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_api_template_generation_jobs_templatejobid**](TemplateGenerationApi.md#get_api_template_generation_jobs_templatejobid) | **GET** /api/template-generation/jobs/{templateJobId} | 
[**post_api_template_generation_jobs**](TemplateGenerationApi.md#post_api_template_generation_jobs) | **POST** /api/template-generation/jobs | 


# **get_api_template_generation_jobs_templatejobid**
> TemplateResponse get_api_template_generation_jobs_templatejobid(template_job_id, x_organization_id=x_organization_id)


 Get template generation result of a specific job by its unique identifier.

#### Response:
 Returns a JSON representing the derived template.
 In case the derivation fails, an empty template is returned.

#### Error Responses:
`404 Not Found` - If a template generation job with the specified ID does not exist.

`403 Forbidden` - If the user does not have permission to access this job.
   

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.template_response import TemplateResponse
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
    api_instance = numind.openapi_client.TemplateGenerationApi(api_client)
    template_job_id = 'template_job_id_example' # str | Unique template job identifier.
    x_organization_id = 'x_organization_id_example' # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)

    try:
        api_response = api_instance.get_api_template_generation_jobs_templatejobid(template_job_id, x_organization_id=x_organization_id)
        print("The response of TemplateGenerationApi->get_api_template_generation_jobs_templatejobid:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TemplateGenerationApi->get_api_template_generation_jobs_templatejobid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **template_job_id** | **str**| Unique template job identifier. | 
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 

### Return type

[**TemplateResponse**](TemplateResponse.md)

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

# **post_api_template_generation_jobs**
> JobIdResponse post_api_template_generation_jobs(body, x_organization_id=x_organization_id, rasterization_dpi=rasterization_dpi, timeout=timeout)


 Derive a template from the provided **File** as an async job.
 Potentially, this endpoint can equally be used to correct the template to conform to the NuExtract standard.
 The **File** can be a text document, an image, or any document that can be converted to an image (e.g. PDF, Excel, etc.).
 The resulting template is a JSON object that can be used as a project template.

#### Response:
 Returns a JSON containing the job ID that can be used to retrieve the job status and results.

 If the job is completed successfully, the job's output data will contain the derived template.
 The response is an empty template if the derivation fails.

#### Error Responses:
`403 Forbidden` - If the user's billing quota is exceeded.
   

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
    api_instance = numind.openapi_client.TemplateGenerationApi(api_client)
    body = None # bytearray | 
    x_organization_id = 'x_organization_id_example' # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)
    rasterization_dpi = 56 # int | Resolution used to convert formatted documents (PDFs, etc.) to images, in dot per inch (optional).   Ranges between 1 and 300. If not specified, the default value 170 dpi is used.   If the file is already an image or a text, this parameter is ignored. (optional)
    timeout = 'timeout_example' # str | Max time to wait for the processing completion.   Format examples: 1000ms, 10s, 1m, 1h (optional)

    try:
        api_response = api_instance.post_api_template_generation_jobs(body, x_organization_id=x_organization_id, rasterization_dpi=rasterization_dpi, timeout=timeout)
        print("The response of TemplateGenerationApi->post_api_template_generation_jobs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TemplateGenerationApi->post_api_template_generation_jobs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **bytearray**|  | 
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 
 **rasterization_dpi** | **int**| Resolution used to convert formatted documents (PDFs, etc.) to images, in dot per inch (optional).   Ranges between 1 and 300. If not specified, the default value 170 dpi is used.   If the file is already an image or a text, this parameter is ignored. | [optional] 
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
**400** | Invalid value for: query parameter rasterizationDPI, Invalid value for: body |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

