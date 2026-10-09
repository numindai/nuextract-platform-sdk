# ContentSettingsPatchRasterizationDPI

Resolution used to convert formatted documents to images (optional).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------

## Example

```python
from numind.models.content_settings_patch_rasterization_dpi import (
    ContentSettingsPatchRasterizationDPI,
)

# TODO update the JSON string below
json = "{}"
# create an instance of ContentSettingsPatchRasterizationDPI from a JSON string
content_settings_patch_rasterization_dpi_instance = (
    ContentSettingsPatchRasterizationDPI.from_json(json)
)
# print the JSON string representation of the object
print(ContentSettingsPatchRasterizationDPI.to_json())

# convert the object into a dict
content_settings_patch_rasterization_dpi_dict = (
    content_settings_patch_rasterization_dpi_instance.to_dict()
)
# create an instance of ContentSettingsPatchRasterizationDPI from a dict
content_settings_patch_rasterization_dpi_from_dict = (
    ContentSettingsPatchRasterizationDPI.from_dict(
        content_settings_patch_rasterization_dpi_dict
    )
)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


