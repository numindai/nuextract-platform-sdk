# LocalizationParameters


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**extraction** | **object** |  | 
**settings** | [**LocalizationSettings**](LocalizationSettings.md) |  | [optional] 

## Example

```python
from numind.models.localization_parameters import LocalizationParameters

# TODO update the JSON string below
json = "{}"
# create an instance of LocalizationParameters from a JSON string
localization_parameters_instance = LocalizationParameters.from_json(json)
# print the JSON string representation of the object
print(LocalizationParameters.to_json())

# convert the object into a dict
localization_parameters_dict = localization_parameters_instance.to_dict()
# create an instance of LocalizationParameters from a dict
localization_parameters_from_dict = LocalizationParameters.from_dict(
    localization_parameters_dict
)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


