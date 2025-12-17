# ExtractionResponseDeprecated


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**result** | **object** | Inference result conforming to the template. | 
**raw_result** | [**RawResult**](RawResult.md) |  | [optional] 
**document_info** | [**DocumentInfo**](DocumentInfo.md) | Basic information on the document used for inference. | [optional] 
**output_tokens** | **int** | Output tokens used for inference. | 
**input_tokens** | **int** | Input tokens used for inference. | 
**total_tokens** | **int** | Total number of tokens used for inference (input + output). | 
**logprobs** | **float** | Logprob of the inference result (sum of logprobs of all tokens). | 

## Example

```python
from numind.models.extraction_response_deprecated import ExtractionResponseDeprecated

# TODO update the JSON string below
json = "{}"
# create an instance of ExtractionResponseDeprecated from a JSON string
extraction_response_deprecated_instance = ExtractionResponseDeprecated.from_json(json)
# print the JSON string representation of the object
print(ExtractionResponseDeprecated.to_json())

# convert the object into a dict
extraction_response_deprecated_dict = extraction_response_deprecated_instance.to_dict()
# create an instance of ExtractionResponseDeprecated from a dict
extraction_response_deprecated_from_dict = ExtractionResponseDeprecated.from_dict(extraction_response_deprecated_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


