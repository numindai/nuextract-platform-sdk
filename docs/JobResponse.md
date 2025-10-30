# JobResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique job identifier. | 
**job_type** | **str** | Job type. | 
**status** | **str** | Job status. | 
**owner_user** | **str** | Job owner. | 
**owner_organization** | **str** | Job owning organization (if any). | [optional] 
**input_data** | **str** | Job input data. | 
**output_data** | **str** | Job output data (if completed). | [optional] 
**error_message** | **str** | Error message (if failed). | [optional] 
**error_code** | **str** | Error code (if failed). | [optional] 
**started_at** | **str** | Job start time. | 
**completed_at** | **str** | Job completion time (if completed). | [optional] 
**created_at** | **str** | Job creation date. | 
**updated_at** | **str** | Job last update date. | 

## Example

```python
from numind.models.job_response import JobResponse

# TODO update the JSON string below
json = "{}"
# create an instance of JobResponse from a JSON string
job_response_instance = JobResponse.from_json(json)
# print the JSON string representation of the object
print(JobResponse.to_json())

# convert the object into a dict
job_response_dict = job_response_instance.to_dict()
# create an instance of JobResponse from a dict
job_response_from_dict = JobResponse.from_dict(job_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


