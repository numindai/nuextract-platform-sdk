# DiscardedLocalization


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | 
**reason** | **str** |  | 
**value** | **str** | JSON preview of the rejected value, capped at 80 characters; absent for missing fields. Parsed boxes use {page, bbox} with a one-based document page number and normalized coordinates. For invalid_page, the page is outside the document and retains the one-based model page number. Other rejected values, including unexpected fields, retain raw model JSON. | [optional] 

## Example

```python
from numind.models.discarded_localization import DiscardedLocalization

# TODO update the JSON string below
json = "{}"
# create an instance of DiscardedLocalization from a JSON string
discarded_localization_instance = DiscardedLocalization.from_json(json)
# print the JSON string representation of the object
print(DiscardedLocalization.to_json())

# convert the object into a dict
discarded_localization_dict = discarded_localization_instance.to_dict()
# create an instance of DiscardedLocalization from a dict
discarded_localization_from_dict = DiscardedLocalization.from_dict(
    discarded_localization_dict
)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


