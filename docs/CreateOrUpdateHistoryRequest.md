# CreateOrUpdateHistoryRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**owner_organization** | **str** |  | [optional] 
**document_id** | **str** |  | 
**result** | **str** |  | 

## Example

```python
from numind.openapi_client.models.create_or_update_history_request import CreateOrUpdateHistoryRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateOrUpdateHistoryRequest from a JSON string
create_or_update_history_request_instance = CreateOrUpdateHistoryRequest.from_json(json)
# print the JSON string representation of the object
print(CreateOrUpdateHistoryRequest.to_json())

# convert the object into a dict
create_or_update_history_request_dict = create_or_update_history_request_instance.to_dict()
# create an instance of CreateOrUpdateHistoryRequest from a dict
create_or_update_history_request_from_dict = CreateOrUpdateHistoryRequest.from_dict(create_or_update_history_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


