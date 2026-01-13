# MarkdownResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**result** | **str** | Result of NuMarkdown model | [optional] 
**thinking_trace** | **str** | Reasoning of NuMarkdown model | [optional] 
**raw_model_output** | **str** | Full inference result as returned by the model | 
**output_tokens** | **int** | Output tokens used for inference. | 
**input_tokens** | **int** | Input tokens used for inference. | 
**total_tokens** | **int** | Total number of tokens used for inference (input + output). | 
**logprobs** | **float** | Logprob of the inference result (sum of logprobs of all tokens). | 
**output_token_probability** | **float** | Geometric mean of the output token probabilities. | 

## Example

```python
from numind.models.markdown_response import MarkdownResponse

# TODO update the JSON string below
json = "{}"
# create an instance of MarkdownResponse from a JSON string
markdown_response_instance = MarkdownResponse.from_json(json)
# print the JSON string representation of the object
print(MarkdownResponse.to_json())

# convert the object into a dict
markdown_response_dict = markdown_response_instance.to_dict()
# create an instance of MarkdownResponse from a dict
markdown_response_from_dict = MarkdownResponse.from_dict(markdown_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


