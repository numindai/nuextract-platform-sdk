# BillingPeriod


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_from** | **str** |  | 
**to** | **str** |  | 

## Example

```python
from numind.openapi_client.models.billing_period import BillingPeriod

# TODO update the JSON string below
json = "{}"
# create an instance of BillingPeriod from a JSON string
billing_period_instance = BillingPeriod.from_json(json)
# print the JSON string representation of the object
print(BillingPeriod.to_json())

# convert the object into a dict
billing_period_dict = billing_period_instance.to_dict()
# create an instance of BillingPeriod from a dict
billing_period_from_dict = BillingPeriod.from_dict(billing_period_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


