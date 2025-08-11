# NuExtract SDK

Python SDK to interact with NuMind's [**NuExtract**](https://nuextract.ai) API.

## Installation

```sh
pip install numind
```

## Usage and code examples

### Create a client

You must first get an API key on [NuExtract](https://nuextract.ai/app/user?content=api).

```python
import os

from numind import NuMind

# Create a client object to interact with the API
# Providing the `api_key` is not required if the `NUMIND_API_KEY` environment variable
# is already set.
client = NuMind(api_key=os.environ["NUMIND_API_KEY"])
```

### Extract structured information "on the fly"

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
- Generator version: 7.14.0
- Build package: org.openapitools.codegen.languages.PythonClientCodegen

### Documentation for API Endpoints

All URIs are relative to *https://nuextract.ai*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*AuthenticationApi* | [**delete_api_auth_api_keys_apikeyid**](docs/AuthenticationApi.md#delete_api_auth_api_keys_apikeyid) | **DELETE** /api/auth/api-keys/{apiKeyId} | 
*AuthenticationApi* | [**get_api_auth**](docs/AuthenticationApi.md#get_api_auth) | **GET** /api/auth | 
*AuthenticationApi* | [**get_api_auth_api_keys**](docs/AuthenticationApi.md#get_api_auth_api_keys) | **GET** /api/auth/api-keys | 
*AuthenticationApi* | [**get_api_auth_me**](docs/AuthenticationApi.md#get_api_auth_me) | **GET** /api/auth/me | 
*AuthenticationApi* | [**post_api_auth_api_keys**](docs/AuthenticationApi.md#post_api_auth_api_keys) | **POST** /api/auth/api-keys | 
*AuthenticationApi* | [**post_api_auth_logout**](docs/AuthenticationApi.md#post_api_auth_logout) | **POST** /api/auth/logout | 
*AuthenticationApi* | [**post_api_auth_token**](docs/AuthenticationApi.md#post_api_auth_token) | **POST** /api/auth/token | 
*AuthenticationApi* | [**put_api_auth_api_keys_apikeyid**](docs/AuthenticationApi.md#put_api_auth_api_keys_apikeyid) | **PUT** /api/auth/api-keys/{apiKeyId} | 
*DocumentsApi* | [**get_api_documents_documentid**](docs/DocumentsApi.md#get_api_documents_documentid) | **GET** /api/documents/{documentId} | 
*DocumentsApi* | [**get_api_documents_documentid_content**](docs/DocumentsApi.md#get_api_documents_documentid_content) | **GET** /api/documents/{documentId}/content | 
*DocumentsApi* | [**post_api_documents_text**](docs/DocumentsApi.md#post_api_documents_text) | **POST** /api/documents/text | 
*ExamplesApi* | [**delete_api_projects_projectid_examples_exampleid**](docs/ExamplesApi.md#delete_api_projects_projectid_examples_exampleid) | **DELETE** /api/projects/{projectId}/examples/{exampleId} | 
*ExamplesApi* | [**get_api_projects_projectid_examples**](docs/ExamplesApi.md#get_api_projects_projectid_examples) | **GET** /api/projects/{projectId}/examples | 
*ExamplesApi* | [**get_api_projects_projectid_examples_exampleid**](docs/ExamplesApi.md#get_api_projects_projectid_examples_exampleid) | **GET** /api/projects/{projectId}/examples/{exampleId} | 
*ExamplesApi* | [**post_api_projects_projectid_examples**](docs/ExamplesApi.md#post_api_projects_projectid_examples) | **POST** /api/projects/{projectId}/examples | 
*ExamplesApi* | [**put_api_projects_projectid_examples_exampleid**](docs/ExamplesApi.md#put_api_projects_projectid_examples_exampleid) | **PUT** /api/projects/{projectId}/examples/{exampleId} | 
*ExtractionApi* | [**post_api_projects_projectid_extract**](docs/ExtractionApi.md#post_api_projects_projectid_extract) | **POST** /api/projects/{projectId}/extract | 
*ExtractionApi* | [**post_api_projects_projectid_extract_async**](docs/ExtractionApi.md#post_api_projects_projectid_extract_async) | **POST** /api/projects/{projectId}/extract-async | 
*FilesApi* | [**get_api_files_fileid**](docs/FilesApi.md#get_api_files_fileid) | **GET** /api/files/{fileId} | 
*FilesApi* | [**get_api_files_fileid_content**](docs/FilesApi.md#get_api_files_fileid_content) | **GET** /api/files/{fileId}/content | 
*FilesApi* | [**post_api_files**](docs/FilesApi.md#post_api_files) | **POST** /api/files | 
*FilesApi* | [**post_api_files_fileid_convert_to_document**](docs/FilesApi.md#post_api_files_fileid_convert_to_document) | **POST** /api/files/{fileId}/convert-to-document | 
*InferenceApi* | [**post_api_infer_template**](docs/InferenceApi.md#post_api_infer_template) | **POST** /api/infer-template | 
*InferenceApi* | [**post_api_infer_template_document_documentid**](docs/InferenceApi.md#post_api_infer_template_document_documentid) | **POST** /api/infer-template/document/{documentId} | 
*InferenceApi* | [**post_api_infer_template_file**](docs/InferenceApi.md#post_api_infer_template_file) | **POST** /api/infer-template/file | 
*InferenceApi* | [**post_api_projects_projectid_infer_document_async_documentid**](docs/InferenceApi.md#post_api_projects_projectid_infer_document_async_documentid) | **POST** /api/projects/{projectId}/infer-document-async/{documentId} | 
*InferenceApi* | [**post_api_projects_projectid_infer_document_documentid**](docs/InferenceApi.md#post_api_projects_projectid_infer_document_documentid) | **POST** /api/projects/{projectId}/infer-document/{documentId} | 
*InferenceApi* | [**post_api_projects_projectid_infer_text**](docs/InferenceApi.md#post_api_projects_projectid_infer_text) | **POST** /api/projects/{projectId}/infer-text | 
*InferenceApi* | [**post_api_projects_projectid_infer_text_async**](docs/InferenceApi.md#post_api_projects_projectid_infer_text_async) | **POST** /api/projects/{projectId}/infer-text-async | 
*JobsApi* | [**get_api_jobs**](docs/JobsApi.md#get_api_jobs) | **GET** /api/jobs | 
*JobsApi* | [**get_api_jobs_jobid**](docs/JobsApi.md#get_api_jobs_jobid) | **GET** /api/jobs/{jobId} | 
*JobsApi* | [**get_api_jobs_jobid_stream**](docs/JobsApi.md#get_api_jobs_jobid_stream) | **GET** /api/jobs/{jobId}/stream | 
*OrganizationsApi* | [**delete_api_organizations_organizationid**](docs/OrganizationsApi.md#delete_api_organizations_organizationid) | **DELETE** /api/organizations/{organizationId} | 
*OrganizationsApi* | [**delete_api_organizations_organizationid_members_invitations_invitationid**](docs/OrganizationsApi.md#delete_api_organizations_organizationid_members_invitations_invitationid) | **DELETE** /api/organizations/{organizationId}/members/invitations/{invitationId} | 
*OrganizationsApi* | [**delete_api_organizations_organizationid_members_userid**](docs/OrganizationsApi.md#delete_api_organizations_organizationid_members_userid) | **DELETE** /api/organizations/{organizationId}/members/{userId} | 
*OrganizationsApi* | [**get_api_organizations**](docs/OrganizationsApi.md#get_api_organizations) | **GET** /api/organizations | 
*OrganizationsApi* | [**get_api_organizations_organizationid_members**](docs/OrganizationsApi.md#get_api_organizations_organizationid_members) | **GET** /api/organizations/{organizationId}/members | 
*OrganizationsApi* | [**get_api_organizations_organizationid_members_invitations**](docs/OrganizationsApi.md#get_api_organizations_organizationid_members_invitations) | **GET** /api/organizations/{organizationId}/members/invitations | 
*OrganizationsApi* | [**post_api_organizations**](docs/OrganizationsApi.md#post_api_organizations) | **POST** /api/organizations | 
*OrganizationsApi* | [**post_api_organizations_organizationid_members**](docs/OrganizationsApi.md#post_api_organizations_organizationid_members) | **POST** /api/organizations/{organizationId}/members | 
*OrganizationsApi* | [**put_api_organizations_organizationid**](docs/OrganizationsApi.md#put_api_organizations_organizationid) | **PUT** /api/organizations/{organizationId} | 
*PlaygroundApi* | [**delete_api_projects_projectid_playground_playgrounditemid**](docs/PlaygroundApi.md#delete_api_projects_projectid_playground_playgrounditemid) | **DELETE** /api/projects/{projectId}/playground/{playgroundItemId} | 
*PlaygroundApi* | [**get_api_projects_projectid_playground**](docs/PlaygroundApi.md#get_api_projects_projectid_playground) | **GET** /api/projects/{projectId}/playground | 
*PlaygroundApi* | [**get_api_projects_projectid_playground_playgrounditemid**](docs/PlaygroundApi.md#get_api_projects_projectid_playground_playgrounditemid) | **GET** /api/projects/{projectId}/playground/{playgroundItemId} | 
*PlaygroundApi* | [**post_api_projects_projectid_playground**](docs/PlaygroundApi.md#post_api_projects_projectid_playground) | **POST** /api/projects/{projectId}/playground | 
*PlaygroundApi* | [**put_api_projects_projectid_playground_playgrounditemid**](docs/PlaygroundApi.md#put_api_projects_projectid_playground_playgrounditemid) | **PUT** /api/projects/{projectId}/playground/{playgroundItemId} | 
*ProjectManagementApi* | [**delete_api_projects_projectid**](docs/ProjectManagementApi.md#delete_api_projects_projectid) | **DELETE** /api/projects/{projectId} | 
*ProjectManagementApi* | [**get_api_projects**](docs/ProjectManagementApi.md#get_api_projects) | **GET** /api/projects | 
*ProjectManagementApi* | [**get_api_projects_projectid**](docs/ProjectManagementApi.md#get_api_projects_projectid) | **GET** /api/projects/{projectId} | 
*ProjectManagementApi* | [**patch_api_projects_projectid**](docs/ProjectManagementApi.md#patch_api_projects_projectid) | **PATCH** /api/projects/{projectId} | 
*ProjectManagementApi* | [**patch_api_projects_projectid_settings**](docs/ProjectManagementApi.md#patch_api_projects_projectid_settings) | **PATCH** /api/projects/{projectId}/settings | 
*ProjectManagementApi* | [**post_api_projects**](docs/ProjectManagementApi.md#post_api_projects) | **POST** /api/projects | 
*ProjectManagementApi* | [**post_api_projects_projectid_duplicate**](docs/ProjectManagementApi.md#post_api_projects_projectid_duplicate) | **POST** /api/projects/{projectId}/duplicate | 
*ProjectManagementApi* | [**post_api_projects_projectid_lock**](docs/ProjectManagementApi.md#post_api_projects_projectid_lock) | **POST** /api/projects/{projectId}/lock | 
*ProjectManagementApi* | [**post_api_projects_projectid_reset_settings**](docs/ProjectManagementApi.md#post_api_projects_projectid_reset_settings) | **POST** /api/projects/{projectId}/reset-settings | 
*ProjectManagementApi* | [**post_api_projects_projectid_share**](docs/ProjectManagementApi.md#post_api_projects_projectid_share) | **POST** /api/projects/{projectId}/share | 
*ProjectManagementApi* | [**post_api_projects_projectid_unlock**](docs/ProjectManagementApi.md#post_api_projects_projectid_unlock) | **POST** /api/projects/{projectId}/unlock | 
*ProjectManagementApi* | [**post_api_projects_projectid_unshare**](docs/ProjectManagementApi.md#post_api_projects_projectid_unshare) | **POST** /api/projects/{projectId}/unshare | 
*ProjectManagementApi* | [**put_api_projects_projectid_template**](docs/ProjectManagementApi.md#put_api_projects_projectid_template) | **PUT** /api/projects/{projectId}/template | 
*DefaultApi* | [**get_api_debug_status_code**](docs/DefaultApi.md#get_api_debug_status_code) | **GET** /api/debug/status/{code} | 
*DefaultApi* | [**get_api_health**](docs/DefaultApi.md#get_api_health) | **GET** /api/health | 
*DefaultApi* | [**get_api_ping**](docs/DefaultApi.md#get_api_ping) | **GET** /api/ping | 
*DefaultApi* | [**get_api_version**](docs/DefaultApi.md#get_api_version) | **GET** /api/version | 


### Documentation For Models

 - [ApiKeyResponse](docs/ApiKeyResponse.md)
 - [ConvertRequest](docs/ConvertRequest.md)
 - [CreateApiKey](docs/CreateApiKey.md)
 - [CreateOrUpdateExampleRequest](docs/CreateOrUpdateExampleRequest.md)
 - [CreateOrUpdatePlaygroundItemRequest](docs/CreateOrUpdatePlaygroundItemRequest.md)
 - [CreateOrganizationRequest](docs/CreateOrganizationRequest.md)
 - [CreateProjectRequest](docs/CreateProjectRequest.md)
 - [DocumentInfo](docs/DocumentInfo.md)
 - [DocumentResponse](docs/DocumentResponse.md)
 - [Error](docs/Error.md)
 - [ExampleResponse](docs/ExampleResponse.md)
 - [ExtractionResponse](docs/ExtractionResponse.md)
 - [FileResponse](docs/FileResponse.md)
 - [HealthResponse](docs/HealthResponse.md)
 - [ImageInfo](docs/ImageInfo.md)
 - [InferenceResponse](docs/InferenceResponse.md)
 - [InformationResponse](docs/InformationResponse.md)
 - [InvalidInformation](docs/InvalidInformation.md)
 - [InvitationResponse](docs/InvitationResponse.md)
 - [InviteMemberRequest](docs/InviteMemberRequest.md)
 - [JobIdResponse](docs/JobIdResponse.md)
 - [JobResponse](docs/JobResponse.md)
 - [MemberResponse](docs/MemberResponse.md)
 - [OrganizationResponse](docs/OrganizationResponse.md)
 - [PlaygroundItemResponse](docs/PlaygroundItemResponse.md)
 - [ProjectResponse](docs/ProjectResponse.md)
 - [ProjectSettingsResponse](docs/ProjectSettingsResponse.md)
 - [RawResult](docs/RawResult.md)
 - [ServiceStatus](docs/ServiceStatus.md)
 - [TemplateRequest](docs/TemplateRequest.md)
 - [TextInfo](docs/TextInfo.md)
 - [TextRequest](docs/TextRequest.md)
 - [TokenCodeRequest](docs/TokenCodeRequest.md)
 - [TokenRefreshRequest](docs/TokenRefreshRequest.md)
 - [TokenRequest](docs/TokenRequest.md)
 - [TokenResponse](docs/TokenResponse.md)
 - [UpdateApiKey](docs/UpdateApiKey.md)
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

