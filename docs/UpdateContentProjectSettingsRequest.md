# UpdateContentProjectSettingsRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**temperature** | **float** | Model temperature (optional). | [optional] 
**rasterization_dpi** | **int** | Resolution used to convert formatted documents to images (optional). | [optional] 
**max_output_tokens** | **int** | Maximum number of output tokens (optional). Must be positive. Set to 0 for no limit. | [optional] 
**enable_thinking** | **bool** | Enable thinking/reasoning (optional). | [optional] 
**random_seed** | **str** | Inference seed setting (optional). Use a string containing a 64-bit integer for a fixed seed, or &#x60;random&#x60; to generate one for each inference. | [optional] 

## Example

```python
from numind.models.update_content_project_settings_request import (
    UpdateContentProjectSettingsRequest,
)

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateContentProjectSettingsRequest from a JSON string
update_content_project_settings_request_instance = (
    UpdateContentProjectSettingsRequest.from_json(json)
)
# print the JSON string representation of the object
print(UpdateContentProjectSettingsRequest.to_json())

# convert the object into a dict
update_content_project_settings_request_dict = (
    update_content_project_settings_request_instance.to_dict()
)
# create an instance of UpdateContentProjectSettingsRequest from a dict
update_content_project_settings_request_from_dict = (
    UpdateContentProjectSettingsRequest.from_dict(
        update_content_project_settings_request_dict
    )
)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


