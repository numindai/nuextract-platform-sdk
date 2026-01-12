# TemplateResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**result** | **object** | Template in NuExtract format. | 
**raw_model_output** | **str** | Raw inference result as returned by the model. | 
**error** | [**InferenceValidationError**](InferenceValidationError.md) | Inference result validation error if the result does not conform to the NuExtract template format. | [optional] 
**output_tokens** | **int** | Output tokens used for inference. | 
**input_tokens** | **int** | Input tokens used for inference. | 
**total_tokens** | **int** | Total number of tokens used for inference (input + output). | 
**logprobs** | **float** | Logprob of the inference result (sum of logprobs of all tokens). | 
**output_token_probability** | **float** | Geometric mean of the output token probabilities. | 

## Example

```python
from numind.models.template_response import TemplateResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TemplateResponse from a JSON string
template_response_instance = TemplateResponse.from_json(json)
# print the JSON string representation of the object
print(TemplateResponse.to_json())

# convert the object into a dict
template_response_dict = template_response_instance.to_dict()
# create an instance of TemplateResponse from a dict
template_response_from_dict = TemplateResponse.from_dict(template_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


