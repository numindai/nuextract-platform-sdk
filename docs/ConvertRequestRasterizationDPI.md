# ConvertRequestRasterizationDPI

Resolution used to convert formatted documents (PDFs, etc.) to images, in dot per inch.   Use 'null' or an integer between 1 and 600. Numeric strings are also accepted.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------

## Example

```python
from numind.models.convert_request_rasterization_dpi import (
    ConvertRequestRasterizationDPI,
)

# TODO update the JSON string below
json = "{}"
# create an instance of ConvertRequestRasterizationDPI from a JSON string
convert_request_rasterization_dpi_instance = ConvertRequestRasterizationDPI.from_json(
    json
)
# print the JSON string representation of the object
print(ConvertRequestRasterizationDPI.to_json())

# convert the object into a dict
convert_request_rasterization_dpi_dict = (
    convert_request_rasterization_dpi_instance.to_dict()
)
# create an instance of ConvertRequestRasterizationDPI from a dict
convert_request_rasterization_dpi_from_dict = ConvertRequestRasterizationDPI.from_dict(
    convert_request_rasterization_dpi_dict
)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


