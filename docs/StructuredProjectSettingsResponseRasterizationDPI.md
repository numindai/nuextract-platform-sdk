# StructuredProjectSettingsResponseRasterizationDPI

Resolution used to convert formatted documents to images: Use 'null' or an integer between 1 and 600.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------

## Example

```python
from numind.models.structured_project_settings_response_rasterization_dpi import (
    StructuredProjectSettingsResponseRasterizationDPI,
)

# TODO update the JSON string below
json = "{}"
# create an instance of StructuredProjectSettingsResponseRasterizationDPI from a JSON string
structured_project_settings_response_rasterization_dpi_instance = (
    StructuredProjectSettingsResponseRasterizationDPI.from_json(json)
)
# print the JSON string representation of the object
print(StructuredProjectSettingsResponseRasterizationDPI.to_json())

# convert the object into a dict
structured_project_settings_response_rasterization_dpi_dict = (
    structured_project_settings_response_rasterization_dpi_instance.to_dict()
)
# create an instance of StructuredProjectSettingsResponseRasterizationDPI from a dict
structured_project_settings_response_rasterization_dpi_from_dict = (
    StructuredProjectSettingsResponseRasterizationDPI.from_dict(
        structured_project_settings_response_rasterization_dpi_dict
    )
)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


