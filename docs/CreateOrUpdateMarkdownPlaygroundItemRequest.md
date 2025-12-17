# CreateOrUpdateMarkdownPlaygroundItemRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**owner_organization** | **str** | Project owning organization (optional). | [optional] 
**document_id** | **str** | Unique document identifier. | 
**result** | **str** | Markdown result. | 
**thinking_trace** | **str** | Thinking/reasoning process. | 
**total_tokens** | **int** | Total number of tokens used for inference (input + output). | [optional] 
**output_tokens** | **int** | Output tokens used for extraction. | [optional] 
**input_tokens** | **int** | Input tokens used for extraction. | [optional] 

## Example

```python
from numind.models.create_or_update_markdown_playground_item_request import CreateOrUpdateMarkdownPlaygroundItemRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateOrUpdateMarkdownPlaygroundItemRequest from a JSON string
create_or_update_markdown_playground_item_request_instance = CreateOrUpdateMarkdownPlaygroundItemRequest.from_json(json)
# print the JSON string representation of the object
print(CreateOrUpdateMarkdownPlaygroundItemRequest.to_json())

# convert the object into a dict
create_or_update_markdown_playground_item_request_dict = create_or_update_markdown_playground_item_request_instance.to_dict()
# create an instance of CreateOrUpdateMarkdownPlaygroundItemRequest from a dict
create_or_update_markdown_playground_item_request_from_dict = CreateOrUpdateMarkdownPlaygroundItemRequest.from_dict(create_or_update_markdown_playground_item_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


