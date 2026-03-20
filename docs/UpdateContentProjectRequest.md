# UpdateContentProjectRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Project name (optional). | [optional] 
**description** | **str** | A brief explanation of the project (optional). | [optional] 

## Example

```python
from numind.models.update_content_project_request import UpdateContentProjectRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateContentProjectRequest from a JSON string
update_content_project_request_instance = UpdateContentProjectRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateContentProjectRequest.to_json())

# convert the object into a dict
update_content_project_request_dict = update_content_project_request_instance.to_dict()
# create an instance of UpdateContentProjectRequest from a dict
update_content_project_request_from_dict = UpdateContentProjectRequest.from_dict(update_content_project_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


