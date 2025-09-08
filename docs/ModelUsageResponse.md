# ModelUsageResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**usage** | **int** |  | 
**balance** | **int** |  | 
**overage** | **int** |  | 

## Example

```python
from numind.openapi_client.models.model_usage_response import ModelUsageResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ModelUsageResponse from a JSON string
model_usage_response_instance = ModelUsageResponse.from_json(json)
# print the JSON string representation of the object
print(ModelUsageResponse.to_json())

# convert the object into a dict
model_usage_response_dict = model_usage_response_instance.to_dict()
# create an instance of ModelUsageResponse from a dict
model_usage_response_from_dict = ModelUsageResponse.from_dict(model_usage_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


