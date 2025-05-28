# numind.openapi_client.ProjectsApi

All URIs are relative to *https://nuextract.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_api_projects_projectid**](ProjectsApi.md#delete_api_projects_projectid) | **DELETE** /api/projects/{projectId} | 
[**get_api_projects**](ProjectsApi.md#get_api_projects) | **GET** /api/projects | 
[**get_api_projects_projectid**](ProjectsApi.md#get_api_projects_projectid) | **GET** /api/projects/{projectId} | 
[**patch_api_projects_projectid**](ProjectsApi.md#patch_api_projects_projectid) | **PATCH** /api/projects/{projectId} | 
[**patch_api_projects_projectid_settings**](ProjectsApi.md#patch_api_projects_projectid_settings) | **PATCH** /api/projects/{projectId}/settings | 
[**post_api_projects**](ProjectsApi.md#post_api_projects) | **POST** /api/projects | 
[**post_api_projects_projectid_duplicate**](ProjectsApi.md#post_api_projects_projectid_duplicate) | **POST** /api/projects/{projectId}/duplicate | 
[**post_api_projects_projectid_lock**](ProjectsApi.md#post_api_projects_projectid_lock) | **POST** /api/projects/{projectId}/lock | 
[**post_api_projects_projectid_reset_settings**](ProjectsApi.md#post_api_projects_projectid_reset_settings) | **POST** /api/projects/{projectId}/reset-settings | 
[**post_api_projects_projectid_share**](ProjectsApi.md#post_api_projects_projectid_share) | **POST** /api/projects/{projectId}/share | 
[**post_api_projects_projectid_unlock**](ProjectsApi.md#post_api_projects_projectid_unlock) | **POST** /api/projects/{projectId}/unlock | 
[**post_api_projects_projectid_unshare**](ProjectsApi.md#post_api_projects_projectid_unshare) | **POST** /api/projects/{projectId}/unshare | 


# **delete_api_projects_projectid**
> delete_api_projects_projectid(project_id)


Permanently removes a project and all related data.


#### Effect:
Deletes the project together with the associated examples and playground items.


#### Error Responses:
`404 Not Found` - If a project with the specified projectId does not exist.

`403 Forbidden` - If the user does not have permission to delete this project.

`403 Locked` - If the project is locked.
  

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
    api_instance = numind.openapi_client.ProjectsApi(api_client)
    project_id = 'project_id_example' # str | Unique project identifier.

    try:
        api_instance.delete_api_projects_projectid(project_id)
    except Exception as e:
        print("Exception when calling ProjectsApi->delete_api_projects_projectid: %s\n" % e)
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
> List[ProjectResponse] get_api_projects(organization_id=organization_id, shared=shared)


Retrieves a list of projects accessible to the authenticated user.

#### Error Responses:
`403 Forbidden` - If the user attempts to access an unauthorized organization.
  

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.project_response import ProjectResponse
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
    api_instance = numind.openapi_client.ProjectsApi(api_client)
    organization_id = 'organization_id_example' # str | Optional organization identifier.     If provided, only projects owned by this organization are returned.     This parameter is ignored if ***shared=true***. (optional)
    shared = True # bool | If **true**, only reference projects (shared projects) are returned.     If **false**, only non-reference projects are returned. (optional)

    try:
        api_response = api_instance.get_api_projects(organization_id=organization_id, shared=shared)
        print("The response of ProjectsApi->get_api_projects:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectsApi->get_api_projects: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_id** | **str**| Optional organization identifier.     If provided, only projects owned by this organization are returned.     This parameter is ignored if ***shared&#x3D;true***. | [optional] 
 **shared** | **bool**| If **true**, only reference projects (shared projects) are returned.     If **false**, only non-reference projects are returned. | [optional] 

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
**400** | Invalid value for: query parameter shared |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_api_projects_projectid**
> ProjectResponse get_api_projects_projectid(project_id)


Fetches the details of a specific project.

#### Error Responses:
`404 Not Found` - If a project with the specified projectId does not exist.

`403 Forbidden` - If the user does not have permission to view this project.
  

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.project_response import ProjectResponse
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
    api_instance = numind.openapi_client.ProjectsApi(api_client)
    project_id = 'project_id_example' # str | Unique project identifier.

    try:
        api_response = api_instance.get_api_projects_projectid(project_id)
        print("The response of ProjectsApi->get_api_projects_projectid:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectsApi->get_api_projects_projectid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Unique project identifier. | 

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

# **patch_api_projects_projectid**
> ProjectResponse patch_api_projects_projectid(project_id, update_project_request)


Updates the details of an existing unlocked project.


Note that you cannot change the lock or shared status via this endpoint.
To modify these states, use the lock/unlock and share/unshare project endpoints.

#### Error Responses:
`404 Not Found` - If a project with the specified projectId does not exist.

`403 Forbidden` - If the user does not have permission to update this project.

`403 Locked` - If the project is locked.
  

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.project_response import ProjectResponse
from numind.openapi_client.models.update_project_request import UpdateProjectRequest
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
    api_instance = numind.openapi_client.ProjectsApi(api_client)
    project_id = 'project_id_example' # str | Unique project identifier.
    update_project_request = {"template":{"orderId":"verbatim-string","customerId":"verbatim-string","orderDate":"date-time","status":["pending","processed","shipped","delivered","cancelled"],"totalAmount":"number","currency":"string","items":[{"productId":"string","quantity":"number","unitPrice":"number"}],"shippingAddress":{"street":"string","city":"string","state":"string","country":"string","zip":"string"},"comments":"string","deliveryPreferences":[["contactless_delivery","signature_required","leave_at_door","pickup_from_store","deliver_to_neighbor","schedule_delivery"]],"estimatedDelivery":"date-time"}} # UpdateProjectRequest | 

    try:
        api_response = api_instance.patch_api_projects_projectid(project_id, update_project_request)
        print("The response of ProjectsApi->patch_api_projects_projectid:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectsApi->patch_api_projects_projectid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Unique project identifier. | 
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

# **patch_api_projects_projectid_settings**
> ProjectResponse patch_api_projects_projectid_settings(project_id, update_project_settings_request)


Updates the settings of an existing unlocked project.


#### Error Responses:
`404 Not Found` - If a project with the specified projectId does not exist.

`403 Forbidden` - If the user does not have permission to update this project.

`403 Locked` - If the project is locked.
  

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.project_response import ProjectResponse
from numind.openapi_client.models.update_project_settings_request import UpdateProjectSettingsRequest
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
    api_instance = numind.openapi_client.ProjectsApi(api_client)
    project_id = 'project_id_example' # str | Unique project identifier.
    update_project_settings_request = {"temperature":0,"rasterizationDpi":115} # UpdateProjectSettingsRequest | 

    try:
        api_response = api_instance.patch_api_projects_projectid_settings(project_id, update_project_settings_request)
        print("The response of ProjectsApi->patch_api_projects_projectid_settings:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectsApi->patch_api_projects_projectid_settings: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Unique project identifier. | 
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

# **post_api_projects**
> ProjectResponse post_api_projects(create_project_request)


Creates a new project to organize an information extraction task.

#### Effect:
A project is created with default settings:

 Parameter | Default |
-----------|---------|
 `temperature` | 0.0 |
 `rasterizationDpi` | 115 |


If *ownerOrganization* is not provided, the project will be owned by the authenticated user.
When created, a project is not locked and is owned by the authenticated user and the organization (if specified in the request).

#### Response:
 The response contains `projectId`, which
 is required to modify the project, perform CRUD operations on project examples and
 project playground items, and run inference for this project. 
  

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.create_project_request import CreateProjectRequest
from numind.openapi_client.models.project_response import ProjectResponse
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
    api_instance = numind.openapi_client.ProjectsApi(api_client)
    create_project_request = {"name":"Example: Order Delivery Information Extraction","description":"Example: Automated extraction of order delivery details from emails and scanned documents","template":{"orderId":"verbatim-string","customerId":"verbatim-string","orderDate":"date-time","status":["pending","processed","shipped","delivered","cancelled"],"totalAmount":"number","currency":"string","items":[{"productId":"string","quantity":"number","unitPrice":"number"}],"shippingAddress":{"street":"string","city":"string","state":"string","country":"string","zip":"string"},"comments":"string","deliveryPreferences":[["contactless_delivery","signature_required","leave_at_door","pickup_from_store","deliver_to_neighbor","schedule_delivery"]],"estimatedDelivery":"date-time"}} # CreateProjectRequest | 

    try:
        api_response = api_instance.post_api_projects(create_project_request)
        print("The response of ProjectsApi->post_api_projects:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectsApi->post_api_projects: %s\n" % e)
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

# **post_api_projects_projectid_duplicate**
> ProjectResponse post_api_projects_projectid_duplicate(project_id)

Creates a copy of an existing project.

It is allowed to duplicate locked projects and reference projects.


#### Effect:
- The duplicated project retains the **same template, settings, examples and playground**.
- A new name is assigned ("Original Name (copy)").

#### Response:
 The response contains a newly generated
 `projectId`. When duplicated, a new project is always unlocked. The duplicated reference projects
 are private and owned by the authenticated user.

#### Error Responses:
`404 Not Found` - If a project with the specified projectId does not exist.

`403 Forbidden` - If the user does not have permission to duplicate this project.


### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.project_response import ProjectResponse
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
    api_instance = numind.openapi_client.ProjectsApi(api_client)
    project_id = 'project_id_example' # str | Unique project identifier.

    try:
        api_response = api_instance.post_api_projects_projectid_duplicate(project_id)
        print("The response of ProjectsApi->post_api_projects_projectid_duplicate:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectsApi->post_api_projects_projectid_duplicate: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Unique project identifier. | 

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

# **post_api_projects_projectid_lock**
> post_api_projects_projectid_lock(project_id)

Locks a project to prevent modifications.


#### Effect:
- While locked, the project **cannot be updated or deleted**. Read access is still available.
- CRUD operations on project examples are not allowed.
- Inference is still allowed.
- CRUD access to project playground items is still available.

#### Error Responses:
 `404 Not Found` - If a project with the specified projectId does not exist.

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
    api_instance = numind.openapi_client.ProjectsApi(api_client)
    project_id = 'project_id_example' # str | Unique project identifier.

    try:
        api_instance.post_api_projects_projectid_lock(project_id)
    except Exception as e:
        print("Exception when calling ProjectsApi->post_api_projects_projectid_lock: %s\n" % e)
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
> ProjectResponse post_api_projects_projectid_reset_settings(project_id)


Resets the settings of an existing unlocked project to their default values.

Default values are:

 Parameter | Default |
-----------|---------|
 `temperature` | 0.0 |
 `rasterizationDpi` | 115 |

#### Error Responses:
`404 Not Found` - If a project with the specified projectId does not exist.

`403 Forbidden` - If the user does not have permission to update this project.

`403 Locked` - If the project is locked.
  

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.project_response import ProjectResponse
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
    api_instance = numind.openapi_client.ProjectsApi(api_client)
    project_id = 'project_id_example' # str | Unique project identifier.

    try:
        api_response = api_instance.post_api_projects_projectid_reset_settings(project_id)
        print("The response of ProjectsApi->post_api_projects_projectid_reset_settings:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectsApi->post_api_projects_projectid_reset_settings: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Unique project identifier. | 

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

# **post_api_projects_projectid_share**
> post_api_projects_projectid_share(project_id)

Shares a project with other users.

 This endpoint turns an existing project into a reference project.
 Only NuMind administrators can share a project with other users.
 Lock state does not prevent sharing. Likewise, sharing does not change the lock state.

#### Effect:

- Reference projects are shared with the community (read access is granted to all users).
- Project examples and playground items are shared as well.
- Only NuMind administrators can update or delete reference projects.
- Only NuMind administrators can create, update, or delete reference project examples and playground items.
- The inference is allowed for all users.

#### Error Responses:

`404 Not Found` - If a project with the specified projectId does not exist.

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
    api_instance = numind.openapi_client.ProjectsApi(api_client)
    project_id = 'project_id_example' # str | Unique project identifier.

    try:
        api_instance.post_api_projects_projectid_share(project_id)
    except Exception as e:
        print("Exception when calling ProjectsApi->post_api_projects_projectid_share: %s\n" % e)
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

Unlocks a previously locked project.

#### Effect:
- Once unlocked, the project **can be updated or deleted**.
- Full CRUD access to project examples is restored.

#### Error Responses:
`404 Not Found` - If a project with the specified projectId does not exist.

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
    api_instance = numind.openapi_client.ProjectsApi(api_client)
    project_id = 'project_id_example' # str | Unique project identifier.

    try:
        api_instance.post_api_projects_projectid_unlock(project_id)
    except Exception as e:
        print("Exception when calling ProjectsApi->post_api_projects_projectid_unlock: %s\n" % e)
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


Unshares a reference project (makes it private).

 Lock state does not prevent unsharing. Likewise, unsharing does not change the lock state.
 The project owner is the initial owner, not the authenicated user.


#### Effect:
- The project is no longer a reference project and is no longer shared with the community.
- Read access is revoked for all users except the project owner.
- Project examples and playground are no longer publicly accessible.
- Only the project owner can manage or delete the project after unsharing.
- Inference is restricted to the project owner.

#### Error Responses:
`404 Not Found` - If a project with the specified projectId does not exist.

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
    api_instance = numind.openapi_client.ProjectsApi(api_client)
    project_id = 'project_id_example' # str | Unique project identifier.

    try:
        api_instance.post_api_projects_projectid_unshare(project_id)
    except Exception as e:
        print("Exception when calling ProjectsApi->post_api_projects_projectid_unshare: %s\n" % e)
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

