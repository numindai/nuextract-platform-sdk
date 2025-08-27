# StripeSubscriptionRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**redirect_url** | **str** |  | 

## Example

```python
from numind.openapi_client.models.stripe_subscription_request import StripeSubscriptionRequest

# TODO update the JSON string below
json = "{}"
# create an instance of StripeSubscriptionRequest from a JSON string
stripe_subscription_request_instance = StripeSubscriptionRequest.from_json(json)
# print the JSON string representation of the object
print(StripeSubscriptionRequest.to_json())

# convert the object into a dict
stripe_subscription_request_dict = stripe_subscription_request_instance.to_dict()
# create an instance of StripeSubscriptionRequest from a dict
stripe_subscription_request_from_dict = StripeSubscriptionRequest.from_dict(stripe_subscription_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


