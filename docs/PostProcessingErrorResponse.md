# PostProcessingErrorResponse

Post-processing error, if one occurred.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Machine-readable inference error code. | 
**message** | **str** | Human-readable error description. | 
**path** | **str** | Path of the invalid value, if applicable. | [optional] 
**before** | **str** | Value before post-processing, if available. | [optional] 
**details** | **Dict[str, str]** | Additional error details. | 

## Example

```python
from numind.models.post_processing_error_response import PostProcessingErrorResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PostProcessingErrorResponse from a JSON string
post_processing_error_response_instance = PostProcessingErrorResponse.from_json(json)
# print the JSON string representation of the object
print(PostProcessingErrorResponse.to_json())

# convert the object into a dict
post_processing_error_response_dict = post_processing_error_response_instance.to_dict()
# create an instance of PostProcessingErrorResponse from a dict
post_processing_error_response_from_dict = PostProcessingErrorResponse.from_dict(
    post_processing_error_response_dict
)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


