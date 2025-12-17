# MarkdownProjectSettingsResponse

Project settings.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**temperature** | **float** | Model temperature. | 
**rasterization_dpi** | **int** | Resolution used to convert formatted documents to images. | 
**max_output_tokens** | **int** | Maximum number of output tokens (optional). Must be positive. Set to 0 for no limit. | 

## Example

```python
from numind.models.markdown_project_settings_response import MarkdownProjectSettingsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of MarkdownProjectSettingsResponse from a JSON string
markdown_project_settings_response_instance = MarkdownProjectSettingsResponse.from_json(json)
# print the JSON string representation of the object
print(MarkdownProjectSettingsResponse.to_json())

# convert the object into a dict
markdown_project_settings_response_dict = markdown_project_settings_response_instance.to_dict()
# create an instance of MarkdownProjectSettingsResponse from a dict
markdown_project_settings_response_from_dict = MarkdownProjectSettingsResponse.from_dict(markdown_project_settings_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


