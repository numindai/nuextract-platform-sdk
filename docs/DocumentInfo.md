# DocumentInfo


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**document_id** | **str** | Unique document identifier. | 
**file_id** | **str** | Unique file identifier of the file used to generate this document. | 
**file_name** | **str** | Filename of the initial file if any.     **None** for text input. | 
**possible_transformations** | **List[str]** | Possible transformations that can be done with this document. | [optional] 
**dpi** | **int** | Resolution used to convert formatted documents (PDFs, etc.) to images, in dot per inch. | [optional] 
**type** | **str** |  | 
**text** | **str** | The text content of the document. | 

## Example

```python
from numind.openapi_client.models.document_info import DocumentInfo

# TODO update the JSON string below
json = "{}"
# create an instance of DocumentInfo from a JSON string
document_info_instance = DocumentInfo.from_json(json)
# print the JSON string representation of the object
print(DocumentInfo.to_json())

# convert the object into a dict
document_info_dict = document_info_instance.to_dict()
# create an instance of DocumentInfo from a dict
document_info_from_dict = DocumentInfo.from_dict(document_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


