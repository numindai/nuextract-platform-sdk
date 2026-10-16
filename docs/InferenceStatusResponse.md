# InferenceStatusResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**inference** | [**InferenceStatus**](InferenceStatus.md) |  | 

## Example

```python
from numind.models.inference_status_response import InferenceStatusResponse

# TODO update the JSON string below
json = "{}"
# create an instance of InferenceStatusResponse from a JSON string
inference_status_response_instance = InferenceStatusResponse.from_json(json)
# print the JSON string representation of the object
print(InferenceStatusResponse.to_json())

# convert the object into a dict
inference_status_response_dict = inference_status_response_instance.to_dict()
# create an instance of InferenceStatusResponse from a dict
inference_status_response_from_dict = InferenceStatusResponse.from_dict(
    inference_status_response_dict
)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


