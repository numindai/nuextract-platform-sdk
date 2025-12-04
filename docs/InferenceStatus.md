# InferenceStatus


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**running** | **int** |  | 
**waiting** | **int** |  | 

## Example

```python
from numind.models.inference_status import InferenceStatus

# TODO update the JSON string below
json = "{}"
# create an instance of InferenceStatus from a JSON string
inference_status_instance = InferenceStatus.from_json(json)
# print the JSON string representation of the object
print(InferenceStatus.to_json())

# convert the object into a dict
inference_status_dict = inference_status_instance.to_dict()
# create an instance of InferenceStatus from a dict
inference_status_from_dict = InferenceStatus.from_dict(inference_status_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


