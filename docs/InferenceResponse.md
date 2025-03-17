# InferenceResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**result** | [**Obj1**](Obj1.md) |  | 
**raw_result** | [**RawResult**](RawResult.md) |  | [optional] 
**document_info** | [**DocumentInfo**](DocumentInfo.md) |  | 
**tokens** | **int** |  | 

## Example

```python
from numind.openapi_client.models.inference_response import InferenceResponse

# TODO update the JSON string below
json = "{}"
# create an instance of InferenceResponse from a JSON string
inference_response_instance = InferenceResponse.from_json(json)
# print the JSON string representation of the object
print(InferenceResponse.to_json())

# convert the object into a dict
inference_response_dict = inference_response_instance.to_dict()
# create an instance of InferenceResponse from a dict
inference_response_from_dict = InferenceResponse.from_dict(inference_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


