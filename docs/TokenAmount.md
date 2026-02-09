# TokenAmount


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**amount** | **int** |  | 
**type** | **str** |  | 

## Example

```python
from numind.models.token_amount import TokenAmount

# TODO update the JSON string below
json = "{}"
# create an instance of TokenAmount from a JSON string
token_amount_instance = TokenAmount.from_json(json)
# print the JSON string representation of the object
print(TokenAmount.to_json())

# convert the object into a dict
token_amount_dict = token_amount_instance.to_dict()
# create an instance of TokenAmount from a dict
token_amount_from_dict = TokenAmount.from_dict(token_amount_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


