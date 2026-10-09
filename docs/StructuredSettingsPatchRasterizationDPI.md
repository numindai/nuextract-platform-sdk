# StructuredSettingsPatchRasterizationDPI

Resolution used to convert formatted documents to images (optional). Use 'null' or an integer between 1 and 600. Numeric strings are also accepted.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------

## Example

```python
from numind.models.structured_settings_patch_rasterization_dpi import (
    StructuredSettingsPatchRasterizationDPI,
)

# TODO update the JSON string below
json = "{}"
# create an instance of StructuredSettingsPatchRasterizationDPI from a JSON string
structured_settings_patch_rasterization_dpi_instance = (
    StructuredSettingsPatchRasterizationDPI.from_json(json)
)
# print the JSON string representation of the object
print(StructuredSettingsPatchRasterizationDPI.to_json())

# convert the object into a dict
structured_settings_patch_rasterization_dpi_dict = (
    structured_settings_patch_rasterization_dpi_instance.to_dict()
)
# create an instance of StructuredSettingsPatchRasterizationDPI from a dict
structured_settings_patch_rasterization_dpi_from_dict = (
    StructuredSettingsPatchRasterizationDPI.from_dict(
        structured_settings_patch_rasterization_dpi_dict
    )
)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


