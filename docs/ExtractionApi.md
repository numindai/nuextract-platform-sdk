# numind.openapi_client.ExtractionApi

All URIs are relative to *https://nuextract.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**post_api_projects_projectid_extract**](ExtractionApi.md#post_api_projects_projectid_extract) | **POST** /api/projects/{projectId}/extract | 


# **post_api_projects_projectid_extract**
> ExtractionResponse post_api_projects_projectid_extract(project_id, body, temperature=temperature, rasterization_dpi=rasterization_dpi)


 Extract information from the provided text or file. Some files are converted to images - 
the **rasterizationDPI** parameter controls their resolution. When **temperature** or **rasterizationDPI** 
parameters are not specified, they are set to their project-setting values.

#### Response:
Returns a JSON representing the extracted information.
 The ***result*** field is guaranteed to conform to the template via post-processing
 of the raw model output. In the event that the raw model output did not conform to the template,
 it is included in the ***rawResponse*** field, together with the corresponding error message,
 and an HTTP code 206 is returned.

#### Error Responses:
`404 Not Found` - If a **Project** with the specified `projectId` does not exist.

`403 Forbidden` - If the user does not have permission to run inference on this **Project**.
   

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.extraction_response import ExtractionResponse
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

    try:
        api_response = api_instance.post_api_projects_projectid_extract(project_id, body, temperature=temperature, rasterization_dpi=rasterization_dpi)
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
**400** | Invalid value for: query parameter temperature, Invalid value for: query parameter rasterizationDPI, Invalid value for: body |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

