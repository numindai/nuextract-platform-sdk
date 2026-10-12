# StructuredProjectSettingsResponse

Project settings.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**temperature** | **float** | Model temperature. Controls output diversity. Ranges between 0 and 2. | 
**rasterization_dpi** | [**ContentProjectSettingsResponseRasterizationDPI**](ContentProjectSettingsResponseRasterizationDPI.md) |  | 
**max_output_tokens** | **int** | Maximum number of tokens for the corresponding budget (output or thinking). Use a positive integer, or 0 for no limit. The thinking budget is only used when thinking is enabled. | 
**max_example_token_number** | **int** | Maximum number of tokens allocated to smart examples. Must be between 0 and 130000, within the model&#39;s context window. | 
**max_example_number** | **int** | Maximum number of examples to use. Must be positive. Set to 0 for no limit. | 
**min_example_similarity** | **float** | Minimum similarity between the document and the examples. Must be between 0 and 1. Set to 0 for any similarity and 1 for exact match. | 
**enable_thinking** | **bool** | Enable thinking/reasoning. | 
**thinking_token_budget** | **int** | Maximum number of tokens for the corresponding budget (output or thinking). Use a positive integer, or 0 for no limit. The thinking budget is only used when thinking is enabled. | 
**loop_detection** | **bool** | Stop the generation when the model repeats itself. | 
**random_seed** | **str** | Inference seed setting. Use a string containing a 64-bit integer for a fixed seed, or &#x60;random&#x60; to generate one for each inference. | 

## Example

```python
from numind.models.structured_project_settings_response import (
    StructuredProjectSettingsResponse,
)

# TODO update the JSON string below
json = "{}"
# create an instance of StructuredProjectSettingsResponse from a JSON string
structured_project_settings_response_instance = (
    StructuredProjectSettingsResponse.from_json(json)
)
# print the JSON string representation of the object
print(StructuredProjectSettingsResponse.to_json())

# convert the object into a dict
structured_project_settings_response_dict = (
    structured_project_settings_response_instance.to_dict()
)
# create an instance of StructuredProjectSettingsResponse from a dict
structured_project_settings_response_from_dict = (
    StructuredProjectSettingsResponse.from_dict(
        structured_project_settings_response_dict
    )
)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


