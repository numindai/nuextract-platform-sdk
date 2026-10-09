# ReferenceProjectResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique project identifier. | 
**name** | **str** | Project name. | 
**description** | **str** | A brief explanation of the project. | 

## Example

```python
from numind.models.reference_project_response import ReferenceProjectResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ReferenceProjectResponse from a JSON string
reference_project_response_instance = ReferenceProjectResponse.from_json(json)
# print the JSON string representation of the object
print(ReferenceProjectResponse.to_json())

# convert the object into a dict
reference_project_response_dict = reference_project_response_instance.to_dict()
# create an instance of ReferenceProjectResponse from a dict
reference_project_response_from_dict = ReferenceProjectResponse.from_dict(
    reference_project_response_dict
)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


