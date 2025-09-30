# numind.openapi_client.FilesApi

All URIs are relative to *https://nuextract.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_api_files_fileid**](FilesApi.md#get_api_files_fileid) | **GET** /api/files/{fileId} | 
[**get_api_files_fileid_content**](FilesApi.md#get_api_files_fileid_content) | **GET** /api/files/{fileId}/content | 
[**post_api_files**](FilesApi.md#post_api_files) | **POST** /api/files | 
[**post_api_files_fileid_convert_to_document**](FilesApi.md#post_api_files_fileid_convert_to_document) | **POST** /api/files/{fileId}/convert-to-document | 


# **get_api_files_fileid**
> FileResponse get_api_files_fileid(file_id)


 Return meta information about a specific **File**.

#### Error Responses:
`404 Not Found` - If a **File** with the specified `fileId` does not exist.

`403 Forbidden` - If the user does not have permission to view this **File**.
    

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.file_response import FileResponse
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
    api_instance = numind.openapi_client.FilesApi(api_client)
    file_id = 'file_id_example' # str | Unique file identifier.

    try:
        api_response = api_instance.get_api_files_fileid(file_id)
        print("The response of FilesApi->get_api_files_fileid:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilesApi->get_api_files_fileid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_id** | **str**| Unique file identifier. | 

### Return type

[**FileResponse**](FileResponse.md)

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

# **get_api_files_fileid_content**
> bytearray get_api_files_fileid_content(file_id)


 Return the content of a specific **File**.

#### Error Responses:
`404 Not Found` - If a **File** with the specified `fileId` does not exist.

`403 Forbidden` - If the user does not have permission to view this **File**.
   

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
    api_instance = numind.openapi_client.FilesApi(api_client)
    file_id = 'file_id_example' # str | Unique file identifier.

    try:
        api_response = api_instance.get_api_files_fileid_content(file_id)
        print("The response of FilesApi->get_api_files_fileid_content:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilesApi->get_api_files_fileid_content: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_id** | **str**| Unique file identifier. | 

### Return type

**bytearray**

### Authorization

[oauth2Auth](../README.md#oauth2Auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/octet-stream, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  * Content-Type - MIME type of document content <br>  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_api_files**
> FileResponse post_api_files(x_file_name, body, x_organization=x_organization)


 Uploads a new file into a **File**.
 Use `/api/files/{fileId}/convert-to-document` to convert this **File** to a **Document**.
    

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.file_response import FileResponse
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
    api_instance = numind.openapi_client.FilesApi(api_client)
    x_file_name = 'x_file_name_example' # str | The name of the file to be uploaded.
    body = None # bytearray | 
    x_organization = 'x_organization_example' # str | The id of the current organization. This organization will own created resources (optional)

    try:
        api_response = api_instance.post_api_files(x_file_name, body, x_organization=x_organization)
        print("The response of FilesApi->post_api_files:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilesApi->post_api_files: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_file_name** | **str**| The name of the file to be uploaded. | 
 **body** | **bytearray**|  | 
 **x_organization** | **str**| The id of the current organization. This organization will own created resources | [optional] 

### Return type

[**FileResponse**](FileResponse.md)

### Authorization

[oauth2Auth](../README.md#oauth2Auth)

### HTTP request headers

 - **Content-Type**: application/octet-stream
 - **Accept**: application/json, text/plain

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**400** | Invalid value for: header x-file-name, Invalid value for: body |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_api_files_fileid_convert_to_document**
> DocumentResponse post_api_files_fileid_convert_to_document(file_id, convert_request)


 Convert the **File** into a **Document**

 - For ***text and image files***, the content is used as-is — no conversion is performed.
 - For ***other supported file types*** (e.g., PDFs, WORD, PPTX, Excel),
 the file is ***converted to an image*** in the background,
 using the **conversion parameters** provided in the request body (e.g., `rasterizationDPI`).

 The resulting image is then saved as a **Document** and can be used for inference or further processing.

 Once saved, this **Document** can be used to perform inference,
 create **Examples**, and/or save **Playground Items** with the text as input.
 
#### Response:
 The response contains a `documentId`, which is required in order to access and use this **Document**.

#### Error Responses:
`404 Not Found` - If a **File** with the specified `fileId` does not exist.


### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.convert_request import ConvertRequest
from numind.models.document_response import DocumentResponse
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
    api_instance = numind.openapi_client.FilesApi(api_client)
    file_id = 'file_id_example' # str | Unique file identifier.
    convert_request = numind.openapi_client.ConvertRequest() # ConvertRequest | 

    try:
        api_response = api_instance.post_api_files_fileid_convert_to_document(file_id, convert_request)
        print("The response of FilesApi->post_api_files_fileid_convert_to_document:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilesApi->post_api_files_fileid_convert_to_document: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_id** | **str**| Unique file identifier. | 
 **convert_request** | [**ConvertRequest**](ConvertRequest.md)|  | 

### Return type

[**DocumentResponse**](DocumentResponse.md)

### Authorization

[oauth2Auth](../README.md#oauth2Auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, text/plain

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**400** | Invalid value for: body |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

