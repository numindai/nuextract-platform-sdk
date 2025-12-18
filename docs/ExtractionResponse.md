# ExtractionResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**result** | **object** | Inference result conforming to the template. | 
**raw_model_output** | **str** | Raw inference result as returned by the model. | 
**error** | [**InferenceValidationError**](InferenceValidationError.md) | Inference result validation error if the result does not conform to the template. | [optional] 
**document_info** | [**DocumentInfo**](DocumentInfo.md) | Basic information on the document used for inference. | [optional] 
**output_tokens** | **int** | Output tokens used for inference. | 
**input_tokens** | **int** | Input tokens used for inference. | 
**total_tokens** | **int** | Total number of tokens used for inference (input + output). | 
**logprobs** | **float** | Logprob of the inference result (sum of logprobs of all tokens). | 
**selected_examples** | [**List[InferenceExample]**](InferenceExample.md) | Examples selected for inference. | [optional] 

## Example

```python
from numind.models.extraction_response import ExtractionResponse

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


