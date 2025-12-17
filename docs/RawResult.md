# RawResult

Inference result if not conforming to the template.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**result** | **str** | Inference result not conforming to the format. | 
**error** | **str** | Error message explaining why the inference result is invalid. | 
**inference_error** | **str** | Inference error code. | 

## Example

```python
from numind.models.raw_result import RawResult

# TODO update the JSON string below
json = "{}"
# create an instance of RawResult from a JSON string
raw_result_instance = RawResult.from_json(json)
# print the JSON string representation of the object
print(RawResult.to_json())

# convert the object into a dict
raw_result_dict = raw_result_instance.to_dict()
# create an instance of RawResult from a dict
raw_result_from_dict = RawResult.from_dict(raw_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


