# InformationResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**information** | [**Obj1**](Obj1.md) |  | 
**error** | **str** |  | 
**type** | **str** |  | 

## Example

```python
from numind.openapi_client.models.information_response import InformationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of InformationResponse from a JSON string
information_response_instance = InformationResponse.from_json(json)
# print the JSON string representation of the object
print(InformationResponse.to_json())

# convert the object into a dict
information_response_dict = information_response_instance.to_dict()
# create an instance of InformationResponse from a dict
information_response_from_dict = InformationResponse.from_dict(information_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


