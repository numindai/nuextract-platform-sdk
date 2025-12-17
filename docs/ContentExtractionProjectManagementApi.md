# numind.openapi_client.ContentExtractionProjectManagementApi

All URIs are relative to *https://nuextract.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_api_content_extraction**](ContentExtractionProjectManagementApi.md#get_api_content_extraction) | **GET** /api/content-extraction | 
[**patch_api_content_extraction_contentextractionprojectid**](ContentExtractionProjectManagementApi.md#patch_api_content_extraction_contentextractionprojectid) | **PATCH** /api/content-extraction/{contentExtractionProjectId} | 
[**patch_api_content_extraction_contentextractionprojectid_settings**](ContentExtractionProjectManagementApi.md#patch_api_content_extraction_contentextractionprojectid_settings) | **PATCH** /api/content-extraction/{contentExtractionProjectId}/settings | 
[**post_api_content_extraction**](ContentExtractionProjectManagementApi.md#post_api_content_extraction) | **POST** /api/content-extraction | 
[**post_api_content_extraction_contentextractionprojectid_reset_settings**](ContentExtractionProjectManagementApi.md#post_api_content_extraction_contentextractionprojectid_reset_settings) | **POST** /api/content-extraction/{contentExtractionProjectId}/reset-settings | 


# **get_api_content_extraction**
> List[MarkdownProjectResponse] get_api_content_extraction(organization_id=organization_id)


List all **NuMarkdown Projects** the authenticated user has access to.

#### Query Parameters:

* `organization`: (Optional) Filter projects by organization
    

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.markdown_project_response import MarkdownProjectResponse
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
    organization_id = 'organization_id_example' # str | Optional organization identifier.   When specified, projects of the given organization are returned instead of personal projects. (optional)

    try:
        api_response = api_instance.get_api_content_extraction(organization_id=organization_id)
        print("The response of ContentExtractionProjectManagementApi->get_api_content_extraction:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ContentExtractionProjectManagementApi->get_api_content_extraction: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_id** | **str**| Optional organization identifier.   When specified, projects of the given organization are returned instead of personal projects. | [optional] 

### Return type

[**List[MarkdownProjectResponse]**](MarkdownProjectResponse.md)

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

# **patch_api_content_extraction_contentextractionprojectid**
> MarkdownProjectResponse patch_api_content_extraction_contentextractionprojectid(content_extraction_project_id, update_markdown_project_request)


Update an existing **NuMarkdown Project**.

#### Body Fields:

* `name`: (Optional) New name of the project
* `description`: (Optional) New description of the project
    

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.markdown_project_response import MarkdownProjectResponse
from numind.models.update_markdown_project_request import UpdateMarkdownProjectRequest
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
    content_extraction_project_id = 'content_extraction_project_id_example' # str | Unique content extraction project identifier.
    update_markdown_project_request = {"name":"New Project Name"} # UpdateMarkdownProjectRequest | 

    try:
        api_response = api_instance.patch_api_content_extraction_contentextractionprojectid(content_extraction_project_id, update_markdown_project_request)
        print("The response of ContentExtractionProjectManagementApi->patch_api_content_extraction_contentextractionprojectid:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ContentExtractionProjectManagementApi->patch_api_content_extraction_contentextractionprojectid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **content_extraction_project_id** | **str**| Unique content extraction project identifier. | 
 **update_markdown_project_request** | [**UpdateMarkdownProjectRequest**](UpdateMarkdownProjectRequest.md)|  | 

### Return type

[**MarkdownProjectResponse**](MarkdownProjectResponse.md)

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

# **patch_api_content_extraction_contentextractionprojectid_settings**
> MarkdownProjectResponse patch_api_content_extraction_contentextractionprojectid_settings(content_extraction_project_id, update_markdown_project_settings_request)


Update the settings of an existing **Markdown Project**.

#### Error Responses:
`404 Not Found` - If a **Markdown Project** with the specified `projectId` does not exist.

`403 Forbidden` - If the user does not have permission to update this **Markdown Project**.
  

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.markdown_project_response import MarkdownProjectResponse
from numind.models.update_markdown_project_settings_request import UpdateMarkdownProjectSettingsRequest
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
    content_extraction_project_id = 'content_extraction_project_id_example' # str | Unique content extraction project identifier.
    update_markdown_project_settings_request = {"temperature":0,"rasterizationDPI":170,"maxOutputTokens":0} # UpdateMarkdownProjectSettingsRequest | 

    try:
        api_response = api_instance.patch_api_content_extraction_contentextractionprojectid_settings(content_extraction_project_id, update_markdown_project_settings_request)
        print("The response of ContentExtractionProjectManagementApi->patch_api_content_extraction_contentextractionprojectid_settings:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ContentExtractionProjectManagementApi->patch_api_content_extraction_contentextractionprojectid_settings: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **content_extraction_project_id** | **str**| Unique content extraction project identifier. | 
 **update_markdown_project_settings_request** | [**UpdateMarkdownProjectSettingsRequest**](UpdateMarkdownProjectSettingsRequest.md)|  | 

### Return type

[**MarkdownProjectResponse**](MarkdownProjectResponse.md)

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
> MarkdownProjectResponse post_api_content_extraction(create_markdown_project_request)


Create a new **NuMarkdown Project** to define a markdown generation task.

#### Body Fields:

* `name`: Name of the project
* `description`: Description of the project
* `ownerOrganization`: (Optional) Organization that will own the project
    

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.create_markdown_project_request import CreateMarkdownProjectRequest
from numind.models.markdown_project_response import MarkdownProjectResponse
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
    create_markdown_project_request = {"name":"Example: Order Delivery Information Extraction","description":"Example: Automated extraction of order delivery details from emails and scanned documents"} # CreateMarkdownProjectRequest | 

    try:
        api_response = api_instance.post_api_content_extraction(create_markdown_project_request)
        print("The response of ContentExtractionProjectManagementApi->post_api_content_extraction:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ContentExtractionProjectManagementApi->post_api_content_extraction: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_markdown_project_request** | [**CreateMarkdownProjectRequest**](CreateMarkdownProjectRequest.md)|  | 

### Return type

[**MarkdownProjectResponse**](MarkdownProjectResponse.md)

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

# **post_api_content_extraction_contentextractionprojectid_reset_settings**
> MarkdownProjectResponse post_api_content_extraction_contentextractionprojectid_reset_settings(content_extraction_project_id)


Reset the settings of an existing **Markdown Project** to their default values.

Default values are:

 Setting | Default |
-----------|---------|
 `temperature` | 0.0 |
 `rasterizationDPI` | 170 |
 `maxOutputTokens` | 0 (no limit) |

#### Error Responses:
`404 Not Found` - If a **Markdown Project** with the specified `projectId` does not exist.

`403 Forbidden` - If the user does not have permission to update this **Markdown Project**.
  

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.markdown_project_response import MarkdownProjectResponse
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
    content_extraction_project_id = 'content_extraction_project_id_example' # str | Unique content extraction project identifier.

    try:
        api_response = api_instance.post_api_content_extraction_contentextractionprojectid_reset_settings(content_extraction_project_id)
        print("The response of ContentExtractionProjectManagementApi->post_api_content_extraction_contentextractionprojectid_reset_settings:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ContentExtractionProjectManagementApi->post_api_content_extraction_contentextractionprojectid_reset_settings: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **content_extraction_project_id** | **str**| Unique content extraction project identifier. | 

### Return type

[**MarkdownProjectResponse**](MarkdownProjectResponse.md)

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

