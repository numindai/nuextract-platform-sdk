# numind.openapi_client.DocumentsApi

All URIs are relative to *https://nuextract.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_api_documents_documentid**](DocumentsApi.md#get_api_documents_documentid) | **GET** /api/documents/{documentId} | 
[**get_api_documents_documentid_content**](DocumentsApi.md#get_api_documents_documentid_content) | **GET** /api/documents/{documentId}/content | 
[**post_api_documents_text**](DocumentsApi.md#post_api_documents_text) | **POST** /api/documents/text | 
[**post_api_projects_projectid_documents_file**](DocumentsApi.md#post_api_projects_projectid_documents_file) | **POST** /api/projects/{projectId}/documents/file | 


# **get_api_documents_documentid**
> DocumentResponse get_api_documents_documentid(document_id)


 Retrieves meta information about a specific document. 
 For text documents, this includes the text content.
 In order to access the non-text document content, uset the endpoint `/api/documents/{documentId}/content`

#### Error Responses:
`404 Not Found` - If a document with the specified documentId does not exist.

`403 Forbidden` - If the user does not have permission to view this document.
   

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.document_response import DocumentResponse
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
    api_instance = numind.openapi_client.DocumentsApi(api_client)
    document_id = 'document_id_example' # str | Unique document identifier.

    try:
        api_response = api_instance.get_api_documents_documentid(document_id)
        print("The response of DocumentsApi->get_api_documents_documentid:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocumentsApi->get_api_documents_documentid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **document_id** | **str**| Unique document identifier. | 

### Return type

[**DocumentResponse**](DocumentResponse.md)

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

# **get_api_documents_documentid_content**
> bytearray get_api_documents_documentid_content(token, document_id)


 Retrieves the content of a specific document.

#### Error Responses:
`404 Not Found` - If a document with the specified documentId does not exist.

`403 Forbidden` - If the user does not have permission to view this document.
   

### Example


```python
import numind.openapi_client
from numind.openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://nuextract.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = numind.openapi_client.Configuration(
    host = "https://nuextract.ai"
)


# Enter a context with an instance of the API client
with numind.openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = numind.openapi_client.DocumentsApi(api_client)
    token = 'token_example' # str | 
    document_id = 'document_id_example' # str | Unique document identifier.

    try:
        api_response = api_instance.get_api_documents_documentid_content(token, document_id)
        print("The response of DocumentsApi->get_api_documents_documentid_content:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocumentsApi->get_api_documents_documentid_content: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **token** | **str**|  | 
 **document_id** | **str**| Unique document identifier. | 

### Return type

**bytearray**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/octet-stream, text/plain, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  * Content-Type - MIME type of document content <br>  |
**400** | Invalid value for: query parameter token |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_api_documents_text**
> DocumentResponse post_api_documents_text(text_request)


 Save the text as a document. 
 Once saved, this document can be used to perform inference,
 create ICL (In-Context Learning) examples,
 and/or save playground items with the text as input.
 
 In order to save non-text files, use the `/api/documents/file` endpoint.


#### Response:
 The response contains a `documentId`, which is required in order to access and use this document.
   

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.document_response import DocumentResponse
from numind.openapi_client.models.text_request import TextRequest
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
    api_instance = numind.openapi_client.DocumentsApi(api_client)
    text_request = {"text":"[EXAMPLE ONLY] Your order (ID: o-89123) has been successfully processed. The customer ID for this order is c-20485. It was placed on March 10, 2024, at 11:15 AM UTC and is now marked as shipped. The total amount charged is $149.99 USD. The items in this order include: Product ID p-00876 with a quantity of 1 at a unit price of $79.99, and Product ID p-00321 with a quantity of 2 at a unit price of $35.00. The shipping address is 782 Pine St, Austin, TX, 73301, USA. The customer has requested: \"Leave package at the front door.\" Additional delivery preferences include no signature required and standard delivery. The estimated delivery date is March 15, 2024, by 5:00 PM UTC."} # TextRequest | 

    try:
        api_response = api_instance.post_api_documents_text(text_request)
        print("The response of DocumentsApi->post_api_documents_text:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocumentsApi->post_api_documents_text: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **text_request** | [**TextRequest**](TextRequest.md)|  | 

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

# **post_api_projects_projectid_documents_file**
> DocumentResponse post_api_projects_projectid_documents_file(project_id, x_file_name, body)


 Save the file as a document. 

 Once saved, this document can be used to perform inference,
 create ICL (In-Context Learning) examples,
 and/or save playground items with the text as input.
 
 All non-image files are automatically converted to an image in the background when possible.
 For that, a parameter **rasterizationDpi** is taken into account. 
 This parameter can be set in the project settings.



#### Response:
 The response contains a `documentId`, which is required in order to access and use this document.
 When referencing a non-text/image file by `documentId`, only its converted image equivalents are accessible.

#### Error Responses:
`404 Not Found` - If a project with the specified projectId does not exist.


### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.document_response import DocumentResponse
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
    api_instance = numind.openapi_client.DocumentsApi(api_client)
    project_id = 'project_id_example' # str | Unique project identifier.
    x_file_name = 'x_file_name_example' # str | The name of the file to be uploaded.
    body = None # bytearray | 

    try:
        api_response = api_instance.post_api_projects_projectid_documents_file(project_id, x_file_name, body)
        print("The response of DocumentsApi->post_api_projects_projectid_documents_file:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocumentsApi->post_api_projects_projectid_documents_file: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Unique project identifier. | 
 **x_file_name** | **str**| The name of the file to be uploaded. | 
 **body** | **bytearray**|  | 

### Return type

[**DocumentResponse**](DocumentResponse.md)

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

