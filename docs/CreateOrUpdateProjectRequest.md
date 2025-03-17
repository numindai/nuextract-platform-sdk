# CreateOrUpdateProjectRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**description** | **str** |  | 
**template** | [**Obj**](Obj.md) |  | 
**owner_organization** | **str** |  | [optional] 

## Example

```python
from numind.openapi_client.models.create_or_update_project_request import CreateOrUpdateProjectRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateOrUpdateProjectRequest from a JSON string
create_or_update_project_request_instance = CreateOrUpdateProjectRequest.from_json(json)
# print the JSON string representation of the object
print(CreateOrUpdateProjectRequest.to_json())

# convert the object into a dict
create_or_update_project_request_dict = create_or_update_project_request_instance.to_dict()
# create an instance of CreateOrUpdateProjectRequest from a dict
create_or_update_project_request_from_dict = CreateOrUpdateProjectRequest.from_dict(create_or_update_project_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


