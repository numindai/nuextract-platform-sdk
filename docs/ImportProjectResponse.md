# ImportProjectResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project** | [**StructuredProjectResponse**](StructuredProjectResponse.md) |  | 
**type** | **str** |  | 

## Example

```python
from numind.models.import_project_response import ImportProjectResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ImportProjectResponse from a JSON string
import_project_response_instance = ImportProjectResponse.from_json(json)
# print the JSON string representation of the object
print(ImportProjectResponse.to_json())

# convert the object into a dict
import_project_response_dict = import_project_response_instance.to_dict()
# create an instance of ImportProjectResponse from a dict
import_project_response_from_dict = ImportProjectResponse.from_dict(import_project_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


