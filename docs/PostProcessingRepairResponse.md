# PostProcessingRepairResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sequence** | **int** | One-based order in which this repair was applied. | 
**code** | **str** | Repair type. | 
**message** | **str** | Human-readable repair description. | 
**path** | **str** | Path of the repaired value, if applicable. | [optional] 
**before** | **str** | Value before the repair, if available. | [optional] 
**after** | **str** | Value after the repair, if available. | [optional] 
**details** | **Dict[str, str]** | Additional repair details. | 

## Example

```python
from numind.models.post_processing_repair_response import PostProcessingRepairResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PostProcessingRepairResponse from a JSON string
post_processing_repair_response_instance = PostProcessingRepairResponse.from_json(json)
# print the JSON string representation of the object
print(PostProcessingRepairResponse.to_json())

# convert the object into a dict
post_processing_repair_response_dict = (
    post_processing_repair_response_instance.to_dict()
)
# create an instance of PostProcessingRepairResponse from a dict
post_processing_repair_response_from_dict = PostProcessingRepairResponse.from_dict(
    post_processing_repair_response_dict
)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


