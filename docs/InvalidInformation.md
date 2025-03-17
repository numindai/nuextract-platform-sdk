# InvalidInformation


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**information** | **str** |  | 
**error** | **str** |  | 
**type** | **str** |  | 

## Example

```python
from numind.openapi_client.models.invalid_information import InvalidInformation

# TODO update the JSON string below
json = "{}"
# create an instance of InvalidInformation from a JSON string
invalid_information_instance = InvalidInformation.from_json(json)
# print the JSON string representation of the object
print(InvalidInformation.to_json())

# convert the object into a dict
invalid_information_dict = invalid_information_instance.to_dict()
# create an instance of InvalidInformation from a dict
invalid_information_from_dict = InvalidInformation.from_dict(invalid_information_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


