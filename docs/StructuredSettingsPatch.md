# StructuredSettingsPatch


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**temperature** | **float** | Model temperature. Controls output diversity. Ranges between 0 and 2. | [optional] 
**rasterization_dpi** | [**ContentProjectSettingsResponseRasterizationDPI**](ContentProjectSettingsResponseRasterizationDPI.md) |  | [optional] 
**max_output_tokens** | **str** | Maximum number of tokens for the corresponding budget (output or thinking). Given as a string: a strictly positive integer string, or Unlimited for no limit; zero is invalid. The thinking budget is only used when thinking is enabled. | [optional] 
**max_example_token_number** | **int** | Maximum number of tokens allocated to smart examples. Must be between 0 and 130000, within the model&#39;s context window. | [optional] 
**max_example_number** | **str** | Maximum number of examples to use. Given as a string: 0 for no examples, a positive integer string for a limit, or Unlimited for no count limit. | [optional] 
**min_example_similarity** | **float** | Minimum similarity between the document and the examples. Must be between 0 and 1. Set to 0 for any similarity and 1 for exact match. | [optional] 
**enable_thinking** | **bool** | Enable thinking/reasoning. | [optional] 
**thinking_token_budget** | **str** | Maximum number of tokens for the corresponding budget (output or thinking). Given as a string: a strictly positive integer string, or Unlimited for no limit; zero is invalid. The thinking budget is only used when thinking is enabled. | [optional] 
**loop_detection** | **bool** | Stop the generation when the model repeats itself. | [optional] 
**random_seed** | **str** | Inference seed setting. Use a string containing a 64-bit integer for a fixed seed, or &#x60;random&#x60; to generate one for each inference. | [optional] 
**image_width** | [**ContentProjectSettingsResponseImageWidth**](ContentProjectSettingsResponseImageWidth.md) |  | [optional] 

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


