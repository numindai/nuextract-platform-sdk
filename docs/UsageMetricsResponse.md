# UsageMetricsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**inference_count** | **int** | Inference count | 
**input_token_count** | **int** | Input token count | 
**output_token_count** | **int** | Output token count | 

## Example

```python
from numind.models.usage_metrics_response import UsageMetricsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of UsageMetricsResponse from a JSON string
usage_metrics_response_instance = UsageMetricsResponse.from_json(json)
# print the JSON string representation of the object
print(UsageMetricsResponse.to_json())

# convert the object into a dict
usage_metrics_response_dict = usage_metrics_response_instance.to_dict()
# create an instance of UsageMetricsResponse from a dict
usage_metrics_response_from_dict = UsageMetricsResponse.from_dict(usage_metrics_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


