# UsageResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**period** | [**DateRange**](DateRange.md) |  | 
**template_usage** | [**UsageItemResponse**](UsageItemResponse.md) | Template extraction usage | 
**structured_usage** | [**UsageItemResponse**](UsageItemResponse.md) | Structured data extraction usage | 
**content_usage** | [**UsageItemResponse**](UsageItemResponse.md) | Content extraction usage | 

## Example

```python
from numind.models.usage_response import UsageResponse

# TODO update the JSON string below
json = "{}"
# create an instance of UsageResponse from a JSON string
usage_response_instance = UsageResponse.from_json(json)
# print the JSON string representation of the object
print(UsageResponse.to_json())

# convert the object into a dict
usage_response_dict = usage_response_instance.to_dict()
# create an instance of UsageResponse from a dict
usage_response_from_dict = UsageResponse.from_dict(usage_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


