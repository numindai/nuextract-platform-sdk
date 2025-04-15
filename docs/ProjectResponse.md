# ProjectResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique project identifier. | 
**name** | **str** | Project name. | 
**description** | **str** | A brief explanation of the project. | 
**template** | **object** | Extraction template (NuExtract format). | 
**owner_user** | **str** | Project owner. | 
**owner_organization** | **str** | Project owning organization (if any). | [optional] 
**created_at** | **str** | Project creation date. | 
**updated_at** | **str** | Project last update date. | 
**lock_state** | **bool** | The lock state of the project. | 
**shared** | **bool** | The shared state of the project. | 
**settings** | [**ProjectSettingsResponse**](ProjectSettingsResponse.md) |  | 

## Example

```python
from numind.openapi_client.models.project_response import ProjectResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ProjectResponse from a JSON string
project_response_instance = ProjectResponse.from_json(json)
# print the JSON string representation of the object
print(ProjectResponse.to_json())

# convert the object into a dict
project_response_dict = project_response_instance.to_dict()
# create an instance of ProjectResponse from a dict
project_response_from_dict = ProjectResponse.from_dict(project_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


