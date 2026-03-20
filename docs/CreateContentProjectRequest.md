# CreateContentProjectRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Name of the project. | 
**description** | **str** | Text description of the project (can be left empty). | 

## Example

```python
from numind.models.create_content_project_request import CreateContentProjectRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateContentProjectRequest from a JSON string
create_content_project_request_instance = CreateContentProjectRequest.from_json(json)
# print the JSON string representation of the object
print(CreateContentProjectRequest.to_json())

# convert the object into a dict
create_content_project_request_dict = create_content_project_request_instance.to_dict()
# create an instance of CreateContentProjectRequest from a dict
create_content_project_request_from_dict = CreateContentProjectRequest.from_dict(create_content_project_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


