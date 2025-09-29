# FeatureCardResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**usage** | **int** |  | 
**free_tokens** | **int** |  | 
**price** | **float** |  | 

## Example

```python
from numind.openapi_client.models.feature_card_response import FeatureCardResponse

# TODO update the JSON string below
json = "{}"
# create an instance of FeatureCardResponse from a JSON string
feature_card_response_instance = FeatureCardResponse.from_json(json)
# print the JSON string representation of the object
print(FeatureCardResponse.to_json())

# convert the object into a dict
feature_card_response_dict = feature_card_response_instance.to_dict()
# create an instance of FeatureCardResponse from a dict
feature_card_response_from_dict = FeatureCardResponse.from_dict(feature_card_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


