# UsageItemResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**api_usage** | [**UsageMetricsResponse**](UsageMetricsResponse.md) | API usage (billable) | 
**interface_usage** | [**UsageMetricsResponse**](UsageMetricsResponse.md) | Interface usage (non-billable) | 

## Example

```python
from numind.models.usage_item_response import UsageItemResponse

# TODO update the JSON string below
json = "{}"
# create an instance of UsageItemResponse from a JSON string
usage_item_response_instance = UsageItemResponse.from_json(json)
# print the JSON string representation of the object
print(UsageItemResponse.to_json())

# convert the object into a dict
usage_item_response_dict = usage_item_response_instance.to_dict()
# create an instance of UsageItemResponse from a dict
usage_item_response_from_dict = UsageItemResponse.from_dict(usage_item_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


