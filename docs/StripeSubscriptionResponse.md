# StripeSubscriptionResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | **str** |  | 

## Example

```python
from numind.openapi_client.models.stripe_subscription_response import StripeSubscriptionResponse

# TODO update the JSON string below
json = "{}"
# create an instance of StripeSubscriptionResponse from a JSON string
stripe_subscription_response_instance = StripeSubscriptionResponse.from_json(json)
# print the JSON string representation of the object
print(StripeSubscriptionResponse.to_json())

# convert the object into a dict
stripe_subscription_response_dict = stripe_subscription_response_instance.to_dict()
# create an instance of StripeSubscriptionResponse from a dict
stripe_subscription_response_from_dict = StripeSubscriptionResponse.from_dict(stripe_subscription_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


