# ProjectResponseDeprecated


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
**shared** | **bool** | The shared (reference) state of the project. | 
**settings** | [**ProjectSettingsResponseDeprecated**](ProjectSettingsResponseDeprecated.md) |  | 

## Example

```python
from numind.models.project_response_deprecated import ProjectResponseDeprecated

# TODO update the JSON string below
json = "{}"
# create an instance of ProjectResponseDeprecated from a JSON string
project_response_deprecated_instance = ProjectResponseDeprecated.from_json(json)
# print the JSON string representation of the object
print(ProjectResponseDeprecated.to_json())

# convert the object into a dict
project_response_deprecated_dict = project_response_deprecated_instance.to_dict()
# create an instance of ProjectResponseDeprecated from a dict
project_response_deprecated_from_dict = ProjectResponseDeprecated.from_dict(project_response_deprecated_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


