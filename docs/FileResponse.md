# FileResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**file_id** | **str** | Unique file identifier. | 
**file_name** | **str** | Filename of the initial file. | [optional] 
**owner_user** | **str** | File owner. | 
**owner_organization** | **str** | File owning organization (if any). | [optional] 
**content_type** | **str** | Mime type of the file. | 
**created_at** | **str** | File creation date. | 

## Example

```python
from numind.openapi_client.models.file_response import FileResponse

# TODO update the JSON string below
json = "{}"
# create an instance of FileResponse from a JSON string
file_response_instance = FileResponse.from_json(json)
# print the JSON string representation of the object
print(FileResponse.to_json())

# convert the object into a dict
file_response_dict = file_response_instance.to_dict()
# create an instance of FileResponse from a dict
file_response_from_dict = FileResponse.from_dict(file_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


