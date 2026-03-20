# ContentProjectResponse


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
**settings** | [**ContentProjectSettingsResponse**](ContentProjectSettingsResponse.md) |  | 

## Example

```python
from numind.models.content_project_response import ContentProjectResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ContentProjectResponse from a JSON string
content_project_response_instance = ContentProjectResponse.from_json(json)
# print the JSON string representation of the object
print(ContentProjectResponse.to_json())

# convert the object into a dict
content_project_response_dict = content_project_response_instance.to_dict()
# create an instance of ContentProjectResponse from a dict
content_project_response_from_dict = ContentProjectResponse.from_dict(content_project_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


