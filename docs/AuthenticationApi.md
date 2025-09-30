# numind.openapi_client.AuthenticationApi

All URIs are relative to *https://nuextract.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_api_auth_api_keys_apikeyid**](AuthenticationApi.md#delete_api_auth_api_keys_apikeyid) | **DELETE** /api/auth/api-keys/{apiKeyId} | 
[**get_api_auth**](AuthenticationApi.md#get_api_auth) | **GET** /api/auth | 
[**get_api_auth_api_keys**](AuthenticationApi.md#get_api_auth_api_keys) | **GET** /api/auth/api-keys | 
[**get_api_auth_me**](AuthenticationApi.md#get_api_auth_me) | **GET** /api/auth/me | 
[**post_api_auth_api_keys**](AuthenticationApi.md#post_api_auth_api_keys) | **POST** /api/auth/api-keys | 
[**post_api_auth_logout**](AuthenticationApi.md#post_api_auth_logout) | **POST** /api/auth/logout | 
[**post_api_auth_token**](AuthenticationApi.md#post_api_auth_token) | **POST** /api/auth/token | 
[**put_api_auth_api_keys_apikeyid**](AuthenticationApi.md#put_api_auth_api_keys_apikeyid) | **PUT** /api/auth/api-keys/{apiKeyId} | 


# **delete_api_auth_api_keys_apikeyid**
> delete_api_auth_api_keys_apikeyid(api_key_id)

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
    api_instance = numind.openapi_client.AuthenticationApi(api_client)
    api_key_id = 'api_key_id_example' # str | Unique api key identifier.

    try:
        api_instance.delete_api_auth_api_keys_apikeyid(api_key_id)
    except Exception as e:
        print("Exception when calling AuthenticationApi->delete_api_auth_api_keys_apikeyid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_key_id** | **str**| Unique api key identifier. | 

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

# **get_api_auth**
> str get_api_auth(redirect_uri)

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
    api_instance = numind.openapi_client.AuthenticationApi(api_client)
    redirect_uri = 'redirect_uri_example' # str | 

    try:
        api_response = api_instance.get_api_auth(redirect_uri)
        print("The response of AuthenticationApi->get_api_auth:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuthenticationApi->get_api_auth: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **redirect_uri** | **str**|  | 

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
**400** | Invalid value for: query parameter redirectUri |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_api_auth_api_keys**
> List[ApiKeyResponse] get_api_auth_api_keys()

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.api_key_response import ApiKeyResponse
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
    api_instance = numind.openapi_client.AuthenticationApi(api_client)

    try:
        api_response = api_instance.get_api_auth_api_keys()
        print("The response of AuthenticationApi->get_api_auth_api_keys:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuthenticationApi->get_api_auth_api_keys: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[ApiKeyResponse]**](ApiKeyResponse.md)

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

# **get_api_auth_me**
> User get_api_auth_me()

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.user import User
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
    api_instance = numind.openapi_client.AuthenticationApi(api_client)

    try:
        api_response = api_instance.get_api_auth_me()
        print("The response of AuthenticationApi->get_api_auth_me:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuthenticationApi->get_api_auth_me: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**User**](User.md)

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

# **post_api_auth_api_keys**
> ApiKeyResponse post_api_auth_api_keys(create_api_key)

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.api_key_response import ApiKeyResponse
from numind.models.create_api_key import CreateApiKey
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
    api_instance = numind.openapi_client.AuthenticationApi(api_client)
    create_api_key = numind.openapi_client.CreateApiKey() # CreateApiKey | 

    try:
        api_response = api_instance.post_api_auth_api_keys(create_api_key)
        print("The response of AuthenticationApi->post_api_auth_api_keys:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuthenticationApi->post_api_auth_api_keys: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_api_key** | [**CreateApiKey**](CreateApiKey.md)|  | 

### Return type

[**ApiKeyResponse**](ApiKeyResponse.md)

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

# **post_api_auth_logout**
> object post_api_auth_logout(body)

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
    api_instance = numind.openapi_client.AuthenticationApi(api_client)
    body = 'body_example' # str | 

    try:
        api_response = api_instance.post_api_auth_logout(body)
        print("The response of AuthenticationApi->post_api_auth_logout:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuthenticationApi->post_api_auth_logout: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **str**|  | 

### Return type

**object**

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

# **post_api_auth_token**
> TokenResponse post_api_auth_token(token_request)

### Example


```python
import numind.openapi_client
from numind.models.token_request import TokenRequest
from numind.models.token_response import TokenResponse
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
    api_instance = numind.openapi_client.AuthenticationApi(api_client)
    token_request = {"type":"ai.numind.extract.shared.TokenCodeRequest","code":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SbXT6e7R0N1hVeJHtTh2uFd7y8Rg-Vu0oiL4T1jbAY0","redirectUri":"http://localhost:5173"} # TokenRequest | 

    try:
        api_response = api_instance.post_api_auth_token(token_request)
        print("The response of AuthenticationApi->post_api_auth_token:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuthenticationApi->post_api_auth_token: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **token_request** | [**TokenRequest**](TokenRequest.md)|  | 

### Return type

[**TokenResponse**](TokenResponse.md)

### Authorization

No authorization required

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

# **put_api_auth_api_keys_apikeyid**
> ApiKeyResponse put_api_auth_api_keys_apikeyid(api_key_id, update_api_key)

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.api_key_response import ApiKeyResponse
from numind.models.update_api_key import UpdateApiKey
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
    api_instance = numind.openapi_client.AuthenticationApi(api_client)
    api_key_id = 'api_key_id_example' # str | Unique api key identifier.
    update_api_key = numind.openapi_client.UpdateApiKey() # UpdateApiKey | 

    try:
        api_response = api_instance.put_api_auth_api_keys_apikeyid(api_key_id, update_api_key)
        print("The response of AuthenticationApi->put_api_auth_api_keys_apikeyid:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuthenticationApi->put_api_auth_api_keys_apikeyid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_key_id** | **str**| Unique api key identifier. | 
 **update_api_key** | [**UpdateApiKey**](UpdateApiKey.md)|  | 

### Return type

[**ApiKeyResponse**](ApiKeyResponse.md)

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

