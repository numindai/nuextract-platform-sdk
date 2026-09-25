# UpdateStructuredProjectSettingsRequestRasterizationDPI

Resolution used to convert formatted documents to images (optional). Use 'null' or an integer between 1 and 600. Numeric strings are also accepted.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------

## Example

```python
from numind.models.update_structured_project_settings_request_rasterization_dpi import (
    UpdateStructuredProjectSettingsRequestRasterizationDPI,
)

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateStructuredProjectSettingsRequestRasterizationDPI from a JSON string
update_structured_project_settings_request_rasterization_dpi_instance = (
    UpdateStructuredProjectSettingsRequestRasterizationDPI.from_json(json)
)
# print the JSON string representation of the object
print(UpdateStructuredProjectSettingsRequestRasterizationDPI.to_json())

# convert the object into a dict
update_structured_project_settings_request_rasterization_dpi_dict = (
    update_structured_project_settings_request_rasterization_dpi_instance.to_dict()
)
# create an instance of UpdateStructuredProjectSettingsRequestRasterizationDPI from a dict
update_structured_project_settings_request_rasterization_dpi_from_dict = (
    UpdateStructuredProjectSettingsRequestRasterizationDPI.from_dict(
        update_structured_project_settings_request_rasterization_dpi_dict
    )
)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


