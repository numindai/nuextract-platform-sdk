# ContentProjectSettingsResponse

Project settings.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**temperature** | **float** | Model temperature. | 
**rasterization_dpi** | **int** | Resolution used to convert formatted documents to images. | 
**max_output_tokens** | **int** | Maximum number of output tokens. Must be positive. Set to 0 for no limit. | 
**enable_thinking** | **bool** | Enable thinking/reasoning. | 

## Example

```python
from numind.models.content_project_settings_response import ContentProjectSettingsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ContentProjectSettingsResponse from a JSON string
content_project_settings_response_instance = ContentProjectSettingsResponse.from_json(json)
# print the JSON string representation of the object
print(ContentProjectSettingsResponse.to_json())

# convert the object into a dict
content_project_settings_response_dict = content_project_settings_response_instance.to_dict()
# create an instance of ContentProjectSettingsResponse from a dict
content_project_settings_response_from_dict = ContentProjectSettingsResponse.from_dict(content_project_settings_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


