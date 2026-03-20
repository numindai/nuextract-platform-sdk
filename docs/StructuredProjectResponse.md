# StructuredProjectResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique project identifier. | 
**name** | **str** | Project name. | 
**description** | **str** | A brief explanation of the project. | 
**template** | **object** | Extraction template (NuExtract format). | 
**instructions** | **str** | Instructions to give more context. | 
**owner_user** | **str** | Project owner. | 
**owner_organization** | **str** | Project owning organization (if any). | [optional] 
**created_at** | **str** | Project creation date. | 
**updated_at** | **str** | Project last update date. | 
**lock_state** | **bool** | The lock state of the project. | 
**shared** | **bool** | The shared (reference) state of the project. | 
**settings** | [**StructuredProjectSettingsResponse**](StructuredProjectSettingsResponse.md) |  | 

## Example

```python
from numind.models.structured_project_response import StructuredProjectResponse

# TODO update the JSON string below
json = "{}"
# create an instance of StructuredProjectResponse from a JSON string
structured_project_response_instance = StructuredProjectResponse.from_json(json)
# print the JSON string representation of the object
print(StructuredProjectResponse.to_json())

# convert the object into a dict
structured_project_response_dict = structured_project_response_instance.to_dict()
# create an instance of StructuredProjectResponse from a dict
structured_project_response_from_dict = StructuredProjectResponse.from_dict(structured_project_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


