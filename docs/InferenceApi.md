# numind.openapi_client.InferenceApi

All URIs are relative to *https://nuextract.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**post_api_infer_template**](InferenceApi.md#post_api_infer_template) | **POST** /api/infer-template | 
[**post_api_projects_projectid_infer_document_documentid**](InferenceApi.md#post_api_projects_projectid_infer_document_documentid) | **POST** /api/projects/{projectId}/infer-document/{documentId} | 
[**post_api_projects_projectid_infer_text**](InferenceApi.md#post_api_projects_projectid_infer_text) | **POST** /api/projects/{projectId}/infer-text | 


# **post_api_infer_template**
> object post_api_infer_template(template_request)


 Derive a template from the provided natural language description.
 Potentially, this endpoint can equally be used to correct the template to conform to the NuExtract standard.
 The resulting template is a JSON object that can be used as a project template.


#### Response:
 Returns a JSON representing the derived template.
 The response is an empty template if the derivation fails.

   

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
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
    api_instance = numind.openapi_client.InferenceApi(api_client)
    template_request = {"description":"[EXAMPLE ONLY] Create a template that extracts key information from an order confirmation email. The template should be able to pull details like the order ID, customer ID, date and time of the order, status, total amount, currency, item details (product ID, quantity, and unit price), shipping address, any customer requests or delivery preferences, and the estimated delivery date."} # TemplateRequest | 

    try:
        api_response = api_instance.post_api_infer_template(template_request)
        print("The response of InferenceApi->post_api_infer_template:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling InferenceApi->post_api_infer_template: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **template_request** | [**TemplateRequest**](TemplateRequest.md)|  | 

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

# **post_api_projects_projectid_infer_document_documentid**
> InferenceResponse post_api_projects_projectid_infer_document_documentid(project_id, document_id)


 Performs information extraction inference on a specific **Document**.
 The **Document** content must be compatible with the template of the project.
 Inference **temperature** can be set in the project settings.

#### Response:
 The ***result*** field is guaranteed to conform to the template.
 If the model returns an invalid response, the ***result*** contains an empty template. 
 In this case, the raw response is additionally included in ***rawResponse*** field, 
 together with the error message.

#### Error Responses:
`404 Not Found` - If a **Document** with the given `documentId`, or a **Project** with the specified `projectId` does not exist.

`403 Forbidden` - If the user does not have permission to use this **Document** or run inference on this **Project**.
   

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
    api_instance = numind.openapi_client.InferenceApi(api_client)
    project_id = 'project_id_example' # str | Unique project identifier.
    document_id = 'document_id_example' # str | Unique document identifier.

    try:
        api_response = api_instance.post_api_projects_projectid_infer_document_documentid(project_id, document_id)
        print("The response of InferenceApi->post_api_projects_projectid_infer_document_documentid:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling InferenceApi->post_api_projects_projectid_infer_document_documentid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Unique project identifier. | 
 **document_id** | **str**| Unique document identifier. | 

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

# **post_api_projects_projectid_infer_text**
> InferenceResponse post_api_projects_projectid_infer_text(project_id, text_request)


 Perform information extraction inference on the provided text.
 The text content must be compatible with the template of the project.
 Inference **temperature** can be set in the project settings.


#### Response:
 Returns a JSON representing the inference result.
 The ***result*** field is guaranteed to conform to the template.
 If the model returns an invalid response, the ***result*** contains an empty template. 
 In this case, the raw response is additionally included in ***rawResponse*** field, 
 together with the error message. 
 Additionally, the response contains `documentId`, which allows to reuse this text **Document** in the future.

#### Error Responses:
`404 Not Found` - If a **Project** with the specified `projectId` does not exist.

`403 Forbidden` - If the user does not have permission to run inference on this **Project**.
   

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
    api_instance = numind.openapi_client.InferenceApi(api_client)
    project_id = 'project_id_example' # str | Unique project identifier.
    text_request = {text=[EXAMPLE ONLY] Your order (ID: o-89123) has been successfully processed. The customer ID for this order is c-20485. It was placed on March 10, 2024, at 11:15 AM UTC and is now marked as shipped. The total amount charged is $149.99 USD. The items in this order include: Product ID p-00876 with a quantity of 1 at a unit price of $79.99, and Product ID p-00321 with a quantity of 2 at a unit price of $35.00. The shipping address is 782 Pine St, Austin, TX, 73301, USA. The customer has requested: "Leave package at the front door." Additional delivery preferences include no signature required and standard delivery. The estimated delivery date is March 15, 2024, by 5:00 PM UTC.} # TextRequest | 

    try:
        api_response = api_instance.post_api_projects_projectid_infer_text(project_id, text_request)
        print("The response of InferenceApi->post_api_projects_projectid_infer_text:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling InferenceApi->post_api_projects_projectid_infer_text: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Unique project identifier. | 
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

