# numind.openapi_client.UsageApi

All URIs are relative to *https://nuextract.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_api_usage_global**](UsageApi.md#get_api_usage_global) | **GET** /api/usage/global | 


# **get_api_usage_global**
> UsageResponse get_api_usage_global(x_organization_id=x_organization_id, project_id=project_id, inference_type=inference_type, api_key_id=api_key_id, var_from=var_from, to=to)

Get global platform usage metrics with optional filters

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.usage_response import UsageResponse
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
    api_instance = numind.openapi_client.UsageApi(api_client)
    x_organization_id = 'x_organization_id_example' # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)
    project_id = 'project_id_example' # str | Filter usage by project ID. When provided, 'inferenceType' is required. (optional)
    inference_type = 'inference_type_example' # str | Filter usage by inference type: structured, content, or template extraction. (optional)
    api_key_id = 'api_key_id_example' # str | Filter usage by API key ID (optional)
    var_from = 'var_from_example' # str | Start date for usage period (inclusive), in YYYY-MM-DD format (e.g. 2026-01-01).    Must be provided together with 'to'. If neither is provided, defaults to current month. (optional)
    to = 'to_example' # str | End date for usage period (inclusive), in YYYY-MM-DD format (e.g. 2026-01-31).   Must be provided together with 'from'. If neither is provided, defaults to current month. (optional)

    try:
        api_response = api_instance.get_api_usage_global(x_organization_id=x_organization_id, project_id=project_id, inference_type=inference_type, api_key_id=api_key_id, var_from=var_from, to=to)
        print("The response of UsageApi->get_api_usage_global:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsageApi->get_api_usage_global: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 
 **project_id** | **str**| Filter usage by project ID. When provided, &#39;inferenceType&#39; is required. | [optional] 
 **inference_type** | **str**| Filter usage by inference type: structured, content, or template extraction. | [optional] 
 **api_key_id** | **str**| Filter usage by API key ID | [optional] 
 **var_from** | **str**| Start date for usage period (inclusive), in YYYY-MM-DD format (e.g. 2026-01-01).    Must be provided together with &#39;to&#39;. If neither is provided, defaults to current month. | [optional] 
 **to** | **str**| End date for usage period (inclusive), in YYYY-MM-DD format (e.g. 2026-01-31).   Must be provided together with &#39;from&#39;. If neither is provided, defaults to current month. | [optional] 

### Return type

[**UsageResponse**](UsageResponse.md)

### Authorization

[oauth2Auth](../README.md#oauth2Auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, text/plain

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**400** | Invalid value for: query parameter inferenceType |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

