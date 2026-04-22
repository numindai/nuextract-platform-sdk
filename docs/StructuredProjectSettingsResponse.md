# StructuredProjectSettingsResponse

Project settings.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**temperature** | **float** | Model temperature. | 
**rasterization_dpi** | **int** | Resolution used to convert formatted documents to images. | 
**max_output_tokens** | **int** | Maximum number of output tokens (optional). Must be positive. Set to 0 for no limit. | 
**max_example_token_number** | **int** | Maximum number of output tokens for smart examples (optional). Must be positive. | 
**max_example_number** | **int** | Maximum number of examples to use (optional). Must be positive. Set to 0 for no limit. | 
**min_example_similarity** | **float** | Minimum similarity between the document and the examples (optional). Must be between 0 and 1. Set to 0 for any similarity and 1 for exact match. | 
**enable_thinking** | **bool** | Enable thinking/reasoning. | 

## Example

```python
from numind.models.structured_project_settings_response import StructuredProjectSettingsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of StructuredProjectSettingsResponse from a JSON string
structured_project_settings_response_instance = StructuredProjectSettingsResponse.from_json(json)
# print the JSON string representation of the object
print(StructuredProjectSettingsResponse.to_json())

# convert the object into a dict
structured_project_settings_response_dict = structured_project_settings_response_instance.to_dict()
# create an instance of StructuredProjectSettingsResponse from a dict
structured_project_settings_response_from_dict = StructuredProjectSettingsResponse.from_dict(structured_project_settings_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


