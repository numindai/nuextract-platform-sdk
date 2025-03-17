# ExampleResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**project_id** | **str** |  | 
**owner_user** | **str** |  | 
**document_info** | [**DocumentInfo**](DocumentInfo.md) |  | 
**result** | [**InformationResponse**](InformationResponse.md) |  | 
**created_at** | **str** |  | 
**updated_at** | **str** |  | 

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


