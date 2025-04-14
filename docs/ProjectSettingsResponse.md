# ProjectSettingsResponse

Project settings.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**temperature** | **float** | The temperature to use for inference. | 
**rasterization_dpi** | **int** | Rasterization DPI used during file to image conversion. | 

## Example

```python
from numind.openapi_client.models.project_settings_response import ProjectSettingsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ProjectSettingsResponse from a JSON string
project_settings_response_instance = ProjectSettingsResponse.from_json(json)
# print the JSON string representation of the object
print(ProjectSettingsResponse.to_json())

# convert the object into a dict
project_settings_response_dict = project_settings_response_instance.to_dict()
# create an instance of ProjectSettingsResponse from a dict
project_settings_response_from_dict = ProjectSettingsResponse.from_dict(project_settings_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


