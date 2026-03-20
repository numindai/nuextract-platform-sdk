# StructuredExampleResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique example identifier. | 
**project_id** | **str** | Unique project identifier. | 
**owner_user** | **str** | Example owner. | 
**document_info** | [**DocumentInfo**](DocumentInfo.md) | Basic information on the document used to create this example. | 
**result** | [**InformationResponse**](InformationResponse.md) | Expected inference result. | 
**created_at** | **str** | Example creation date. | 
**updated_at** | **str** | Example last update date. | 

## Example

```python
from numind.models.structured_example_response import StructuredExampleResponse

# TODO update the JSON string below
json = "{}"
# create an instance of StructuredExampleResponse from a JSON string
structured_example_response_instance = StructuredExampleResponse.from_json(json)
# print the JSON string representation of the object
print(StructuredExampleResponse.to_json())

# convert the object into a dict
structured_example_response_dict = structured_example_response_instance.to_dict()
# create an instance of StructuredExampleResponse from a dict
structured_example_response_from_dict = StructuredExampleResponse.from_dict(structured_example_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


