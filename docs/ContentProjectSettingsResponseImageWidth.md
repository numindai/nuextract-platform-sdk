# ContentProjectSettingsResponseImageWidth

Original standalone images only (not PDF/TIFF or converted pages). Use automatic for a 1280 px short side, original to preserve the upload, or a positive integer for the upright image width in pixels. Aspect ratio is preserved; upscaling is allowed.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------

## Example

```python
from numind.models.content_project_settings_response_image_width import (
    ContentProjectSettingsResponseImageWidth,
)

# TODO update the JSON string below
json = "{}"
# create an instance of ContentProjectSettingsResponseImageWidth from a JSON string
content_project_settings_response_image_width_instance = (
    ContentProjectSettingsResponseImageWidth.from_json(json)
)
# print the JSON string representation of the object
print(ContentProjectSettingsResponseImageWidth.to_json())

# convert the object into a dict
content_project_settings_response_image_width_dict = (
    content_project_settings_response_image_width_instance.to_dict()
)
# create an instance of ContentProjectSettingsResponseImageWidth from a dict
content_project_settings_response_image_width_from_dict = (
    ContentProjectSettingsResponseImageWidth.from_dict(
        content_project_settings_response_image_width_dict
    )
)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


