# PlaygroundItemResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique playground item identifier. | 
**project_id** | **str** | Unique project identifier. | 
**owner_user** | **str** | Playground item owner. | 
**document_info** | [**DocumentInfo**](DocumentInfo.md) | Basic information on the document used for inference. | 
**result** | [**InformationResponse**](InformationResponse.md) | Inference result. | 
**created_at** | **str** | Playground item creation date. | 
**updated_at** | **str** | Playground item last update date. | 
**total_tokens** | **int** | Total number of tokens used for inference (input + output). | [optional] 
**completion_tokens** | **int** | Completion tokens used for inference (output). | [optional] 
**prompt_tokens** | **int** | Prompt tokens used for inference (input). | [optional] 

## Example

```python
from numind.models.playground_item_response import PlaygroundItemResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PlaygroundItemResponse from a JSON string
playground_item_response_instance = PlaygroundItemResponse.from_json(json)
# print the JSON string representation of the object
print(PlaygroundItemResponse.to_json())

# convert the object into a dict
playground_item_response_dict = playground_item_response_instance.to_dict()
# create an instance of PlaygroundItemResponse from a dict
playground_item_response_from_dict = PlaygroundItemResponse.from_dict(playground_item_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


