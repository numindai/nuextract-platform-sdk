# InferenceExample


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**example_id** | **str** | Unique example identifier. | 
**example_name** | **str** | Example name (filename if any, or the beginning of the text). | 
**tokens_count** | **int** | Tokens count of the example. | 
**similarity** | **float** | Similarity between the document and the example. | 

## Example

```python
from numind.models.inference_example import InferenceExample

# TODO update the JSON string below
json = "{}"
# create an instance of InferenceExample from a JSON string
inference_example_instance = InferenceExample.from_json(json)
# print the JSON string representation of the object
print(InferenceExample.to_json())

# convert the object into a dict
inference_example_dict = inference_example_instance.to_dict()
# create an instance of InferenceExample from a dict
inference_example_from_dict = InferenceExample.from_dict(inference_example_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


