# DocumentResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**doc_info** | [**DocumentInfo**](DocumentInfo.md) | Basic document information. | 
**owner_user** | **str** | Document owner. | 
**owner_organization** | **str** | Document owning organization (if any). | [optional] 
**original_content_type** | **str** | Mime type of the original file. | 
**content_type** | **str** | Mime type of the converted document. | 
**created_at** | **str** | Document creation date. | 
**updated_at** | **str** | Document last update date. | 
**shared** | **bool** | The shared state of the document. | 

## Example

```python
from numind.openapi_client.models.document_response import DocumentResponse

# TODO update the JSON string below
json = "{}"
# create an instance of DocumentResponse from a JSON string
document_response_instance = DocumentResponse.from_json(json)
# print the JSON string representation of the object
print(DocumentResponse.to_json())

# convert the object into a dict
document_response_dict = document_response_instance.to_dict()
# create an instance of DocumentResponse from a dict
document_response_from_dict = DocumentResponse.from_dict(document_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


