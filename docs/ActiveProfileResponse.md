# ActiveProfileResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**plan_id** | **str** |  | 
**current_billing_period** | [**BillingPeriod**](BillingPeriod.md) |  | [optional] 
**input_feature_card** | [**FeatureCardResponse**](FeatureCardResponse.md) |  | 
**output_feature_card** | [**FeatureCardResponse**](FeatureCardResponse.md) |  | 
**payment_connected** | **bool** |  | 
**type** | **str** |  | 

## Example

```python
from numind.openapi_client.models.active_profile_response import ActiveProfileResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ActiveProfileResponse from a JSON string
active_profile_response_instance = ActiveProfileResponse.from_json(json)
# print the JSON string representation of the object
print(ActiveProfileResponse.to_json())

# convert the object into a dict
active_profile_response_dict = active_profile_response_instance.to_dict()
# create an instance of ActiveProfileResponse from a dict
active_profile_response_from_dict = ActiveProfileResponse.from_dict(active_profile_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


