# numind.openapi_client.PlaygroundApi

All URIs are relative to *https://nuextract.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_api_projects_projectid_playground_playgrounditemid**](PlaygroundApi.md#delete_api_projects_projectid_playground_playgrounditemid) | **DELETE** /api/projects/{projectId}/playground/{playgroundItemId} | 
[**get_api_projects_projectid_playground**](PlaygroundApi.md#get_api_projects_projectid_playground) | **GET** /api/projects/{projectId}/playground | 
[**get_api_projects_projectid_playground_playgrounditemid**](PlaygroundApi.md#get_api_projects_projectid_playground_playgrounditemid) | **GET** /api/projects/{projectId}/playground/{playgroundItemId} | 
[**post_api_projects_projectid_playground**](PlaygroundApi.md#post_api_projects_projectid_playground) | **POST** /api/projects/{projectId}/playground | 
[**put_api_projects_projectid_playground_playgrounditemid**](PlaygroundApi.md#put_api_projects_projectid_playground_playgrounditemid) | **PUT** /api/projects/{projectId}/playground/{playgroundItemId} | 


# **delete_api_projects_projectid_playground_playgrounditemid**
> delete_api_projects_projectid_playground_playgrounditemid(project_id, playground_item_id)


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
    api_instance = numind.openapi_client.PlaygroundApi(api_client)
    project_id = 'project_id_example' # str | Unique project identifier.
    playground_item_id = 'playground_item_id_example' # str | Unique playground item identifier.

    try:
        api_instance.delete_api_projects_projectid_playground_playgrounditemid(project_id, playground_item_id)
    except Exception as e:
        print("Exception when calling PlaygroundApi->delete_api_projects_projectid_playground_playgrounditemid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Unique project identifier. | 
 **playground_item_id** | **str**| Unique playground item identifier. | 

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

# **get_api_projects_projectid_playground**
> List[PlaygroundItemResponse] get_api_projects_projectid_playground(project_id)


Return a list of **Playground Items** associated to the specified **Project**.

#### Error Responses:
`404 Not Found` - If a **Project** with the specified `projectId` does not exist.

`403 Forbidden` - If the user does not have permission to view this **Project**.
  

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.playground_item_response import PlaygroundItemResponse
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
    api_instance = numind.openapi_client.PlaygroundApi(api_client)
    project_id = 'project_id_example' # str | Unique project identifier.

    try:
        api_response = api_instance.get_api_projects_projectid_playground(project_id)
        print("The response of PlaygroundApi->get_api_projects_projectid_playground:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PlaygroundApi->get_api_projects_projectid_playground: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Unique project identifier. | 

### Return type

[**List[PlaygroundItemResponse]**](PlaygroundItemResponse.md)

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

# **get_api_projects_projectid_playground_playgrounditemid**
> PlaygroundItemResponse get_api_projects_projectid_playground_playgrounditemid(project_id, playground_item_id)


Return a specific **Playground Item**.

#### Error Responses:
`404 Not Found` - If a **Playground Item** with the specified `playgroundItemId` associated with the given `projectId` does not exist.

`403 Forbidden` - If the user does not have permission to view this **Project**.
  

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.playground_item_response import PlaygroundItemResponse
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
    api_instance = numind.openapi_client.PlaygroundApi(api_client)
    project_id = 'project_id_example' # str | Unique project identifier.
    playground_item_id = 'playground_item_id_example' # str | Unique playground item identifier.

    try:
        api_response = api_instance.get_api_projects_projectid_playground_playgrounditemid(project_id, playground_item_id)
        print("The response of PlaygroundApi->get_api_projects_projectid_playground_playgrounditemid:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PlaygroundApi->get_api_projects_projectid_playground_playgrounditemid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Unique project identifier. | 
 **playground_item_id** | **str**| Unique playground item identifier. | 

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

# **post_api_projects_projectid_playground**
> PlaygroundItemResponse post_api_projects_projectid_playground(project_id, create_or_update_playground_item_request)


Create a new **Playground Item** associated to the specified **Project**.

#### Error Responses:
`404 Not Found` - If a **Project** with the specified `projectId` does not exist or a **Document** with the specified `documentId` does not exist.

`403 Forbidden` - If the user does not have permission to update this **Project** or use the specified **Document**.
  

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.create_or_update_playground_item_request import CreateOrUpdatePlaygroundItemRequest
from numind.openapi_client.models.playground_item_response import PlaygroundItemResponse
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
    api_instance = numind.openapi_client.PlaygroundApi(api_client)
    project_id = 'project_id_example' # str | Unique project identifier.
    create_or_update_playground_item_request = {"documentId":"0d25d758-d475-4c14-aafa-eb5d6a40b670","result":{"orderId":"Example: o-89123","customerId":"Example: c-20485","orderDate":"2024-03-10T11:15:00.000Z","status":"shipped","totalAmount":149.99,"currency":"USD","items":[{"productId":"p-00876","quantity":1,"unitPrice":79.99},{"productId":"p-00321","quantity":2,"unitPrice":35}],"shippingAddress":{"street":"782 Pine St","city":"Austin","state":"TX","country":"USA","zip":"73301"},"comments":"Leave package at the front door.","deliveryPreferences":["no_signature_required","standard_delivery"],"estimatedDelivery":"2024-03-15T17:00:00.000Z"},"totalTokens":567,"completionTokens":267,"promptTokens":300} # CreateOrUpdatePlaygroundItemRequest | 

    try:
        api_response = api_instance.post_api_projects_projectid_playground(project_id, create_or_update_playground_item_request)
        print("The response of PlaygroundApi->post_api_projects_projectid_playground:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PlaygroundApi->post_api_projects_projectid_playground: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Unique project identifier. | 
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

# **put_api_projects_projectid_playground_playgrounditemid**
> PlaygroundItemResponse put_api_projects_projectid_playground_playgrounditemid(project_id, playground_item_id, create_or_update_playground_item_request)


Update a specific **Playground Item**.

#### Error Responses:
`404 Not Found` - If a **Playground Item** with the specified `playgroundItemId` associated with the given `projectId` does not exist, or if a **Document** with the specified `documentId` cannot be found.

`403 Forbidden` - If the user does not have permission to update this **Project** or use the specified **Document**.
  

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.create_or_update_playground_item_request import CreateOrUpdatePlaygroundItemRequest
from numind.openapi_client.models.playground_item_response import PlaygroundItemResponse
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
    api_instance = numind.openapi_client.PlaygroundApi(api_client)
    project_id = 'project_id_example' # str | Unique project identifier.
    playground_item_id = 'playground_item_id_example' # str | Unique playground item identifier.
    create_or_update_playground_item_request = {documentId=0d25d758-d475-4c14-aafa-eb5d6a40b670, result={orderId=Example: o-89123, customerId=Example: c-20485, orderDate=2024-03-10T11:15:00.000Z, status=shipped, totalAmount=149.99, currency=USD, items=[{productId=p-00876, quantity=1, unitPrice=79.99}, {productId=p-00321, quantity=2, unitPrice=35}], shippingAddress={street=782 Pine St, city=Austin, state=TX, country=USA, zip=73301}, comments=Leave package at the front door., deliveryPreferences=[no_signature_required, standard_delivery], estimatedDelivery=2024-03-15T17:00:00.000Z}, totalTokens=567, completionTokens=267, promptTokens=300} # CreateOrUpdatePlaygroundItemRequest | 

    try:
        api_response = api_instance.put_api_projects_projectid_playground_playgrounditemid(project_id, playground_item_id, create_or_update_playground_item_request)
        print("The response of PlaygroundApi->put_api_projects_projectid_playground_playgrounditemid:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PlaygroundApi->put_api_projects_projectid_playground_playgrounditemid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Unique project identifier. | 
 **playground_item_id** | **str**| Unique playground item identifier. | 
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

