# InfoNode


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**values** | [**List[InfoNode]**](InfoNode.md) |  | [optional] 
**value** | **str** |  | 
**schemas** | [**Dict[str, SchemaNode]**](SchemaNode.md) |  | 

## Example

```python
from numind.openapi_client.models.info_node import InfoNode

# TODO update the JSON string below
json = "{}"
# create an instance of InfoNode from a JSON string
info_node_instance = InfoNode.from_json(json)
# print the JSON string representation of the object
print(InfoNode.to_json())

# convert the object into a dict
info_node_dict = info_node_instance.to_dict()
# create an instance of InfoNode from a dict
info_node_from_dict = InfoNode.from_dict(info_node_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


