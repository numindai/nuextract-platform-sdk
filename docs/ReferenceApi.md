# numind.openapi_client.ReferenceApi

All URIs are relative to *https://nuextract.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_api_reference_projects_projectid**](ReferenceApi.md#delete_api_reference_projects_projectid) | **DELETE** /api/reference/projects/{projectId} | 
[**delete_api_reference_projects_projectid_examples_exampleid**](ReferenceApi.md#delete_api_reference_projects_projectid_examples_exampleid) | **DELETE** /api/reference/projects/{projectId}/examples/{exampleId} | 
[**delete_api_reference_projects_projectid_results_historyid**](ReferenceApi.md#delete_api_reference_projects_projectid_results_historyid) | **DELETE** /api/reference/projects/{projectId}/results/{historyId} | 
[**get_api_reference_documents_documentid**](ReferenceApi.md#get_api_reference_documents_documentid) | **GET** /api/reference/documents/{documentId} | 
[**get_api_reference_documents_documentid_content**](ReferenceApi.md#get_api_reference_documents_documentid_content) | **GET** /api/reference/documents/{documentId}/content | 
[**get_api_reference_projects**](ReferenceApi.md#get_api_reference_projects) | **GET** /api/reference/projects | 
[**get_api_reference_projects_projectid**](ReferenceApi.md#get_api_reference_projects_projectid) | **GET** /api/reference/projects/{projectId} | 
[**get_api_reference_projects_projectid_examples**](ReferenceApi.md#get_api_reference_projects_projectid_examples) | **GET** /api/reference/projects/{projectId}/examples | 
[**get_api_reference_projects_projectid_examples_exampleid**](ReferenceApi.md#get_api_reference_projects_projectid_examples_exampleid) | **GET** /api/reference/projects/{projectId}/examples/{exampleId} | 
[**get_api_reference_projects_projectid_results**](ReferenceApi.md#get_api_reference_projects_projectid_results) | **GET** /api/reference/projects/{projectId}/results | 
[**get_api_reference_projects_projectid_results_historyid**](ReferenceApi.md#get_api_reference_projects_projectid_results_historyid) | **GET** /api/reference/projects/{projectId}/results/{historyId} | 
[**post_api_reference_documents_file**](ReferenceApi.md#post_api_reference_documents_file) | **POST** /api/reference/documents/file | 
[**post_api_reference_documents_text**](ReferenceApi.md#post_api_reference_documents_text) | **POST** /api/reference/documents/text | 
[**post_api_reference_infer_template**](ReferenceApi.md#post_api_reference_infer_template) | **POST** /api/reference/infer-template | 
[**post_api_reference_projects**](ReferenceApi.md#post_api_reference_projects) | **POST** /api/reference/projects | 
[**post_api_reference_projects_projectid_duplicate**](ReferenceApi.md#post_api_reference_projects_projectid_duplicate) | **POST** /api/reference/projects/{projectId}/duplicate | 
[**post_api_reference_projects_projectid_examples**](ReferenceApi.md#post_api_reference_projects_projectid_examples) | **POST** /api/reference/projects/{projectId}/examples | 
[**post_api_reference_projects_projectid_infer_document_documentid**](ReferenceApi.md#post_api_reference_projects_projectid_infer_document_documentid) | **POST** /api/reference/projects/{projectId}/infer-document/{documentId} | 
[**post_api_reference_projects_projectid_infer_file**](ReferenceApi.md#post_api_reference_projects_projectid_infer_file) | **POST** /api/reference/projects/{projectId}/infer-file | 
[**post_api_reference_projects_projectid_infer_text**](ReferenceApi.md#post_api_reference_projects_projectid_infer_text) | **POST** /api/reference/projects/{projectId}/infer-text | 
[**post_api_reference_projects_projectid_lock**](ReferenceApi.md#post_api_reference_projects_projectid_lock) | **POST** /api/reference/projects/{projectId}/lock | 
[**post_api_reference_projects_projectid_results**](ReferenceApi.md#post_api_reference_projects_projectid_results) | **POST** /api/reference/projects/{projectId}/results | 
[**post_api_reference_projects_projectid_share**](ReferenceApi.md#post_api_reference_projects_projectid_share) | **POST** /api/reference/projects/{projectId}/share | 
[**post_api_reference_projects_projectid_unlock**](ReferenceApi.md#post_api_reference_projects_projectid_unlock) | **POST** /api/reference/projects/{projectId}/unlock | 
[**post_api_reference_projects_projectid_unshare**](ReferenceApi.md#post_api_reference_projects_projectid_unshare) | **POST** /api/reference/projects/{projectId}/unshare | 
[**put_api_reference_projects_projectid**](ReferenceApi.md#put_api_reference_projects_projectid) | **PUT** /api/reference/projects/{projectId} | 
[**put_api_reference_projects_projectid_examples_exampleid**](ReferenceApi.md#put_api_reference_projects_projectid_examples_exampleid) | **PUT** /api/reference/projects/{projectId}/examples/{exampleId} | 
[**put_api_reference_projects_projectid_results_historyid**](ReferenceApi.md#put_api_reference_projects_projectid_results_historyid) | **PUT** /api/reference/projects/{projectId}/results/{historyId} | 


# **delete_api_reference_projects_projectid**
> delete_api_reference_projects_projectid(project_id)

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
    api_instance = numind.openapi_client.ReferenceApi(api_client)
    project_id = 'project_id_example' # str | 

    try:
        api_instance.delete_api_reference_projects_projectid(project_id)
    except Exception as e:
        print("Exception when calling ReferenceApi->delete_api_reference_projects_projectid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 

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

# **delete_api_reference_projects_projectid_examples_exampleid**
> delete_api_reference_projects_projectid_examples_exampleid(project_id, example_id)

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
    api_instance = numind.openapi_client.ReferenceApi(api_client)
    project_id = 'project_id_example' # str | 
    example_id = 'example_id_example' # str | 

    try:
        api_instance.delete_api_reference_projects_projectid_examples_exampleid(project_id, example_id)
    except Exception as e:
        print("Exception when calling ReferenceApi->delete_api_reference_projects_projectid_examples_exampleid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **example_id** | **str**|  | 

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

# **delete_api_reference_projects_projectid_results_historyid**
> delete_api_reference_projects_projectid_results_historyid(project_id, history_id)

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
    api_instance = numind.openapi_client.ReferenceApi(api_client)
    project_id = 'project_id_example' # str | 
    history_id = 'history_id_example' # str | 

    try:
        api_instance.delete_api_reference_projects_projectid_results_historyid(project_id, history_id)
    except Exception as e:
        print("Exception when calling ReferenceApi->delete_api_reference_projects_projectid_results_historyid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **history_id** | **str**|  | 

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

# **get_api_reference_documents_documentid**
> DocumentResponse get_api_reference_documents_documentid(document_id)

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.document_response import DocumentResponse
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
    api_instance = numind.openapi_client.ReferenceApi(api_client)
    document_id = 'document_id_example' # str | 

    try:
        api_response = api_instance.get_api_reference_documents_documentid(document_id)
        print("The response of ReferenceApi->get_api_reference_documents_documentid:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReferenceApi->get_api_reference_documents_documentid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **document_id** | **str**|  | 

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

# **get_api_reference_documents_documentid_content**
> bytearray get_api_reference_documents_documentid_content(token, document_id)

### Example


```python
import numind.openapi_client
from numind.openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://nuextract.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = numind.openapi_client.Configuration(
    host = "https://nuextract.ai"
)


# Enter a context with an instance of the API client
with numind.openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = numind.openapi_client.ReferenceApi(api_client)
    token = 'token_example' # str | 
    document_id = 'document_id_example' # str | 

    try:
        api_response = api_instance.get_api_reference_documents_documentid_content(token, document_id)
        print("The response of ReferenceApi->get_api_reference_documents_documentid_content:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReferenceApi->get_api_reference_documents_documentid_content: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **token** | **str**|  | 
 **document_id** | **str**|  | 

### Return type

**bytearray**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/octet-stream, text/plain, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  * Content-Type -  <br>  |
**400** | Invalid value for: query parameter token |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_api_reference_projects**
> List[ProjectResponse] get_api_reference_projects(shared, organization_id=organization_id)

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
    api_instance = numind.openapi_client.ReferenceApi(api_client)
    shared = True # bool | 
    organization_id = 'organization_id_example' # str |  (optional)

    try:
        api_response = api_instance.get_api_reference_projects(shared, organization_id=organization_id)
        print("The response of ReferenceApi->get_api_reference_projects:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReferenceApi->get_api_reference_projects: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **shared** | **bool**|  | 
 **organization_id** | **str**|  | [optional] 

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

# **get_api_reference_projects_projectid**
> ProjectResponse get_api_reference_projects_projectid(project_id)

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
    api_instance = numind.openapi_client.ReferenceApi(api_client)
    project_id = 'project_id_example' # str | 

    try:
        api_response = api_instance.get_api_reference_projects_projectid(project_id)
        print("The response of ReferenceApi->get_api_reference_projects_projectid:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReferenceApi->get_api_reference_projects_projectid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 

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

# **get_api_reference_projects_projectid_examples**
> List[ExampleResponse] get_api_reference_projects_projectid_examples(project_id)

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.example_response import ExampleResponse
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
    api_instance = numind.openapi_client.ReferenceApi(api_client)
    project_id = 'project_id_example' # str | 

    try:
        api_response = api_instance.get_api_reference_projects_projectid_examples(project_id)
        print("The response of ReferenceApi->get_api_reference_projects_projectid_examples:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReferenceApi->get_api_reference_projects_projectid_examples: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 

### Return type

[**List[ExampleResponse]**](ExampleResponse.md)

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

# **get_api_reference_projects_projectid_examples_exampleid**
> ExampleResponse get_api_reference_projects_projectid_examples_exampleid(project_id, example_id)

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.example_response import ExampleResponse
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
    api_instance = numind.openapi_client.ReferenceApi(api_client)
    project_id = 'project_id_example' # str | 
    example_id = 'example_id_example' # str | 

    try:
        api_response = api_instance.get_api_reference_projects_projectid_examples_exampleid(project_id, example_id)
        print("The response of ReferenceApi->get_api_reference_projects_projectid_examples_exampleid:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReferenceApi->get_api_reference_projects_projectid_examples_exampleid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **example_id** | **str**|  | 

### Return type

[**ExampleResponse**](ExampleResponse.md)

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

# **get_api_reference_projects_projectid_results**
> List[HistoryResponse] get_api_reference_projects_projectid_results(project_id)

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.history_response import HistoryResponse
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
    api_instance = numind.openapi_client.ReferenceApi(api_client)
    project_id = 'project_id_example' # str | 

    try:
        api_response = api_instance.get_api_reference_projects_projectid_results(project_id)
        print("The response of ReferenceApi->get_api_reference_projects_projectid_results:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReferenceApi->get_api_reference_projects_projectid_results: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 

### Return type

[**List[HistoryResponse]**](HistoryResponse.md)

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

# **get_api_reference_projects_projectid_results_historyid**
> HistoryResponse get_api_reference_projects_projectid_results_historyid(project_id, history_id)

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.history_response import HistoryResponse
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
    api_instance = numind.openapi_client.ReferenceApi(api_client)
    project_id = 'project_id_example' # str | 
    history_id = 'history_id_example' # str | 

    try:
        api_response = api_instance.get_api_reference_projects_projectid_results_historyid(project_id, history_id)
        print("The response of ReferenceApi->get_api_reference_projects_projectid_results_historyid:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReferenceApi->get_api_reference_projects_projectid_results_historyid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **history_id** | **str**|  | 

### Return type

[**HistoryResponse**](HistoryResponse.md)

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

# **post_api_reference_documents_file**
> DocumentResponse post_api_reference_documents_file(x_file_name, body)

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.document_response import DocumentResponse
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
    api_instance = numind.openapi_client.ReferenceApi(api_client)
    x_file_name = 'x_file_name_example' # str | 
    body = None # bytearray | 

    try:
        api_response = api_instance.post_api_reference_documents_file(x_file_name, body)
        print("The response of ReferenceApi->post_api_reference_documents_file:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReferenceApi->post_api_reference_documents_file: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_file_name** | **str**|  | 
 **body** | **bytearray**|  | 

### Return type

[**DocumentResponse**](DocumentResponse.md)

### Authorization

[oauth2Auth](../README.md#oauth2Auth)

### HTTP request headers

 - **Content-Type**: application/octet-stream
 - **Accept**: application/json, text/plain

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**400** | Invalid value for: header x-file-name, Invalid value for: body |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_api_reference_documents_text**
> DocumentResponse post_api_reference_documents_text(text_request)

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.document_response import DocumentResponse
from numind.openapi_client.models.text_request import TextRequest
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
    api_instance = numind.openapi_client.ReferenceApi(api_client)
    text_request = numind.openapi_client.TextRequest() # TextRequest | 

    try:
        api_response = api_instance.post_api_reference_documents_text(text_request)
        print("The response of ReferenceApi->post_api_reference_documents_text:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReferenceApi->post_api_reference_documents_text: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **text_request** | [**TextRequest**](TextRequest.md)|  | 

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

# **post_api_reference_infer_template**
> Obj post_api_reference_infer_template(template_request)

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.obj import Obj
from numind.openapi_client.models.template_request import TemplateRequest
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
    api_instance = numind.openapi_client.ReferenceApi(api_client)
    template_request = numind.openapi_client.TemplateRequest() # TemplateRequest | 

    try:
        api_response = api_instance.post_api_reference_infer_template(template_request)
        print("The response of ReferenceApi->post_api_reference_infer_template:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReferenceApi->post_api_reference_infer_template: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **template_request** | [**TemplateRequest**](TemplateRequest.md)|  | 

### Return type

[**Obj**](Obj.md)

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

# **post_api_reference_projects**
> ProjectResponse post_api_reference_projects(create_or_update_project_request)

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.create_or_update_project_request import CreateOrUpdateProjectRequest
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
    api_instance = numind.openapi_client.ReferenceApi(api_client)
    create_or_update_project_request = {"name":"Order Delivery Information Extraction","description":"Automated extraction of order delivery details from scanned documents","template":{"orderId":"verbatim-string","customerId":"verbatim-string","orderDate":"date-time","status":["pending","processed","shipped","delivered","cancelled"],"totalAmount":"number","currency":"string","items":[{"productId":"string","quantity":"number","unitPrice":"number"}],"shippingAddress":{"street":"string","city":"string","state":"string","country":"string","zip":"string"},"comments":"string","deliveryPreferences":[["contactless_delivery","signature_required","leave_at_door","pickup_from_store","deliver_to_neighbor","schedule_delivery"]],"estimatedDelivery":"date-time"},"ownerOrganization":"cd5cd82a-cc30-42be-ab39-f29fd7db279e"} # CreateOrUpdateProjectRequest | 

    try:
        api_response = api_instance.post_api_reference_projects(create_or_update_project_request)
        print("The response of ReferenceApi->post_api_reference_projects:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReferenceApi->post_api_reference_projects: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_or_update_project_request** | [**CreateOrUpdateProjectRequest**](CreateOrUpdateProjectRequest.md)|  | 

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

# **post_api_reference_projects_projectid_duplicate**
> ProjectResponse post_api_reference_projects_projectid_duplicate(project_id)

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
    api_instance = numind.openapi_client.ReferenceApi(api_client)
    project_id = 'project_id_example' # str | 

    try:
        api_response = api_instance.post_api_reference_projects_projectid_duplicate(project_id)
        print("The response of ReferenceApi->post_api_reference_projects_projectid_duplicate:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReferenceApi->post_api_reference_projects_projectid_duplicate: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 

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

# **post_api_reference_projects_projectid_examples**
> ExampleResponse post_api_reference_projects_projectid_examples(project_id, create_or_update_example_request)

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.create_or_update_example_request import CreateOrUpdateExampleRequest
from numind.openapi_client.models.example_response import ExampleResponse
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
    api_instance = numind.openapi_client.ReferenceApi(api_client)
    project_id = 'project_id_example' # str | 
    create_or_update_example_request = {"documentId":"eb0f0c2f-b01b-4f63-8356-95efb3d4f755","result":{"orderId":"o-56789","customerId":"c-10293","orderDate":"2024-02-28T14:30:00.000Z","status":"shipped","totalAmount":199.98,"currency":"USD","items":[{"productId":"p-00123","quantity":2,"unitPrice":99.99},{"productId":"p-00456","quantity":1,"unitPrice":49.99}],"shippingAddress":{"street":"456 Oak Ave","city":"Seattle","state":"WA","country":"USA","zip":"98101"},"comments":"Please call before delivery","deliveryPreferences":["signature_required","schedule_delivery"],"estimatedDelivery":"2024-03-05T18:00:00.000Z"}} # CreateOrUpdateExampleRequest | 

    try:
        api_response = api_instance.post_api_reference_projects_projectid_examples(project_id, create_or_update_example_request)
        print("The response of ReferenceApi->post_api_reference_projects_projectid_examples:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReferenceApi->post_api_reference_projects_projectid_examples: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **create_or_update_example_request** | [**CreateOrUpdateExampleRequest**](CreateOrUpdateExampleRequest.md)|  | 

### Return type

[**ExampleResponse**](ExampleResponse.md)

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

# **post_api_reference_projects_projectid_infer_document_documentid**
> InferenceResponse post_api_reference_projects_projectid_infer_document_documentid(project_id, document_id)

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.inference_response import InferenceResponse
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
    api_instance = numind.openapi_client.ReferenceApi(api_client)
    project_id = 'project_id_example' # str | 
    document_id = 'document_id_example' # str | 

    try:
        api_response = api_instance.post_api_reference_projects_projectid_infer_document_documentid(project_id, document_id)
        print("The response of ReferenceApi->post_api_reference_projects_projectid_infer_document_documentid:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReferenceApi->post_api_reference_projects_projectid_infer_document_documentid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **document_id** | **str**|  | 

### Return type

[**InferenceResponse**](InferenceResponse.md)

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

# **post_api_reference_projects_projectid_infer_file**
> InferenceResponse post_api_reference_projects_projectid_infer_file(project_id, x_file_name, body)

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.inference_response import InferenceResponse
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
    api_instance = numind.openapi_client.ReferenceApi(api_client)
    project_id = 'project_id_example' # str | 
    x_file_name = 'x_file_name_example' # str | 
    body = None # bytearray | 

    try:
        api_response = api_instance.post_api_reference_projects_projectid_infer_file(project_id, x_file_name, body)
        print("The response of ReferenceApi->post_api_reference_projects_projectid_infer_file:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReferenceApi->post_api_reference_projects_projectid_infer_file: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **x_file_name** | **str**|  | 
 **body** | **bytearray**|  | 

### Return type

[**InferenceResponse**](InferenceResponse.md)

### Authorization

[oauth2Auth](../README.md#oauth2Auth)

### HTTP request headers

 - **Content-Type**: application/octet-stream
 - **Accept**: application/json, text/plain

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**400** | Invalid value for: header x-file-name, Invalid value for: body |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_api_reference_projects_projectid_infer_text**
> InferenceResponse post_api_reference_projects_projectid_infer_text(project_id, text_request)

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.inference_response import InferenceResponse
from numind.openapi_client.models.text_request import TextRequest
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
    api_instance = numind.openapi_client.ReferenceApi(api_client)
    project_id = 'project_id_example' # str | 
    text_request = numind.openapi_client.TextRequest() # TextRequest | 

    try:
        api_response = api_instance.post_api_reference_projects_projectid_infer_text(project_id, text_request)
        print("The response of ReferenceApi->post_api_reference_projects_projectid_infer_text:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReferenceApi->post_api_reference_projects_projectid_infer_text: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **text_request** | [**TextRequest**](TextRequest.md)|  | 

### Return type

[**InferenceResponse**](InferenceResponse.md)

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

# **post_api_reference_projects_projectid_lock**
> post_api_reference_projects_projectid_lock(project_id)

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
    api_instance = numind.openapi_client.ReferenceApi(api_client)
    project_id = 'project_id_example' # str | 

    try:
        api_instance.post_api_reference_projects_projectid_lock(project_id)
    except Exception as e:
        print("Exception when calling ReferenceApi->post_api_reference_projects_projectid_lock: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 

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

# **post_api_reference_projects_projectid_results**
> HistoryResponse post_api_reference_projects_projectid_results(project_id, create_or_update_history_request)

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.create_or_update_history_request import CreateOrUpdateHistoryRequest
from numind.openapi_client.models.history_response import HistoryResponse
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
    api_instance = numind.openapi_client.ReferenceApi(api_client)
    project_id = 'project_id_example' # str | 
    create_or_update_history_request = {"ownerOrganization":"a0e8d543-877a-4ed7-a37b-55c181a39ad3","documentId":"a799cb81-9f92-4587-af28-fe57ae43607b","result":{"orderId":"o-56789","customerId":"c-10293","orderDate":"2024-02-28T14:30:00.000Z","status":"shipped","totalAmount":199.98,"currency":"USD","items":[{"productId":"p-00123","quantity":2,"unitPrice":99.99},{"productId":"p-00456","quantity":1,"unitPrice":49.99}],"shippingAddress":{"street":"456 Oak Ave","city":"Seattle","state":"WA","country":"USA","zip":"98101"},"comments":"Please call before delivery","deliveryPreferences":["signature_required","schedule_delivery"],"estimatedDelivery":"2024-03-05T18:00:00.000Z"}} # CreateOrUpdateHistoryRequest | 

    try:
        api_response = api_instance.post_api_reference_projects_projectid_results(project_id, create_or_update_history_request)
        print("The response of ReferenceApi->post_api_reference_projects_projectid_results:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReferenceApi->post_api_reference_projects_projectid_results: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **create_or_update_history_request** | [**CreateOrUpdateHistoryRequest**](CreateOrUpdateHistoryRequest.md)|  | 

### Return type

[**HistoryResponse**](HistoryResponse.md)

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

# **post_api_reference_projects_projectid_share**
> post_api_reference_projects_projectid_share(project_id)

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
    api_instance = numind.openapi_client.ReferenceApi(api_client)
    project_id = 'project_id_example' # str | 

    try:
        api_instance.post_api_reference_projects_projectid_share(project_id)
    except Exception as e:
        print("Exception when calling ReferenceApi->post_api_reference_projects_projectid_share: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 

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

# **post_api_reference_projects_projectid_unlock**
> post_api_reference_projects_projectid_unlock(project_id)

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
    api_instance = numind.openapi_client.ReferenceApi(api_client)
    project_id = 'project_id_example' # str | 

    try:
        api_instance.post_api_reference_projects_projectid_unlock(project_id)
    except Exception as e:
        print("Exception when calling ReferenceApi->post_api_reference_projects_projectid_unlock: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 

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

# **post_api_reference_projects_projectid_unshare**
> post_api_reference_projects_projectid_unshare(project_id)

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
    api_instance = numind.openapi_client.ReferenceApi(api_client)
    project_id = 'project_id_example' # str | 

    try:
        api_instance.post_api_reference_projects_projectid_unshare(project_id)
    except Exception as e:
        print("Exception when calling ReferenceApi->post_api_reference_projects_projectid_unshare: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 

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

# **put_api_reference_projects_projectid**
> ProjectResponse put_api_reference_projects_projectid(project_id, create_or_update_project_request)

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.create_or_update_project_request import CreateOrUpdateProjectRequest
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
    api_instance = numind.openapi_client.ReferenceApi(api_client)
    project_id = 'project_id_example' # str | 
    create_or_update_project_request = {name=Order Delivery Information Extraction, description=Automated extraction of order delivery details from scanned documents, template={orderId=verbatim-string, customerId=verbatim-string, orderDate=date-time, status=[pending, processed, shipped, delivered, cancelled], totalAmount=number, currency=string, items=[{productId=string, quantity=number, unitPrice=number}], shippingAddress={street=string, city=string, state=string, country=string, zip=string}, comments=string, deliveryPreferences=[[contactless_delivery, signature_required, leave_at_door, pickup_from_store, deliver_to_neighbor, schedule_delivery]], estimatedDelivery=date-time}, ownerOrganization=cd5cd82a-cc30-42be-ab39-f29fd7db279e} # CreateOrUpdateProjectRequest | 

    try:
        api_response = api_instance.put_api_reference_projects_projectid(project_id, create_or_update_project_request)
        print("The response of ReferenceApi->put_api_reference_projects_projectid:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReferenceApi->put_api_reference_projects_projectid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **create_or_update_project_request** | [**CreateOrUpdateProjectRequest**](CreateOrUpdateProjectRequest.md)|  | 

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

# **put_api_reference_projects_projectid_examples_exampleid**
> ExampleResponse put_api_reference_projects_projectid_examples_exampleid(project_id, example_id, create_or_update_example_request)

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.create_or_update_example_request import CreateOrUpdateExampleRequest
from numind.openapi_client.models.example_response import ExampleResponse
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
    api_instance = numind.openapi_client.ReferenceApi(api_client)
    project_id = 'project_id_example' # str | 
    example_id = 'example_id_example' # str | 
    create_or_update_example_request = {documentId=eb0f0c2f-b01b-4f63-8356-95efb3d4f755, result={orderId=o-56789, customerId=c-10293, orderDate=2024-02-28T14:30:00.000Z, status=shipped, totalAmount=199.98, currency=USD, items=[{productId=p-00123, quantity=2, unitPrice=99.99}, {productId=p-00456, quantity=1, unitPrice=49.99}], shippingAddress={street=456 Oak Ave, city=Seattle, state=WA, country=USA, zip=98101}, comments=Please call before delivery, deliveryPreferences=[signature_required, schedule_delivery], estimatedDelivery=2024-03-05T18:00:00.000Z}} # CreateOrUpdateExampleRequest | 

    try:
        api_response = api_instance.put_api_reference_projects_projectid_examples_exampleid(project_id, example_id, create_or_update_example_request)
        print("The response of ReferenceApi->put_api_reference_projects_projectid_examples_exampleid:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReferenceApi->put_api_reference_projects_projectid_examples_exampleid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **example_id** | **str**|  | 
 **create_or_update_example_request** | [**CreateOrUpdateExampleRequest**](CreateOrUpdateExampleRequest.md)|  | 

### Return type

[**ExampleResponse**](ExampleResponse.md)

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

# **put_api_reference_projects_projectid_results_historyid**
> HistoryResponse put_api_reference_projects_projectid_results_historyid(project_id, history_id, create_or_update_history_request)

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.create_or_update_history_request import CreateOrUpdateHistoryRequest
from numind.openapi_client.models.history_response import HistoryResponse
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
    api_instance = numind.openapi_client.ReferenceApi(api_client)
    project_id = 'project_id_example' # str | 
    history_id = 'history_id_example' # str | 
    create_or_update_history_request = {ownerOrganization=a0e8d543-877a-4ed7-a37b-55c181a39ad3, documentId=a799cb81-9f92-4587-af28-fe57ae43607b, result={orderId=o-56789, customerId=c-10293, orderDate=2024-02-28T14:30:00.000Z, status=shipped, totalAmount=199.98, currency=USD, items=[{productId=p-00123, quantity=2, unitPrice=99.99}, {productId=p-00456, quantity=1, unitPrice=49.99}], shippingAddress={street=456 Oak Ave, city=Seattle, state=WA, country=USA, zip=98101}, comments=Please call before delivery, deliveryPreferences=[signature_required, schedule_delivery], estimatedDelivery=2024-03-05T18:00:00.000Z}} # CreateOrUpdateHistoryRequest | 

    try:
        api_response = api_instance.put_api_reference_projects_projectid_results_historyid(project_id, history_id, create_or_update_history_request)
        print("The response of ReferenceApi->put_api_reference_projects_projectid_results_historyid:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReferenceApi->put_api_reference_projects_projectid_results_historyid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **history_id** | **str**|  | 
 **create_or_update_history_request** | [**CreateOrUpdateHistoryRequest**](CreateOrUpdateHistoryRequest.md)|  | 

### Return type

[**HistoryResponse**](HistoryResponse.md)

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

