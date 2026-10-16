# PostProcessingReportResponse

Inference post-processing details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**repairs** | [**List[PostProcessingRepairResponse]**](PostProcessingRepairResponse.md) | Repairs applied during post-processing. | [optional] 
**error** | [**PostProcessingErrorResponse**](PostProcessingErrorResponse.md) |  | [optional] 
**used_fallback** | **bool** | Whether fallback output was used. | 

## Example

```python
from numind.models.post_processing_report_response import PostProcessingReportResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PostProcessingReportResponse from a JSON string
post_processing_report_response_instance = PostProcessingReportResponse.from_json(json)
# print the JSON string representation of the object
print(PostProcessingReportResponse.to_json())

# convert the object into a dict
post_processing_report_response_dict = (
    post_processing_report_response_instance.to_dict()
)
# create an instance of PostProcessingReportResponse from a dict
post_processing_report_response_from_dict = PostProcessingReportResponse.from_dict(
    post_processing_report_response_dict
)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


