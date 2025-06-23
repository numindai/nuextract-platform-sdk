# UpdateProjectTemplateRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**template** | **object** | Extraction template (NuExtract format). | 

## Example

```python
from numind.openapi_client.models.update_project_template_request import UpdateProjectTemplateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateProjectTemplateRequest from a JSON string
update_project_template_request_instance = UpdateProjectTemplateRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateProjectTemplateRequest.to_json())

# convert the object into a dict
update_project_template_request_dict = update_project_template_request_instance.to_dict()
# create an instance of UpdateProjectTemplateRequest from a dict
update_project_template_request_from_dict = UpdateProjectTemplateRequest.from_dict(update_project_template_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


