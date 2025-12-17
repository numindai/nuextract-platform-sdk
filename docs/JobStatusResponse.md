# JobStatusResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique job identifier. | 
**job_type** | **str** | Job type. | 
**status** | **str** | Job status. | 
**owner_user** | **str** | Job owner. | 
**owner_organization** | **str** | Job owning organization (if any). | [optional] 
**started_at** | **str** | Job start time. | 
**completed_at** | **str** | Job completion time (if completed). | [optional] 
**created_at** | **str** | Job creation date. | 
**updated_at** | **str** | Job last update date. | 

## Example

```python
from numind.models.job_status_response import JobStatusResponse

# TODO update the JSON string below
json = "{}"
# create an instance of JobStatusResponse from a JSON string
job_status_response_instance = JobStatusResponse.from_json(json)
# print the JSON string representation of the object
print(JobStatusResponse.to_json())

# convert the object into a dict
job_status_response_dict = job_status_response_instance.to_dict()
# create an instance of JobStatusResponse from a dict
job_status_response_from_dict = JobStatusResponse.from_dict(job_status_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


