# TextInfo


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**document_id** | **str** |  | 
**file_name** | **str** |  | [optional] 
**text** | **str** |  | 
**type** | **str** |  | 

## Example

```python
from numind.openapi_client.models.text_info import TextInfo

# TODO update the JSON string below
json = "{}"
# create an instance of TextInfo from a JSON string
text_info_instance = TextInfo.from_json(json)
# print the JSON string representation of the object
print(TextInfo.to_json())

# convert the object into a dict
text_info_dict = text_info_instance.to_dict()
# create an instance of TextInfo from a dict
text_info_from_dict = TextInfo.from_dict(text_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


