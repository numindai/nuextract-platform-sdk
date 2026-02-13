# numind.openapi_client.StructuredExtractionProjectManagementApi

All URIs are relative to *https://nuextract.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_api_structured_extraction_structuredextractionprojectid**](StructuredExtractionProjectManagementApi.md#delete_api_structured_extraction_structuredextractionprojectid) | **DELETE** /api/structured-extraction/{structuredExtractionProjectId} | 
[**get_api_structured_extraction**](StructuredExtractionProjectManagementApi.md#get_api_structured_extraction) | **GET** /api/structured-extraction | 
[**get_api_structured_extraction_structuredextractionprojectid**](StructuredExtractionProjectManagementApi.md#get_api_structured_extraction_structuredextractionprojectid) | **GET** /api/structured-extraction/{structuredExtractionProjectId} | 
[**patch_api_structured_extraction_structuredextractionprojectid**](StructuredExtractionProjectManagementApi.md#patch_api_structured_extraction_structuredextractionprojectid) | **PATCH** /api/structured-extraction/{structuredExtractionProjectId} | 
[**patch_api_structured_extraction_structuredextractionprojectid_settings**](StructuredExtractionProjectManagementApi.md#patch_api_structured_extraction_structuredextractionprojectid_settings) | **PATCH** /api/structured-extraction/{structuredExtractionProjectId}/settings | 
[**post_api_structured_extraction**](StructuredExtractionProjectManagementApi.md#post_api_structured_extraction) | **POST** /api/structured-extraction | 
[**post_api_structured_extraction_structuredextractionprojectid_lock**](StructuredExtractionProjectManagementApi.md#post_api_structured_extraction_structuredextractionprojectid_lock) | **POST** /api/structured-extraction/{structuredExtractionProjectId}/lock | 
[**post_api_structured_extraction_structuredextractionprojectid_reset_settings**](StructuredExtractionProjectManagementApi.md#post_api_structured_extraction_structuredextractionprojectid_reset_settings) | **POST** /api/structured-extraction/{structuredExtractionProjectId}/reset-settings | 
[**post_api_structured_extraction_structuredextractionprojectid_unlock**](StructuredExtractionProjectManagementApi.md#post_api_structured_extraction_structuredextractionprojectid_unlock) | **POST** /api/structured-extraction/{structuredExtractionProjectId}/unlock | 


# **delete_api_structured_extraction_structuredextractionprojectid**
> delete_api_structured_extraction_structuredextractionprojectid(structured_extraction_project_id)


Permanently remove a **Project** and all related data.


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
    structured_extraction_project_id = 'structured_extraction_project_id_example' # str | Unique structured extraction project identifier.

    try:
        api_instance.delete_api_structured_extraction_structuredextractionprojectid(structured_extraction_project_id)
    except Exception as e:
        print("Exception when calling StructuredExtractionProjectManagementApi->delete_api_structured_extraction_structuredextractionprojectid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **structured_extraction_project_id** | **str**| Unique structured extraction project identifier. | 

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
> List[ProjectResponse] get_api_structured_extraction(organization_id=organization_id, reference=reference)


Return a list of **Projects** accessible to the authenticated user.

#### Error Responses:
`403 Forbidden` - If the user attempts to access an unauthorized organization.
  

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.project_response import ProjectResponse
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
    organization_id = 'organization_id_example' # str | Optional organization identifier.   When specified, projects of the given organization are returned instead of personal projects.   This parameter is ignored if ***reference=true***. (optional)
    reference = True # bool | If **true**, only reference projects are returned. (optional)

    try:
        api_response = api_instance.get_api_structured_extraction(organization_id=organization_id, reference=reference)
        print("The response of StructuredExtractionProjectManagementApi->get_api_structured_extraction:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StructuredExtractionProjectManagementApi->get_api_structured_extraction: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_id** | **str**| Optional organization identifier.   When specified, projects of the given organization are returned instead of personal projects.   This parameter is ignored if ***reference&#x3D;true***. | [optional] 
 **reference** | **bool**| If **true**, only reference projects are returned. | [optional] 

### Return type

[**List[ProjectResponse]**](ProjectResponse.md)

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

# **get_api_structured_extraction_structuredextractionprojectid**
> ProjectResponse get_api_structured_extraction_structuredextractionprojectid(structured_extraction_project_id)


Return the details of a specific **Project**.

#### Error Responses:
`404 Not Found` - If a **Project** with the specified `projectId` does not exist.

`403 Forbidden` - If the user does not have permission to view this **Project**.
  

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.project_response import ProjectResponse
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
    structured_extraction_project_id = 'structured_extraction_project_id_example' # str | Unique structured extraction project identifier.

    try:
        api_response = api_instance.get_api_structured_extraction_structuredextractionprojectid(structured_extraction_project_id)
        print("The response of StructuredExtractionProjectManagementApi->get_api_structured_extraction_structuredextractionprojectid:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StructuredExtractionProjectManagementApi->get_api_structured_extraction_structuredextractionprojectid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **structured_extraction_project_id** | **str**| Unique structured extraction project identifier. | 

### Return type

[**ProjectResponse**](ProjectResponse.md)

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

# **patch_api_structured_extraction_structuredextractionprojectid**
> ProjectResponse patch_api_structured_extraction_structuredextractionprojectid(structured_extraction_project_id, update_project_request)


Update the details of an existing **Project**.


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
from numind.models.project_response import ProjectResponse
from numind.models.update_project_request import UpdateProjectRequest
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
    structured_extraction_project_id = 'structured_extraction_project_id_example' # str | Unique structured extraction project identifier.
    update_project_request = {"template":{"orderId":"verbatim-string","customerId":"verbatim-string","orderDate":"date-time","status":["pending","processed","shipped","delivered","cancelled"],"totalAmount":"number","currency":"string","items":[{"productId":"string","quantity":"number","unitPrice":"number"}],"shippingAddress":{"street":"string","city":"string","state":"string","country":"string","zip":"string"},"comments":"string","deliveryPreferences":[["contactless_delivery","signature_required","leave_at_door","pickup_from_store","deliver_to_neighbor","schedule_delivery"]],"estimatedDelivery":"date-time"}} # UpdateProjectRequest | 

    try:
        api_response = api_instance.patch_api_structured_extraction_structuredextractionprojectid(structured_extraction_project_id, update_project_request)
        print("The response of StructuredExtractionProjectManagementApi->patch_api_structured_extraction_structuredextractionprojectid:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StructuredExtractionProjectManagementApi->patch_api_structured_extraction_structuredextractionprojectid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **structured_extraction_project_id** | **str**| Unique structured extraction project identifier. | 
 **update_project_request** | [**UpdateProjectRequest**](UpdateProjectRequest.md)|  | 

### Return type

[**ProjectResponse**](ProjectResponse.md)

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

# **patch_api_structured_extraction_structuredextractionprojectid_settings**
> ProjectResponse patch_api_structured_extraction_structuredextractionprojectid_settings(structured_extraction_project_id, update_project_settings_request)


Update the settings of an existing **Project**.


#### Error Responses:
`404 Not Found` - If a **Project** with the specified `projectId` does not exist.

`403 Forbidden` - If the user does not have permission to update this **Project**.

`403 Locked` - If the **Project** is locked.
  

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.project_response import ProjectResponse
from numind.models.update_project_settings_request import UpdateProjectSettingsRequest
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
    structured_extraction_project_id = 'structured_extraction_project_id_example' # str | Unique structured extraction project identifier.
    update_project_settings_request = {"temperature":0,"rasterizationDPI":170,"maxOutputTokens":0,"degradedMode":"Reject","maxExampleTokenNumber":90000,"maxExampleNumber":0,"minExampleSimilarity":0} # UpdateProjectSettingsRequest | 

    try:
        api_response = api_instance.patch_api_structured_extraction_structuredextractionprojectid_settings(structured_extraction_project_id, update_project_settings_request)
        print("The response of StructuredExtractionProjectManagementApi->patch_api_structured_extraction_structuredextractionprojectid_settings:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StructuredExtractionProjectManagementApi->patch_api_structured_extraction_structuredextractionprojectid_settings: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **structured_extraction_project_id** | **str**| Unique structured extraction project identifier. | 
 **update_project_settings_request** | [**UpdateProjectSettingsRequest**](UpdateProjectSettingsRequest.md)|  | 

### Return type

[**ProjectResponse**](ProjectResponse.md)

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
> ProjectResponse post_api_structured_extraction(create_project_request)


Create a new **Project** to define an extraction task.

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
from numind.models.create_project_request import CreateProjectRequest
from numind.models.project_response import ProjectResponse
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
    create_project_request = {"name":"Example: Order Delivery Information Extraction","description":"Example: Automated extraction of order delivery details from emails and scanned documents","template":{"orderId":"verbatim-string","customerId":"verbatim-string","orderDate":"date-time","status":["pending","processed","shipped","delivered","cancelled"],"totalAmount":"number","currency":"string","items":[{"productId":"string","quantity":"number","unitPrice":"number"}],"shippingAddress":{"street":"string","city":"string","state":"string","country":"string","zip":"string"},"comments":"string","deliveryPreferences":[["contactless_delivery","signature_required","leave_at_door","pickup_from_store","deliver_to_neighbor","schedule_delivery"]],"estimatedDelivery":"date-time"},"instructions":"[EXAMPLE ONLY] Orders are most likely in the US."} # CreateProjectRequest | 

    try:
        api_response = api_instance.post_api_structured_extraction(create_project_request)
        print("The response of StructuredExtractionProjectManagementApi->post_api_structured_extraction:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StructuredExtractionProjectManagementApi->post_api_structured_extraction: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_project_request** | [**CreateProjectRequest**](CreateProjectRequest.md)|  | 

### Return type

[**ProjectResponse**](ProjectResponse.md)

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

# **post_api_structured_extraction_structuredextractionprojectid_lock**
> post_api_structured_extraction_structuredextractionprojectid_lock(structured_extraction_project_id)

Locks a project to prevent modifications.


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
    structured_extraction_project_id = 'structured_extraction_project_id_example' # str | Unique structured extraction project identifier.

    try:
        api_instance.post_api_structured_extraction_structuredextractionprojectid_lock(structured_extraction_project_id)
    except Exception as e:
        print("Exception when calling StructuredExtractionProjectManagementApi->post_api_structured_extraction_structuredextractionprojectid_lock: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **structured_extraction_project_id** | **str**| Unique structured extraction project identifier. | 

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

# **post_api_structured_extraction_structuredextractionprojectid_reset_settings**
> ProjectResponse post_api_structured_extraction_structuredextractionprojectid_reset_settings(structured_extraction_project_id)


Reset the settings of an existing **Project** to their default values.

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
from numind.models.project_response import ProjectResponse
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
    structured_extraction_project_id = 'structured_extraction_project_id_example' # str | Unique structured extraction project identifier.

    try:
        api_response = api_instance.post_api_structured_extraction_structuredextractionprojectid_reset_settings(structured_extraction_project_id)
        print("The response of StructuredExtractionProjectManagementApi->post_api_structured_extraction_structuredextractionprojectid_reset_settings:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StructuredExtractionProjectManagementApi->post_api_structured_extraction_structuredextractionprojectid_reset_settings: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **structured_extraction_project_id** | **str**| Unique structured extraction project identifier. | 

### Return type

[**ProjectResponse**](ProjectResponse.md)

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

# **post_api_structured_extraction_structuredextractionprojectid_unlock**
> post_api_structured_extraction_structuredextractionprojectid_unlock(structured_extraction_project_id)


Unlock a **Project**.

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
    structured_extraction_project_id = 'structured_extraction_project_id_example' # str | Unique structured extraction project identifier.

    try:
        api_instance.post_api_structured_extraction_structuredextractionprojectid_unlock(structured_extraction_project_id)
    except Exception as e:
        print("Exception when calling StructuredExtractionProjectManagementApi->post_api_structured_extraction_structuredextractionprojectid_unlock: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **structured_extraction_project_id** | **str**| Unique structured extraction project identifier. | 

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

