# numind.openapi_client.ProjectImportExportApi

All URIs are relative to *https://nuextract.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_api_extraction_export_jobs_jobid_download**](ProjectImportExportApi.md#get_api_extraction_export_jobs_jobid_download) | **GET** /api/extraction/export/jobs/{jobId}/download | 
[**get_api_extraction_projectkind_projectid_export**](ProjectImportExportApi.md#get_api_extraction_projectkind_projectid_export) | **GET** /api/extraction/{projectKind}/{projectId}/export | 
[**post_api_extraction_import**](ProjectImportExportApi.md#post_api_extraction_import) | **POST** /api/extraction/import | 
[**post_api_extraction_import_jobs**](ProjectImportExportApi.md#post_api_extraction_import_jobs) | **POST** /api/extraction/import/jobs | 
[**post_api_extraction_projectkind_projectid_export_jobs**](ProjectImportExportApi.md#post_api_extraction_projectkind_projectid_export_jobs) | **POST** /api/extraction/{projectKind}/{projectId}/export/jobs | 


# **get_api_extraction_export_jobs_jobid_download**
> bytes get_api_extraction_export_jobs_jobid_download(job_id, x_organization_id=x_organization_id)


 Download the zip archive produced by a completed project export job.

#### Error Responses:
`400 Bad Request` - If the job is not a project export job, or has not completed yet.

`404 Not Found` - If the job does not exist, or its archive has expired.

`403 Forbidden` - If the user does not have permission to access this job.

`409 Conflict` - If the job was canceled.

`500 Internal Server Error` - If the job timed out.

If the job failed, the response is the job's own error, with its status code.
    

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://nuextract.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = numind.openapi_client.Configuration(host="https://nuextract.ai")

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
with numind.openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = numind.openapi_client.ProjectImportExportApi(api_client)
    job_id = "job_id_example"  # str | Unique project export job identifier.
    x_organization_id = "x_organization_id_example"  # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)

    try:
        api_response = api_instance.get_api_extraction_export_jobs_jobid_download(
            job_id, x_organization_id=x_organization_id
        )
        print(
            "The response of ProjectImportExportApi->get_api_extraction_export_jobs_jobid_download:\n"
        )
        pprint(api_response)
    except Exception as e:
        print(
            "Exception when calling ProjectImportExportApi->get_api_extraction_export_jobs_jobid_download: %s\n"
            % e
        )
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **job_id** | **str**| Unique project export job identifier. | 
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 

### Return type

**bytes**

### Authorization

[oauth2Auth](../README.md#oauth2Auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/zip, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  * Content-Type -  <br>  * Content-Disposition -  <br>  * X-Filename -  <br>  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_api_extraction_projectkind_projectid_export**
> bytes get_api_extraction_projectkind_projectid_export(project_kind, project_id, x_organization_id=x_organization_id)

Exports a project as a zip archive.

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://nuextract.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = numind.openapi_client.Configuration(host="https://nuextract.ai")

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
with numind.openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = numind.openapi_client.ProjectImportExportApi(api_client)
    project_kind = "project_kind_example"  # str | Project kind to export.
    project_id = "project_id_example"  # str | Unique project identifier.
    x_organization_id = "x_organization_id_example"  # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)

    try:
        api_response = api_instance.get_api_extraction_projectkind_projectid_export(
            project_kind, project_id, x_organization_id=x_organization_id
        )
        print(
            "The response of ProjectImportExportApi->get_api_extraction_projectkind_projectid_export:\n"
        )
        pprint(api_response)
    except Exception as e:
        print(
            "Exception when calling ProjectImportExportApi->get_api_extraction_projectkind_projectid_export: %s\n"
            % e
        )
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_kind** | **str**| Project kind to export. | 
 **project_id** | **str**| Unique project identifier. | 
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 

### Return type

**bytes**

### Authorization

[oauth2Auth](../README.md#oauth2Auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/zip, text/plain, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  * Content-Type -  <br>  * Content-Disposition -  <br>  * X-Filename -  <br>  |
**400** | Invalid value for: path parameter projectKind |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_api_extraction_import**
> ImportProjectResponse post_api_extraction_import(body, x_organization_id=x_organization_id)

Imports a project from a zip archive.

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.import_project_response import ImportProjectResponse
from numind.openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://nuextract.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = numind.openapi_client.Configuration(host="https://nuextract.ai")

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
with numind.openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = numind.openapi_client.ProjectImportExportApi(api_client)
    body = None  # bytes |
    x_organization_id = "x_organization_id_example"  # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)

    try:
        api_response = api_instance.post_api_extraction_import(
            body, x_organization_id=x_organization_id
        )
        print("The response of ProjectImportExportApi->post_api_extraction_import:\n")
        pprint(api_response)
    except Exception as e:
        print(
            "Exception when calling ProjectImportExportApi->post_api_extraction_import: %s\n"
            % e
        )
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **bytes**|  | 
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 

### Return type

[**ImportProjectResponse**](ImportProjectResponse.md)

### Authorization

[oauth2Auth](../README.md#oauth2Auth)

### HTTP request headers

 - **Content-Type**: application/octet-stream
 - **Accept**: application/json, text/plain

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**400** | Invalid value for: body |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_api_extraction_import_jobs**
> JobIdResponse post_api_extraction_import_jobs(body, x_organization_id=x_organization_id)


 Import a project from a zip archive produced by a project export, in an async job.

#### Response:
 Returns a JSON containing the job ID that can be used to retrieve the job status and results.

 If the job is completed successfully, the job's output data contains the imported project.

#### Error Responses:
`400 Bad Request` - If the archive is not a valid project archive.
    

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.job_id_response import JobIdResponse
from numind.openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://nuextract.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = numind.openapi_client.Configuration(host="https://nuextract.ai")

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
with numind.openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = numind.openapi_client.ProjectImportExportApi(api_client)
    body = None  # bytes |
    x_organization_id = "x_organization_id_example"  # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)

    try:
        api_response = api_instance.post_api_extraction_import_jobs(
            body, x_organization_id=x_organization_id
        )
        print(
            "The response of ProjectImportExportApi->post_api_extraction_import_jobs:\n"
        )
        pprint(api_response)
    except Exception as e:
        print(
            "Exception when calling ProjectImportExportApi->post_api_extraction_import_jobs: %s\n"
            % e
        )
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **bytes**|  | 
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 

### Return type

[**JobIdResponse**](JobIdResponse.md)

### Authorization

[oauth2Auth](../README.md#oauth2Auth)

### HTTP request headers

 - **Content-Type**: application/octet-stream
 - **Accept**: application/json, text/plain

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**400** | Invalid value for: body |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_api_extraction_projectkind_projectid_export_jobs**
> JobIdResponse post_api_extraction_projectkind_projectid_export_jobs(project_kind, project_id, x_organization_id=x_organization_id)


 Export a project as a zip archive, in an async job.

#### Response:
 Returns a JSON containing the job ID that can be used to retrieve the job status and results.

 Once the job is completed, download the archive with `GET /extraction/export/jobs/{jobId}/download`.
 The archive can be downloaded until the job is deleted.

#### Error Responses:
`404 Not Found` - If the project does not exist.

`403 Forbidden` - If the user does not have permission to access this project.
    

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.job_id_response import JobIdResponse
from numind.openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://nuextract.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = numind.openapi_client.Configuration(host="https://nuextract.ai")

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
with numind.openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = numind.openapi_client.ProjectImportExportApi(api_client)
    project_kind = "project_kind_example"  # str | Project kind to export.
    project_id = "project_id_example"  # str | Unique project identifier.
    x_organization_id = "x_organization_id_example"  # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)

    try:
        api_response = (
            api_instance.post_api_extraction_projectkind_projectid_export_jobs(
                project_kind, project_id, x_organization_id=x_organization_id
            )
        )
        print(
            "The response of ProjectImportExportApi->post_api_extraction_projectkind_projectid_export_jobs:\n"
        )
        pprint(api_response)
    except Exception as e:
        print(
            "Exception when calling ProjectImportExportApi->post_api_extraction_projectkind_projectid_export_jobs: %s\n"
            % e
        )
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_kind** | **str**| Project kind to export. | 
 **project_id** | **str**| Unique project identifier. | 
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 

### Return type

[**JobIdResponse**](JobIdResponse.md)

### Authorization

[oauth2Auth](../README.md#oauth2Auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, text/plain

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**400** | Invalid value for: path parameter projectKind |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

