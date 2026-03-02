# CreateMarkdownProjectRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Name of the project. | 
**description** | **str** | Text description of the project (can be left empty). | 

## Example

```python
from numind.models.create_markdown_project_request import CreateMarkdownProjectRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateMarkdownProjectRequest from a JSON string
create_markdown_project_request_instance = CreateMarkdownProjectRequest.from_json(json)
# print the JSON string representation of the object
print(CreateMarkdownProjectRequest.to_json())

# convert the object into a dict
create_markdown_project_request_dict = create_markdown_project_request_instance.to_dict()
# create an instance of CreateMarkdownProjectRequest from a dict
create_markdown_project_request_from_dict = CreateMarkdownProjectRequest.from_dict(create_markdown_project_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


