# NuMind SDK

Python SDK to interact with NuMind's models API: [**NuExtract**](https://nuextract.ai) and [**NuMarkdown**](https://huggingface.co/numind/NuMarkdown-8B-Thinking).

## Installation

```sh
pip install numind
```

## Usage and code examples

### Create a client

You must first get an API key on the [NuExtract platform](https://nuextract.ai/app/user?content=api).

```python
import os

from numind import NuMind

# Create a client object to interact with the API
# Providing the `api_key` is not required if the `NUMIND_API_KEY` environment variable
# is already set.
client = NuMind(api_key=os.environ["NUMIND_API_KEY"])
```

### Create an async client

You can create an **async** client by using the `NuMindAsync` class:

```python
import asyncio
from numind import NuMindAsync

client = NuMindAsync(api_key="API_KEY")
requests = [{}]

async def main():
    return [
        await client.extract(project_id, **request_kwargs)
        for request_kwargs in requests
    ]

responses = asyncio.run(main())
```

The methods and their usages are the same as for the sync `NuMind` client except that API methods are coroutines that must be awaited.

### NuExtract: Extract structured information "on the fly"

If you want to extract structured information from data without projects but just by providing the input template, you can use the `extract` method which provides a more user-friendly way to interact with the API:

```python
template = {
    "destination": {
        "name": "verbatim-string",
        "zip_code": "string",
        "country": "string"
    },
    "accommodation": "verbatim-string",
    "activities": ["verbatim-string"],
    "duration": {
        "time_unit": ["day", "week", "month", "year"],
        "time_quantity": "integer"
    }
}
input_text = """My dream vacation would be a month-long escape to the stunning islands of Tahiti.
I’d stay in an overwater bungalow in Bora Bora, waking up to crystal-clear turquoise waters and breathtaking sunrises.
Days would be spent snorkeling with vibrant marine life, paddleboarding over coral gardens, and basking on pristine white-sand beaches.
I’d explore lush rainforests, hidden waterfalls, and the rich Polynesian culture through traditional dance, music, and cuisine.
Evenings would be filled with romantic beachside dinners under the stars, with the soothing sound of waves as the perfect backdrop."""

output = client.extract(template=template, input_text=input_text)
print(output)

# Can also work with files, replace the path with your own
# from pathlib import Path
# output = client.extract(template=template, input_file="file.ppt")
```

```json
{
    "destination": {
        "name": "Tahiti",
        "zip_code": "98730",
        "country": "France"
    },
    "accommodation": "overwater bungalow in Bora Bora",
    "activities": [
        "snorkeling",
        "paddleboarding",
        "basking",
        "explore lush rainforests, hidden waterfalls, and the rich Polynesian culture"
    ],
    "duration": {
        "time_unit": null,
        "time_quantity": null
    }
}
```

### Create a good template

NuExtract uses JSON schemas as extraction templates which specify the information to retrieve and their types, which are:

* **string**: a text, whose value can be abstract, i.e. totally free and can be deduced from calculations, reasoning, external knowledge;
* **verbatim-string**: a purely extractive text whose value must be present in the document. Some flexibility might be allowed on the formatting, e.g. new lines and escaped characters (e.g. `\n`) in a documents might be represented with a space;
* **integer**: an integer number;
* **number**: any number, that may be a floating point number or an integer;
* **boolean**: a boolean whose value should be either true or false;
* **date-time**: a date or time whose value should follow the ISO 8601 standard (`YYYY-MM-DDThh:mm:ss`). It may feature "reduced" accuracy, i.e. omitting certain date or time components not useful in specific cases. For examples, if the extracted value is a date, `YYYY-MM-DD` is a valid value format. The same applies to times with the `hh:mm:ss` format (without omitting the leading `T` symbol). Additionally, the "least significant" component might be omitted if it is not required or specified. For example, a specific month and year can be specified as `YYYY-MM` while omitting the day component `DD`. A specific hour can be specified as `hh` while omitting the minutes and seconds components. When combining dates and time, only the least significant time components can be omitted, e.g. `YYYY-MM-DDThh:mm` which is omitting the seconds.

Additionally, the value of a field can be:

* a **nested dictionary**, i.e. another branch, describing elements associated to their parent node (key);
* an **array** of items of the form `["type"]`, whose values are elements of a given "type", which can also be a dictionary of unspecified depth;
* an **enum**, i.e. a list of elements to choose from of the form `["choice1", "choice2", ...]`. For values of this type, just set the value of the item to choose, e.g. "choice1", and do not set the value as an array containing the item such as `["choice1"]`;
* a **multi-enum**, i.e. a list from which multiple elements can be picked, of the form `[["choice1", "choice2", ...]]` (double square brackets).

#### Inferring a template

The "infer_template" method allows to quickly create a template that you can start to work with from a text description.

```python
from numind.openapi_client import TemplateRequest
from pydantic import StrictStr

description = "Create a template that extracts key information from an order confirmation email. The template should be able to pull details like the order ID, customer ID, date and time of the order, status, total amount, currency, item details (product ID, quantity, and unit price), shipping address, any customer requests or delivery preferences, and the estimated delivery date."
input_schema = client.post_api_infer_template(
    template_request=TemplateRequest(description=StrictStr(description))
)
```

### Create a project

A project allows to define an information extraction task from a template and examples.

```python
from numind.openapi_client import CreateProjectRequest

project_id = client.post_api_projects(
    CreateProjectRequest(
        name="vacation",
        description="Extraction of locations and activities",
        template=template,
    )
)
```

The `project_id` can also be found in the "API" tab of a project on the NuExtract website.

### Add examples to a project to teach NuExtract via ICL (In-Context Learning)

```python
from pathlib import Path

# Prepare examples, here a text and a file
example_1_input = "This is a text example"
example_1_expected_output = {
    "destination": {"name": None, "zip_code": None, "country": None}
}
with Path("example_2.odt").open("rb") as file:  # read bytes
    example_2_input = file.read()
example_2_expected_output = {
    "destination": {"name": None, "zip_code": None, "country": None}
}
examples = [
    (example_1_input, example_1_expected_output),
    (example_2_input, example_2_expected_output),
]

# Add the examples to the project
client.add_examples_to_project(project_id, examples)
```

### Extract structured information from text

```python
output_schema = client.extract(project_id, input_text=input_text)
```

### Extract structured information from a file

```python
from pathlib import Path

file_path = Path("document.odt")
with file_path.open("rb") as file:
    input_file = file.read()
output_schema = client.extract(project_id, input_file=input_file)
```

### NuMarkdown: Convert a document to a RAG-ready Markdown

```python
from pathlib import Path

file_path = Path("document.pdf")
with file_path.open("rb") as file:
    input_file = file.read()
markdown = client.numarkdown(input_file)
```

# Documentation

### Extracting Information from Documents

Once your project is ready, you can use it to extract information from documents in real time via this RESTful API.

Each project has its own extraction endpoint:

`https://nuextract.ai/api/projects/{projectId}/extract`

You provide it a document and it returns the extracted information according to the task defined in the project. To use it, you need:

- To create an API key in the [Account section](https://nuextract.ai/app/user?content=api)
- To replace `{projectId}` by the project ID found in the API tab of the project

You can test your extraction endpoint in your terminal using this command-line example with curl (make sure that you replace values of `PROJECT_ID` and `NUEXTRACT_API_KEY`):

```bash
NUEXTRACT_API_KEY=\"_your_api_key_here_\"; \\
PROJECT_ID=\"a24fd84a-44ab-4fd4-95a9-bebd46e4768b\"; \\
curl \"https://nuextract.ai/api/projects/${PROJECT_ID}/extract\" \\
  -X POST \\
  -H \"Authorization: Bearer ${NUEXTRACT_API_KEY}\" \\
  -H \"Content-Type: application/octet-stream\" \\
  --data-binary @\"${FILE_NAME}\"
```

You can also use the [Python SDK](https://github.com/numindai/nuextract-platform-sdk#documentation), by replacing the
`project_id`, `api_key` and `file_path` variables in the following code:

```python
from numind import NuMind
from pathlib import Path

client = NuMind(api_key=api_key)
file_path = Path(\"path\", \"to\", \"document.odt\")
with file_path.open(\"rb\") as file:
    input_file = file.read()
output_schema = client.post_api_projects_projectid_extract(project_id, input_file)
```

### Using the Platform via API

Everything you can do on the web platform can be done via API -
 check the [user guide](https://www.notion.so/User-Guide-17c16b1df8c580d3a579ebfb24ddbea7?pvs=21) to learn about how the platform works.
 This can be useful to create projects automatically, or to make your production more robust for example.

#### Main resources

- **Project** - user project, identified by `projectId`
- **File** - uploaded file,  identified by `fileId`, stored up to two weeks if not tied to an **Example**
- **Document** - internal representation of a document, identified by `documentId`, created from a File or a text, stored up to two weeks if not tied to an Example
- **Example** - document-extraction pair given to teach NuExtract, identified by `exampleId`, created from a Document

#### Most common API operations

- Creating a **Project** via `POST /api/projects`
- Changing the template of a **Project** via `PATCH /api/projects/{projectId}`
- Uploading a file to a **File** via `POST /api/files` (up to 2 weeks storage)
- Creating a **Document** via `POST /api/documents/text` and `POST /api/files/{fileID}/convert-to-document` from a text or a **File**
- Adding an **Example** to a **Project** via `POST /api/projects/{projectId}/examples`
- Changing Project settings via `POST /api/projects/{projectId}/settings`
- Locking a **Project** via `POST /api/projects/{projectId}/lock`

This Python package is automatically generated by the [OpenAPI Generator](https://openapi-generator.tech) project:

- API version: 
- Package version: 1.0.0
- Generator version: 7.17.0
- Build package: org.openapitools.codegen.languages.PythonClientCodegen

### Documentation for API Endpoints

All URIs are relative to *https://nuextract.ai*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*ContentExtractionApi* | [**get_api_content_extraction_jobs_contentextractionjobid**](docs/ContentExtractionApi.md#get_api_content_extraction_jobs_contentextractionjobid) | **GET** /api/content-extraction/jobs/{contentExtractionJobId} | 
*ContentExtractionApi* | [**post_api_content_extraction_jobs**](docs/ContentExtractionApi.md#post_api_content_extraction_jobs) | **POST** /api/content-extraction/jobs | 
*ContentExtractionPlaygroundApi* | [**delete_api_content_extraction_contentextractionprojectid_playground_contentextractionplaygrounditemid**](docs/ContentExtractionPlaygroundApi.md#delete_api_content_extraction_contentextractionprojectid_playground_contentextractionplaygrounditemid) | **DELETE** /api/content-extraction/{contentExtractionProjectId}/playground/{contentExtractionPlaygroundItemId} | 
*ContentExtractionPlaygroundApi* | [**get_api_content_extraction_contentextractionprojectid_playground**](docs/ContentExtractionPlaygroundApi.md#get_api_content_extraction_contentextractionprojectid_playground) | **GET** /api/content-extraction/{contentExtractionProjectId}/playground | 
*ContentExtractionPlaygroundApi* | [**get_api_content_extraction_contentextractionprojectid_playground_contentextractionplaygrounditemid**](docs/ContentExtractionPlaygroundApi.md#get_api_content_extraction_contentextractionprojectid_playground_contentextractionplaygrounditemid) | **GET** /api/content-extraction/{contentExtractionProjectId}/playground/{contentExtractionPlaygroundItemId} | 
*ContentExtractionPlaygroundApi* | [**post_api_content_extraction_contentextractionprojectid_playground**](docs/ContentExtractionPlaygroundApi.md#post_api_content_extraction_contentextractionprojectid_playground) | **POST** /api/content-extraction/{contentExtractionProjectId}/playground | 
*ContentExtractionPlaygroundApi* | [**put_api_content_extraction_contentextractionprojectid_playground_contentextractionplaygrounditemid**](docs/ContentExtractionPlaygroundApi.md#put_api_content_extraction_contentextractionprojectid_playground_contentextractionplaygrounditemid) | **PUT** /api/content-extraction/{contentExtractionProjectId}/playground/{contentExtractionPlaygroundItemId} | 
*ContentExtractionProjectManagementApi* | [**get_api_content_extraction**](docs/ContentExtractionProjectManagementApi.md#get_api_content_extraction) | **GET** /api/content-extraction | 
*ContentExtractionProjectManagementApi* | [**patch_api_content_extraction_contentextractionprojectid**](docs/ContentExtractionProjectManagementApi.md#patch_api_content_extraction_contentextractionprojectid) | **PATCH** /api/content-extraction/{contentExtractionProjectId} | 
*ContentExtractionProjectManagementApi* | [**patch_api_content_extraction_contentextractionprojectid_settings**](docs/ContentExtractionProjectManagementApi.md#patch_api_content_extraction_contentextractionprojectid_settings) | **PATCH** /api/content-extraction/{contentExtractionProjectId}/settings | 
*ContentExtractionProjectManagementApi* | [**post_api_content_extraction**](docs/ContentExtractionProjectManagementApi.md#post_api_content_extraction) | **POST** /api/content-extraction | 
*ContentExtractionProjectManagementApi* | [**post_api_content_extraction_contentextractionprojectid_reset_settings**](docs/ContentExtractionProjectManagementApi.md#post_api_content_extraction_contentextractionprojectid_reset_settings) | **POST** /api/content-extraction/{contentExtractionProjectId}/reset-settings | 
*DefaultApi* | [**get_api_debug_status_code**](docs/DefaultApi.md#get_api_debug_status_code) | **GET** /api/debug/status/{code} | 
*DefaultApi* | [**get_api_health**](docs/DefaultApi.md#get_api_health) | **GET** /api/health | 
*DefaultApi* | [**get_api_inference_status**](docs/DefaultApi.md#get_api_inference_status) | **GET** /api/inference-status | 
*DefaultApi* | [**get_api_ping**](docs/DefaultApi.md#get_api_ping) | **GET** /api/ping | 
*DefaultApi* | [**get_api_version**](docs/DefaultApi.md#get_api_version) | **GET** /api/version | 
*DocumentsApi* | [**get_api_documents_documentid**](docs/DocumentsApi.md#get_api_documents_documentid) | **GET** /api/documents/{documentId} | 
*DocumentsApi* | [**get_api_documents_documentid_content**](docs/DocumentsApi.md#get_api_documents_documentid_content) | **GET** /api/documents/{documentId}/content | 
*DocumentsApi* | [**post_api_documents_text**](docs/DocumentsApi.md#post_api_documents_text) | **POST** /api/documents/text | 
*ExamplesDeprecatedApi* | [**delete_api_projects_projectid_examples_exampleid**](docs/ExamplesDeprecatedApi.md#delete_api_projects_projectid_examples_exampleid) | **DELETE** /api/projects/{projectId}/examples/{exampleId} | 
*ExamplesDeprecatedApi* | [**get_api_projects_projectid_examples**](docs/ExamplesDeprecatedApi.md#get_api_projects_projectid_examples) | **GET** /api/projects/{projectId}/examples | 
*ExamplesDeprecatedApi* | [**get_api_projects_projectid_examples_exampleid**](docs/ExamplesDeprecatedApi.md#get_api_projects_projectid_examples_exampleid) | **GET** /api/projects/{projectId}/examples/{exampleId} | 
*ExamplesDeprecatedApi* | [**post_api_projects_projectid_examples**](docs/ExamplesDeprecatedApi.md#post_api_projects_projectid_examples) | **POST** /api/projects/{projectId}/examples | 
*ExamplesDeprecatedApi* | [**put_api_projects_projectid_examples_exampleid**](docs/ExamplesDeprecatedApi.md#put_api_projects_projectid_examples_exampleid) | **PUT** /api/projects/{projectId}/examples/{exampleId} | 
*FilesApi* | [**get_api_files_fileid**](docs/FilesApi.md#get_api_files_fileid) | **GET** /api/files/{fileId} | 
*FilesApi* | [**get_api_files_fileid_content**](docs/FilesApi.md#get_api_files_fileid_content) | **GET** /api/files/{fileId}/content | 
*FilesApi* | [**post_api_files**](docs/FilesApi.md#post_api_files) | **POST** /api/files | 
*FilesApi* | [**post_api_files_fileid_convert_to_document**](docs/FilesApi.md#post_api_files_fileid_convert_to_document) | **POST** /api/files/{fileId}/convert-to-document | 
*InferenceApi* | [**post_api_content_extraction_contentextractionprojectid_jobs_document_documentid**](docs/InferenceApi.md#post_api_content_extraction_contentextractionprojectid_jobs_document_documentid) | **POST** /api/content-extraction/{contentExtractionProjectId}/jobs/document/{documentId} | 
*InferenceApi* | [**post_api_structured_extraction_structuredextractionprojectid_jobs_document_documentid**](docs/InferenceApi.md#post_api_structured_extraction_structuredextractionprojectid_jobs_document_documentid) | **POST** /api/structured-extraction/{structuredExtractionProjectId}/jobs/document/{documentId} | 
*InferenceApi* | [**post_api_structured_extraction_structuredextractionprojectid_jobs_text**](docs/InferenceApi.md#post_api_structured_extraction_structuredextractionprojectid_jobs_text) | **POST** /api/structured-extraction/{structuredExtractionProjectId}/jobs/text | 
*InferenceApi* | [**post_api_template_generation_jobs_document_documentid**](docs/InferenceApi.md#post_api_template_generation_jobs_document_documentid) | **POST** /api/template-generation/jobs/document/{documentId} | 
*InferenceApi* | [**post_api_template_generation_jobs_text**](docs/InferenceApi.md#post_api_template_generation_jobs_text) | **POST** /api/template-generation/jobs/text | 
*InferenceDeprecatedApi* | [**post_api_infer_template**](docs/InferenceDeprecatedApi.md#post_api_infer_template) | **POST** /api/infer-template | 
*InferenceDeprecatedApi* | [**post_api_infer_template_async**](docs/InferenceDeprecatedApi.md#post_api_infer_template_async) | **POST** /api/infer-template-async | 
*InferenceDeprecatedApi* | [**post_api_infer_template_async_document_documentid**](docs/InferenceDeprecatedApi.md#post_api_infer_template_async_document_documentid) | **POST** /api/infer-template-async/document/{documentId} | 
*InferenceDeprecatedApi* | [**post_api_infer_template_document_documentid**](docs/InferenceDeprecatedApi.md#post_api_infer_template_document_documentid) | **POST** /api/infer-template/document/{documentId} | 
*InferenceDeprecatedApi* | [**post_api_infer_template_file**](docs/InferenceDeprecatedApi.md#post_api_infer_template_file) | **POST** /api/infer-template/file | 
*InferenceDeprecatedApi* | [**post_api_projects_projectid_infer_document_async_documentid**](docs/InferenceDeprecatedApi.md#post_api_projects_projectid_infer_document_async_documentid) | **POST** /api/projects/{projectId}/infer-document-async/{documentId} | 
*InferenceDeprecatedApi* | [**post_api_projects_projectid_infer_document_documentid**](docs/InferenceDeprecatedApi.md#post_api_projects_projectid_infer_document_documentid) | **POST** /api/projects/{projectId}/infer-document/{documentId} | 
*InferenceDeprecatedApi* | [**post_api_projects_projectid_infer_text**](docs/InferenceDeprecatedApi.md#post_api_projects_projectid_infer_text) | **POST** /api/projects/{projectId}/infer-text | 
*InferenceDeprecatedApi* | [**post_api_projects_projectid_infer_text_async**](docs/InferenceDeprecatedApi.md#post_api_projects_projectid_infer_text_async) | **POST** /api/projects/{projectId}/infer-text-async | 
*JobsApi* | [**get_api_jobs**](docs/JobsApi.md#get_api_jobs) | **GET** /api/jobs | 
*JobsApi* | [**get_api_jobs_jobid**](docs/JobsApi.md#get_api_jobs_jobid) | **GET** /api/jobs/{jobId} | 
*JobsApi* | [**get_api_jobs_jobid_status**](docs/JobsApi.md#get_api_jobs_jobid_status) | **GET** /api/jobs/{jobId}/status | 
*JobsApi* | [**get_api_jobs_jobid_stream**](docs/JobsApi.md#get_api_jobs_jobid_stream) | **GET** /api/jobs/{jobId}/stream | 
*OrganizationManagementApi* | [**delete_api_organizations_organizationid**](docs/OrganizationManagementApi.md#delete_api_organizations_organizationid) | **DELETE** /api/organizations/{organizationId} | 
*OrganizationManagementApi* | [**delete_api_organizations_organizationid_members_invitations_invitationid**](docs/OrganizationManagementApi.md#delete_api_organizations_organizationid_members_invitations_invitationid) | **DELETE** /api/organizations/{organizationId}/members/invitations/{invitationId} | 
*OrganizationManagementApi* | [**delete_api_organizations_organizationid_members_userid**](docs/OrganizationManagementApi.md#delete_api_organizations_organizationid_members_userid) | **DELETE** /api/organizations/{organizationId}/members/{userId} | 
*OrganizationManagementApi* | [**get_api_organizations**](docs/OrganizationManagementApi.md#get_api_organizations) | **GET** /api/organizations | 
*OrganizationManagementApi* | [**get_api_organizations_organizationid_members**](docs/OrganizationManagementApi.md#get_api_organizations_organizationid_members) | **GET** /api/organizations/{organizationId}/members | 
*OrganizationManagementApi* | [**get_api_organizations_organizationid_members_invitations**](docs/OrganizationManagementApi.md#get_api_organizations_organizationid_members_invitations) | **GET** /api/organizations/{organizationId}/members/invitations | 
*OrganizationManagementApi* | [**post_api_organizations**](docs/OrganizationManagementApi.md#post_api_organizations) | **POST** /api/organizations | 
*OrganizationManagementApi* | [**post_api_organizations_organizationid_members**](docs/OrganizationManagementApi.md#post_api_organizations_organizationid_members) | **POST** /api/organizations/{organizationId}/members | 
*OrganizationManagementApi* | [**put_api_organizations_organizationid**](docs/OrganizationManagementApi.md#put_api_organizations_organizationid) | **PUT** /api/organizations/{organizationId} | 
*PlaygroundDeprecatedApi* | [**delete_api_projects_projectid_playground_playgrounditemid**](docs/PlaygroundDeprecatedApi.md#delete_api_projects_projectid_playground_playgrounditemid) | **DELETE** /api/projects/{projectId}/playground/{playgroundItemId} | 
*PlaygroundDeprecatedApi* | [**get_api_projects_projectid_playground**](docs/PlaygroundDeprecatedApi.md#get_api_projects_projectid_playground) | **GET** /api/projects/{projectId}/playground | 
*PlaygroundDeprecatedApi* | [**get_api_projects_projectid_playground_playgrounditemid**](docs/PlaygroundDeprecatedApi.md#get_api_projects_projectid_playground_playgrounditemid) | **GET** /api/projects/{projectId}/playground/{playgroundItemId} | 
*PlaygroundDeprecatedApi* | [**post_api_projects_projectid_playground**](docs/PlaygroundDeprecatedApi.md#post_api_projects_projectid_playground) | **POST** /api/projects/{projectId}/playground | 
*PlaygroundDeprecatedApi* | [**put_api_projects_projectid_playground_playgrounditemid**](docs/PlaygroundDeprecatedApi.md#put_api_projects_projectid_playground_playgrounditemid) | **PUT** /api/projects/{projectId}/playground/{playgroundItemId} | 
*ProjectManagementDeprecatedApi* | [**delete_api_projects_projectid**](docs/ProjectManagementDeprecatedApi.md#delete_api_projects_projectid) | **DELETE** /api/projects/{projectId} | 
*ProjectManagementDeprecatedApi* | [**get_api_projects**](docs/ProjectManagementDeprecatedApi.md#get_api_projects) | **GET** /api/projects | 
*ProjectManagementDeprecatedApi* | [**get_api_projects_projectid**](docs/ProjectManagementDeprecatedApi.md#get_api_projects_projectid) | **GET** /api/projects/{projectId} | 
*ProjectManagementDeprecatedApi* | [**patch_api_projects_projectid**](docs/ProjectManagementDeprecatedApi.md#patch_api_projects_projectid) | **PATCH** /api/projects/{projectId} | 
*ProjectManagementDeprecatedApi* | [**patch_api_projects_projectid_settings**](docs/ProjectManagementDeprecatedApi.md#patch_api_projects_projectid_settings) | **PATCH** /api/projects/{projectId}/settings | 
*ProjectManagementDeprecatedApi* | [**post_api_projects**](docs/ProjectManagementDeprecatedApi.md#post_api_projects) | **POST** /api/projects | 
*ProjectManagementDeprecatedApi* | [**post_api_projects_projectid_duplicate**](docs/ProjectManagementDeprecatedApi.md#post_api_projects_projectid_duplicate) | **POST** /api/projects/{projectId}/duplicate | 
*ProjectManagementDeprecatedApi* | [**post_api_projects_projectid_lock**](docs/ProjectManagementDeprecatedApi.md#post_api_projects_projectid_lock) | **POST** /api/projects/{projectId}/lock | 
*ProjectManagementDeprecatedApi* | [**post_api_projects_projectid_reset_settings**](docs/ProjectManagementDeprecatedApi.md#post_api_projects_projectid_reset_settings) | **POST** /api/projects/{projectId}/reset-settings | 
*ProjectManagementDeprecatedApi* | [**post_api_projects_projectid_share**](docs/ProjectManagementDeprecatedApi.md#post_api_projects_projectid_share) | **POST** /api/projects/{projectId}/share | 
*ProjectManagementDeprecatedApi* | [**post_api_projects_projectid_unlock**](docs/ProjectManagementDeprecatedApi.md#post_api_projects_projectid_unlock) | **POST** /api/projects/{projectId}/unlock | 
*ProjectManagementDeprecatedApi* | [**post_api_projects_projectid_unshare**](docs/ProjectManagementDeprecatedApi.md#post_api_projects_projectid_unshare) | **POST** /api/projects/{projectId}/unshare | 
*ProjectManagementDeprecatedApi* | [**put_api_projects_projectid_template**](docs/ProjectManagementDeprecatedApi.md#put_api_projects_projectid_template) | **PUT** /api/projects/{projectId}/template | 
*StructuredDataExtractionApi* | [**get_api_structured_extraction_jobs_structuredextractionjobid**](docs/StructuredDataExtractionApi.md#get_api_structured_extraction_jobs_structuredextractionjobid) | **GET** /api/structured-extraction/jobs/{structuredExtractionJobId} | 
*StructuredDataExtractionApi* | [**post_api_projects_projectid_extract**](docs/StructuredDataExtractionApi.md#post_api_projects_projectid_extract) | **POST** /api/projects/{projectId}/extract | 
*StructuredDataExtractionApi* | [**post_api_projects_projectid_extract_async**](docs/StructuredDataExtractionApi.md#post_api_projects_projectid_extract_async) | **POST** /api/projects/{projectId}/extract-async | 
*StructuredDataExtractionApi* | [**post_api_structured_extraction_structuredextractionprojectid_jobs**](docs/StructuredDataExtractionApi.md#post_api_structured_extraction_structuredextractionprojectid_jobs) | **POST** /api/structured-extraction/{structuredExtractionProjectId}/jobs | 
*StructuredExtractionExamplesApi* | [**delete_api_structured_extraction_structuredextractionprojectid_examples_structuredextractionexampleid**](docs/StructuredExtractionExamplesApi.md#delete_api_structured_extraction_structuredextractionprojectid_examples_structuredextractionexampleid) | **DELETE** /api/structured-extraction/{structuredExtractionProjectId}/examples/{structuredExtractionExampleId} | 
*StructuredExtractionExamplesApi* | [**get_api_structured_extraction_structuredextractionprojectid_examples**](docs/StructuredExtractionExamplesApi.md#get_api_structured_extraction_structuredextractionprojectid_examples) | **GET** /api/structured-extraction/{structuredExtractionProjectId}/examples | 
*StructuredExtractionExamplesApi* | [**get_api_structured_extraction_structuredextractionprojectid_examples_structuredextractionexampleid**](docs/StructuredExtractionExamplesApi.md#get_api_structured_extraction_structuredextractionprojectid_examples_structuredextractionexampleid) | **GET** /api/structured-extraction/{structuredExtractionProjectId}/examples/{structuredExtractionExampleId} | 
*StructuredExtractionExamplesApi* | [**post_api_structured_extraction_structuredextractionprojectid_examples**](docs/StructuredExtractionExamplesApi.md#post_api_structured_extraction_structuredextractionprojectid_examples) | **POST** /api/structured-extraction/{structuredExtractionProjectId}/examples | 
*StructuredExtractionExamplesApi* | [**put_api_structured_extraction_structuredextractionprojectid_examples_structuredextractionexampleid**](docs/StructuredExtractionExamplesApi.md#put_api_structured_extraction_structuredextractionprojectid_examples_structuredextractionexampleid) | **PUT** /api/structured-extraction/{structuredExtractionProjectId}/examples/{structuredExtractionExampleId} | 
*StructuredExtractionPlaygroundApi* | [**delete_api_structured_extraction_structuredextractionprojectid_playground_structuredextractionplaygrounditemid**](docs/StructuredExtractionPlaygroundApi.md#delete_api_structured_extraction_structuredextractionprojectid_playground_structuredextractionplaygrounditemid) | **DELETE** /api/structured-extraction/{structuredExtractionProjectId}/playground/{structuredExtractionPlaygroundItemId} | 
*StructuredExtractionPlaygroundApi* | [**get_api_structured_extraction_structuredextractionprojectid_playground**](docs/StructuredExtractionPlaygroundApi.md#get_api_structured_extraction_structuredextractionprojectid_playground) | **GET** /api/structured-extraction/{structuredExtractionProjectId}/playground | 
*StructuredExtractionPlaygroundApi* | [**get_api_structured_extraction_structuredextractionprojectid_playground_structuredextractionplaygrounditemid**](docs/StructuredExtractionPlaygroundApi.md#get_api_structured_extraction_structuredextractionprojectid_playground_structuredextractionplaygrounditemid) | **GET** /api/structured-extraction/{structuredExtractionProjectId}/playground/{structuredExtractionPlaygroundItemId} | 
*StructuredExtractionPlaygroundApi* | [**post_api_structured_extraction_structuredextractionprojectid_playground**](docs/StructuredExtractionPlaygroundApi.md#post_api_structured_extraction_structuredextractionprojectid_playground) | **POST** /api/structured-extraction/{structuredExtractionProjectId}/playground | 
*StructuredExtractionPlaygroundApi* | [**put_api_structured_extraction_structuredextractionprojectid_playground_structuredextractionplaygrounditemid**](docs/StructuredExtractionPlaygroundApi.md#put_api_structured_extraction_structuredextractionprojectid_playground_structuredextractionplaygrounditemid) | **PUT** /api/structured-extraction/{structuredExtractionProjectId}/playground/{structuredExtractionPlaygroundItemId} | 
*StructuredExtractionProjectManagementApi* | [**delete_api_structured_extraction_structuredextractionprojectid**](docs/StructuredExtractionProjectManagementApi.md#delete_api_structured_extraction_structuredextractionprojectid) | **DELETE** /api/structured-extraction/{structuredExtractionProjectId} | 
*StructuredExtractionProjectManagementApi* | [**get_api_structured_extraction**](docs/StructuredExtractionProjectManagementApi.md#get_api_structured_extraction) | **GET** /api/structured-extraction | 
*StructuredExtractionProjectManagementApi* | [**get_api_structured_extraction_structuredextractionprojectid**](docs/StructuredExtractionProjectManagementApi.md#get_api_structured_extraction_structuredextractionprojectid) | **GET** /api/structured-extraction/{structuredExtractionProjectId} | 
*StructuredExtractionProjectManagementApi* | [**patch_api_structured_extraction_structuredextractionprojectid**](docs/StructuredExtractionProjectManagementApi.md#patch_api_structured_extraction_structuredextractionprojectid) | **PATCH** /api/structured-extraction/{structuredExtractionProjectId} | 
*StructuredExtractionProjectManagementApi* | [**patch_api_structured_extraction_structuredextractionprojectid_settings**](docs/StructuredExtractionProjectManagementApi.md#patch_api_structured_extraction_structuredextractionprojectid_settings) | **PATCH** /api/structured-extraction/{structuredExtractionProjectId}/settings | 
*StructuredExtractionProjectManagementApi* | [**post_api_structured_extraction**](docs/StructuredExtractionProjectManagementApi.md#post_api_structured_extraction) | **POST** /api/structured-extraction | 
*StructuredExtractionProjectManagementApi* | [**post_api_structured_extraction_structuredextractionprojectid_duplicate**](docs/StructuredExtractionProjectManagementApi.md#post_api_structured_extraction_structuredextractionprojectid_duplicate) | **POST** /api/structured-extraction/{structuredExtractionProjectId}/duplicate | 
*StructuredExtractionProjectManagementApi* | [**post_api_structured_extraction_structuredextractionprojectid_lock**](docs/StructuredExtractionProjectManagementApi.md#post_api_structured_extraction_structuredextractionprojectid_lock) | **POST** /api/structured-extraction/{structuredExtractionProjectId}/lock | 
*StructuredExtractionProjectManagementApi* | [**post_api_structured_extraction_structuredextractionprojectid_reset_settings**](docs/StructuredExtractionProjectManagementApi.md#post_api_structured_extraction_structuredextractionprojectid_reset_settings) | **POST** /api/structured-extraction/{structuredExtractionProjectId}/reset-settings | 
*StructuredExtractionProjectManagementApi* | [**post_api_structured_extraction_structuredextractionprojectid_share**](docs/StructuredExtractionProjectManagementApi.md#post_api_structured_extraction_structuredextractionprojectid_share) | **POST** /api/structured-extraction/{structuredExtractionProjectId}/share | 
*StructuredExtractionProjectManagementApi* | [**post_api_structured_extraction_structuredextractionprojectid_unlock**](docs/StructuredExtractionProjectManagementApi.md#post_api_structured_extraction_structuredextractionprojectid_unlock) | **POST** /api/structured-extraction/{structuredExtractionProjectId}/unlock | 
*StructuredExtractionProjectManagementApi* | [**post_api_structured_extraction_structuredextractionprojectid_unshare**](docs/StructuredExtractionProjectManagementApi.md#post_api_structured_extraction_structuredextractionprojectid_unshare) | **POST** /api/structured-extraction/{structuredExtractionProjectId}/unshare | 
*StructuredExtractionProjectManagementApi* | [**put_api_structured_extraction_structuredextractionprojectid_template**](docs/StructuredExtractionProjectManagementApi.md#put_api_structured_extraction_structuredextractionprojectid_template) | **PUT** /api/structured-extraction/{structuredExtractionProjectId}/template | 
*TemplateGenerationApi* | [**get_api_template_generation_jobs_templatejobid**](docs/TemplateGenerationApi.md#get_api_template_generation_jobs_templatejobid) | **GET** /api/template-generation/jobs/{templateJobId} | 
*TemplateGenerationApi* | [**post_api_template_generation_jobs**](docs/TemplateGenerationApi.md#post_api_template_generation_jobs) | **POST** /api/template-generation/jobs | 


### Documentation For Models

 - [ApiKeyResponse](docs/ApiKeyResponse.md)
 - [ConvertRequest](docs/ConvertRequest.md)
 - [CreateApiKey](docs/CreateApiKey.md)
 - [CreateMarkdownProjectRequest](docs/CreateMarkdownProjectRequest.md)
 - [CreateOrUpdateExampleRequest](docs/CreateOrUpdateExampleRequest.md)
 - [CreateOrUpdateMarkdownPlaygroundItemRequest](docs/CreateOrUpdateMarkdownPlaygroundItemRequest.md)
 - [CreateOrUpdatePlaygroundItemRequest](docs/CreateOrUpdatePlaygroundItemRequest.md)
 - [CreateOrganizationRequest](docs/CreateOrganizationRequest.md)
 - [CreateProjectRequest](docs/CreateProjectRequest.md)
 - [DocumentInfo](docs/DocumentInfo.md)
 - [DocumentResponse](docs/DocumentResponse.md)
 - [Error](docs/Error.md)
 - [ExampleResponse](docs/ExampleResponse.md)
 - [ExtractionResponse](docs/ExtractionResponse.md)
 - [ExtractionResponseDeprecated](docs/ExtractionResponseDeprecated.md)
 - [FileResponse](docs/FileResponse.md)
 - [HealthResponse](docs/HealthResponse.md)
 - [ImageInfo](docs/ImageInfo.md)
 - [InferenceExample](docs/InferenceExample.md)
 - [InferenceStatus](docs/InferenceStatus.md)
 - [InferenceValidationError](docs/InferenceValidationError.md)
 - [InformationResponse](docs/InformationResponse.md)
 - [InvalidInformation](docs/InvalidInformation.md)
 - [InvitationResponse](docs/InvitationResponse.md)
 - [InviteMemberRequest](docs/InviteMemberRequest.md)
 - [JobIdResponse](docs/JobIdResponse.md)
 - [JobResponse](docs/JobResponse.md)
 - [JobStatusResponse](docs/JobStatusResponse.md)
 - [MarkdownPlaygroundItemResponse](docs/MarkdownPlaygroundItemResponse.md)
 - [MarkdownProjectResponse](docs/MarkdownProjectResponse.md)
 - [MarkdownProjectSettingsResponse](docs/MarkdownProjectSettingsResponse.md)
 - [MarkdownResponse](docs/MarkdownResponse.md)
 - [MemberResponse](docs/MemberResponse.md)
 - [OrganizationResponse](docs/OrganizationResponse.md)
 - [PaginatedResponseExampleResponse](docs/PaginatedResponseExampleResponse.md)
 - [PaginatedResponseJobResponse](docs/PaginatedResponseJobResponse.md)
 - [PaginatedResponseMarkdownPlaygroundItemResponse](docs/PaginatedResponseMarkdownPlaygroundItemResponse.md)
 - [PaginatedResponsePlaygroundItemResponse](docs/PaginatedResponsePlaygroundItemResponse.md)
 - [PlaygroundItemResponse](docs/PlaygroundItemResponse.md)
 - [ProjectResponse](docs/ProjectResponse.md)
 - [ProjectResponseDeprecated](docs/ProjectResponseDeprecated.md)
 - [ProjectSettingsResponse](docs/ProjectSettingsResponse.md)
 - [ProjectSettingsResponseDeprecated](docs/ProjectSettingsResponseDeprecated.md)
 - [RawResult](docs/RawResult.md)
 - [ServiceStatus](docs/ServiceStatus.md)
 - [TemplateRequest](docs/TemplateRequest.md)
 - [TemplateResponse](docs/TemplateResponse.md)
 - [TextInfo](docs/TextInfo.md)
 - [TextRequest](docs/TextRequest.md)
 - [TokenCodeRequest](docs/TokenCodeRequest.md)
 - [TokenRefreshRequest](docs/TokenRefreshRequest.md)
 - [TokenRequest](docs/TokenRequest.md)
 - [TokenResponse](docs/TokenResponse.md)
 - [UpdateApiKey](docs/UpdateApiKey.md)
 - [UpdateMarkdownProjectRequest](docs/UpdateMarkdownProjectRequest.md)
 - [UpdateMarkdownProjectSettingsRequest](docs/UpdateMarkdownProjectSettingsRequest.md)
 - [UpdateOrganizationRequest](docs/UpdateOrganizationRequest.md)
 - [UpdateProjectRequest](docs/UpdateProjectRequest.md)
 - [UpdateProjectSettingsRequest](docs/UpdateProjectSettingsRequest.md)
 - [UpdateProjectTemplateRequest](docs/UpdateProjectTemplateRequest.md)
 - [User](docs/User.md)
 - [ValidInformation](docs/ValidInformation.md)
 - [VersionResponse](docs/VersionResponse.md)


<a id="documentation-for-authorization"></a>
### Documentation For Authorization


Authentication schemes defined for the API:
<a id="oauth2Auth"></a>
#### oauth2Auth

- **Type**: OAuth
- **Flow**: accessCode
- **Authorization URL**: https://users.numind.ai/realms/extract-platform/protocol/openid-connect/auth
- **Scopes**: 
 - **openid**: OpenID connect
 - **profile**: view profile
 - **email**: view email

