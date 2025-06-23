# ExtractionResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**result** | **object** | Extraction result conforming to the template. | 
**raw_result** | [**RawResult**](RawResult.md) | Extraction result if not conforming to the template. | [optional] 
**completion_tokens** | **int** | Completion tokens used for extraction (output). | 
**prompt_tokens** | **int** | Prompt tokens used for extraction (input). | 
**total_tokens** | **int** | Total number of tokens used for extraction (input + output). | 
**logprobs** | **float** | Logprob of the extraction result (sum of logprobs of all tokens). | 

## Example

```python
from numind.openapi_client.models.extraction_response import ExtractionResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ExtractionResponse from a JSON string
extraction_response_instance = ExtractionResponse.from_json(json)
# print the JSON string representation of the object
print(ExtractionResponse.to_json())

# convert the object into a dict
extraction_response_dict = extraction_response_instance.to_dict()
# create an instance of ExtractionResponse from a dict
extraction_response_from_dict = ExtractionResponse.from_dict(extraction_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


