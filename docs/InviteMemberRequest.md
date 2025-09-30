# InviteMemberRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**email** | **str** | email of the user to invite | 

## Example

```python
from numind.models.invite_member_request import InviteMemberRequest

# TODO update the JSON string below
json = "{}"
# create an instance of InviteMemberRequest from a JSON string
invite_member_request_instance = InviteMemberRequest.from_json(json)
# print the JSON string representation of the object
print(InviteMemberRequest.to_json())

# convert the object into a dict
invite_member_request_dict = invite_member_request_instance.to_dict()
# create an instance of InviteMemberRequest from a dict
invite_member_request_from_dict = InviteMemberRequest.from_dict(invite_member_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


