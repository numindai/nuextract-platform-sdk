# UpdateProjectSettingsRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**temperature** | **float** | Model temperature (optional). | [optional] 
**rasterization_dpi** | **int** | Resolution used to convert formatted documents to images (optional). | [optional] 
**max_output_tokens** | **int** | Maximum number of output tokens (optional). Must be positive. Set to 0 for no limit. | [optional] 

## Example

```python
from numind.openapi_client.models.update_project_settings_request import UpdateProjectSettingsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateProjectSettingsRequest from a JSON string
update_project_settings_request_instance = UpdateProjectSettingsRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateProjectSettingsRequest.to_json())

# convert the object into a dict
update_project_settings_request_dict = update_project_settings_request_instance.to_dict()
# create an instance of UpdateProjectSettingsRequest from a dict
update_project_settings_request_from_dict = UpdateProjectSettingsRequest.from_dict(update_project_settings_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


