# CreateOrUpdatePlaygroundItemRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**owner_organization** | **str** | Project owning organization (optional). | [optional] 
**document_id** | **str** | Unique document identifier. | 
**result** | **object** | Inference result. | 
**total_tokens** | **int** | Total number of tokens used for inference (input + output). | [optional] 
**output_tokens** | **int** | Output tokens used for inference. | [optional] 
**input_tokens** | **int** | Input tokens used for inference. | [optional] 

## Example

```python
from numind.models.create_or_update_playground_item_request import CreateOrUpdatePlaygroundItemRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateOrUpdatePlaygroundItemRequest from a JSON string
create_or_update_playground_item_request_instance = CreateOrUpdatePlaygroundItemRequest.from_json(json)
# print the JSON string representation of the object
print(CreateOrUpdatePlaygroundItemRequest.to_json())

# convert the object into a dict
create_or_update_playground_item_request_dict = create_or_update_playground_item_request_instance.to_dict()
# create an instance of CreateOrUpdatePlaygroundItemRequest from a dict
create_or_update_playground_item_request_from_dict = CreateOrUpdatePlaygroundItemRequest.from_dict(create_or_update_playground_item_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


