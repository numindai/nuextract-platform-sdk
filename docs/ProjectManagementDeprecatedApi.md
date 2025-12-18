# numind.openapi_client.ProjectManagementDeprecatedApi

All URIs are relative to *https://nuextract.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_api_projects_projectid**](ProjectManagementDeprecatedApi.md#delete_api_projects_projectid) | **DELETE** /api/projects/{projectId} | 
[**get_api_projects**](ProjectManagementDeprecatedApi.md#get_api_projects) | **GET** /api/projects | 
[**get_api_projects_projectid**](ProjectManagementDeprecatedApi.md#get_api_projects_projectid) | **GET** /api/projects/{projectId} | 
[**patch_api_projects_projectid**](ProjectManagementDeprecatedApi.md#patch_api_projects_projectid) | **PATCH** /api/projects/{projectId} | 
[**patch_api_projects_projectid_settings**](ProjectManagementDeprecatedApi.md#patch_api_projects_projectid_settings) | **PATCH** /api/projects/{projectId}/settings | 
[**post_api_projects**](ProjectManagementDeprecatedApi.md#post_api_projects) | **POST** /api/projects | 
[**post_api_projects_projectid_duplicate**](ProjectManagementDeprecatedApi.md#post_api_projects_projectid_duplicate) | **POST** /api/projects/{projectId}/duplicate | 
[**post_api_projects_projectid_lock**](ProjectManagementDeprecatedApi.md#post_api_projects_projectid_lock) | **POST** /api/projects/{projectId}/lock | 
[**post_api_projects_projectid_reset_settings**](ProjectManagementDeprecatedApi.md#post_api_projects_projectid_reset_settings) | **POST** /api/projects/{projectId}/reset-settings | 
[**post_api_projects_projectid_share**](ProjectManagementDeprecatedApi.md#post_api_projects_projectid_share) | **POST** /api/projects/{projectId}/share | 
[**post_api_projects_projectid_unlock**](ProjectManagementDeprecatedApi.md#post_api_projects_projectid_unlock) | **POST** /api/projects/{projectId}/unlock | 
[**post_api_projects_projectid_unshare**](ProjectManagementDeprecatedApi.md#post_api_projects_projectid_unshare) | **POST** /api/projects/{projectId}/unshare | 
[**put_api_projects_projectid_template**](ProjectManagementDeprecatedApi.md#put_api_projects_projectid_template) | **PUT** /api/projects/{projectId}/template | 


# **delete_api_projects_projectid**
> delete_api_projects_projectid(project_id)


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
    api_instance = numind.openapi_client.ProjectManagementDeprecatedApi(api_client)
    project_id = 'project_id_example' # str | Unique project identifier.

    try:
        api_instance.delete_api_projects_projectid(project_id)
    except Exception as e:
        print("Exception when calling ProjectManagementDeprecatedApi->delete_api_projects_projectid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Unique project identifier. | 

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

# **get_api_projects**
> List[ProjectResponseDeprecated] get_api_projects(organization_id=organization_id, reference=reference)


Return a list of **Projects** accessible to the authenticated user.

#### Error Responses:
`403 Forbidden` - If the user attempts to access an unauthorized organization.
  

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.project_response_deprecated import ProjectResponseDeprecated
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
    api_instance = numind.openapi_client.ProjectManagementDeprecatedApi(api_client)
    organization_id = 'organization_id_example' # str | Optional organization identifier.   When specified, projects of the given organization are returned instead of personal projects.   This parameter is ignored if ***reference=true***. (optional)
    reference = True # bool | If **true**, only reference projects are returned. (optional)

    try:
        api_response = api_instance.get_api_projects(organization_id=organization_id, reference=reference)
        print("The response of ProjectManagementDeprecatedApi->get_api_projects:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectManagementDeprecatedApi->get_api_projects: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_id** | **str**| Optional organization identifier.   When specified, projects of the given organization are returned instead of personal projects.   This parameter is ignored if ***reference&#x3D;true***. | [optional] 
 **reference** | **bool**| If **true**, only reference projects are returned. | [optional] 

### Return type

[**List[ProjectResponseDeprecated]**](ProjectResponseDeprecated.md)

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

# **get_api_projects_projectid**
> ProjectResponseDeprecated get_api_projects_projectid(project_id)


Return the details of a specific **Project**.

#### Error Responses:
`404 Not Found` - If a **Project** with the specified `projectId` does not exist.

`403 Forbidden` - If the user does not have permission to view this **Project**.
  

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.project_response_deprecated import ProjectResponseDeprecated
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
    api_instance = numind.openapi_client.ProjectManagementDeprecatedApi(api_client)
    project_id = 'project_id_example' # str | Unique project identifier.

    try:
        api_response = api_instance.get_api_projects_projectid(project_id)
        print("The response of ProjectManagementDeprecatedApi->get_api_projects_projectid:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectManagementDeprecatedApi->get_api_projects_projectid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Unique project identifier. | 

### Return type

[**ProjectResponseDeprecated**](ProjectResponseDeprecated.md)

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

# **patch_api_projects_projectid**
> ProjectResponseDeprecated patch_api_projects_projectid(project_id, update_project_request)


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
from numind.models.project_response_deprecated import ProjectResponseDeprecated
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
    api_instance = numind.openapi_client.ProjectManagementDeprecatedApi(api_client)
    project_id = 'project_id_example' # str | Unique project identifier.
    update_project_request = {template={orderId=verbatim-string, customerId=verbatim-string, orderDate=date-time, status=[pending, processed, shipped, delivered, cancelled], totalAmount=number, currency=string, items=[{productId=string, quantity=number, unitPrice=number}], shippingAddress={street=string, city=string, state=string, country=string, zip=string}, comments=string, deliveryPreferences=[[contactless_delivery, signature_required, leave_at_door, pickup_from_store, deliver_to_neighbor, schedule_delivery]], estimatedDelivery=date-time}} # UpdateProjectRequest | 

    try:
        api_response = api_instance.patch_api_projects_projectid(project_id, update_project_request)
        print("The response of ProjectManagementDeprecatedApi->patch_api_projects_projectid:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectManagementDeprecatedApi->patch_api_projects_projectid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Unique project identifier. | 
 **update_project_request** | [**UpdateProjectRequest**](UpdateProjectRequest.md)|  | 

### Return type

[**ProjectResponseDeprecated**](ProjectResponseDeprecated.md)

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

# **patch_api_projects_projectid_settings**
> ProjectResponseDeprecated patch_api_projects_projectid_settings(project_id, update_project_settings_request)


Update the settings of an existing **Project**.


#### Error Responses:
`404 Not Found` - If a **Project** with the specified `projectId` does not exist.

`403 Forbidden` - If the user does not have permission to update this **Project**.

`403 Locked` - If the **Project** is locked.
  

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.project_response_deprecated import ProjectResponseDeprecated
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
    api_instance = numind.openapi_client.ProjectManagementDeprecatedApi(api_client)
    project_id = 'project_id_example' # str | Unique project identifier.
    update_project_settings_request = {temperature=0, rasterizationDPI=170, maxOutputTokens=0, degradedMode=Reject, maxExampleTokenNumber=90000, maxExampleNumber=0, minExampleSimilarity=0} # UpdateProjectSettingsRequest | 

    try:
        api_response = api_instance.patch_api_projects_projectid_settings(project_id, update_project_settings_request)
        print("The response of ProjectManagementDeprecatedApi->patch_api_projects_projectid_settings:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectManagementDeprecatedApi->patch_api_projects_projectid_settings: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Unique project identifier. | 
 **update_project_settings_request** | [**UpdateProjectSettingsRequest**](UpdateProjectSettingsRequest.md)|  | 

### Return type

[**ProjectResponseDeprecated**](ProjectResponseDeprecated.md)

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

# **post_api_projects**
> ProjectResponseDeprecated post_api_projects(create_project_request)


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
from numind.models.project_response_deprecated import ProjectResponseDeprecated
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
    api_instance = numind.openapi_client.ProjectManagementDeprecatedApi(api_client)
    create_project_request = {name=Example: Order Delivery Information Extraction, description=Example: Automated extraction of order delivery details from emails and scanned documents, template={orderId=verbatim-string, customerId=verbatim-string, orderDate=date-time, status=[pending, processed, shipped, delivered, cancelled], totalAmount=number, currency=string, items=[{productId=string, quantity=number, unitPrice=number}], shippingAddress={street=string, city=string, state=string, country=string, zip=string}, comments=string, deliveryPreferences=[[contactless_delivery, signature_required, leave_at_door, pickup_from_store, deliver_to_neighbor, schedule_delivery]], estimatedDelivery=date-time}} # CreateProjectRequest | 

    try:
        api_response = api_instance.post_api_projects(create_project_request)
        print("The response of ProjectManagementDeprecatedApi->post_api_projects:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectManagementDeprecatedApi->post_api_projects: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_project_request** | [**CreateProjectRequest**](CreateProjectRequest.md)|  | 

### Return type

[**ProjectResponseDeprecated**](ProjectResponseDeprecated.md)

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

# **post_api_projects_projectid_duplicate**
> ProjectResponseDeprecated post_api_projects_projectid_duplicate(project_id, organization_id=organization_id)


Create a copy of an existing **Project**.

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
from numind.models.project_response_deprecated import ProjectResponseDeprecated
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
    api_instance = numind.openapi_client.ProjectManagementDeprecatedApi(api_client)
    project_id = 'project_id_example' # str | Unique project identifier.
    organization_id = 'organization_id_example' # str | Destination organization id. If not specified, the project is copied to the user projects. (optional)

    try:
        api_response = api_instance.post_api_projects_projectid_duplicate(project_id, organization_id=organization_id)
        print("The response of ProjectManagementDeprecatedApi->post_api_projects_projectid_duplicate:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectManagementDeprecatedApi->post_api_projects_projectid_duplicate: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Unique project identifier. | 
 **organization_id** | **str**| Destination organization id. If not specified, the project is copied to the user projects. | [optional] 

### Return type

[**ProjectResponseDeprecated**](ProjectResponseDeprecated.md)

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

# **post_api_projects_projectid_lock**
> post_api_projects_projectid_lock(project_id)

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
    api_instance = numind.openapi_client.ProjectManagementDeprecatedApi(api_client)
    project_id = 'project_id_example' # str | Unique project identifier.

    try:
        api_instance.post_api_projects_projectid_lock(project_id)
    except Exception as e:
        print("Exception when calling ProjectManagementDeprecatedApi->post_api_projects_projectid_lock: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Unique project identifier. | 

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

# **post_api_projects_projectid_reset_settings**
> ProjectResponseDeprecated post_api_projects_projectid_reset_settings(project_id)


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
from numind.models.project_response_deprecated import ProjectResponseDeprecated
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
    api_instance = numind.openapi_client.ProjectManagementDeprecatedApi(api_client)
    project_id = 'project_id_example' # str | Unique project identifier.

    try:
        api_response = api_instance.post_api_projects_projectid_reset_settings(project_id)
        print("The response of ProjectManagementDeprecatedApi->post_api_projects_projectid_reset_settings:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectManagementDeprecatedApi->post_api_projects_projectid_reset_settings: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Unique project identifier. | 

### Return type

[**ProjectResponseDeprecated**](ProjectResponseDeprecated.md)

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

# **post_api_projects_projectid_share**
> post_api_projects_projectid_share(project_id)


Turn an existing **Project** into a **Reference Project**.
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
    api_instance = numind.openapi_client.ProjectManagementDeprecatedApi(api_client)
    project_id = 'project_id_example' # str | Unique project identifier.

    try:
        api_instance.post_api_projects_projectid_share(project_id)
    except Exception as e:
        print("Exception when calling ProjectManagementDeprecatedApi->post_api_projects_projectid_share: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Unique project identifier. | 

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

# **post_api_projects_projectid_unlock**
> post_api_projects_projectid_unlock(project_id)


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
    api_instance = numind.openapi_client.ProjectManagementDeprecatedApi(api_client)
    project_id = 'project_id_example' # str | Unique project identifier.

    try:
        api_instance.post_api_projects_projectid_unlock(project_id)
    except Exception as e:
        print("Exception when calling ProjectManagementDeprecatedApi->post_api_projects_projectid_unlock: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Unique project identifier. | 

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

# **post_api_projects_projectid_unshare**
> post_api_projects_projectid_unshare(project_id)


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
    api_instance = numind.openapi_client.ProjectManagementDeprecatedApi(api_client)
    project_id = 'project_id_example' # str | Unique project identifier.

    try:
        api_instance.post_api_projects_projectid_unshare(project_id)
    except Exception as e:
        print("Exception when calling ProjectManagementDeprecatedApi->post_api_projects_projectid_unshare: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Unique project identifier. | 

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

# **put_api_projects_projectid_template**
> ProjectResponseDeprecated put_api_projects_projectid_template(project_id, update_project_template_request)


Update the template of an existing **Project**.


#### Error Responses:
`404 Not Found` - If a **Project** with the specified `projectId` does not exist.

`403 Forbidden` - If the user does not have permission to update this **Project**.

`403 Locked` - If the **Project** is locked.
  

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.project_response_deprecated import ProjectResponseDeprecated
from numind.models.update_project_template_request import UpdateProjectTemplateRequest
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
    api_instance = numind.openapi_client.ProjectManagementDeprecatedApi(api_client)
    project_id = 'project_id_example' # str | Unique project identifier.
    update_project_template_request = numind.openapi_client.UpdateProjectTemplateRequest() # UpdateProjectTemplateRequest | 

    try:
        api_response = api_instance.put_api_projects_projectid_template(project_id, update_project_template_request)
        print("The response of ProjectManagementDeprecatedApi->put_api_projects_projectid_template:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectManagementDeprecatedApi->put_api_projects_projectid_template: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Unique project identifier. | 
 **update_project_template_request** | [**UpdateProjectTemplateRequest**](UpdateProjectTemplateRequest.md)|  | 

### Return type

[**ProjectResponseDeprecated**](ProjectResponseDeprecated.md)

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

