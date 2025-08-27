# BillingProfileResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**plan_id** | **str** |  | 
**usage** | **int** |  | 
**balance** | **int** |  | 
**overage** | **int** |  | 
**subscriptions** | [**List[Subscription]**](Subscription.md) |  | [optional] 
**can_display_invoices** | **bool** |  | 

## Example

```python
from numind.openapi_client.models.billing_profile_response import BillingProfileResponse

# TODO update the JSON string below
json = "{}"
# create an instance of BillingProfileResponse from a JSON string
billing_profile_response_instance = BillingProfileResponse.from_json(json)
# print the JSON string representation of the object
print(BillingProfileResponse.to_json())

# convert the object into a dict
billing_profile_response_dict = billing_profile_response_instance.to_dict()
# create an instance of BillingProfileResponse from a dict
billing_profile_response_from_dict = BillingProfileResponse.from_dict(billing_profile_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


