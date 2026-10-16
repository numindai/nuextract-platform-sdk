# ContentProjectSettingsResponseRasterizationDPI

Resolution used to convert formatted documents (PDFs, etc.) to images, in dots per inch. Use 'automatic' or an integer between 1 and 600. Numeric strings are also accepted. Ignored for files that are already images or text.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------

## Example

```python
from numind.models.content_project_settings_response_rasterization_dpi import (
    ContentProjectSettingsResponseRasterizationDPI,
)

# TODO update the JSON string below
json = "{}"
# create an instance of ContentProjectSettingsResponseRasterizationDPI from a JSON string
content_project_settings_response_rasterization_dpi_instance = (
    ContentProjectSettingsResponseRasterizationDPI.from_json(json)
)
# print the JSON string representation of the object
print(ContentProjectSettingsResponseRasterizationDPI.to_json())

# convert the object into a dict
content_project_settings_response_rasterization_dpi_dict = (
    content_project_settings_response_rasterization_dpi_instance.to_dict()
)
# create an instance of ContentProjectSettingsResponseRasterizationDPI from a dict
content_project_settings_response_rasterization_dpi_from_dict = (
    ContentProjectSettingsResponseRasterizationDPI.from_dict(
        content_project_settings_response_rasterization_dpi_dict
    )
)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


