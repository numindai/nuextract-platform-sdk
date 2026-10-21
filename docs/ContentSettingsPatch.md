# ContentSettingsPatch


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**temperature** | **float** | Model temperature. Controls output diversity. Ranges between 0 and 2. | [optional] 
**rasterization_dpi** | [**ContentProjectSettingsResponseRasterizationDPI**](ContentProjectSettingsResponseRasterizationDPI.md) |  | [optional] 
**max_output_tokens** | **int** | Maximum number of tokens for the corresponding budget (output or thinking). Use a positive integer, or 0 for no limit. The thinking budget is only used when thinking is enabled. | [optional] 
**enable_thinking** | **bool** | Enable thinking/reasoning. | [optional] 
**thinking_token_budget** | **int** | Maximum number of tokens for the corresponding budget (output or thinking). Use a positive integer, or 0 for no limit. The thinking budget is only used when thinking is enabled. | [optional] 
**loop_detection** | **bool** | Stop the generation when the model repeats itself. | [optional] 
**random_seed** | **str** | Inference seed setting. Use a string containing a 64-bit integer for a fixed seed, or &#x60;random&#x60; to generate one for each inference. | [optional] 
**image_width** | [**ContentProjectSettingsResponseImageWidth**](ContentProjectSettingsResponseImageWidth.md) |  | [optional] 

## Example

```python
from numind.models.content_settings_patch import ContentSettingsPatch

# TODO update the JSON string below
json = "{}"
# create an instance of ContentSettingsPatch from a JSON string
content_settings_patch_instance = ContentSettingsPatch.from_json(json)
# print the JSON string representation of the object
print(ContentSettingsPatch.to_json())

# convert the object into a dict
content_settings_patch_dict = content_settings_patch_instance.to_dict()
# create an instance of ContentSettingsPatch from a dict
content_settings_patch_from_dict = ContentSettingsPatch.from_dict(
    content_settings_patch_dict
)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


