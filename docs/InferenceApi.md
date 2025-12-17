# numind.openapi_client.InferenceApi

All URIs are relative to *https://nuextract.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**post_api_content_extraction_contentextractionprojectid_jobs_document_documentid**](InferenceApi.md#post_api_content_extraction_contentextractionprojectid_jobs_document_documentid) | **POST** /api/content-extraction/{contentExtractionProjectId}/jobs/document/{documentId} | 
[**post_api_structured_extraction_structuredextractionprojectid_jobs_document_documentid**](InferenceApi.md#post_api_structured_extraction_structuredextractionprojectid_jobs_document_documentid) | **POST** /api/structured-extraction/{structuredExtractionProjectId}/jobs/document/{documentId} | 
[**post_api_structured_extraction_structuredextractionprojectid_jobs_text**](InferenceApi.md#post_api_structured_extraction_structuredextractionprojectid_jobs_text) | **POST** /api/structured-extraction/{structuredExtractionProjectId}/jobs/text | 
[**post_api_template_generation_jobs_document_documentid**](InferenceApi.md#post_api_template_generation_jobs_document_documentid) | **POST** /api/template-generation/jobs/document/{documentId} | 
[**post_api_template_generation_jobs_text**](InferenceApi.md#post_api_template_generation_jobs_text) | **POST** /api/template-generation/jobs/text | 


# **post_api_content_extraction_contentextractionprojectid_jobs_document_documentid**
> JobIdResponse post_api_content_extraction_contentextractionprojectid_jobs_document_documentid(content_extraction_project_id, document_id, timeout=timeout)


 Extract markdown from the provided document using NuMarkdown model as an async job.
 Inference **temperature** can be set in the project settings.

#### Response:
 Returns a JSON containing the job ID that can be used to retrieve the job status and results.

 If the job is completed successfully, the job's output data will contain a JSON representing the extracted information.
 The ***result*** field contains the extracted markdown. The ***thinking*** field contains the reasoning trace.
 If one of the fields ***result*** or ***thinking*** is empty, the ***rawResponse*** field contains the raw model output.
 and an HTTP code 206 is returned.

#### Error Responses:
`404 Not Found` - If a **Project** or **Document** with the specified ID does not exist.

`403 Forbidden` - If the user does not have permission to run inference on this **Project** or access the **Document**,
 or if the user's billing quota is exceeded.
   

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.job_id_response import JobIdResponse
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
    content_extraction_project_id = 'content_extraction_project_id_example' # str | Unique content extraction project identifier.
    document_id = 'document_id_example' # str | Unique document identifier.
    timeout = 'timeout_example' # str | Max time to wait for the processing completion.   Format examples: 1000ms, 10s, 1m, 1h (optional)

    try:
        api_response = api_instance.post_api_content_extraction_contentextractionprojectid_jobs_document_documentid(content_extraction_project_id, document_id, timeout=timeout)
        print("The response of InferenceApi->post_api_content_extraction_contentextractionprojectid_jobs_document_documentid:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling InferenceApi->post_api_content_extraction_contentextractionprojectid_jobs_document_documentid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **content_extraction_project_id** | **str**| Unique content extraction project identifier. | 
 **document_id** | **str**| Unique document identifier. | 
 **timeout** | **str**| Max time to wait for the processing completion.   Format examples: 1000ms, 10s, 1m, 1h | [optional] 

### Return type

[**JobIdResponse**](JobIdResponse.md)

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

# **post_api_structured_extraction_structuredextractionprojectid_jobs_document_documentid**
> JobIdResponse post_api_structured_extraction_structuredextractionprojectid_jobs_document_documentid(structured_extraction_project_id, document_id, temperature=temperature, max_output_tokens=max_output_tokens, example_token_limit=example_token_limit, timeout=timeout)


 Perform information extraction inference on the provided document as an async job.
 The document must be compatible with the template of the project.
 Inference **temperature** can be set in the project settings.

#### Response:
 Returns a JSON containing the job ID that can be used to retrieve the job status and results.

 If the job is completed successfully, the job's output data will contain a JSON representing the extracted information.
 The ***result*** field is guaranteed to conform to the template.
 If the model returns an invalid response, the ***result*** contains an empty template.
 In this case, the raw response is additionally included in ***rawResponse*** field,
 together with the error message.

#### Error Responses:
`404 Not Found` - If a **Project** or **Document** with the specified ID does not exist.

`403 Forbidden` - If the user does not have permission to run inference on this **Project** or access the **Document**,
 or if the user's billing quota is exceeded.
   

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.job_id_response import JobIdResponse
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
    structured_extraction_project_id = 'structured_extraction_project_id_example' # str | Unique structured extraction project identifier.
    document_id = 'document_id_example' # str | Unique document identifier.
    temperature = 3.4 # float | Model temperature (optional). Controls output diversity.  When not specified, the project value is used.   Ranges between 0 and 1. (optional)
    max_output_tokens = 56 # int | Maximum number of output tokens (optional).  When not specified, the project value is used.   Use 0 to indicate no limit. (optional)
    example_token_limit = 56 # int | Controls the maximum number of tokens that can be allocated to the examples.  Must be positive. Ranges in the context window of the model. (optional)
    timeout = 'timeout_example' # str | Max time to wait for the processing completion.   Format examples: 1000ms, 10s, 1m, 1h (optional)

    try:
        api_response = api_instance.post_api_structured_extraction_structuredextractionprojectid_jobs_document_documentid(structured_extraction_project_id, document_id, temperature=temperature, max_output_tokens=max_output_tokens, example_token_limit=example_token_limit, timeout=timeout)
        print("The response of InferenceApi->post_api_structured_extraction_structuredextractionprojectid_jobs_document_documentid:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling InferenceApi->post_api_structured_extraction_structuredextractionprojectid_jobs_document_documentid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **structured_extraction_project_id** | **str**| Unique structured extraction project identifier. | 
 **document_id** | **str**| Unique document identifier. | 
 **temperature** | **float**| Model temperature (optional). Controls output diversity.  When not specified, the project value is used.   Ranges between 0 and 1. | [optional] 
 **max_output_tokens** | **int**| Maximum number of output tokens (optional).  When not specified, the project value is used.   Use 0 to indicate no limit. | [optional] 
 **example_token_limit** | **int**| Controls the maximum number of tokens that can be allocated to the examples.  Must be positive. Ranges in the context window of the model. | [optional] 
 **timeout** | **str**| Max time to wait for the processing completion.   Format examples: 1000ms, 10s, 1m, 1h | [optional] 

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
**400** | Invalid value for: query parameter temperature, Invalid value for: query parameter maxOutputTokens, Invalid value for: query parameter exampleTokenLimit |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_api_structured_extraction_structuredextractionprojectid_jobs_text**
> JobIdResponse post_api_structured_extraction_structuredextractionprojectid_jobs_text(structured_extraction_project_id, text_request, temperature=temperature, max_output_tokens=max_output_tokens, example_token_limit=example_token_limit, timeout=timeout)


 Perform information extraction inference on the provided text as an async job.
 The text content must be compatible with the template of the project.
 Inference parameters **temperature**, **maxOutputTokens** and **exampleTokenLimit**
 can be set in the project settings.

#### Response:
 Returns a JSON containing the job ID that can be used to retrieve the job status and results.

 If the job is completed successfully, the job's output data will contain a JSON representing the extracted information.
 The ***result*** field is guaranteed to conform to the template.
 If the model returns an invalid response, the ***result*** contains an empty template.
 In this case, the raw response is additionally included in ***rawResponse*** field,
 together with the error message.
 Additionally, the response contains `documentId`, which allows to reuse this text **Document** in the future.

#### Error Responses:
`404 Not Found` - If a **Project** with the specified `projectId` does not exist.

`403 Forbidden` - If the user does not have permission to run inference on this **Project** or if the user's billing quota is exceeded.
   

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.job_id_response import JobIdResponse
from numind.models.text_request import TextRequest
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
    structured_extraction_project_id = 'structured_extraction_project_id_example' # str | Unique structured extraction project identifier.
    text_request = {text=[EXAMPLE ONLY] Your order (ID: o-89123) has been successfully processed. The customer ID for this order is c-20485. It was placed on March 10, 2024, at 11:15 AM UTC and is now marked as shipped. The total amount charged is $149.99 USD. The items in this order include: Product ID p-00876 with a quantity of 1 at a unit price of $79.99, and Product ID p-00321 with a quantity of 2 at a unit price of $35.00. The shipping address is 782 Pine St, Austin, TX, 73301, USA. The customer has requested: "Leave package at the front door." Additional delivery preferences include no signature required and standard delivery. The estimated delivery date is March 15, 2024, by 5:00 PM UTC.} # TextRequest | 
    temperature = 3.4 # float | Model temperature (optional). Controls output diversity.  When not specified, the project value is used.   Ranges between 0 and 1. (optional)
    max_output_tokens = 56 # int | Maximum number of output tokens (optional).  When not specified, the project value is used.   Use 0 to indicate no limit. (optional)
    example_token_limit = 56 # int | Controls the maximum number of tokens that can be allocated to the examples.  Must be positive. Ranges in the context window of the model. (optional)
    timeout = 'timeout_example' # str | Max time to wait for the processing completion.   Format examples: 1000ms, 10s, 1m, 1h (optional)

    try:
        api_response = api_instance.post_api_structured_extraction_structuredextractionprojectid_jobs_text(structured_extraction_project_id, text_request, temperature=temperature, max_output_tokens=max_output_tokens, example_token_limit=example_token_limit, timeout=timeout)
        print("The response of InferenceApi->post_api_structured_extraction_structuredextractionprojectid_jobs_text:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling InferenceApi->post_api_structured_extraction_structuredextractionprojectid_jobs_text: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **structured_extraction_project_id** | **str**| Unique structured extraction project identifier. | 
 **text_request** | [**TextRequest**](TextRequest.md)|  | 
 **temperature** | **float**| Model temperature (optional). Controls output diversity.  When not specified, the project value is used.   Ranges between 0 and 1. | [optional] 
 **max_output_tokens** | **int**| Maximum number of output tokens (optional).  When not specified, the project value is used.   Use 0 to indicate no limit. | [optional] 
 **example_token_limit** | **int**| Controls the maximum number of tokens that can be allocated to the examples.  Must be positive. Ranges in the context window of the model. | [optional] 
 **timeout** | **str**| Max time to wait for the processing completion.   Format examples: 1000ms, 10s, 1m, 1h | [optional] 

### Return type

[**JobIdResponse**](JobIdResponse.md)

### Authorization

[oauth2Auth](../README.md#oauth2Auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, text/plain

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**400** | Invalid value for: query parameter temperature, Invalid value for: query parameter maxOutputTokens, Invalid value for: query parameter exampleTokenLimit, Invalid value for: body |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_api_template_generation_jobs_document_documentid**
> JobIdResponse post_api_template_generation_jobs_document_documentid(document_id, timeout=timeout)


 Derive a template from the provided **Document** as an async job.
 Potentially, this endpoint can equally be used to correct the template to conform to the NuExtract standard.
 The resulting template is a JSON object that can be used as a project template.

#### Response:
 Returns a JSON containing the job ID that can be used to retrieve the job status and results.

 If the job is completed successfully, the job's output data will contain the derived template.
 The response is an empty template if the derivation fails.

#### Error Responses:
`404 Not Found` - If a **Document** with the specified `documentId` does not exist.

`403 Forbidden` - If the user does not have permission to run inference on this **Document** or if the user's billing quota is exceeded.
   

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.job_id_response import JobIdResponse
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
    document_id = 'document_id_example' # str | Unique document identifier.
    timeout = 'timeout_example' # str | Max time to wait for the processing completion.   Format examples: 1000ms, 10s, 1m, 1h (optional)

    try:
        api_response = api_instance.post_api_template_generation_jobs_document_documentid(document_id, timeout=timeout)
        print("The response of InferenceApi->post_api_template_generation_jobs_document_documentid:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling InferenceApi->post_api_template_generation_jobs_document_documentid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **document_id** | **str**| Unique document identifier. | 
 **timeout** | **str**| Max time to wait for the processing completion.   Format examples: 1000ms, 10s, 1m, 1h | [optional] 

### Return type

[**JobIdResponse**](JobIdResponse.md)

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

# **post_api_template_generation_jobs_text**
> JobIdResponse post_api_template_generation_jobs_text(template_request, timeout=timeout)


 Derive a template from the provided natural language description as an async job.
 Potentially, this endpoint can equally be used to correct the template to conform to the NuExtract standard.
 The resulting template is a JSON object that can be used as a project template.

#### Response:
 Returns a JSON containing the job ID that can be used to retrieve the job status and results.

 If the job is completed successfully, the job's output data will contain the derived template.
 The response is an empty template if the derivation fails.

#### Error Responses:
`404 Not Found` - If a **Project** with the specified `projectId` does not exist.

`403 Forbidden` - If the user does not have permission to run inference on this **Project** or if the user's billing quota is exceeded.
   

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.job_id_response import JobIdResponse
from numind.models.template_request import TemplateRequest
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
    timeout = 'timeout_example' # str | Max time to wait for the processing completion.   Format examples: 1000ms, 10s, 1m, 1h (optional)

    try:
        api_response = api_instance.post_api_template_generation_jobs_text(template_request, timeout=timeout)
        print("The response of InferenceApi->post_api_template_generation_jobs_text:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling InferenceApi->post_api_template_generation_jobs_text: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **template_request** | [**TemplateRequest**](TemplateRequest.md)|  | 
 **timeout** | **str**| Max time to wait for the processing completion.   Format examples: 1000ms, 10s, 1m, 1h | [optional] 

### Return type

[**JobIdResponse**](JobIdResponse.md)

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

