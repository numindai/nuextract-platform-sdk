# FixedTokenAmount


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**amount** | **int** |  | 
**type** | **str** |  | 

## Example

```python
from numind.models.fixed_token_amount import FixedTokenAmount

# TODO update the JSON string below
json = "{}"
# create an instance of FixedTokenAmount from a JSON string
fixed_token_amount_instance = FixedTokenAmount.from_json(json)
# print the JSON string representation of the object
print(FixedTokenAmount.to_json())

# convert the object into a dict
fixed_token_amount_dict = fixed_token_amount_instance.to_dict()
# create an instance of FixedTokenAmount from a dict
fixed_token_amount_from_dict = FixedTokenAmount.from_dict(fixed_token_amount_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


