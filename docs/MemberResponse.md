# MemberResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | identifier of the user | 
**display_name** | **str** | name of the user | 
**email** | **str** | email of the user | 
**roles** | **List[str]** | roles of the user | [optional] 

## Example

```python
from numind.models.member_response import MemberResponse

# TODO update the JSON string below
json = "{}"
# create an instance of MemberResponse from a JSON string
member_response_instance = MemberResponse.from_json(json)
# print the JSON string representation of the object
print(MemberResponse.to_json())

# convert the object into a dict
member_response_dict = member_response_instance.to_dict()
# create an instance of MemberResponse from a dict
member_response_from_dict = MemberResponse.from_dict(member_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


