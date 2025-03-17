# InvalidSchema


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_schema** | **str** |  | 
**error** | **str** |  | 
**type** | **str** |  | 

## Example

```python
from numind.openapi_client.models.invalid_schema import InvalidSchema

# TODO update the JSON string below
json = "{}"
# create an instance of InvalidSchema from a JSON string
invalid_schema_instance = InvalidSchema.from_json(json)
# print the JSON string representation of the object
print(InvalidSchema.to_json())

# convert the object into a dict
invalid_schema_dict = invalid_schema_instance.to_dict()
# create an instance of InvalidSchema from a dict
invalid_schema_from_dict = InvalidSchema.from_dict(invalid_schema_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


