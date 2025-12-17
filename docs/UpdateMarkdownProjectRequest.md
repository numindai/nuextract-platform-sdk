# UpdateMarkdownProjectRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Project name (optional). | [optional] 
**description** | **str** | A brief explanation of the project (optional). | [optional] 

## Example

```python
from numind.models.update_markdown_project_request import UpdateMarkdownProjectRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateMarkdownProjectRequest from a JSON string
update_markdown_project_request_instance = UpdateMarkdownProjectRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateMarkdownProjectRequest.to_json())

# convert the object into a dict
update_markdown_project_request_dict = update_markdown_project_request_instance.to_dict()
# create an instance of UpdateMarkdownProjectRequest from a dict
update_markdown_project_request_from_dict = UpdateMarkdownProjectRequest.from_dict(update_markdown_project_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


