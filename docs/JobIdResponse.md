# JobIdResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**job_id** | **str** | Unique job identifier. | 

## Example

```python
from numind.models.job_id_response import JobIdResponse

# TODO update the JSON string below
json = "{}"
# create an instance of JobIdResponse from a JSON string
job_id_response_instance = JobIdResponse.from_json(json)
# print the JSON string representation of the object
print(JobIdResponse.to_json())

# convert the object into a dict
job_id_response_dict = job_id_response_instance.to_dict()
# create an instance of JobIdResponse from a dict
job_id_response_from_dict = JobIdResponse.from_dict(job_id_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


