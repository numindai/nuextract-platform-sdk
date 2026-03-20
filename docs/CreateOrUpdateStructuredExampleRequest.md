# CreateOrUpdateStructuredExampleRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**document_id** | **str** | Unique document identifier. | 
**result** | **object** | Expected inference result. | 

## Example

```python
from numind.models.create_or_update_structured_example_request import CreateOrUpdateStructuredExampleRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateOrUpdateStructuredExampleRequest from a JSON string
create_or_update_structured_example_request_instance = CreateOrUpdateStructuredExampleRequest.from_json(json)
# print the JSON string representation of the object
print(CreateOrUpdateStructuredExampleRequest.to_json())

# convert the object into a dict
create_or_update_structured_example_request_dict = create_or_update_structured_example_request_instance.to_dict()
# create an instance of CreateOrUpdateStructuredExampleRequest from a dict
create_or_update_structured_example_request_from_dict = CreateOrUpdateStructuredExampleRequest.from_dict(create_or_update_structured_example_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


