# numind.openapi_client.DefaultApi

All URIs are relative to *https://nuextract.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_api_debug_status_code**](DefaultApi.md#get_api_debug_status_code) | **GET** /api/debug/status/{code} | 
[**get_api_health**](DefaultApi.md#get_api_health) | **GET** /api/health | 
[**get_api_inference_status**](DefaultApi.md#get_api_inference_status) | **GET** /api/inference-status | 
[**get_api_ping**](DefaultApi.md#get_api_ping) | **GET** /api/ping | 
[**get_api_version**](DefaultApi.md#get_api_version) | **GET** /api/version | 


# **get_api_debug_status_code**
> get_api_debug_status_code(code, delay_ms=delay_ms)

Simulate HTTP status code and latency for debugging. Requires X-Internal-Debug header.

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
    api_instance = numind.openapi_client.DefaultApi(api_client)
    code = 56 # int | HTTP status code to return
    delay_ms = 56 # int | Optional delay in ms before responding (default 0) (optional)

    try:
        api_instance.get_api_debug_status_code(code, delay_ms=delay_ms)
    except Exception as e:
        print("Exception when calling DefaultApi->get_api_debug_status_code: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **int**| HTTP status code to return | 
 **delay_ms** | **int**| Optional delay in ms before responding (default 0) | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  * X-Debug-DelayMs - Actual delay applied in ms <br>  |
**400** | Invalid value for: path parameter code, Invalid value for: query parameter delayMs |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_api_health**
> HealthResponse get_api_health()

### Example


```python
import numind.openapi_client
from numind.models.health_response import HealthResponse
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
    api_instance = numind.openapi_client.DefaultApi(api_client)

    try:
        api_response = api_instance.get_api_health()
        print("The response of DefaultApi->get_api_health:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_api_health: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**HealthResponse**](HealthResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_api_inference_status**
> Dict[str, InferenceStatus] get_api_inference_status()

### Example


```python
import numind.openapi_client
from numind.models.inference_status import InferenceStatus
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
    api_instance = numind.openapi_client.DefaultApi(api_client)

    try:
        api_response = api_instance.get_api_inference_status()
        print("The response of DefaultApi->get_api_inference_status:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_api_inference_status: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**Dict[str, InferenceStatus]**](InferenceStatus.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_api_ping**
> str get_api_ping()

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
    api_instance = numind.openapi_client.DefaultApi(api_client)

    try:
        api_response = api_instance.get_api_ping()
        print("The response of DefaultApi->get_api_ping:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_api_ping: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_api_version**
> VersionResponse get_api_version()

### Example


```python
import numind.openapi_client
from numind.models.version_response import VersionResponse
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
    api_instance = numind.openapi_client.DefaultApi(api_client)

    try:
        api_response = api_instance.get_api_version()
        print("The response of DefaultApi->get_api_version:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_api_version: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**VersionResponse**](VersionResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

