# ExampleResponse


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
from numind.openapi_client.models.example_response import ExampleResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ExampleResponse from a JSON string
example_response_instance = ExampleResponse.from_json(json)
# print the JSON string representation of the object
print(ExampleResponse.to_json())

# convert the object into a dict
example_response_dict = example_response_instance.to_dict()
# create an instance of ExampleResponse from a dict
example_response_from_dict = ExampleResponse.from_dict(example_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


