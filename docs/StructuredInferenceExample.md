# StructuredInferenceExample


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**example_id** | **str** | Unique example identifier. | 
**example_name** | **str** | Example name (filename if any, or the beginning of the text). | 
**tokens_count** | **int** | Estimated tokens count of the example. | 
**similarity** | **float** | Similarity between the document and the example. | [optional] 

## Example

```python
from numind.models.structured_inference_example import StructuredInferenceExample

# TODO update the JSON string below
json = "{}"
# create an instance of StructuredInferenceExample from a JSON string
structured_inference_example_instance = StructuredInferenceExample.from_json(json)
# print the JSON string representation of the object
print(StructuredInferenceExample.to_json())

# convert the object into a dict
structured_inference_example_dict = structured_inference_example_instance.to_dict()
# create an instance of StructuredInferenceExample from a dict
structured_inference_example_from_dict = StructuredInferenceExample.from_dict(structured_inference_example_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


