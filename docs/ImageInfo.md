# ImageInfo


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**document_id** | **str** | Unique document identifier. | 
**file_id** | **str** | Unique file identifier of the file used to generate this document. | 
**file_name** | **str** | Filename of the initial file. | 
**possible_transformations** | **List[str]** | Possible transformations that can be done with this document. | [optional] 
**dpi** | **int** | Resolution used to convert formatted documents (PDFs, etc.) to images, in dot per inch. | [optional] 
**type** | **str** |  | 

## Example

```python
from numind.openapi_client.models.image_info import ImageInfo

# TODO update the JSON string below
json = "{}"
# create an instance of ImageInfo from a JSON string
image_info_instance = ImageInfo.from_json(json)
# print the JSON string representation of the object
print(ImageInfo.to_json())

# convert the object into a dict
image_info_dict = image_info_instance.to_dict()
# create an instance of ImageInfo from a dict
image_info_from_dict = ImageInfo.from_dict(image_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


