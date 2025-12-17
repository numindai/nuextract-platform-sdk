# numind.openapi_client.ContentExtractionPlaygroundApi

All URIs are relative to *https://nuextract.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_api_content_extraction_contentextractionprojectid_playground_contentextractionplaygrounditemid**](ContentExtractionPlaygroundApi.md#delete_api_content_extraction_contentextractionprojectid_playground_contentextractionplaygrounditemid) | **DELETE** /api/content-extraction/{contentExtractionProjectId}/playground/{contentExtractionPlaygroundItemId} | 
[**get_api_content_extraction_contentextractionprojectid_playground**](ContentExtractionPlaygroundApi.md#get_api_content_extraction_contentextractionprojectid_playground) | **GET** /api/content-extraction/{contentExtractionProjectId}/playground | 
[**get_api_content_extraction_contentextractionprojectid_playground_contentextractionplaygrounditemid**](ContentExtractionPlaygroundApi.md#get_api_content_extraction_contentextractionprojectid_playground_contentextractionplaygrounditemid) | **GET** /api/content-extraction/{contentExtractionProjectId}/playground/{contentExtractionPlaygroundItemId} | 
[**post_api_content_extraction_contentextractionprojectid_playground**](ContentExtractionPlaygroundApi.md#post_api_content_extraction_contentextractionprojectid_playground) | **POST** /api/content-extraction/{contentExtractionProjectId}/playground | 
[**put_api_content_extraction_contentextractionprojectid_playground_contentextractionplaygrounditemid**](ContentExtractionPlaygroundApi.md#put_api_content_extraction_contentextractionprojectid_playground_contentextractionplaygrounditemid) | **PUT** /api/content-extraction/{contentExtractionProjectId}/playground/{contentExtractionPlaygroundItemId} | 


# **delete_api_content_extraction_contentextractionprojectid_playground_contentextractionplaygrounditemid**
> delete_api_content_extraction_contentextractionprojectid_playground_contentextractionplaygrounditemid(content_extraction_project_id, content_extraction_playground_item_id)


Delete a **NuMarkdown Playground Item**. This action cannot be undone.
    

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
    api_instance = numind.openapi_client.ContentExtractionPlaygroundApi(api_client)
    content_extraction_project_id = 'content_extraction_project_id_example' # str | Unique content extraction project identifier.
    content_extraction_playground_item_id = 'content_extraction_playground_item_id_example' # str | Unique content extraction playground item identifier.

    try:
        api_instance.delete_api_content_extraction_contentextractionprojectid_playground_contentextractionplaygrounditemid(content_extraction_project_id, content_extraction_playground_item_id)
    except Exception as e:
        print("Exception when calling ContentExtractionPlaygroundApi->delete_api_content_extraction_contentextractionprojectid_playground_contentextractionplaygrounditemid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **content_extraction_project_id** | **str**| Unique content extraction project identifier. | 
 **content_extraction_playground_item_id** | **str**| Unique content extraction playground item identifier. | 

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

# **get_api_content_extraction_contentextractionprojectid_playground**
> PaginatedResponseMarkdownPlaygroundItemResponse get_api_content_extraction_contentextractionprojectid_playground(content_extraction_project_id, skip=skip, per_page=per_page)


List all **NuMarkdown Playground Items** associated with a specific **NuMarkdown Project**.

#### Query Parameters:

* `skip`: (Optional) Number of playground items to skip
* `perPage`: (Optional) Number of playground items per page
    

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.paginated_response_markdown_playground_item_response import PaginatedResponseMarkdownPlaygroundItemResponse
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
    api_instance = numind.openapi_client.ContentExtractionPlaygroundApi(api_client)
    content_extraction_project_id = 'content_extraction_project_id_example' # str | Unique content extraction project identifier.
    skip = 56 # int | Number of playground items to skip. Min: 0. Default: 0. (optional)
    per_page = 56 # int | Number of playground items per page. Min: 1. Max: 300. Default: 30. (optional)

    try:
        api_response = api_instance.get_api_content_extraction_contentextractionprojectid_playground(content_extraction_project_id, skip=skip, per_page=per_page)
        print("The response of ContentExtractionPlaygroundApi->get_api_content_extraction_contentextractionprojectid_playground:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ContentExtractionPlaygroundApi->get_api_content_extraction_contentextractionprojectid_playground: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **content_extraction_project_id** | **str**| Unique content extraction project identifier. | 
 **skip** | **int**| Number of playground items to skip. Min: 0. Default: 0. | [optional] 
 **per_page** | **int**| Number of playground items per page. Min: 1. Max: 300. Default: 30. | [optional] 

### Return type

[**PaginatedResponseMarkdownPlaygroundItemResponse**](PaginatedResponseMarkdownPlaygroundItemResponse.md)

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

# **get_api_content_extraction_contentextractionprojectid_playground_contentextractionplaygrounditemid**
> MarkdownPlaygroundItemResponse get_api_content_extraction_contentextractionprojectid_playground_contentextractionplaygrounditemid(content_extraction_project_id, content_extraction_playground_item_id)


Get a specific **NuMarkdown Playground Item** by ID.
    

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.markdown_playground_item_response import MarkdownPlaygroundItemResponse
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
    api_instance = numind.openapi_client.ContentExtractionPlaygroundApi(api_client)
    content_extraction_project_id = 'content_extraction_project_id_example' # str | Unique content extraction project identifier.
    content_extraction_playground_item_id = 'content_extraction_playground_item_id_example' # str | Unique content extraction playground item identifier.

    try:
        api_response = api_instance.get_api_content_extraction_contentextractionprojectid_playground_contentextractionplaygrounditemid(content_extraction_project_id, content_extraction_playground_item_id)
        print("The response of ContentExtractionPlaygroundApi->get_api_content_extraction_contentextractionprojectid_playground_contentextractionplaygrounditemid:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ContentExtractionPlaygroundApi->get_api_content_extraction_contentextractionprojectid_playground_contentextractionplaygrounditemid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **content_extraction_project_id** | **str**| Unique content extraction project identifier. | 
 **content_extraction_playground_item_id** | **str**| Unique content extraction playground item identifier. | 

### Return type

[**MarkdownPlaygroundItemResponse**](MarkdownPlaygroundItemResponse.md)

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

# **post_api_content_extraction_contentextractionprojectid_playground**
> MarkdownPlaygroundItemResponse post_api_content_extraction_contentextractionprojectid_playground(content_extraction_project_id, create_or_update_markdown_playground_item_request)


Create a new **NuMarkdown Playground Item** associated with a specific **NuMarkdown Project**.

#### Body Fields:

* `ownerOrganization`: (Optional) Organization that will own the playground item
* `documentId`: Unique identifier of the document used as input
* `result`: Markdown result
* `thinking`: Thinking/reasoning process
* `totalTokens`: (Optional) Total number of tokens used for inference
* `outputTokens`: (Optional) Output tokens used for inference
* `inputTokens`: (Optional) Input tokens used for inference
    

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.create_or_update_markdown_playground_item_request import CreateOrUpdateMarkdownPlaygroundItemRequest
from numind.models.markdown_playground_item_response import MarkdownPlaygroundItemResponse
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
    api_instance = numind.openapi_client.ContentExtractionPlaygroundApi(api_client)
    content_extraction_project_id = 'content_extraction_project_id_example' # str | Unique content extraction project identifier.
    create_or_update_markdown_playground_item_request = {"documentId":"0d25d758-d475-4c14-aafa-eb5d6a40b670","result":"# Analysis of Order Confirmation\n\nThis document contains details about an order with ID o-89123 for customer c-20485.","thinkingTrace":"The document appears to be an order confirmation email with shipping details and product information. I'll extract the key information in a structured format.","totalTokens":567,"outputTokens":267,"inputTokens":300} # CreateOrUpdateMarkdownPlaygroundItemRequest | 

    try:
        api_response = api_instance.post_api_content_extraction_contentextractionprojectid_playground(content_extraction_project_id, create_or_update_markdown_playground_item_request)
        print("The response of ContentExtractionPlaygroundApi->post_api_content_extraction_contentextractionprojectid_playground:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ContentExtractionPlaygroundApi->post_api_content_extraction_contentextractionprojectid_playground: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **content_extraction_project_id** | **str**| Unique content extraction project identifier. | 
 **create_or_update_markdown_playground_item_request** | [**CreateOrUpdateMarkdownPlaygroundItemRequest**](CreateOrUpdateMarkdownPlaygroundItemRequest.md)|  | 

### Return type

[**MarkdownPlaygroundItemResponse**](MarkdownPlaygroundItemResponse.md)

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

# **put_api_content_extraction_contentextractionprojectid_playground_contentextractionplaygrounditemid**
> MarkdownPlaygroundItemResponse put_api_content_extraction_contentextractionprojectid_playground_contentextractionplaygrounditemid(content_extraction_project_id, content_extraction_playground_item_id, create_or_update_markdown_playground_item_request)


Update an existing **NuMarkdown Playground Item**.

#### Body Fields:

* `ownerOrganization`: (Optional) Organization that will own the playground item
* `documentId`: Unique identifier of the document used as input
* `result`: Markdown result
* `thinking`: Thinking/reasoning process
* `totalTokens`: (Optional) Total number of tokens used for inference
* `outputTokens`: (Optional) Output tokens used for inference
* `inputTokens`: (Optional) Input tokens used for inference
    

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.create_or_update_markdown_playground_item_request import CreateOrUpdateMarkdownPlaygroundItemRequest
from numind.models.markdown_playground_item_response import MarkdownPlaygroundItemResponse
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
    api_instance = numind.openapi_client.ContentExtractionPlaygroundApi(api_client)
    content_extraction_project_id = 'content_extraction_project_id_example' # str | Unique content extraction project identifier.
    content_extraction_playground_item_id = 'content_extraction_playground_item_id_example' # str | Unique content extraction playground item identifier.
    create_or_update_markdown_playground_item_request = {documentId=0d25d758-d475-4c14-aafa-eb5d6a40b670, result=# Analysis of Order Confirmation

This document contains details about an order with ID o-89123 for customer c-20485., thinkingTrace=The document appears to be an order confirmation email with shipping details and product information. I'll extract the key information in a structured format., totalTokens=567, outputTokens=267, inputTokens=300} # CreateOrUpdateMarkdownPlaygroundItemRequest | 

    try:
        api_response = api_instance.put_api_content_extraction_contentextractionprojectid_playground_contentextractionplaygrounditemid(content_extraction_project_id, content_extraction_playground_item_id, create_or_update_markdown_playground_item_request)
        print("The response of ContentExtractionPlaygroundApi->put_api_content_extraction_contentextractionprojectid_playground_contentextractionplaygrounditemid:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ContentExtractionPlaygroundApi->put_api_content_extraction_contentextractionprojectid_playground_contentextractionplaygrounditemid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **content_extraction_project_id** | **str**| Unique content extraction project identifier. | 
 **content_extraction_playground_item_id** | **str**| Unique content extraction playground item identifier. | 
 **create_or_update_markdown_playground_item_request** | [**CreateOrUpdateMarkdownPlaygroundItemRequest**](CreateOrUpdateMarkdownPlaygroundItemRequest.md)|  | 

### Return type

[**MarkdownPlaygroundItemResponse**](MarkdownPlaygroundItemResponse.md)

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

