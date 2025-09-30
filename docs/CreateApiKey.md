# CreateApiKey


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**maybe_orga** | **str** |  | [optional] 
**name** | **str** |  | 

## Example

```python
from numind.models.create_api_key import CreateApiKey

# TODO update the JSON string below
json = "{}"
# create an instance of CreateApiKey from a JSON string
create_api_key_instance = CreateApiKey.from_json(json)
# print the JSON string representation of the object
print(CreateApiKey.to_json())

# convert the object into a dict
create_api_key_dict = create_api_key_instance.to_dict()
# create an instance of CreateApiKey from a dict
create_api_key_from_dict = CreateApiKey.from_dict(create_api_key_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


