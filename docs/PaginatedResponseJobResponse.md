# PaginatedResponseJobResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total_count** | **int** | Total number of items available. | 
**skip** | **int** | Number of items skipped. | 
**per_page** | **int** | Number of items per page. | 
**items** | [**List[JobResponse]**](JobResponse.md) | List of items. | [optional] 

## Example

```python
from numind.models.paginated_response_job_response import PaginatedResponseJobResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PaginatedResponseJobResponse from a JSON string
paginated_response_job_response_instance = PaginatedResponseJobResponse.from_json(json)
# print the JSON string representation of the object
print(PaginatedResponseJobResponse.to_json())

# convert the object into a dict
paginated_response_job_response_dict = paginated_response_job_response_instance.to_dict()
# create an instance of PaginatedResponseJobResponse from a dict
paginated_response_job_response_from_dict = PaginatedResponseJobResponse.from_dict(paginated_response_job_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


