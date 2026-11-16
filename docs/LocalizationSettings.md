# LocalizationSettings


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**temperature** | **float** |  | [optional] 
**max_output_tokens** | **str** | A string containing a positive integer or Unlimited. | [optional] 
**loop_detection** | **bool** |  | [optional] 
**random_seed** | **str** |  | [optional] 

## Example

```python
from numind.models.localization_settings import LocalizationSettings

# TODO update the JSON string below
json = "{}"
# create an instance of LocalizationSettings from a JSON string
localization_settings_instance = LocalizationSettings.from_json(json)
# print the JSON string representation of the object
print(LocalizationSettings.to_json())

# convert the object into a dict
localization_settings_dict = localization_settings_instance.to_dict()
# create an instance of LocalizationSettings from a dict
localization_settings_from_dict = LocalizationSettings.from_dict(
    localization_settings_dict
)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


