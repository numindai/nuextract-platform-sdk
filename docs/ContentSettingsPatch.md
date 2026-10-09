# ContentSettingsPatch


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**temperature** | **float** | Model temperature (optional). | [optional] 
**rasterization_dpi** | [**ContentSettingsPatchRasterizationDPI**](ContentSettingsPatchRasterizationDPI.md) |  | [optional] 
**max_output_tokens** | **int** | Maximum number of output tokens (optional). Must be positive. Set to 0 for no limit. | [optional] 
**enable_thinking** | **bool** | Enable thinking/reasoning (optional). | [optional] 
**thinking_token_budget** | **int** | Maximum number of thinking tokens (optional). Set to 0 for no limit. | [optional] 
**loop_detection** | **bool** | Stop the generation when the model repeats itself (optional). | [optional] 
**random_seed** | **str** | Inference seed setting (optional). Use a string containing a 64-bit integer for a fixed seed, or &#x60;random&#x60; to generate one for each inference. | [optional] 

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


