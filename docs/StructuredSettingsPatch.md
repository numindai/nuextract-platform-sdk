# StructuredSettingsPatch


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**temperature** | **float** | Model temperature (optional). | [optional] 
**rasterization_dpi** | [**StructuredSettingsPatchRasterizationDPI**](StructuredSettingsPatchRasterizationDPI.md) |  | [optional] 
**max_output_tokens** | **int** | Maximum number of output tokens (optional). Must be positive. Set to 0 for no limit. | [optional] 
**max_example_token_number** | **int** | Maximum number of output tokens for smart examples (optional). Must be positive. | [optional] 
**max_example_number** | **int** | Maximum number of examples to use (optional). Must be positive. Set to 0 for no limit. | [optional] 
**min_example_similarity** | **float** | Minimum similarity between the document and the examples (optional). Must be between 0 and 1. Set to 0 for any similarity and 1 for exact match. | [optional] 
**enable_thinking** | **bool** | Enable thinking/reasoning (optional). | [optional] 
**thinking_token_budget** | **int** | Maximum number of thinking tokens (optional). Set to 0 for no limit. | [optional] 
**loop_detection** | **bool** | Stop the generation when the model repeats itself (optional). | [optional] 
**random_seed** | **str** | Inference seed setting (optional). Use a string containing a 64-bit integer for a fixed seed, or &#x60;random&#x60; to generate one for each inference. | [optional] 

## Example

```python
from numind.models.structured_settings_patch import StructuredSettingsPatch

# TODO update the JSON string below
json = "{}"
# create an instance of StructuredSettingsPatch from a JSON string
structured_settings_patch_instance = StructuredSettingsPatch.from_json(json)
# print the JSON string representation of the object
print(StructuredSettingsPatch.to_json())

# convert the object into a dict
structured_settings_patch_dict = structured_settings_patch_instance.to_dict()
# create an instance of StructuredSettingsPatch from a dict
structured_settings_patch_from_dict = StructuredSettingsPatch.from_dict(
    structured_settings_patch_dict
)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


