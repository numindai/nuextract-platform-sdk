# MarkdownProjectResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique project identifier. | 
**name** | **str** | Project name. | 
**description** | **str** | A brief explanation of the project. | 
**owner_user** | **str** | Project owner. | 
**owner_organization** | **str** | Project owning organization (if any). | [optional] 
**created_at** | **str** | Project creation date. | 
**updated_at** | **str** | Project last update date. | 
**settings** | [**MarkdownProjectSettingsResponse**](MarkdownProjectSettingsResponse.md) |  | 

## Example

```python
from numind.models.markdown_project_response import MarkdownProjectResponse

# TODO update the JSON string below
json = "{}"
# create an instance of MarkdownProjectResponse from a JSON string
markdown_project_response_instance = MarkdownProjectResponse.from_json(json)
# print the JSON string representation of the object
print(MarkdownProjectResponse.to_json())

# convert the object into a dict
markdown_project_response_dict = markdown_project_response_instance.to_dict()
# create an instance of MarkdownProjectResponse from a dict
markdown_project_response_from_dict = MarkdownProjectResponse.from_dict(markdown_project_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


