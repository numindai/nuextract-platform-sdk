# StripePortalRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**organization_id** | **str** |  | [optional] 
**return_url** | **str** |  | 

## Example

```python
from numind.openapi_client.models.stripe_portal_request import StripePortalRequest

# TODO update the JSON string below
json = "{}"
# create an instance of StripePortalRequest from a JSON string
stripe_portal_request_instance = StripePortalRequest.from_json(json)
# print the JSON string representation of the object
print(StripePortalRequest.to_json())

# convert the object into a dict
stripe_portal_request_dict = stripe_portal_request_instance.to_dict()
# create an instance of StripePortalRequest from a dict
stripe_portal_request_from_dict = StripePortalRequest.from_dict(stripe_portal_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


