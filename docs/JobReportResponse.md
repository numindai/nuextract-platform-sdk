# JobReportResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**job_id** | **str** | Job that produced this report. | 
**parent_job_id** | **str** | Parent job identifier, for a fan-out child job. | [optional] 
**job_type** | **str** | Job type. | 
**job_index** | **int** | Zero-based position of a fan-out child job. | 
**report** | [**PostProcessingReportResponse**](PostProcessingReportResponse.md) |  | 
**created_at** | **str** | Report creation date. | 
**updated_at** | **str** | Report last update date. | 

## Example

```python
from numind.models.job_report_response import JobReportResponse

# TODO update the JSON string below
json = "{}"
# create an instance of JobReportResponse from a JSON string
job_report_response_instance = JobReportResponse.from_json(json)
# print the JSON string representation of the object
print(JobReportResponse.to_json())

# convert the object into a dict
job_report_response_dict = job_report_response_instance.to_dict()
# create an instance of JobReportResponse from a dict
job_report_response_from_dict = JobReportResponse.from_dict(job_report_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


