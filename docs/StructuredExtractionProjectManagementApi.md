# numind.openapi_client.StructuredExtractionProjectManagementApi

All URIs are relative to *https://nuextract.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_api_structured_extraction_structuredprojectid**](StructuredExtractionProjectManagementApi.md#delete_api_structured_extraction_structuredprojectid) | **DELETE** /api/structured-extraction/{structuredProjectId} | 
[**get_api_structured_extraction**](StructuredExtractionProjectManagementApi.md#get_api_structured_extraction) | **GET** /api/structured-extraction | 
[**get_api_structured_extraction_structuredprojectid**](StructuredExtractionProjectManagementApi.md#get_api_structured_extraction_structuredprojectid) | **GET** /api/structured-extraction/{structuredProjectId} | 
[**patch_api_structured_extraction_structuredprojectid**](StructuredExtractionProjectManagementApi.md#patch_api_structured_extraction_structuredprojectid) | **PATCH** /api/structured-extraction/{structuredProjectId} | 
[**patch_api_structured_extraction_structuredprojectid_settings**](StructuredExtractionProjectManagementApi.md#patch_api_structured_extraction_structuredprojectid_settings) | **PATCH** /api/structured-extraction/{structuredProjectId}/settings | 
[**post_api_structured_extraction**](StructuredExtractionProjectManagementApi.md#post_api_structured_extraction) | **POST** /api/structured-extraction | 
[**post_api_structured_extraction_structuredprojectid_duplicate**](StructuredExtractionProjectManagementApi.md#post_api_structured_extraction_structuredprojectid_duplicate) | **POST** /api/structured-extraction/{structuredProjectId}/duplicate | 
[**post_api_structured_extraction_structuredprojectid_lock**](StructuredExtractionProjectManagementApi.md#post_api_structured_extraction_structuredprojectid_lock) | **POST** /api/structured-extraction/{structuredProjectId}/lock | 
[**post_api_structured_extraction_structuredprojectid_reset_settings**](StructuredExtractionProjectManagementApi.md#post_api_structured_extraction_structuredprojectid_reset_settings) | **POST** /api/structured-extraction/{structuredProjectId}/reset-settings | 
[**post_api_structured_extraction_structuredprojectid_share**](StructuredExtractionProjectManagementApi.md#post_api_structured_extraction_structuredprojectid_share) | **POST** /api/structured-extraction/{structuredProjectId}/share | 
[**post_api_structured_extraction_structuredprojectid_unlock**](StructuredExtractionProjectManagementApi.md#post_api_structured_extraction_structuredprojectid_unlock) | **POST** /api/structured-extraction/{structuredProjectId}/unlock | 
[**post_api_structured_extraction_structuredprojectid_unshare**](StructuredExtractionProjectManagementApi.md#post_api_structured_extraction_structuredprojectid_unshare) | **POST** /api/structured-extraction/{structuredProjectId}/unshare | 


# **delete_api_structured_extraction_structuredprojectid**
> delete_api_structured_extraction_structuredprojectid(structured_project_id, x_organization_id=x_organization_id)


Permanently remove a **Structured Extraction Project** and all related data.


#### Effect:
Deletes the **Project** together with the associated **Examples** and **Playground** items.


#### Error Responses:
`404 Not Found` - If a **Project** with the specified projectId does not exist.

`403 Forbidden` - If the user does not have permission to delete this **Project**.

`403 Locked` - If the **Project** is locked.
  

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
    api_instance = numind.openapi_client.StructuredExtractionProjectManagementApi(api_client)
    structured_project_id = 'structured_project_id_example' # str | Unique structured extraction project identifier.
    x_organization_id = 'x_organization_id_example' # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)

    try:
        api_instance.delete_api_structured_extraction_structuredprojectid(structured_project_id, x_organization_id=x_organization_id)
    except Exception as e:
        print("Exception when calling StructuredExtractionProjectManagementApi->delete_api_structured_extraction_structuredprojectid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **structured_project_id** | **str**| Unique structured extraction project identifier. | 
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 

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

# **get_api_structured_extraction**
> List[StructuredProjectResponse] get_api_structured_extraction(x_organization_id=x_organization_id, reference=reference)


Return a list of **Structured Extraction Projects** accessible to the authenticated user.

#### Error Responses:
`403 Forbidden` - If the user attempts to access an unauthorized organization.
  

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.structured_project_response import StructuredProjectResponse
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
    api_instance = numind.openapi_client.StructuredExtractionProjectManagementApi(api_client)
    x_organization_id = 'x_organization_id_example' # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)
    reference = True # bool | If **true**, only reference projects are returned. (optional)

    try:
        api_response = api_instance.get_api_structured_extraction(x_organization_id=x_organization_id, reference=reference)
        print("The response of StructuredExtractionProjectManagementApi->get_api_structured_extraction:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StructuredExtractionProjectManagementApi->get_api_structured_extraction: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 
 **reference** | **bool**| If **true**, only reference projects are returned. | [optional] 

### Return type

[**List[StructuredProjectResponse]**](StructuredProjectResponse.md)

### Authorization

[oauth2Auth](../README.md#oauth2Auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, text/plain

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**400** | Invalid value for: query parameter reference |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_api_structured_extraction_structuredprojectid**
> StructuredProjectResponse get_api_structured_extraction_structuredprojectid(structured_project_id, x_organization_id=x_organization_id)


Return the details of a specific **Structured Extraction Project**.

#### Error Responses:
`404 Not Found` - If a **Project** with the specified `projectId` does not exist.

`403 Forbidden` - If the user does not have permission to view this **Project**.
  

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.structured_project_response import StructuredProjectResponse
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
    api_instance = numind.openapi_client.StructuredExtractionProjectManagementApi(api_client)
    structured_project_id = 'structured_project_id_example' # str | Unique structured extraction project identifier.
    x_organization_id = 'x_organization_id_example' # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)

    try:
        api_response = api_instance.get_api_structured_extraction_structuredprojectid(structured_project_id, x_organization_id=x_organization_id)
        print("The response of StructuredExtractionProjectManagementApi->get_api_structured_extraction_structuredprojectid:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StructuredExtractionProjectManagementApi->get_api_structured_extraction_structuredprojectid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **structured_project_id** | **str**| Unique structured extraction project identifier. | 
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 

### Return type

[**StructuredProjectResponse**](StructuredProjectResponse.md)

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

# **patch_api_structured_extraction_structuredprojectid**
> StructuredProjectResponse patch_api_structured_extraction_structuredprojectid(structured_project_id, update_structured_project_request, x_organization_id=x_organization_id)


Update the details of an existing **Structured Extraction Project**.


Note that you cannot change the lock or reference (shared) status via this endpoint.
To modify these states, use the lock/unlock and share/unshare project endpoints.

#### Error Responses:
`404 Not Found` - If a **Project** with the specified `projectId` does not exist.

`403 Forbidden` - If the user does not have permission to update this **Project**.

`403 Locked` - If the **Project** is locked.
  

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.structured_project_response import StructuredProjectResponse
from numind.models.update_structured_project_request import UpdateStructuredProjectRequest
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
    api_instance = numind.openapi_client.StructuredExtractionProjectManagementApi(api_client)
    structured_project_id = 'structured_project_id_example' # str | Unique structured extraction project identifier.
    update_structured_project_request = {"template":{"orderId":"verbatim-string","customerId":"verbatim-string","orderDate":"date-time","status":["pending","processed","shipped","delivered","cancelled"],"totalAmount":"number","currency":"string","items":[{"productId":"string","quantity":"number","unitPrice":"number"}],"shippingAddress":{"street":"string","city":"string","state":"string","country":"string","zip":"string"},"comments":"string","deliveryPreferences":[["contactless_delivery","signature_required","leave_at_door","pickup_from_store","deliver_to_neighbor","schedule_delivery"]],"estimatedDelivery":"date-time"}} # UpdateStructuredProjectRequest | 
    x_organization_id = 'x_organization_id_example' # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)

    try:
        api_response = api_instance.patch_api_structured_extraction_structuredprojectid(structured_project_id, update_structured_project_request, x_organization_id=x_organization_id)
        print("The response of StructuredExtractionProjectManagementApi->patch_api_structured_extraction_structuredprojectid:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StructuredExtractionProjectManagementApi->patch_api_structured_extraction_structuredprojectid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **structured_project_id** | **str**| Unique structured extraction project identifier. | 
 **update_structured_project_request** | [**UpdateStructuredProjectRequest**](UpdateStructuredProjectRequest.md)|  | 
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 

### Return type

[**StructuredProjectResponse**](StructuredProjectResponse.md)

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

# **patch_api_structured_extraction_structuredprojectid_settings**
> StructuredProjectResponse patch_api_structured_extraction_structuredprojectid_settings(structured_project_id, update_structured_project_settings_request, x_organization_id=x_organization_id)


Update the settings of an existing **Structured Extraction Project**.


#### Error Responses:
`404 Not Found` - If a **Project** with the specified `projectId` does not exist.

`403 Forbidden` - If the user does not have permission to update this **Project**.

`403 Locked` - If the **Project** is locked.
  

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.structured_project_response import StructuredProjectResponse
from numind.models.update_structured_project_settings_request import UpdateStructuredProjectSettingsRequest
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
    api_instance = numind.openapi_client.StructuredExtractionProjectManagementApi(api_client)
    structured_project_id = 'structured_project_id_example' # str | Unique structured extraction project identifier.
    update_structured_project_settings_request = {"temperature":0,"rasterizationDPI":170,"maxOutputTokens":0,"degradedMode":"Reject","maxExampleTokenNumber":90000,"maxExampleNumber":0,"minExampleSimilarity":0,"enableThinking":false} # UpdateStructuredProjectSettingsRequest | 
    x_organization_id = 'x_organization_id_example' # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)

    try:
        api_response = api_instance.patch_api_structured_extraction_structuredprojectid_settings(structured_project_id, update_structured_project_settings_request, x_organization_id=x_organization_id)
        print("The response of StructuredExtractionProjectManagementApi->patch_api_structured_extraction_structuredprojectid_settings:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StructuredExtractionProjectManagementApi->patch_api_structured_extraction_structuredprojectid_settings: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **structured_project_id** | **str**| Unique structured extraction project identifier. | 
 **update_structured_project_settings_request** | [**UpdateStructuredProjectSettingsRequest**](UpdateStructuredProjectSettingsRequest.md)|  | 
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 

### Return type

[**StructuredProjectResponse**](StructuredProjectResponse.md)

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

# **post_api_structured_extraction**
> StructuredProjectResponse post_api_structured_extraction(create_structured_project_request, x_organization_id=x_organization_id)


Create a new **Structured Extraction Project** to define an extraction task.

#### Body Fields:

 Name | Description |
------|-------------|
 `name` | Name of the **Project**. |
 `template` | Template of the **Project**. |
 `description` | Text description of the **Project** (can be left empty). |
 `ownerOrganization` | Optional organization identifier. When specified, the project will belong to the given organization instead of being a personal project. |

#### Effect:
A **Project** is created with default settings:

 Setting | Default |
---------|---------|
 `temperature` | 0.0 |
 `rasterizationDPI` | 170|
 `maxOutputTokens` | 0 (no limit) |
 `degradedMode` (deprecated) | Reject|
 `maxExampleTokenNumber` (former `maxTokensSmartExample`) | 90000|


If *ownerOrganization* is not provided, the **Project** will be owned by the authenticated user.
When created, a **Project** is not locked and is owned by the authenticated user and the organization (if specified in the request).

#### Response:
 The response contains `projectId`, which
 is required to modify the **Project**, perform CRUD operations on project **Examples** and
 project **Playground** items, and run inference for this **Project**.
  

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.create_structured_project_request import CreateStructuredProjectRequest
from numind.models.structured_project_response import StructuredProjectResponse
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
    api_instance = numind.openapi_client.StructuredExtractionProjectManagementApi(api_client)
    create_structured_project_request = {"name":"Example: Order Delivery Information Extraction","description":"Example: Automated extraction of order delivery details from emails and scanned documents","template":{"orderId":"verbatim-string","customerId":"verbatim-string","orderDate":"date-time","status":["pending","processed","shipped","delivered","cancelled"],"totalAmount":"number","currency":"string","items":[{"productId":"string","quantity":"number","unitPrice":"number"}],"shippingAddress":{"street":"string","city":"string","state":"string","country":"string","zip":"string"},"comments":"string","deliveryPreferences":[["contactless_delivery","signature_required","leave_at_door","pickup_from_store","deliver_to_neighbor","schedule_delivery"]],"estimatedDelivery":"date-time"},"instructions":"[EXAMPLE ONLY] Orders are most likely in the US."} # CreateStructuredProjectRequest | 
    x_organization_id = 'x_organization_id_example' # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)

    try:
        api_response = api_instance.post_api_structured_extraction(create_structured_project_request, x_organization_id=x_organization_id)
        print("The response of StructuredExtractionProjectManagementApi->post_api_structured_extraction:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StructuredExtractionProjectManagementApi->post_api_structured_extraction: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_structured_project_request** | [**CreateStructuredProjectRequest**](CreateStructuredProjectRequest.md)|  | 
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 

### Return type

[**StructuredProjectResponse**](StructuredProjectResponse.md)

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

# **post_api_structured_extraction_structuredprojectid_duplicate**
> StructuredProjectResponse post_api_structured_extraction_structuredprojectid_duplicate(structured_project_id, x_organization_id=x_organization_id, organization_id=organization_id)


Create a copy of an existing **Structured Extraction Project**.

It is allowed to duplicate locked **Projects** and **Reference Projects**.


#### Effect:
- The duplicated **Project** retains the same template, settings, **Examples** and **Playground Items**.
- If the target organization is the same as the source, the project name is changed to "Original Name (copy)".
- If the target organization is different from the source, all **Documents** associated with the **Project** are copied.

#### Response:
 The response contains a newly generated
 `projectId`. When duplicated, a new **Project** is always unlocked. The duplicated **Reference Project**
 are private and owned by the authenticated user.

#### Error Responses:
`404 Not Found` - If a **Project** with the specified `projectId` does not exist.

`403 Forbidden` - If the user does not have permission to duplicate this **Project**.


### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.structured_project_response import StructuredProjectResponse
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
    api_instance = numind.openapi_client.StructuredExtractionProjectManagementApi(api_client)
    structured_project_id = 'structured_project_id_example' # str | Unique structured extraction project identifier.
    x_organization_id = 'x_organization_id_example' # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)
    organization_id = 'organization_id_example' # str | Destination organization id. If not specified, the project is copied to the user projects. (optional)

    try:
        api_response = api_instance.post_api_structured_extraction_structuredprojectid_duplicate(structured_project_id, x_organization_id=x_organization_id, organization_id=organization_id)
        print("The response of StructuredExtractionProjectManagementApi->post_api_structured_extraction_structuredprojectid_duplicate:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StructuredExtractionProjectManagementApi->post_api_structured_extraction_structuredprojectid_duplicate: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **structured_project_id** | **str**| Unique structured extraction project identifier. | 
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 
 **organization_id** | **str**| Destination organization id. If not specified, the project is copied to the user projects. | [optional] 

### Return type

[**StructuredProjectResponse**](StructuredProjectResponse.md)

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

# **post_api_structured_extraction_structuredprojectid_lock**
> post_api_structured_extraction_structuredprojectid_lock(structured_project_id, x_organization_id=x_organization_id)

Locks a **Structured Extraction Project** to prevent modifications.


#### Effect:
- While locked, the **Project** cannot be updated or deleted. Read access is still available.
- CRUD operations on **Examples** are not allowed.
- Inference is still allowed.
- CRUD access to **Playground Items** is still available.

#### Error Responses:
 `404 Not Found` - If a **Project** with the specified `projectId` does not exist.

 `403 Forbidden` - If the user does not have permission to lock this project.


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
    api_instance = numind.openapi_client.StructuredExtractionProjectManagementApi(api_client)
    structured_project_id = 'structured_project_id_example' # str | Unique structured extraction project identifier.
    x_organization_id = 'x_organization_id_example' # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)

    try:
        api_instance.post_api_structured_extraction_structuredprojectid_lock(structured_project_id, x_organization_id=x_organization_id)
    except Exception as e:
        print("Exception when calling StructuredExtractionProjectManagementApi->post_api_structured_extraction_structuredprojectid_lock: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **structured_project_id** | **str**| Unique structured extraction project identifier. | 
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 

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

# **post_api_structured_extraction_structuredprojectid_reset_settings**
> StructuredProjectResponse post_api_structured_extraction_structuredprojectid_reset_settings(structured_project_id, x_organization_id=x_organization_id)


Reset the settings of an existing **Structured Extraction Project** to their default values.

Default values are:

 Setting | Default |
-----------|---------|
 `temperature` | 0.0 |
 `rasterizationDPI` | 170|
 `maxOutputTokens` | 0 (no limit) |
 `degradedMode`  (deprecated) | Reject|
 `maxExampleTokenNumber` (former `maxTokensSmartExample`) | 90000|

#### Error Responses:
`404 Not Found` - If a **Project** with the specified `projectId` does not exist.

`403 Forbidden` - If the user does not have permission to update this **Project**.

`403 Locked` - If the **Project** is locked.
  

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.structured_project_response import StructuredProjectResponse
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
    api_instance = numind.openapi_client.StructuredExtractionProjectManagementApi(api_client)
    structured_project_id = 'structured_project_id_example' # str | Unique structured extraction project identifier.
    x_organization_id = 'x_organization_id_example' # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)

    try:
        api_response = api_instance.post_api_structured_extraction_structuredprojectid_reset_settings(structured_project_id, x_organization_id=x_organization_id)
        print("The response of StructuredExtractionProjectManagementApi->post_api_structured_extraction_structuredprojectid_reset_settings:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StructuredExtractionProjectManagementApi->post_api_structured_extraction_structuredprojectid_reset_settings: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **structured_project_id** | **str**| Unique structured extraction project identifier. | 
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 

### Return type

[**StructuredProjectResponse**](StructuredProjectResponse.md)

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

# **post_api_structured_extraction_structuredprojectid_share**
> post_api_structured_extraction_structuredprojectid_share(structured_project_id, x_organization_id=x_organization_id)


Turn an existing **Structured Extraction Project** into a **Reference Project**.
 Only NuMind administrators can share a **Project** with other users.
 Lock state does not prevent sharing. Likewise, sharing does not change the lock state.

#### Effect:

- **Reference Projects** are shared with the community (read access is granted to all users).
- **Project Examples** and **Playground Items** are shared as well.
- Only NuMind administrators can update or delete **Reference Projects**.
- Only NuMind administrators can create, update, or delete **Examples** and **Playground Items** of **Reference Projects**.
- The inference is allowed for all users.

#### Error Responses:

`404 Not Found` - If a **Project** with the specified `projectId` does not exist.

`403 Forbidden` - If the user does not have permission to share projects (not NuMind admin).


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
    api_instance = numind.openapi_client.StructuredExtractionProjectManagementApi(api_client)
    structured_project_id = 'structured_project_id_example' # str | Unique structured extraction project identifier.
    x_organization_id = 'x_organization_id_example' # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)

    try:
        api_instance.post_api_structured_extraction_structuredprojectid_share(structured_project_id, x_organization_id=x_organization_id)
    except Exception as e:
        print("Exception when calling StructuredExtractionProjectManagementApi->post_api_structured_extraction_structuredprojectid_share: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **structured_project_id** | **str**| Unique structured extraction project identifier. | 
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 

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

# **post_api_structured_extraction_structuredprojectid_unlock**
> post_api_structured_extraction_structuredprojectid_unlock(structured_project_id, x_organization_id=x_organization_id)


Unlock a **Structured Extraction Project**.

#### Effect:
- Once unlocked, the **Project** can be updated or deleted.
- Full CRUD access to **Examples** is restored.

#### Error Responses:
`404 Not Found` - If a **Project** with the specified `projectId` does not exist.

`403 Forbidden` - If the user does not have permission to unlock this project.


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
    api_instance = numind.openapi_client.StructuredExtractionProjectManagementApi(api_client)
    structured_project_id = 'structured_project_id_example' # str | Unique structured extraction project identifier.
    x_organization_id = 'x_organization_id_example' # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)

    try:
        api_instance.post_api_structured_extraction_structuredprojectid_unlock(structured_project_id, x_organization_id=x_organization_id)
    except Exception as e:
        print("Exception when calling StructuredExtractionProjectManagementApi->post_api_structured_extraction_structuredprojectid_unlock: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **structured_project_id** | **str**| Unique structured extraction project identifier. | 
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 

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

# **post_api_structured_extraction_structuredprojectid_unshare**
> post_api_structured_extraction_structuredprojectid_unshare(structured_project_id, x_organization_id=x_organization_id)


Unshare a **Reference Project** (makes it private).

 Lock state does not prevent unsharing. Likewise, unsharing does not change the lock state.
 The project owner is the initial owner, not the authenicated user.


#### Effect:
- The **Project** is no longer a **Reference Project** and is no longer shared with the community.
- Read access is revoked for all users except the project owner.
- **Examples** and **Playground Items** are no longer publicly accessible.
- Only the project owner can manage or delete the project after unsharing.
- Inference is restricted to the project owner.

#### Error Responses:
`404 Not Found` - If a **Project** with the specified `projectId` does not exist.

`403 Forbidden` - If the user does not have permission to unshare projects (not NuMind admin).


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
    api_instance = numind.openapi_client.StructuredExtractionProjectManagementApi(api_client)
    structured_project_id = 'structured_project_id_example' # str | Unique structured extraction project identifier.
    x_organization_id = 'x_organization_id_example' # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)

    try:
        api_instance.post_api_structured_extraction_structuredprojectid_unshare(structured_project_id, x_organization_id=x_organization_id)
    except Exception as e:
        print("Exception when calling StructuredExtractionProjectManagementApi->post_api_structured_extraction_structuredprojectid_unshare: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **structured_project_id** | **str**| Unique structured extraction project identifier. | 
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 

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

