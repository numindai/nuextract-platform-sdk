# MarkdownPlaygroundItemResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique playground item identifier. | 
**project_id** | **str** | Unique project identifier (NuMarkdown project). | 
**owner_user** | **str** | Playground item owner. | 
**document_info** | [**DocumentInfo**](DocumentInfo.md) | Basic information on the document used for inference. | 
**result** | **str** | Markdown result. | 
**thinking_trace** | **str** | Thinking/reasoning process. | 
**created_at** | **str** | Playground item creation date. | 
**updated_at** | **str** | Playground item last update date. | 
**total_tokens** | **int** | Total number of tokens used for inference (input + output). | [optional] 
**output_tokens** | **int** | Output tokens used for inference. | [optional] 
**input_tokens** | **int** | Input tokens used for inference. | [optional] 

## Example

```python
from numind.models.markdown_playground_item_response import MarkdownPlaygroundItemResponse

# TODO update the JSON string below
json = "{}"
# create an instance of MarkdownPlaygroundItemResponse from a JSON string
markdown_playground_item_response_instance = MarkdownPlaygroundItemResponse.from_json(json)
# print the JSON string representation of the object
print(MarkdownPlaygroundItemResponse.to_json())

# convert the object into a dict
markdown_playground_item_response_dict = markdown_playground_item_response_instance.to_dict()
# create an instance of MarkdownPlaygroundItemResponse from a dict
markdown_playground_item_response_from_dict = MarkdownPlaygroundItemResponse.from_dict(markdown_playground_item_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


