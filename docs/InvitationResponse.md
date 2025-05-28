# InvitationResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | identifier of this invitation | 
**email** | **str** | email of the person invited | 
**roles** | **List[str]** | roles associated with this invitation | [optional] 

## Example

```python
from numind.openapi_client.models.invitation_response import InvitationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of InvitationResponse from a JSON string
invitation_response_instance = InvitationResponse.from_json(json)
# print the JSON string representation of the object
print(InvitationResponse.to_json())

# convert the object into a dict
invitation_response_dict = invitation_response_instance.to_dict()
# create an instance of InvitationResponse from a dict
invitation_response_from_dict = InvitationResponse.from_dict(invitation_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


