# Obj


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**schemas** | [**Dict[str, SchemaNode]**](SchemaNode.md) |  | 

## Example

```python
from numind.openapi_client.models.obj import Obj

# TODO update the JSON string below
json = "{}"
# create an instance of Obj from a JSON string
obj_instance = Obj.from_json(json)
# print the JSON string representation of the object
print(Obj.to_json())

# convert the object into a dict
obj_dict = obj_instance.to_dict()
# create an instance of Obj from a dict
obj_from_dict = Obj.from_dict(obj_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


