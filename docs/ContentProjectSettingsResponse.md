# ContentProjectSettingsResponse

Project settings.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**temperature** | **float** | Model temperature. Controls output diversity. Ranges between 0 and 2. | 
**rasterization_dpi** | [**ContentProjectSettingsResponseRasterizationDPI**](ContentProjectSettingsResponseRasterizationDPI.md) |  | 
**max_output_tokens** | **int** | Maximum number of tokens for the corresponding budget (output or thinking). Use a positive integer, or 0 for no limit. The thinking budget is only used when thinking is enabled. | 
**enable_thinking** | **bool** | Enable thinking/reasoning. | 
**thinking_token_budget** | **int** | Maximum number of tokens for the corresponding budget (output or thinking). Use a positive integer, or 0 for no limit. The thinking budget is only used when thinking is enabled. | 
**loop_detection** | **bool** | Stop the generation when the model repeats itself. | 
**random_seed** | **str** | Inference seed setting. Use a string containing a 64-bit integer for a fixed seed, or &#x60;random&#x60; to generate one for each inference. | 
**image_width** | [**ContentProjectSettingsResponseImageWidth**](ContentProjectSettingsResponseImageWidth.md) |  | 

## Example

```python
from numind.models.content_project_settings_response import (
    ContentProjectSettingsResponse,
)

# TODO update the JSON string below
json = "{}"
# create an instance of ContentProjectSettingsResponse from a JSON string
content_project_settings_response_instance = ContentProjectSettingsResponse.from_json(
    json
)
# print the JSON string representation of the object
print(ContentProjectSettingsResponse.to_json())

# convert the object into a dict
content_project_settings_response_dict = (
    content_project_settings_response_instance.to_dict()
)
# create an instance of ContentProjectSettingsResponse from a dict
content_project_settings_response_from_dict = ContentProjectSettingsResponse.from_dict(
    content_project_settings_response_dict
)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


