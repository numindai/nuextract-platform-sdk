# InferenceValidationError


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | **str** | Error message explaining why the inference result is invalid. | 
**error_code** | **str** | Inference error code. | 

## Example

```python
from numind.models.inference_validation_error import InferenceValidationError

# TODO update the JSON string below
json = "{}"
# create an instance of InferenceValidationError from a JSON string
inference_validation_error_instance = InferenceValidationError.from_json(json)
# print the JSON string representation of the object
print(InferenceValidationError.to_json())

# convert the object into a dict
inference_validation_error_dict = inference_validation_error_instance.to_dict()
# create an instance of InferenceValidationError from a dict
inference_validation_error_from_dict = InferenceValidationError.from_dict(inference_validation_error_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


