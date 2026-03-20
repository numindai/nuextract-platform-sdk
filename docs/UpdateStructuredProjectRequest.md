# UpdateStructuredProjectRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Project name (optional). | [optional] 
**description** | **str** | A brief explanation of the project (optional). | [optional] 
**template** | **object** | Extraction template (NuExtract format) (optional). | [optional] 
**instructions** | **str** | Instructions to give more context (optional). | [optional] 

## Example

```python
from numind.models.update_structured_project_request import UpdateStructuredProjectRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateStructuredProjectRequest from a JSON string
update_structured_project_request_instance = UpdateStructuredProjectRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateStructuredProjectRequest.to_json())

# convert the object into a dict
update_structured_project_request_dict = update_structured_project_request_instance.to_dict()
# create an instance of UpdateStructuredProjectRequest from a dict
update_structured_project_request_from_dict = UpdateStructuredProjectRequest.from_dict(update_structured_project_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


