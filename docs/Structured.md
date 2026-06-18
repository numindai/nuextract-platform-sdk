# Structured


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project** | [**StructuredProjectResponse**](StructuredProjectResponse.md) |  | 
**type** | **str** |  | 

## Example

```python
from numind.models.structured import Structured

# TODO update the JSON string below
json = "{}"
# create an instance of Structured from a JSON string
structured_instance = Structured.from_json(json)
# print the JSON string representation of the object
print(Structured.to_json())

# convert the object into a dict
structured_dict = structured_instance.to_dict()
# create an instance of Structured from a dict
structured_from_dict = Structured.from_dict(structured_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


