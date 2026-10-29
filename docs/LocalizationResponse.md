# LocalizationResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**localization** | [**Dict[str, Optional[LocalizationValue]]**](LocalizationValue.md) | Localization groups. Each field contains a list of boxes with a one-based document page number and a bbox array of normalized [x1, y1, x2, y2] coordinates (0–1). | 
**discarded_localization_count** | **int** | Number of localization validation errors. | 
**discarded_localizations** | [**List[DiscardedLocalization]**](DiscardedLocalization.md) | Localization validation errors, including invalid boxes and missing or unexpected fields. | [optional] 
**diagnostics** | **List[str]** | Diagnostics explaining why results are partial. | [optional] 
**input_tokens** | **int** | Input tokens used for localization inference, when available. | [optional] 
**output_tokens** | **int** | Output tokens used for localization inference, when available. | [optional] 
**raw_model_output** | **str** | Exact model content before localization post-processing. | 

## Example

```python
from numind.models.localization_response import LocalizationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of LocalizationResponse from a JSON string
localization_response_instance = LocalizationResponse.from_json(json)
# print the JSON string representation of the object
print(LocalizationResponse.to_json())

# convert the object into a dict
localization_response_dict = localization_response_instance.to_dict()
# create an instance of LocalizationResponse from a dict
localization_response_from_dict = LocalizationResponse.from_dict(
    localization_response_dict
)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


