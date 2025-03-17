# numind.openapi_client.AuthenticationApi

All URIs are relative to *https://api.nuextract.ai/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_api_auth_user_tokens_usertokenid**](AuthenticationApi.md#delete_api_auth_user_tokens_usertokenid) | **DELETE** /api/auth/user-tokens/{userTokenId} | 
[**get_api_auth**](AuthenticationApi.md#get_api_auth) | **GET** /api/auth | 
[**get_api_auth_me**](AuthenticationApi.md#get_api_auth_me) | **GET** /api/auth/me | 
[**get_api_auth_user_tokens**](AuthenticationApi.md#get_api_auth_user_tokens) | **GET** /api/auth/user-tokens | 
[**post_api_auth_logout**](AuthenticationApi.md#post_api_auth_logout) | **POST** /api/auth/logout | 
[**post_api_auth_token**](AuthenticationApi.md#post_api_auth_token) | **POST** /api/auth/token | 
[**post_api_auth_user_tokens**](AuthenticationApi.md#post_api_auth_user_tokens) | **POST** /api/auth/user-tokens | 
[**put_api_auth_user_tokens_usertokenid**](AuthenticationApi.md#put_api_auth_user_tokens_usertokenid) | **PUT** /api/auth/user-tokens/{userTokenId} | 


# **delete_api_auth_user_tokens_usertokenid**
> delete_api_auth_user_tokens_usertokenid(user_token_id)

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.nuextract.ai/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = numind.openapi_client.Configuration(
    host = "https://api.nuextract.ai/v1"
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
    user_token_id = 'user_token_id_example' # str | 

    try:
        api_instance.delete_api_auth_user_tokens_usertokenid(user_token_id)
    except Exception as e:
        print("Exception when calling AuthenticationApi->delete_api_auth_user_tokens_usertokenid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_token_id** | **str**|  | 

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

# Defining the host is optional and defaults to https://api.nuextract.ai/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = numind.openapi_client.Configuration(
    host = "https://api.nuextract.ai/v1"
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

# **get_api_auth_me**
> User get_api_auth_me()

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.user import User
from numind.openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.nuextract.ai/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = numind.openapi_client.Configuration(
    host = "https://api.nuextract.ai/v1"
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

# **get_api_auth_user_tokens**
> List[UserTokenResponse] get_api_auth_user_tokens()

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.user_token_response import UserTokenResponse
from numind.openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.nuextract.ai/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = numind.openapi_client.Configuration(
    host = "https://api.nuextract.ai/v1"
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
        api_response = api_instance.get_api_auth_user_tokens()
        print("The response of AuthenticationApi->get_api_auth_user_tokens:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuthenticationApi->get_api_auth_user_tokens: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[UserTokenResponse]**](UserTokenResponse.md)

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

# **post_api_auth_logout**
> object post_api_auth_logout(body)

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.nuextract.ai/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = numind.openapi_client.Configuration(
    host = "https://api.nuextract.ai/v1"
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
from numind.openapi_client.models.token_request import TokenRequest
from numind.openapi_client.models.token_response import TokenResponse
from numind.openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.nuextract.ai/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = numind.openapi_client.Configuration(
    host = "https://api.nuextract.ai/v1"
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

# **post_api_auth_user_tokens**
> UserTokenResponse post_api_auth_user_tokens(create_or_update_user_token)

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.create_or_update_user_token import CreateOrUpdateUserToken
from numind.openapi_client.models.user_token_response import UserTokenResponse
from numind.openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.nuextract.ai/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = numind.openapi_client.Configuration(
    host = "https://api.nuextract.ai/v1"
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
    create_or_update_user_token = numind.openapi_client.CreateOrUpdateUserToken() # CreateOrUpdateUserToken | 

    try:
        api_response = api_instance.post_api_auth_user_tokens(create_or_update_user_token)
        print("The response of AuthenticationApi->post_api_auth_user_tokens:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuthenticationApi->post_api_auth_user_tokens: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_or_update_user_token** | [**CreateOrUpdateUserToken**](CreateOrUpdateUserToken.md)|  | 

### Return type

[**UserTokenResponse**](UserTokenResponse.md)

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

# **put_api_auth_user_tokens_usertokenid**
> UserTokenResponse put_api_auth_user_tokens_usertokenid(user_token_id, create_or_update_user_token)

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.create_or_update_user_token import CreateOrUpdateUserToken
from numind.openapi_client.models.user_token_response import UserTokenResponse
from numind.openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.nuextract.ai/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = numind.openapi_client.Configuration(
    host = "https://api.nuextract.ai/v1"
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
    user_token_id = 'user_token_id_example' # str | 
    create_or_update_user_token = numind.openapi_client.CreateOrUpdateUserToken() # CreateOrUpdateUserToken | 

    try:
        api_response = api_instance.put_api_auth_user_tokens_usertokenid(user_token_id, create_or_update_user_token)
        print("The response of AuthenticationApi->put_api_auth_user_tokens_usertokenid:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuthenticationApi->put_api_auth_user_tokens_usertokenid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_token_id** | **str**|  | 
 **create_or_update_user_token** | [**CreateOrUpdateUserToken**](CreateOrUpdateUserToken.md)|  | 

### Return type

[**UserTokenResponse**](UserTokenResponse.md)

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

