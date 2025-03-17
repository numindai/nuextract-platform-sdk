# HistoryResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**project_id** | **str** |  | 
**owner_user** | **str** |  | 
**document_info** | [**DocumentInfo**](DocumentInfo.md) |  | 
**result** | [**InformationResponse**](InformationResponse.md) |  | 
**created_at** | **str** |  | 
**updated_at** | **str** |  | 

## Example

```python
from numind.openapi_client.models.history_response import HistoryResponse

# TODO update the JSON string below
json = "{}"
# create an instance of HistoryResponse from a JSON string
history_response_instance = HistoryResponse.from_json(json)
# print the JSON string representation of the object
print(HistoryResponse.to_json())

# convert the object into a dict
history_response_dict = history_response_instance.to_dict()
# create an instance of HistoryResponse from a dict
history_response_from_dict = HistoryResponse.from_dict(history_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


