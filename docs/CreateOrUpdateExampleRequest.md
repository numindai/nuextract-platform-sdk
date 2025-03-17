# CreateOrUpdateExampleRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**document_id** | **str** |  | 
**result** | [**Obj1**](Obj1.md) |  | 

## Example

```python
from numind.openapi_client.models.create_or_update_example_request import CreateOrUpdateExampleRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateOrUpdateExampleRequest from a JSON string
create_or_update_example_request_instance = CreateOrUpdateExampleRequest.from_json(json)
# print the JSON string representation of the object
print(CreateOrUpdateExampleRequest.to_json())

# convert the object into a dict
create_or_update_example_request_dict = create_or_update_example_request_instance.to_dict()
# create an instance of CreateOrUpdateExampleRequest from a dict
create_or_update_example_request_from_dict = CreateOrUpdateExampleRequest.from_dict(create_or_update_example_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


