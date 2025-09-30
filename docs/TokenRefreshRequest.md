# TokenRefreshRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**token** | **str** |  | 
**type** | **str** |  | 

## Example

```python
from numind.models.token_refresh_request import TokenRefreshRequest

# TODO update the JSON string below
json = "{}"
# create an instance of TokenRefreshRequest from a JSON string
token_refresh_request_instance = TokenRefreshRequest.from_json(json)
# print the JSON string representation of the object
print(TokenRefreshRequest.to_json())

# convert the object into a dict
token_refresh_request_dict = token_refresh_request_instance.to_dict()
# create an instance of TokenRefreshRequest from a dict
token_refresh_request_from_dict = TokenRefreshRequest.from_dict(token_refresh_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


