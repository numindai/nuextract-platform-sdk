# numind

Python SDK to interact with the NuMind API.

## Requirements

Python 3.8+

## Getting Started

### Installation

```sh
pip install numind
```

### Usage

#### Create a client

```python
import os

from numind import NuMind

# Create a client object to interact with the API
# Providing the `api_key` is not required if the `NUMIND_API_KEY` environment variable
# is already set.
client = NuMind(api_key=os.environ["NUMIND_API_KEY"])
```

#### Create a project

A project allows to define, on the platform, an input schema along with examples to provide to the model to extract the structured information you want from data.

```python
from numind.openapi_client import CreateProjectRequest

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

project_id = client.post_api_projects(
    CreateProjectRequest(
        name="vacation",
        description="Extraction of locations and activities",
        template=template,
    )
)
```

#### Extract structured information from text

```python
from numind.openapi_client import TextRequest

input_text = """My dream vacation would be a month-long escape to the stunning islands of Tahiti.
I’d stay in an overwater bungalow in Bora Bora, waking up to crystal-clear turquoise waters and breathtaking sunrises.
Days would be spent snorkeling with vibrant marine life, paddleboarding over coral gardens, and basking on pristine white-sand beaches.
I’d explore lush rainforests, hidden waterfalls, and the rich Polynesian culture through traditional dance, music, and cuisine.
Evenings would be filled with romantic beachside dinners under the stars, with the soothing sound of waves as the perfect backdrop."""
output_schema = client.post_api_projects_projectid_infer_text(
    project_id=project_id, text_request=TextRequest(text=input_text)
)
print(output_schema)
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

#### Extract structured information from a file

```python
from pathlib import Path

file_path = Path("path", "to", "document.odt")
with file_path.open("rb") as file:  # read bytes
    intput_file = file.read()
output_schema = client.post_api_projects_projectid_infer_file(
    project_id, file_path.name, intput_file
)
```

#### Extract structured information with no attached project ("on the fly")

If you want to extract structured information from data without projects but just by providing the input template, you can use the `infer` method which provides a more user-friendly way to interact with the API:

```python
from numind import NuMind

# Create a client object to interact with the API
# Providing the `api_key` is not required if the `NUMIND_API_KEY` environment variable
# is already set.
client = NuMind(api_key=os.environ["NUMIND_API_KEY"])

output_schema_text = client.infer(template=template, input_text=input_text)
output_schema_file = client.infer(template=template, input_file=Path("to", "file.ppt"))
```

# Documentation

## Workflow for Using NuExtract API for Information Extraction

### Creating and Managing Projects

A **Project** in NuExtract 2.0 serves as the **main entity** for organizing and managing an **information extraction task**.
It provides a structured approach to processing and extracting data from multiple documents using a **shared template**.

1. **Create a Project**: A project stores the template for information extraction and can optionally include extraction examples to improve model performance.
2. **Define a Template**: The template specifies what information should be extracted from documents within this project. If needed, a template can be derived from a free-form description using the `/api/infer-template` endpoint.
3. **Managing Project Examples**:
   - Project examples (optional) help refine model accuracy and consistency.
   - They serve as **ICL (In-Context Learning) examples** during inference and represent tuples of (input, output).
   - Only examples that match the current project template are used in inference calls.
   - Examples are managed via the ***examples*** endpoints (CRUD operations), requiring a project ID.
4. **Storing Inference Playground Items**:
   - Inference results can be stored within the **project playground** without adding them as ICL examples.
   - This ensures that outputs are retained without affecting inference behavior or increasing token usage.

### Performing Inference

 A **Document** represents the atomic unit over which inference is performed.
  It can be created from either **raw text** or **files** (such as text files, images or convertible types like PDFs, WORD, PPTX, or Excel files).

  When using `/api/projects/{projectId}/infer-text`, a document is automatically created from the input text, and the resulting document ID is returned in the response.
  Similarly, when using `/api/projects/{projectId}/infer-file`, if the file is a supported format (image, text or convertible), it is transformed into a document.
  The conversion process can be controlled via parameters such as **RasterizationDpi**, which can be set in the project settings.


  The resulting document ID is essential for:
  - Adding the document as an **in-context example** for other inference calls
  - Creating **playground items**


  If needed, inference can be run directly on any existing document by specifying its document ID.


  Additionally, when a file has been converted to a document, the original file ID remains available in the `docInfo`.
  This enables users to reuse the same file with different **conversion parameters** via the `/api/files/{fileId}/convert-to-document` endpoint, effectively generating alternate versions of the document from the same source file.

Inference **temperature** can be set in the project settings. It controls variability in extraction inference responses.
**RasterizationDpi** sets the dots per inch resolution when converting non-text files to images. Allowed range is (0, 300]

### Locking a Project

The **locking mechanism** allows you to prevent accidental modifications while still permitting inference. When locked:
- The **template and project examples** cannot be modified.
- Project settings such as **temperature** and **rasterizationDpi** are also restricted.
- Users can still perform inference and work with project playground.
- This feature is useful in **production environments** to maintain consistency.

### Project Ownership and Permissions

A project is owned by either a **user** (`ownerUser`) or an **organization** (`ownerOrganization`). If a user leaves an organization, they lose access to its resources, even if they originally created them.

### Additional Features

- **Duplication**: Projects can be **copied**, including examples but **excluding playground**.
- **Deletion**: Removing a project **deletes all associated examples and playground items**.
- **Sharing**: Projects can be shared with the community — in other words, they can be designated as **reference projects**. Sharing and unsharing require **Numind administrator access rights**.
- **Reference Projects**: These are **static, predefined projects** created by the Numind team to serve as examples of extraction tasks. The inference is allowed for all users. However, reference projects cannot be modified but can be **copied**, allowing users to make changes to their duplicates.

By structuring projects efficiently, leveraging examples, and using locking mechanisms, users can ensure **accurate, reproducible, and well-managed** information extraction workflows in NuExtract 2.0.
  

This Python package is automatically generated by the [OpenAPI Generator](https://openapi-generator.tech) project:

- API version: 1.0
- Package version: 1.0.0
- Generator version: 7.13.0
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
*DefaultApi* | [**get_api_debug_status_code**](docs/DefaultApi.md#get_api_debug_status_code) | **GET** /api/debug/status/{code} | 
*DefaultApi* | [**get_api_health**](docs/DefaultApi.md#get_api_health) | **GET** /api/health | 
*DefaultApi* | [**get_api_ping**](docs/DefaultApi.md#get_api_ping) | **GET** /api/ping | 
*DefaultApi* | [**get_api_version**](docs/DefaultApi.md#get_api_version) | **GET** /api/version | 
*DocumentsApi* | [**get_api_documents_documentid**](docs/DocumentsApi.md#get_api_documents_documentid) | **GET** /api/documents/{documentId} | 
*DocumentsApi* | [**get_api_documents_documentid_content**](docs/DocumentsApi.md#get_api_documents_documentid_content) | **GET** /api/documents/{documentId}/content | 
*DocumentsApi* | [**post_api_documents_text**](docs/DocumentsApi.md#post_api_documents_text) | **POST** /api/documents/text | 
*ExamplesApi* | [**delete_api_projects_projectid_examples_exampleid**](docs/ExamplesApi.md#delete_api_projects_projectid_examples_exampleid) | **DELETE** /api/projects/{projectId}/examples/{exampleId} | 
*ExamplesApi* | [**get_api_projects_projectid_examples**](docs/ExamplesApi.md#get_api_projects_projectid_examples) | **GET** /api/projects/{projectId}/examples | 
*ExamplesApi* | [**get_api_projects_projectid_examples_exampleid**](docs/ExamplesApi.md#get_api_projects_projectid_examples_exampleid) | **GET** /api/projects/{projectId}/examples/{exampleId} | 
*ExamplesApi* | [**post_api_projects_projectid_examples**](docs/ExamplesApi.md#post_api_projects_projectid_examples) | **POST** /api/projects/{projectId}/examples | 
*ExamplesApi* | [**put_api_projects_projectid_examples_exampleid**](docs/ExamplesApi.md#put_api_projects_projectid_examples_exampleid) | **PUT** /api/projects/{projectId}/examples/{exampleId} | 
*FilesApi* | [**get_api_files_fileid**](docs/FilesApi.md#get_api_files_fileid) | **GET** /api/files/{fileId} | 
*FilesApi* | [**get_api_files_fileid_content**](docs/FilesApi.md#get_api_files_fileid_content) | **GET** /api/files/{fileId}/content | 
*FilesApi* | [**post_api_files**](docs/FilesApi.md#post_api_files) | **POST** /api/files | 
*FilesApi* | [**post_api_files_fileid_convert_to_document**](docs/FilesApi.md#post_api_files_fileid_convert_to_document) | **POST** /api/files/{fileId}/convert-to-document | 
*InferenceApi* | [**post_api_infer_template**](docs/InferenceApi.md#post_api_infer_template) | **POST** /api/infer-template | 
*InferenceApi* | [**post_api_projects_projectid_infer_document_documentid**](docs/InferenceApi.md#post_api_projects_projectid_infer_document_documentid) | **POST** /api/projects/{projectId}/infer-document/{documentId} | 
*InferenceApi* | [**post_api_projects_projectid_infer_file**](docs/InferenceApi.md#post_api_projects_projectid_infer_file) | **POST** /api/projects/{projectId}/infer-file | 
*InferenceApi* | [**post_api_projects_projectid_infer_text**](docs/InferenceApi.md#post_api_projects_projectid_infer_text) | **POST** /api/projects/{projectId}/infer-text | 
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
*ProjectsApi* | [**delete_api_projects_projectid**](docs/ProjectsApi.md#delete_api_projects_projectid) | **DELETE** /api/projects/{projectId} | 
*ProjectsApi* | [**get_api_projects**](docs/ProjectsApi.md#get_api_projects) | **GET** /api/projects | 
*ProjectsApi* | [**get_api_projects_projectid**](docs/ProjectsApi.md#get_api_projects_projectid) | **GET** /api/projects/{projectId} | 
*ProjectsApi* | [**patch_api_projects_projectid**](docs/ProjectsApi.md#patch_api_projects_projectid) | **PATCH** /api/projects/{projectId} | 
*ProjectsApi* | [**patch_api_projects_projectid_settings**](docs/ProjectsApi.md#patch_api_projects_projectid_settings) | **PATCH** /api/projects/{projectId}/settings | 
*ProjectsApi* | [**post_api_projects**](docs/ProjectsApi.md#post_api_projects) | **POST** /api/projects | 
*ProjectsApi* | [**post_api_projects_projectid_duplicate**](docs/ProjectsApi.md#post_api_projects_projectid_duplicate) | **POST** /api/projects/{projectId}/duplicate | 
*ProjectsApi* | [**post_api_projects_projectid_lock**](docs/ProjectsApi.md#post_api_projects_projectid_lock) | **POST** /api/projects/{projectId}/lock | 
*ProjectsApi* | [**post_api_projects_projectid_reset_settings**](docs/ProjectsApi.md#post_api_projects_projectid_reset_settings) | **POST** /api/projects/{projectId}/reset-settings | 
*ProjectsApi* | [**post_api_projects_projectid_share**](docs/ProjectsApi.md#post_api_projects_projectid_share) | **POST** /api/projects/{projectId}/share | 
*ProjectsApi* | [**post_api_projects_projectid_unlock**](docs/ProjectsApi.md#post_api_projects_projectid_unlock) | **POST** /api/projects/{projectId}/unlock | 
*ProjectsApi* | [**post_api_projects_projectid_unshare**](docs/ProjectsApi.md#post_api_projects_projectid_unshare) | **POST** /api/projects/{projectId}/unshare | 


### Documentation For Models

 - [ApiKeyResponse](docs/ApiKeyResponse.md)
 - [ConvertRequest](docs/ConvertRequest.md)
 - [CreateOrUpdateApiKey](docs/CreateOrUpdateApiKey.md)
 - [CreateOrUpdateExampleRequest](docs/CreateOrUpdateExampleRequest.md)
 - [CreateOrUpdatePlaygroundItemRequest](docs/CreateOrUpdatePlaygroundItemRequest.md)
 - [CreateOrganizationRequest](docs/CreateOrganizationRequest.md)
 - [CreateProjectRequest](docs/CreateProjectRequest.md)
 - [DocumentInfo](docs/DocumentInfo.md)
 - [DocumentResponse](docs/DocumentResponse.md)
 - [Error](docs/Error.md)
 - [ExampleResponse](docs/ExampleResponse.md)
 - [FileResponse](docs/FileResponse.md)
 - [HealthResponse](docs/HealthResponse.md)
 - [ImageInfo](docs/ImageInfo.md)
 - [InferenceResponse](docs/InferenceResponse.md)
 - [InformationResponse](docs/InformationResponse.md)
 - [InvalidInformation](docs/InvalidInformation.md)
 - [InvitationResponse](docs/InvitationResponse.md)
 - [InviteMemberRequest](docs/InviteMemberRequest.md)
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
 - [UpdateOrganizationRequest](docs/UpdateOrganizationRequest.md)
 - [UpdateProjectRequest](docs/UpdateProjectRequest.md)
 - [UpdateProjectSettingsRequest](docs/UpdateProjectSettingsRequest.md)
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

