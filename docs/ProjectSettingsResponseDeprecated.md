# ProjectSettingsResponseDeprecated

Project settings.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**temperature** | **float** | Model temperature. | 
**rasterization_dpi** | **int** | Resolution used to convert formatted documents to images. | 
**max_output_tokens** | **int** | Maximum number of output tokens (optional). Must be positive. Set to 0 for no limit. | 
**degraded_mode** | **str** | Controls whether a response is returned when smart example is not functionning. Rejects by default. | 
**max_tokens_smart_example** | **int** | Maximum number of output tokens for smart examples (optional). Must be positive. | 

## Example

```python
from numind.models.project_settings_response_deprecated import ProjectSettingsResponseDeprecated

# TODO update the JSON string below
json = "{}"
# create an instance of ProjectSettingsResponseDeprecated from a JSON string
project_settings_response_deprecated_instance = ProjectSettingsResponseDeprecated.from_json(json)
# print the JSON string representation of the object
print(ProjectSettingsResponseDeprecated.to_json())

# convert the object into a dict
project_settings_response_deprecated_dict = project_settings_response_deprecated_instance.to_dict()
# create an instance of ProjectSettingsResponseDeprecated from a dict
project_settings_response_deprecated_from_dict = ProjectSettingsResponseDeprecated.from_dict(project_settings_response_deprecated_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


