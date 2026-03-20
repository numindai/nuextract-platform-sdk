# PaginatedResponseStructuredExampleResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total_count** | **int** | Total number of items available. | 
**skip** | **int** | Number of items skipped. | 
**per_page** | **int** | Number of items per page. | 
**items** | [**List[StructuredExampleResponse]**](StructuredExampleResponse.md) | List of items. | [optional] 

## Example

```python
from numind.models.paginated_response_structured_example_response import PaginatedResponseStructuredExampleResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PaginatedResponseStructuredExampleResponse from a JSON string
paginated_response_structured_example_response_instance = PaginatedResponseStructuredExampleResponse.from_json(json)
# print the JSON string representation of the object
print(PaginatedResponseStructuredExampleResponse.to_json())

# convert the object into a dict
paginated_response_structured_example_response_dict = paginated_response_structured_example_response_instance.to_dict()
# create an instance of PaginatedResponseStructuredExampleResponse from a dict
paginated_response_structured_example_response_from_dict = PaginatedResponseStructuredExampleResponse.from_dict(paginated_response_structured_example_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


