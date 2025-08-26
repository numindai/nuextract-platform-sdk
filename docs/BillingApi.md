# numind.openapi_client.BillingApi

All URIs are relative to *https://nuextract.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_api_billing_plans**](BillingApi.md#get_api_billing_plans) | **GET** /api/billing/plans | 
[**get_api_billing_plans_plankey**](BillingApi.md#get_api_billing_plans_plankey) | **GET** /api/billing/plans/{planKey} | 
[**get_api_billing_profile**](BillingApi.md#get_api_billing_profile) | **GET** /api/billing/profile | 
[**post_api_billing_connect_to_stripe**](BillingApi.md#post_api_billing_connect_to_stripe) | **POST** /api/billing/connect-to-stripe | 
[**post_api_billing_restore_subscription**](BillingApi.md#post_api_billing_restore_subscription) | **POST** /api/billing/restore-subscription | 
[**post_api_billing_stripe_portal**](BillingApi.md#post_api_billing_stripe_portal) | **POST** /api/billing/stripe-portal | 
[**post_api_billing_subscribe**](BillingApi.md#post_api_billing_subscribe) | **POST** /api/billing/subscribe | 


# **get_api_billing_plans**
> List[Plan] get_api_billing_plans()

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.plan import Plan
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
    api_instance = numind.openapi_client.BillingApi(api_client)

    try:
        api_response = api_instance.get_api_billing_plans()
        print("The response of BillingApi->get_api_billing_plans:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BillingApi->get_api_billing_plans: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[Plan]**](Plan.md)

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

# **get_api_billing_plans_plankey**
> Plan get_api_billing_plans_plankey(plan_key)

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.plan import Plan
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
    api_instance = numind.openapi_client.BillingApi(api_client)
    plan_key = 'plan_key_example' # str | Plan identifier

    try:
        api_response = api_instance.get_api_billing_plans_plankey(plan_key)
        print("The response of BillingApi->get_api_billing_plans_plankey:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BillingApi->get_api_billing_plans_plankey: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **plan_key** | **str**| Plan identifier | 

### Return type

[**Plan**](Plan.md)

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

# **get_api_billing_profile**
> BillingProfileResponse get_api_billing_profile(organization_id=organization_id)

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.billing_profile_response import BillingProfileResponse
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
    api_instance = numind.openapi_client.BillingApi(api_client)
    organization_id = 'organization_id_example' # str |  (optional)

    try:
        api_response = api_instance.get_api_billing_profile(organization_id=organization_id)
        print("The response of BillingApi->get_api_billing_profile:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BillingApi->get_api_billing_profile: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_id** | **str**|  | [optional] 

### Return type

[**BillingProfileResponse**](BillingProfileResponse.md)

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

# **post_api_billing_connect_to_stripe**
> StripeSubscriptionResponse post_api_billing_connect_to_stripe(stripe_subscription_request, organization_id=organization_id)

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.stripe_subscription_request import StripeSubscriptionRequest
from numind.openapi_client.models.stripe_subscription_response import StripeSubscriptionResponse
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
    api_instance = numind.openapi_client.BillingApi(api_client)
    stripe_subscription_request = {"redirectURL":"https://example.com"} # StripeSubscriptionRequest | 
    organization_id = 'organization_id_example' # str | Optional organization identifier. If provided, the request will be associated with this organization. Otherwise, the request will be associated with the authenticated user.          (optional)

    try:
        api_response = api_instance.post_api_billing_connect_to_stripe(stripe_subscription_request, organization_id=organization_id)
        print("The response of BillingApi->post_api_billing_connect_to_stripe:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BillingApi->post_api_billing_connect_to_stripe: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **stripe_subscription_request** | [**StripeSubscriptionRequest**](StripeSubscriptionRequest.md)|  | 
 **organization_id** | **str**| Optional organization identifier. If provided, the request will be associated with this organization. Otherwise, the request will be associated with the authenticated user.          | [optional] 

### Return type

[**StripeSubscriptionResponse**](StripeSubscriptionResponse.md)

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

# **post_api_billing_restore_subscription**
> post_api_billing_restore_subscription(organization_id=organization_id)

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
    api_instance = numind.openapi_client.BillingApi(api_client)
    organization_id = 'organization_id_example' # str | Optional organization identifier. If provided, the request will be associated with this organization. Otherwise, the request will be associated with the authenticated user.          (optional)

    try:
        api_instance.post_api_billing_restore_subscription(organization_id=organization_id)
    except Exception as e:
        print("Exception when calling BillingApi->post_api_billing_restore_subscription: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_id** | **str**| Optional organization identifier. If provided, the request will be associated with this organization. Otherwise, the request will be associated with the authenticated user.          | [optional] 

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

# **post_api_billing_stripe_portal**
> StripePortalResponse post_api_billing_stripe_portal(stripe_portal_request)

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.stripe_portal_request import StripePortalRequest
from numind.openapi_client.models.stripe_portal_response import StripePortalResponse
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
    api_instance = numind.openapi_client.BillingApi(api_client)
    stripe_portal_request = {"organizationId":"154f97c7-e49b-4780-8274-399fcee48e7f","returnUrl":"https://example.com"} # StripePortalRequest | 

    try:
        api_response = api_instance.post_api_billing_stripe_portal(stripe_portal_request)
        print("The response of BillingApi->post_api_billing_stripe_portal:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BillingApi->post_api_billing_stripe_portal: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **stripe_portal_request** | [**StripePortalRequest**](StripePortalRequest.md)|  | 

### Return type

[**StripePortalResponse**](StripePortalResponse.md)

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

# **post_api_billing_subscribe**
> post_api_billing_subscribe(subscription_request, organization_id=organization_id)

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.models.subscription_request import SubscriptionRequest
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
    api_instance = numind.openapi_client.BillingApi(api_client)
    subscription_request = {"planId":"free_plan"} # SubscriptionRequest | 
    organization_id = 'organization_id_example' # str | Optional organization identifier. If provided, the request will be associated with this organization. Otherwise, the request will be associated with the authenticated user.          (optional)

    try:
        api_instance.post_api_billing_subscribe(subscription_request, organization_id=organization_id)
    except Exception as e:
        print("Exception when calling BillingApi->post_api_billing_subscribe: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **subscription_request** | [**SubscriptionRequest**](SubscriptionRequest.md)|  | 
 **organization_id** | **str**| Optional organization identifier. If provided, the request will be associated with this organization. Otherwise, the request will be associated with the authenticated user.          | [optional] 

### Return type

void (empty response body)

### Authorization

[oauth2Auth](../README.md#oauth2Auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: text/plain, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**400** | Invalid value for: body |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

