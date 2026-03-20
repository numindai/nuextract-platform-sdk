# CreateStructuredProjectRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Name of the project. | 
**description** | **str** | Text description of the project (can be left empty). | 
**template** | **object** | Template of the project. | 
**instructions** | **str** | Instructions to give more context. | 

## Example

```python
from numind.models.create_structured_project_request import CreateStructuredProjectRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateStructuredProjectRequest from a JSON string
create_structured_project_request_instance = CreateStructuredProjectRequest.from_json(json)
# print the JSON string representation of the object
print(CreateStructuredProjectRequest.to_json())

# convert the object into a dict
create_structured_project_request_dict = create_structured_project_request_instance.to_dict()
# create an instance of CreateStructuredProjectRequest from a dict
create_structured_project_request_from_dict = CreateStructuredProjectRequest.from_dict(create_structured_project_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


