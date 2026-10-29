# numind.openapi_client.ContentExtractionApi

All URIs are relative to *https://nuextract.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_api_content_extraction_jobs_contentextractionjobid**](ContentExtractionApi.md#get_api_content_extraction_jobs_contentextractionjobid) | **GET** /api/content-extraction/jobs/{contentExtractionJobId} | 
[**post_api_content_extraction_jobs**](ContentExtractionApi.md#post_api_content_extraction_jobs) | **POST** /api/content-extraction/jobs | 


# **get_api_content_extraction_jobs_contentextractionjobid**
> ContentExtractionResponse get_api_content_extraction_jobs_contentextractionjobid(content_extraction_job_id, x_organization_id=x_organization_id)


 Get content extraction result of a specific job by its unique identifier.

#### Response:
 Returns a markdown string representing the extracted content.
 `isTruncated` is true when at least one document part stops at a token limit; the combined result may be incomplete.

#### Error Responses:
`404 Not Found` - If a content extraction job with the specified ID does not exist.

`403 Forbidden` - If the user does not have permission to access this job.
   

### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.content_extraction_response import ContentExtractionResponse
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
    api_instance = numind.openapi_client.ContentExtractionApi(api_client)
    content_extraction_job_id = "content_extraction_job_id_example"  # str | Unique content extraction job identifier.
    x_organization_id = "x_organization_id_example"  # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)

    try:
        api_response = (
            api_instance.get_api_content_extraction_jobs_contentextractionjobid(
                content_extraction_job_id, x_organization_id=x_organization_id
            )
        )
        print(
            "The response of ContentExtractionApi->get_api_content_extraction_jobs_contentextractionjobid:\n"
        )
        pprint(api_response)
    except Exception as e:
        print(
            "Exception when calling ContentExtractionApi->get_api_content_extraction_jobs_contentextractionjobid: %s\n"
            % e
        )
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **content_extraction_job_id** | **str**| Unique content extraction job identifier. | 
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 

### Return type

[**ContentExtractionResponse**](ContentExtractionResponse.md)

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

# **post_api_content_extraction_jobs**
> JobIdResponse post_api_content_extraction_jobs(file, x_organization_id=x_organization_id, project_id=project_id, temperature=temperature, rasterization_dpi=rasterization_dpi, max_output_tokens=max_output_tokens, enable_thinking=enable_thinking, thinking_token_budget=thinking_token_budget, loop_detection=loop_detection, random_seed=random_seed, image_width=image_width, timeout=timeout, low_priority=low_priority)


 Extract content from the provided file in markdown format as an async job.
 The response contains extracted markdown together with the reasoning trace.
 The model only accepts images. Therefore, some files are converted to images -
 the **rasterizationDPI** parameter controls their resolution.


#### Response:
 Returns a JSON containing the job ID that can be used to retrieve the job status and results.

 If the job is completed successfully, the job's output data will contain a JSON representing the inference result.
 The ***result*** field contains the extracted markdown. The ***thinking*** field contains the reasoning trace.
 If one of the fields ***result*** or ***thinking*** is empty, the ***rawResponse*** field contains the raw model output.
 and an HTTP code 206 is returned.
    
#### Settings:
Request settings override the project settings when `projectId` is provided; otherwise omitted settings use platform defaults.
Platform defaults: temperature 0.8, rasterization DPI `automatic`,
output token budget 20000, thinking enabled, thinking token budget 15000,
loop detection enabled, and random seed `2022`.


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
    api_instance = numind.openapi_client.ContentExtractionApi(api_client)
    file = None  # bytes |
    x_organization_id = "x_organization_id_example"  # str | Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. (optional)
    project_id = "project_id_example"  # str | Optional content project identifier. When provided, project settings are used as fallback for inference parameters; this identifier is also attached to usage and billing events. (optional)
    temperature = 3.4  # float | Model temperature. Controls output diversity. Ranges between 0 and 2. (optional)
    rasterization_dpi = "rasterization_dpi_example"  # str | Resolution used to convert formatted documents (PDFs, etc.) to images, in dots per inch. Use 'automatic' or an integer between 1 and 600. Numeric strings are also accepted. Ignored for files that are already images or text. (optional)
    max_output_tokens = "max_output_tokens_example"  # str | Maximum number of tokens for the corresponding budget (output or thinking). Given as a string: a strictly positive integer string, or Unlimited for no limit; zero is invalid. The thinking budget is only used when thinking is enabled. (optional)
    enable_thinking = True  # bool | Enable thinking/reasoning. (optional)
    thinking_token_budget = "thinking_token_budget_example"  # str | Maximum number of tokens for the corresponding budget (output or thinking). Given as a string: a strictly positive integer string, or Unlimited for no limit; zero is invalid. The thinking budget is only used when thinking is enabled. (optional)
    loop_detection = (
        True  # bool | Stop the generation when the model repeats itself. (optional)
    )
    random_seed = "random_seed_example"  # str | Inference seed setting. Use a string containing a 64-bit integer for a fixed seed, or `random` to generate one for each inference. (optional)
    image_width = "image_width_example"  # str | Original standalone images only (not PDF/TIFF or converted pages). Use automatic for a 1280 px short side, original to preserve the upload, or a positive integer for the upright image width in pixels. Aspect ratio is preserved; upscaling is allowed. (optional)
    timeout = "timeout_example"  # str | Execution timeout for the async inference job. If omitted, the server default of 60m is used.   If provided below the server-configured minimum (5m by default), the effective timeout is clamped to that minimum.   Format examples: 1000ms, 10s, 1m, 1h (optional)
    low_priority = False  # bool | Submit this job with lower scheduling priority in the job queue and inference engine. (optional) (default to False)

    try:
        api_response = api_instance.post_api_content_extraction_jobs(
            file,
            x_organization_id=x_organization_id,
            project_id=project_id,
            temperature=temperature,
            rasterization_dpi=rasterization_dpi,
            max_output_tokens=max_output_tokens,
            enable_thinking=enable_thinking,
            thinking_token_budget=thinking_token_budget,
            loop_detection=loop_detection,
            random_seed=random_seed,
            image_width=image_width,
            timeout=timeout,
            low_priority=low_priority,
        )
        print(
            "The response of ContentExtractionApi->post_api_content_extraction_jobs:\n"
        )
        pprint(api_response)
    except Exception as e:
        print(
            "Exception when calling ContentExtractionApi->post_api_content_extraction_jobs: %s\n"
            % e
        )
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file** | **bytes**|  | 
 **x_organization_id** | **str**| Optional organization to use for this request.   No header means that the user personal account will be used.   This token is *only* used by the _frontend_ application and *will be ignored if used with the API*. When using the api, the organization used will be the one of the api key. | [optional] 
 **project_id** | **str**| Optional content project identifier. When provided, project settings are used as fallback for inference parameters; this identifier is also attached to usage and billing events. | [optional] 
 **temperature** | **float**| Model temperature. Controls output diversity. Ranges between 0 and 2. | [optional] 
 **rasterization_dpi** | **str**| Resolution used to convert formatted documents (PDFs, etc.) to images, in dots per inch. Use &#39;automatic&#39; or an integer between 1 and 600. Numeric strings are also accepted. Ignored for files that are already images or text. | [optional] 
 **max_output_tokens** | **str**| Maximum number of tokens for the corresponding budget (output or thinking). Given as a string: a strictly positive integer string, or Unlimited for no limit; zero is invalid. The thinking budget is only used when thinking is enabled. | [optional] 
 **enable_thinking** | **bool**| Enable thinking/reasoning. | [optional] 
 **thinking_token_budget** | **str**| Maximum number of tokens for the corresponding budget (output or thinking). Given as a string: a strictly positive integer string, or Unlimited for no limit; zero is invalid. The thinking budget is only used when thinking is enabled. | [optional] 
 **loop_detection** | **bool**| Stop the generation when the model repeats itself. | [optional] 
 **random_seed** | **str**| Inference seed setting. Use a string containing a 64-bit integer for a fixed seed, or &#x60;random&#x60; to generate one for each inference. | [optional] 
 **image_width** | **str**| Original standalone images only (not PDF/TIFF or converted pages). Use automatic for a 1280 px short side, original to preserve the upload, or a positive integer for the upright image width in pixels. Aspect ratio is preserved; upscaling is allowed. | [optional] 
 **timeout** | **str**| Execution timeout for the async inference job. If omitted, the server default of 60m is used.   If provided below the server-configured minimum (5m by default), the effective timeout is clamped to that minimum.   Format examples: 1000ms, 10s, 1m, 1h | [optional] 
 **low_priority** | **bool**| Submit this job with lower scheduling priority in the job queue and inference engine. | [optional] [default to False]

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
**400** | Invalid value for: query parameter temperature, Invalid value for: query parameter enableThinking, Invalid value for: query parameter loopDetection, Invalid value for: body, Invalid value for: query parameter lowPriority |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

