# numind.openapi_client.StructuredExtractionPlaygroundApi

All URIs are relative to *https://nuextract.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_api_structured_extraction_structuredextractionprojectid_playground_structuredextractionplaygrounditemid**](StructuredExtractionPlaygroundApi.md#delete_api_structured_extraction_structuredextractionprojectid_playground_structuredextractionplaygrounditemid) | **DELETE** /api/structured-extraction/{structuredExtractionProjectId}/playground/{structuredExtractionPlaygroundItemId} | 
[**get_api_structured_extraction_structuredextractionprojectid_playground**](StructuredExtractionPlaygroundApi.md#get_api_structured_extraction_structuredextractionprojectid_playground) | **GET** /api/structured-extraction/{structuredExtractionProjectId}/playground | 
[**get_api_structured_extraction_structuredextractionprojectid_playground_structuredextractionplaygrounditemid**](StructuredExtractionPlaygroundApi.md#get_api_structured_extraction_structuredextractionprojectid_playground_structuredextractionplaygrounditemid) | **GET** /api/structured-extraction/{structuredExtractionProjectId}/playground/{structuredExtractionPlaygroundItemId} | 
[**post_api_structured_extraction_structuredextractionprojectid_playground**](StructuredExtractionPlaygroundApi.md#post_api_structured_extraction_structuredextractionprojectid_playground) | **POST** /api/structured-extraction/{structuredExtractionProjectId}/playground | 
[**put_api_structured_extraction_structuredextractionprojectid_playground_structuredextractionplaygrounditemid**](StructuredExtractionPlaygroundApi.md#put_api_structured_extraction_structuredextractionprojectid_playground_structuredextractionplaygrounditemid) | **PUT** /api/structured-extraction/{structuredExtractionProjectId}/playground/{structuredExtractionPlaygroundItemId} | 


# **delete_api_structured_extraction_structuredextractionprojectid_playground_structuredextractionplaygrounditemid**
> delete_api_structured_extraction_structuredextractionprojectid_playground_structuredextractionplaygrounditemid(structured_extraction_project_id, structured_extraction_playground_item_id)


Delete a specific **Playground Item**.

#### Error Responses:
`404 Not Found` - If a **Playground Item** with the specified `playgroundItemId` associated with the given `projectId` does not exist.

`403 Forbidden` - If the user does not have permission to update this **Project**.
  

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
    api_instance = numind.openapi_client.StructuredExtractionPlaygroundApi(api_client)
    structured_extraction_project_id = 'structured_extraction_project_id_example' # str | Unique structured extraction project identifier.
    structured_extraction_playground_item_id = 'structured_extraction_playground_item_id_example' # str | Unique structured extraction playground item identifier.

    try:
        api_instance.delete_api_structured_extraction_structuredextractionprojectid_playground_structuredextractionplaygrounditemid(structured_extraction_project_id, structured_extraction_playground_item_id)
    except Exception as e:
        print("Exception when calling StructuredExtractionPlaygroundApi->delete_api_structured_extraction_structuredextractionprojectid_playground_structuredextractionplaygrounditemid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **structured_extraction_project_id** | **str**| Unique structured extraction project identifier. | 
 **structured_extraction_playground_item_id** | **str**| Unique structured extraction playground item identifier. | 

### Return type

void (empty response body)

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

# **get_api_structured_extraction_structuredextractionprojectid_playground**
> PaginatedResponsePlaygroundItemResponse get_api_structured_extraction_structuredextractionprojectid_playground(structured_extraction_project_id, skip=skip, per_page=per_page)


Return a list of **Playground Items** associated to the specified **Project** with pagination support.

#### Error Responses:
`404 Not Found` - If a **Project** with the specified `projectId` does not exist.

`403 Forbidden` - If the user does not have permission to view this **Project**.
  

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.paginated_response_playground_item_response import PaginatedResponsePlaygroundItemResponse
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
    api_instance = numind.openapi_client.StructuredExtractionPlaygroundApi(api_client)
    structured_extraction_project_id = 'structured_extraction_project_id_example' # str | Unique structured extraction project identifier.
    skip = 56 # int | Number of playground items to skip. Min: 0. Default: 0. (optional)
    per_page = 56 # int | Number of playground items per page. Min: 1. Max: 100. Default: 30. (optional)

    try:
        api_response = api_instance.get_api_structured_extraction_structuredextractionprojectid_playground(structured_extraction_project_id, skip=skip, per_page=per_page)
        print("The response of StructuredExtractionPlaygroundApi->get_api_structured_extraction_structuredextractionprojectid_playground:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StructuredExtractionPlaygroundApi->get_api_structured_extraction_structuredextractionprojectid_playground: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **structured_extraction_project_id** | **str**| Unique structured extraction project identifier. | 
 **skip** | **int**| Number of playground items to skip. Min: 0. Default: 0. | [optional] 
 **per_page** | **int**| Number of playground items per page. Min: 1. Max: 100. Default: 30. | [optional] 

### Return type

[**PaginatedResponsePlaygroundItemResponse**](PaginatedResponsePlaygroundItemResponse.md)

### Authorization

[oauth2Auth](../README.md#oauth2Auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, text/plain

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**400** | Invalid value for: query parameter skip, Invalid value for: query parameter perPage |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_api_structured_extraction_structuredextractionprojectid_playground_structuredextractionplaygrounditemid**
> PlaygroundItemResponse get_api_structured_extraction_structuredextractionprojectid_playground_structuredextractionplaygrounditemid(structured_extraction_project_id, structured_extraction_playground_item_id)


Return a specific **Playground Item**.

#### Error Responses:
`404 Not Found` - If a **Playground Item** with the specified `playgroundItemId` associated with the given `projectId` does not exist.

`403 Forbidden` - If the user does not have permission to view this **Project**.
  

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.playground_item_response import PlaygroundItemResponse
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
    api_instance = numind.openapi_client.StructuredExtractionPlaygroundApi(api_client)
    structured_extraction_project_id = 'structured_extraction_project_id_example' # str | Unique structured extraction project identifier.
    structured_extraction_playground_item_id = 'structured_extraction_playground_item_id_example' # str | Unique structured extraction playground item identifier.

    try:
        api_response = api_instance.get_api_structured_extraction_structuredextractionprojectid_playground_structuredextractionplaygrounditemid(structured_extraction_project_id, structured_extraction_playground_item_id)
        print("The response of StructuredExtractionPlaygroundApi->get_api_structured_extraction_structuredextractionprojectid_playground_structuredextractionplaygrounditemid:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StructuredExtractionPlaygroundApi->get_api_structured_extraction_structuredextractionprojectid_playground_structuredextractionplaygrounditemid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **structured_extraction_project_id** | **str**| Unique structured extraction project identifier. | 
 **structured_extraction_playground_item_id** | **str**| Unique structured extraction playground item identifier. | 

### Return type

[**PlaygroundItemResponse**](PlaygroundItemResponse.md)

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

# **post_api_structured_extraction_structuredextractionprojectid_playground**
> PlaygroundItemResponse post_api_structured_extraction_structuredextractionprojectid_playground(structured_extraction_project_id, create_or_update_playground_item_request)


Create a new **Playground Item** associated to the specified **Project**.

#### Note:
 If the **Document** ownership scope does not match the **Project** ownership scope, the **Playground Item** creation will fail.

#### Error Responses:
`404 Not Found` - If a **Project** with the specified `projectId` does not exist or a **Document** with the specified `documentId` does not exist.

`403 Forbidden` - If the user does not have permission to update this **Project**, use the specified **Document**, or the **Document** ownership scope does not match **Project** ownership scope.
  

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.create_or_update_playground_item_request import CreateOrUpdatePlaygroundItemRequest
from numind.models.playground_item_response import PlaygroundItemResponse
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
    api_instance = numind.openapi_client.StructuredExtractionPlaygroundApi(api_client)
    structured_extraction_project_id = 'structured_extraction_project_id_example' # str | Unique structured extraction project identifier.
    create_or_update_playground_item_request = {"documentId":"0d25d758-d475-4c14-aafa-eb5d6a40b670","result":{"orderId":"Example: o-89123","customerId":"Example: c-20485","orderDate":"2024-03-10T11:15:00.000Z","status":"shipped","totalAmount":149.99,"currency":"USD","items":[{"productId":"p-00876","quantity":1,"unitPrice":79.99},{"productId":"p-00321","quantity":2,"unitPrice":35}],"shippingAddress":{"street":"782 Pine St","city":"Austin","state":"TX","country":"USA","zip":"73301"},"comments":"Leave package at the front door.","deliveryPreferences":["no_signature_required","standard_delivery"],"estimatedDelivery":"2024-03-15T17:00:00.000Z"},"totalTokens":567,"outputTokens":267,"inputTokens":300} # CreateOrUpdatePlaygroundItemRequest | 

    try:
        api_response = api_instance.post_api_structured_extraction_structuredextractionprojectid_playground(structured_extraction_project_id, create_or_update_playground_item_request)
        print("The response of StructuredExtractionPlaygroundApi->post_api_structured_extraction_structuredextractionprojectid_playground:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StructuredExtractionPlaygroundApi->post_api_structured_extraction_structuredextractionprojectid_playground: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **structured_extraction_project_id** | **str**| Unique structured extraction project identifier. | 
 **create_or_update_playground_item_request** | [**CreateOrUpdatePlaygroundItemRequest**](CreateOrUpdatePlaygroundItemRequest.md)|  | 

### Return type

[**PlaygroundItemResponse**](PlaygroundItemResponse.md)

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

# **put_api_structured_extraction_structuredextractionprojectid_playground_structuredextractionplaygrounditemid**
> PlaygroundItemResponse put_api_structured_extraction_structuredextractionprojectid_playground_structuredextractionplaygrounditemid(structured_extraction_project_id, structured_extraction_playground_item_id, create_or_update_playground_item_request)


Update a specific **Playground Item**.

#### Note:
 If the **Document** ownership scope does not match the **Project** ownership scope, the **Playground Item** update will fail.

#### Error Responses:
`404 Not Found` - If a **Playground Item** with the specified `playgroundItemId` associated with the given `projectId` does not exist, or if a **Document** with the specified `documentId` cannot be found.

`403 Forbidden` - If the user does not have permission to update this **Project**, use the specified **Document**, or the **Document** ownership scope does not match **Project** ownership scope.
  

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.create_or_update_playground_item_request import CreateOrUpdatePlaygroundItemRequest
from numind.models.playground_item_response import PlaygroundItemResponse
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
    api_instance = numind.openapi_client.StructuredExtractionPlaygroundApi(api_client)
    structured_extraction_project_id = 'structured_extraction_project_id_example' # str | Unique structured extraction project identifier.
    structured_extraction_playground_item_id = 'structured_extraction_playground_item_id_example' # str | Unique structured extraction playground item identifier.
    create_or_update_playground_item_request = {documentId=0d25d758-d475-4c14-aafa-eb5d6a40b670, result={orderId=Example: o-89123, customerId=Example: c-20485, orderDate=2024-03-10T11:15:00.000Z, status=shipped, totalAmount=149.99, currency=USD, items=[{productId=p-00876, quantity=1, unitPrice=79.99}, {productId=p-00321, quantity=2, unitPrice=35}], shippingAddress={street=782 Pine St, city=Austin, state=TX, country=USA, zip=73301}, comments=Leave package at the front door., deliveryPreferences=[no_signature_required, standard_delivery], estimatedDelivery=2024-03-15T17:00:00.000Z}, totalTokens=567, outputTokens=267, inputTokens=300} # CreateOrUpdatePlaygroundItemRequest | 

    try:
        api_response = api_instance.put_api_structured_extraction_structuredextractionprojectid_playground_structuredextractionplaygrounditemid(structured_extraction_project_id, structured_extraction_playground_item_id, create_or_update_playground_item_request)
        print("The response of StructuredExtractionPlaygroundApi->put_api_structured_extraction_structuredextractionprojectid_playground_structuredextractionplaygrounditemid:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StructuredExtractionPlaygroundApi->put_api_structured_extraction_structuredextractionprojectid_playground_structuredextractionplaygrounditemid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **structured_extraction_project_id** | **str**| Unique structured extraction project identifier. | 
 **structured_extraction_playground_item_id** | **str**| Unique structured extraction playground item identifier. | 
 **create_or_update_playground_item_request** | [**CreateOrUpdatePlaygroundItemRequest**](CreateOrUpdatePlaygroundItemRequest.md)|  | 

### Return type

[**PlaygroundItemResponse**](PlaygroundItemResponse.md)

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

