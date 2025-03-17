# TokenCodeRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** |  | 
**redirect_uri** | **str** |  | 
**type** | **str** |  | 

## Example

```python
from numind.openapi_client.models.token_code_request import TokenCodeRequest

# TODO update the JSON string below
json = "{}"
# create an instance of TokenCodeRequest from a JSON string
token_code_request_instance = TokenCodeRequest.from_json(json)
# print the JSON string representation of the object
print(TokenCodeRequest.to_json())

# convert the object into a dict
token_code_request_dict = token_code_request_instance.to_dict()
# create an instance of TokenCodeRequest from a dict
token_code_request_from_dict = TokenCodeRequest.from_dict(token_code_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


