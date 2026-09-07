# numind.openapi_client.StructuredDataExtractionApi

All URIs are relative to *https://nuextract.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_api_structured_extraction_jobs_structuredextractionjobid**](StructuredDataExtractionApi.md#get_api_structured_extraction_jobs_structuredextractionjobid) | **GET** /api/structured-extraction/jobs/{structuredExtractionJobId} | 
[**post_api_structured_extraction_jobs**](StructuredDataExtractionApi.md#post_api_structured_extraction_jobs) | **POST** /api/structured-extraction/jobs | 
[**post_api_structured_extraction_structuredprojectid_jobs**](StructuredDataExtractionApi.md#post_api_structured_extraction_structuredprojectid_jobs) | **POST** /api/structured-extraction/{structuredProjectId}/jobs | 


# **get_api_structured_extraction_jobs_structuredextractionjobid**
> StructuredExtractionResponse get_api_structured_extraction_jobs_structuredextractionjobid(structured_extraction_job_id, x_organization_id=x_organization_id)


 Get structured extraction result of a specific job by its unique identifier.

#### Response:
 Returns a JSON representing the extracted information.
 In case the extraction fails, an empty template is returned.
 HTTP code 206 is returned when the response contains an inference error, including whenever the model does not finish normally.
 Reaching the output token limit is reported as truncation.

#### Error Responses:
`404 Not Found` - If an extraction job with the specified ID does not exist.

`403 Forbidden` - If the user does not have permission to access this job, or if the job failed because the user's billing quota was exceeded.
   

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.structured_extraction_response import StructuredExtractionResponse
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
    api_instance = numind.openapi_client.StructuredDataExtractionApi(api_client)
    structured_extraction_job_id = "structured_extraction_job_id_example"  # str | Unique structured extraction job identifier.
    x_organization_id = "x_organization_id_example"  # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)

    try:
        api_response = (
            api_instance.get_api_structured_extraction_jobs_structuredextractionjobid(
                structured_extraction_job_id, x_organization_id=x_organization_id
            )
        )
        print(
            "The response of StructuredDataExtractionApi->get_api_structured_extraction_jobs_structuredextractionjobid:\n"
        )
        pprint(api_response)
    except Exception as e:
        print(
            "Exception when calling StructuredDataExtractionApi->get_api_structured_extraction_jobs_structuredextractionjobid: %s\n"
            % e
        )
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **structured_extraction_job_id** | **str**| Unique structured extraction job identifier. | 
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 

### Return type

[**StructuredExtractionResponse**](StructuredExtractionResponse.md)

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

# **post_api_structured_extraction_jobs**
> JobIdResponse post_api_structured_extraction_jobs(request, document, x_organization_id=x_organization_id, timeout=timeout, example_files=example_files)


 Submit a projectless structured extraction job.

 This endpoint uses `multipart/form-data`. The multipart body must contain:

 - `request`: a string field containing JSON. `Content-Type: application/json` is recommended, but plain string parts from Swagger UI are accepted.
 - `document`: the target file to extract from
 - `exampleFiles`: zero or more example files, in the same order as `request.examples`

 The `request` JSON contains the schema, optional instructions, optional settings, and optional example outputs.
 Example files themselves are not embedded in JSON; they are attached as `exampleFiles` multipart parts.

#### Request JSON:
```json
{
  "schema": {
    "invoiceNumber": "string",
    "invoiceDate": "date",
    "vendor": "string",
    "total": "number"
  },
  "instructions": "Extract the invoice fields exactly as written in the document.",
  "settings": {
    "temperature": 0.2,
    "rasterizationDPI": 200,
    "maxOutputTokens": 2048,
    "maxExampleTokenNumber": 12000,
    "maxExampleNumber": 3,
    "minExampleSimilarity": 0,
    "enableThinking": false,
    "randomSeed": "99"
  },
  "examples": [
    {
      "result": {
        "invoiceNumber": "INV-001",
        "invoiceDate": "2026-08-31",
        "vendor": "ACME Corp",
        "total": 123.45
      }
    }
  ]
}
```

 In this example, attach one `exampleFiles` part for the single item in `examples`.
 If `examples` has two items, attach two `exampleFiles` parts, ordered the same way.
 If `examples` is omitted or empty, do not attach `exampleFiles`.

#### cURL Example:
```bash
curl -X POST "$BASE_URL/structured-extraction/jobs" \
  -H "Authorization: Bearer $TOKEN" \
  -F 'request=@request.json;type=application/json' \
  -F 'document=@invoice.pdf' \
  -F 'exampleFiles=@example-invoice.pdf'
```

#### Fields:
`schema` is required and uses the same NuExtract schema format as structured projects.

`instructions` is optional. Omit it or use an empty string when no extra guidance is needed.

`settings` is optional. Supported keys are `temperature`, `rasterizationDPI`, `maxOutputTokens`,
`degradedMode`, `maxExampleTokenNumber`, `maxExampleNumber`, `minExampleSimilarity`, `enableThinking`,
and `randomSeed`. `randomSeed` must be a string containing a 64-bit integer or `random`.
Omitted settings use the server defaults for structured extraction.

`examples` is optional. Each example must contain a `result` object that conforms to `schema`.

#### Response:
 Returns a JSON containing the job ID that can be used to retrieve the job status and results.

#### Error Responses:
`400 Bad Request` - If the `request` field is not valid JSON, the schema is invalid, an example result does not conform to the schema,
or the number of `examples` does not match the number of `exampleFiles` parts.
   

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
    api_instance = numind.openapi_client.StructuredDataExtractionApi(api_client)
    request = "request_example"  # str | String field containing the JSON request manifest. Contains `schema`, optional `instructions`, optional `settings`, and optional `examples`.
    document = None  # bytes | Target document to process.
    x_organization_id = "x_organization_id_example"  # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)
    timeout = "timeout_example"  # str | Execution timeout for the async inference job. If omitted, the server default of 60m is used.   If provided below the server-configured minimum (5m by default), the effective timeout is clamped to that minimum.   Format examples: 1000ms, 10s, 1m, 1h (optional)
    example_files = None  # List[bytes] | Example documents, ordered to match `request.examples`. Attach exactly one file for each example result. (optional)

    try:
        api_response = api_instance.post_api_structured_extraction_jobs(
            request,
            document,
            x_organization_id=x_organization_id,
            timeout=timeout,
            example_files=example_files,
        )
        print(
            "The response of StructuredDataExtractionApi->post_api_structured_extraction_jobs:\n"
        )
        pprint(api_response)
    except Exception as e:
        print(
            "Exception when calling StructuredDataExtractionApi->post_api_structured_extraction_jobs: %s\n"
            % e
        )
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **request** | **str**| String field containing the JSON request manifest. Contains &#x60;schema&#x60;, optional &#x60;instructions&#x60;, optional &#x60;settings&#x60;, and optional &#x60;examples&#x60;. | 
 **document** | **bytes**| Target document to process. | 
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 
 **timeout** | **str**| Execution timeout for the async inference job. If omitted, the server default of 60m is used.   If provided below the server-configured minimum (5m by default), the effective timeout is clamped to that minimum.   Format examples: 1000ms, 10s, 1m, 1h | [optional] 
 **example_files** | **List[bytes]**| Example documents, ordered to match &#x60;request.examples&#x60;. Attach exactly one file for each example result. | [optional] 

### Return type

[**JobIdResponse**](JobIdResponse.md)

### Authorization

[oauth2Auth](../README.md#oauth2Auth)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json, text/plain

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**400** | Invalid value for: body |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_api_structured_extraction_structuredprojectid_jobs**
> JobIdResponse post_api_structured_extraction_structuredprojectid_jobs(structured_project_id, body, x_organization_id=x_organization_id, temperature=temperature, dpi=dpi, max_output_tokens=max_output_tokens, max_example_token_number=max_example_token_number, max_example_number=max_example_number, min_example_similarity=min_example_similarity, enable_thinking=enable_thinking, random_seed=random_seed, timeout=timeout)


 Extract structured information from the provided text or file as an async job. Some files are converted to images -
 the **rasterizationDPI** parameter controls their resolution. When **temperature**, **rasterizationDPI**,
 **maxOutputTokens** and **maxExampleTokenNumber** parameters are not specified,
 they are set to their project-setting values.

#### Response:
 Returns a JSON containing the job ID that can be used to retrieve the job status and results.

 If the job is completed successfully, the job's output data will contain a JSON representing the extracted information.
 The ***result*** field is guaranteed to conform to the template via post-processing
 of the raw model output. In the event that the raw model output did not conform to the template,
 it is included in the ***rawResponse*** field, together with the corresponding error message,
 and an HTTP code 206 is returned.
 If the model does not finish normally, the job result is returned with HTTP code 206,
 even when post-processing recovers usable structured information. Reaching the output token limit is reported as truncation.

#### Error Responses:
`404 Not Found` - If a **Project** with the specified `projectId` does not exist.

`403 Forbidden` - If the user does not have permission to run inference on this **Project** or if the user's billing quota is exceeded.
   

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
    api_instance = numind.openapi_client.StructuredDataExtractionApi(api_client)
    structured_project_id = "structured_project_id_example"  # str | Unique structured extraction project identifier.
    body = None  # bytes |
    x_organization_id = "x_organization_id_example"  # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)
    temperature = 3.4  # float | Model temperature (optional). Controls output diversity.  Ranges between 0 and 2. Resolution order: request `temperature` -> project setting. New and reset projects default to 0.6. (optional)
    dpi = 56  # int | DPI for file rasterization (optional).  When not specified, the project value is used.   If the file is already an image or a text, this parameter is ignored. (optional)
    max_output_tokens = 56  # int | Maximum number of output tokens (optional).  When not specified, the project value is used.   Use 0 to indicate no limit. (optional)
    max_example_token_number = 56  # int | Controls the maximum number of tokens that can be allocated to the examples.  Must be positive. Ranges in the context window of the model. (optional)
    max_example_number = 56  # int | Controls the maximum number of examples to use.  Must be positive. Set to 0 for no limit. (optional)
    min_example_similarity = 3.4  # float | Controls the minimum similarity between the document and the examples.  Must be between 0 and 1. Set to 0 for any similarity and 1 for exact match. (optional)
    enable_thinking = True  # bool | Enable thinking/reasoning (optional). Resolution order: request `enableThinking` -> project setting. (optional)
    random_seed = "random_seed_example"  # str | Inference seed override (optional). Use a string containing a 64-bit integer for a fixed seed, or `random` to generate one. When not specified, the project setting is used. (optional)
    timeout = "timeout_example"  # str | Execution timeout for the async inference job. If omitted, the server default of 60m is used.   If provided below the server-configured minimum (5m by default), the effective timeout is clamped to that minimum.   Format examples: 1000ms, 10s, 1m, 1h (optional)

    try:
        api_response = (
            api_instance.post_api_structured_extraction_structuredprojectid_jobs(
                structured_project_id,
                body,
                x_organization_id=x_organization_id,
                temperature=temperature,
                dpi=dpi,
                max_output_tokens=max_output_tokens,
                max_example_token_number=max_example_token_number,
                max_example_number=max_example_number,
                min_example_similarity=min_example_similarity,
                enable_thinking=enable_thinking,
                random_seed=random_seed,
                timeout=timeout,
            )
        )
        print(
            "The response of StructuredDataExtractionApi->post_api_structured_extraction_structuredprojectid_jobs:\n"
        )
        pprint(api_response)
    except Exception as e:
        print(
            "Exception when calling StructuredDataExtractionApi->post_api_structured_extraction_structuredprojectid_jobs: %s\n"
            % e
        )
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **structured_project_id** | **str**| Unique structured extraction project identifier. | 
 **body** | **bytes**|  | 
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 
 **temperature** | **float**| Model temperature (optional). Controls output diversity.  Ranges between 0 and 2. Resolution order: request &#x60;temperature&#x60; -&gt; project setting. New and reset projects default to 0.6. | [optional] 
 **dpi** | **int**| DPI for file rasterization (optional).  When not specified, the project value is used.   If the file is already an image or a text, this parameter is ignored. | [optional] 
 **max_output_tokens** | **int**| Maximum number of output tokens (optional).  When not specified, the project value is used.   Use 0 to indicate no limit. | [optional] 
 **max_example_token_number** | **int**| Controls the maximum number of tokens that can be allocated to the examples.  Must be positive. Ranges in the context window of the model. | [optional] 
 **max_example_number** | **int**| Controls the maximum number of examples to use.  Must be positive. Set to 0 for no limit. | [optional] 
 **min_example_similarity** | **float**| Controls the minimum similarity between the document and the examples.  Must be between 0 and 1. Set to 0 for any similarity and 1 for exact match. | [optional] 
 **enable_thinking** | **bool**| Enable thinking/reasoning (optional). Resolution order: request &#x60;enableThinking&#x60; -&gt; project setting. | [optional] 
 **random_seed** | **str**| Inference seed override (optional). Use a string containing a 64-bit integer for a fixed seed, or &#x60;random&#x60; to generate one. When not specified, the project setting is used. | [optional] 
 **timeout** | **str**| Execution timeout for the async inference job. If omitted, the server default of 60m is used.   If provided below the server-configured minimum (5m by default), the effective timeout is clamped to that minimum.   Format examples: 1000ms, 10s, 1m, 1h | [optional] 

### Return type

[**JobIdResponse**](JobIdResponse.md)

### Authorization

[oauth2Auth](../README.md#oauth2Auth)

### HTTP request headers

 - **Content-Type**: application/octet-stream, multipart/form-data
 - **Accept**: application/json, text/plain

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**400** | Invalid value for: query parameter temperature, Invalid value for: query parameter dpi, Invalid value for: query parameter maxOutputTokens, Invalid value for: query parameter maxExampleTokenNumber, Invalid value for: query parameter maxExampleNumber, Invalid value for: query parameter minExampleSimilarity, Invalid value for: query parameter enableThinking, Invalid value |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

