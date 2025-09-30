# ConvertRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**rasterization_dpi** | **int** | Resolution used to convert formatted documents (PDFs, etc.) to images, in dot per inch.   Ranges between 1 and 300. | 

## Example

```python
from numind.models.convert_request import ConvertRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ConvertRequest from a JSON string
convert_request_instance = ConvertRequest.from_json(json)
# print the JSON string representation of the object
print(ConvertRequest.to_json())

# convert the object into a dict
convert_request_dict = convert_request_instance.to_dict()
# create an instance of ConvertRequest from a dict
convert_request_from_dict = ConvertRequest.from_dict(convert_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


