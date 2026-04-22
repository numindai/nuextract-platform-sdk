# numind.openapi_client.ContentExtractionProjectManagementApi

All URIs are relative to *https://nuextract.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_api_content_extraction**](ContentExtractionProjectManagementApi.md#get_api_content_extraction) | **GET** /api/content-extraction | 
[**patch_api_content_extraction_contentprojectid**](ContentExtractionProjectManagementApi.md#patch_api_content_extraction_contentprojectid) | **PATCH** /api/content-extraction/{contentProjectId} | 
[**patch_api_content_extraction_contentprojectid_settings**](ContentExtractionProjectManagementApi.md#patch_api_content_extraction_contentprojectid_settings) | **PATCH** /api/content-extraction/{contentProjectId}/settings | 
[**post_api_content_extraction**](ContentExtractionProjectManagementApi.md#post_api_content_extraction) | **POST** /api/content-extraction | 
[**post_api_content_extraction_contentprojectid_reset_settings**](ContentExtractionProjectManagementApi.md#post_api_content_extraction_contentprojectid_reset_settings) | **POST** /api/content-extraction/{contentProjectId}/reset-settings | 


# **get_api_content_extraction**
> List[ContentProjectResponse] get_api_content_extraction(x_organization_id=x_organization_id)


List all **Content Extraction Projects** the authenticated user has access to.

#### Query Parameters:

* `organization`: (Optional) Filter projects by organization
    

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.content_project_response import ContentProjectResponse
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
    api_instance = numind.openapi_client.ContentExtractionProjectManagementApi(api_client)
    x_organization_id = 'x_organization_id_example' # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)

    try:
        api_response = api_instance.get_api_content_extraction(x_organization_id=x_organization_id)
        print("The response of ContentExtractionProjectManagementApi->get_api_content_extraction:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ContentExtractionProjectManagementApi->get_api_content_extraction: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 

### Return type

[**List[ContentProjectResponse]**](ContentProjectResponse.md)

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

# **patch_api_content_extraction_contentprojectid**
> ContentProjectResponse patch_api_content_extraction_contentprojectid(content_project_id, update_content_project_request, x_organization_id=x_organization_id)


Update an existing **Content Extraction Project**.
    

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.content_project_response import ContentProjectResponse
from numind.models.update_content_project_request import UpdateContentProjectRequest
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
    api_instance = numind.openapi_client.ContentExtractionProjectManagementApi(api_client)
    content_project_id = 'content_project_id_example' # str | Unique content extraction project identifier.
    update_content_project_request = {"name":"New Project Name"} # UpdateContentProjectRequest | 
    x_organization_id = 'x_organization_id_example' # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)

    try:
        api_response = api_instance.patch_api_content_extraction_contentprojectid(content_project_id, update_content_project_request, x_organization_id=x_organization_id)
        print("The response of ContentExtractionProjectManagementApi->patch_api_content_extraction_contentprojectid:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ContentExtractionProjectManagementApi->patch_api_content_extraction_contentprojectid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **content_project_id** | **str**| Unique content extraction project identifier. | 
 **update_content_project_request** | [**UpdateContentProjectRequest**](UpdateContentProjectRequest.md)|  | 
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 

### Return type

[**ContentProjectResponse**](ContentProjectResponse.md)

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

# **patch_api_content_extraction_contentprojectid_settings**
> ContentProjectResponse patch_api_content_extraction_contentprojectid_settings(content_project_id, update_content_project_settings_request, x_organization_id=x_organization_id)


Update the settings of an existing **Content Extraction Project**.

#### Error Responses:
`404 Not Found` - If a **Content Extraction Project** with the specified `contentProjectId` does not exist.

`403 Forbidden` - If the user does not have permission to update this **Content Extraction Project**.
  

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.content_project_response import ContentProjectResponse
from numind.models.update_content_project_settings_request import UpdateContentProjectSettingsRequest
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
    api_instance = numind.openapi_client.ContentExtractionProjectManagementApi(api_client)
    content_project_id = 'content_project_id_example' # str | Unique content extraction project identifier.
    update_content_project_settings_request = {"temperature":0,"rasterizationDPI":170,"maxOutputTokens":0,"enableThinking":true} # UpdateContentProjectSettingsRequest | 
    x_organization_id = 'x_organization_id_example' # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)

    try:
        api_response = api_instance.patch_api_content_extraction_contentprojectid_settings(content_project_id, update_content_project_settings_request, x_organization_id=x_organization_id)
        print("The response of ContentExtractionProjectManagementApi->patch_api_content_extraction_contentprojectid_settings:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ContentExtractionProjectManagementApi->patch_api_content_extraction_contentprojectid_settings: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **content_project_id** | **str**| Unique content extraction project identifier. | 
 **update_content_project_settings_request** | [**UpdateContentProjectSettingsRequest**](UpdateContentProjectSettingsRequest.md)|  | 
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 

### Return type

[**ContentProjectResponse**](ContentProjectResponse.md)

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

# **post_api_content_extraction**
> ContentProjectResponse post_api_content_extraction(create_content_project_request, x_organization_id=x_organization_id)


Create a new **Content Extraction Project** to define a content extraction task.
    

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.content_project_response import ContentProjectResponse
from numind.models.create_content_project_request import CreateContentProjectRequest
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
    api_instance = numind.openapi_client.ContentExtractionProjectManagementApi(api_client)
    create_content_project_request = {"name":"Example: Order Delivery Information Extraction","description":"Example: Automated extraction of order delivery details from emails and scanned documents"} # CreateContentProjectRequest | 
    x_organization_id = 'x_organization_id_example' # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)

    try:
        api_response = api_instance.post_api_content_extraction(create_content_project_request, x_organization_id=x_organization_id)
        print("The response of ContentExtractionProjectManagementApi->post_api_content_extraction:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ContentExtractionProjectManagementApi->post_api_content_extraction: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_content_project_request** | [**CreateContentProjectRequest**](CreateContentProjectRequest.md)|  | 
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 

### Return type

[**ContentProjectResponse**](ContentProjectResponse.md)

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

# **post_api_content_extraction_contentprojectid_reset_settings**
> ContentProjectResponse post_api_content_extraction_contentprojectid_reset_settings(content_project_id, x_organization_id=x_organization_id)


Reset the settings of an existing **Content Extraction Project** to their default values.

Default values are:

 Setting | Default |
-----------|--------|
 `temperature` | 0.0 |
 `rasterizationDPI` | 170 |
 `maxOutputTokens` | 0 (no limit) |

#### Error Responses:
`404 Not Found` - If a **Content Extraction Project** with the specified `contentProjectId` does not exist.

`403 Forbidden` - If the user does not have permission to update this **Content Extraction Project**.
  

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.content_project_response import ContentProjectResponse
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
    api_instance = numind.openapi_client.ContentExtractionProjectManagementApi(api_client)
    content_project_id = 'content_project_id_example' # str | Unique content extraction project identifier.
    x_organization_id = 'x_organization_id_example' # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)

    try:
        api_response = api_instance.post_api_content_extraction_contentprojectid_reset_settings(content_project_id, x_organization_id=x_organization_id)
        print("The response of ContentExtractionProjectManagementApi->post_api_content_extraction_contentprojectid_reset_settings:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ContentExtractionProjectManagementApi->post_api_content_extraction_contentprojectid_reset_settings: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **content_project_id** | **str**| Unique content extraction project identifier. | 
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 

### Return type

[**ContentProjectResponse**](ContentProjectResponse.md)

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

