# SchemaNode


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_schema** | [**SchemaNode**](SchemaNode.md) |  | 
**values** | **List[str]** |  | [optional] 
**schemas** | [**Dict[str, SchemaNode]**](SchemaNode.md) |  | 

## Example

```python
from numind.openapi_client.models.schema_node import SchemaNode

# TODO update the JSON string below
json = "{}"
# create an instance of SchemaNode from a JSON string
schema_node_instance = SchemaNode.from_json(json)
# print the JSON string representation of the object
print(SchemaNode.to_json())

# convert the object into a dict
schema_node_dict = schema_node_instance.to_dict()
# create an instance of SchemaNode from a dict
schema_node_from_dict = SchemaNode.from_dict(schema_node_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


