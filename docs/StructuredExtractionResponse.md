# StructuredExtractionResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**result** | **object** | Inference result conforming to the template. | 
**thinking_trace** | **str** | Reasoning of structured data extraction model | [optional] 
**raw_model_output** | **str** | Raw inference result as returned by the model. | 
**error** | [**InferenceValidationError**](InferenceValidationError.md) | Inference result validation error if the result does not conform to the template. | [optional] 
**document_info** | [**DocumentInfo**](DocumentInfo.md) | Basic information on the document used for inference. | [optional] 
**output_tokens** | **int** | Output tokens used for inference. | 
**input_tokens** | **int** | Input tokens used for inference. | 
**total_tokens** | **int** | Total number of tokens used for inference (input + output). | 
**logprobs** | **float** | Logprob of the inference result (sum of logprobs of all tokens). | 
**output_token_probability** | **float** | Geometric mean of the output token probabilities. | 
**selected_examples** | [**List[StructuredInferenceExample]**](StructuredInferenceExample.md) | Examples selected for inference. | [optional] 

## Example

```python
from numind.models.structured_extraction_response import StructuredExtractionResponse

# TODO update the JSON string below
json = "{}"
# create an instance of StructuredExtractionResponse from a JSON string
structured_extraction_response_instance = StructuredExtractionResponse.from_json(json)
# print the JSON string representation of the object
print(StructuredExtractionResponse.to_json())

# convert the object into a dict
structured_extraction_response_dict = structured_extraction_response_instance.to_dict()
# create an instance of StructuredExtractionResponse from a dict
structured_extraction_response_from_dict = StructuredExtractionResponse.from_dict(structured_extraction_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


