# numind.openapi_client.DocumentsApi

All URIs are relative to *https://nuextract.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_api_documents_documentid**](DocumentsApi.md#get_api_documents_documentid) | **GET** /api/documents/{documentId} | 
[**get_api_documents_documentid_content**](DocumentsApi.md#get_api_documents_documentid_content) | **GET** /api/documents/{documentId}/content | 
[**post_api_documents_documentid_new_owner**](DocumentsApi.md#post_api_documents_documentid_new_owner) | **POST** /api/documents/{documentId}/new-owner | 
[**post_api_documents_text**](DocumentsApi.md#post_api_documents_text) | **POST** /api/documents/text | 


# **get_api_documents_documentid**
> DocumentResponse get_api_documents_documentid(document_id, x_organization_id=x_organization_id)


 Return meta information about a specific **Document**.
 For text **Documents**, this also includes the text content.
 In order to access the non-text **Document** content, use the endpoint `/api/documents/{documentId}/content`

#### Error Responses:
`404 Not Found` - If a **Document** with the specified `documentId` does not exist.

`403 Forbidden` - If the user does not have permission to view this **Document**.
   

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
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
    api_instance = numind.openapi_client.DocumentsApi(api_client)
    document_id = 'document_id_example' # str | Unique document identifier.
    x_organization_id = 'x_organization_id_example' # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)

    try:
        api_response = api_instance.get_api_documents_documentid(document_id, x_organization_id=x_organization_id)
        print("The response of DocumentsApi->get_api_documents_documentid:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocumentsApi->get_api_documents_documentid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **document_id** | **str**| Unique document identifier. | 
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 

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
> bytearray get_api_documents_documentid_content(document_id, x_organization_id=x_organization_id)


 Return the content of a specific **Document**.

#### Error Responses:
`404 Not Found` - If a **Document** with the specified `documentId` does not exist.

`403 Forbidden` - If the user does not have permission to view this **Document**.
   

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
    api_instance = numind.openapi_client.DocumentsApi(api_client)
    document_id = 'document_id_example' # str | Unique document identifier.
    x_organization_id = 'x_organization_id_example' # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)

    try:
        api_response = api_instance.get_api_documents_documentid_content(document_id, x_organization_id=x_organization_id)
        print("The response of DocumentsApi->get_api_documents_documentid_content:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocumentsApi->get_api_documents_documentid_content: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **document_id** | **str**| Unique document identifier. | 
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 

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
**200** |  |  * Content-Type - MIME type of document content <br>  * Cache-Control -  <br>  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_api_documents_documentid_new_owner**
> DocumentResponse post_api_documents_documentid_new_owner(document_id, x_organization_id=x_organization_id, x_organization=x_organization)


 Transfer the ownership of a **Document** to another user or organization. Since documents are immutable,
 a new document with a new DocumentId, as well as a new File with a new FileId will be created.
 If the document already belongs to the specified user or organization, the initial document will be returned.

#### Error Responses:
`404 Not Found` - If a **Document** with the specified `documentId` does not exist.

`403 Forbidden` - If the user does not have permission to read this **Document** or is not a member of the specified Organization.
   

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
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
    api_instance = numind.openapi_client.DocumentsApi(api_client)
    document_id = 'document_id_example' # str | Unique document identifier.
    x_organization_id = 'x_organization_id_example' # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)
    x_organization = 'x_organization_example' # str | The id of the current organization. This organization will own created resources (optional)

    try:
        api_response = api_instance.post_api_documents_documentid_new_owner(document_id, x_organization_id=x_organization_id, x_organization=x_organization)
        print("The response of DocumentsApi->post_api_documents_documentid_new_owner:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocumentsApi->post_api_documents_documentid_new_owner: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **document_id** | **str**| Unique document identifier. | 
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 
 **x_organization** | **str**| The id of the current organization. This organization will own created resources | [optional] 

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

# **post_api_documents_text**
> DocumentResponse post_api_documents_text(text_request, x_organization_id=x_organization_id)


 Save the text as a **Document**.


 Once saved, this **Document** can be used to perform inference,
 create **Examples**, and/or save **Playground Items** with the text as input.


#### Response:
 The response contains a `documentId`, which is required in order to access and use this **Document**.
   

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.document_response import DocumentResponse
from numind.models.text_request import TextRequest
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
    x_organization_id = 'x_organization_id_example' # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)

    try:
        api_response = api_instance.post_api_documents_text(text_request, x_organization_id=x_organization_id)
        print("The response of DocumentsApi->post_api_documents_text:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocumentsApi->post_api_documents_text: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **text_request** | [**TextRequest**](TextRequest.md)|  | 
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 

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

