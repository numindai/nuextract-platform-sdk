# numind.openapi_client.OrganizationsApi

All URIs are relative to *https://nuextract.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_api_organizations_organizationid**](OrganizationsApi.md#delete_api_organizations_organizationid) | **DELETE** /api/organizations/{organizationId} | 
[**delete_api_organizations_organizationid_members_invitations_invitationid**](OrganizationsApi.md#delete_api_organizations_organizationid_members_invitations_invitationid) | **DELETE** /api/organizations/{organizationId}/members/invitations/{invitationId} | 
[**delete_api_organizations_organizationid_members_userid**](OrganizationsApi.md#delete_api_organizations_organizationid_members_userid) | **DELETE** /api/organizations/{organizationId}/members/{userId} | 
[**get_api_organizations**](OrganizationsApi.md#get_api_organizations) | **GET** /api/organizations | 
[**get_api_organizations_organizationid_members**](OrganizationsApi.md#get_api_organizations_organizationid_members) | **GET** /api/organizations/{organizationId}/members | 
[**get_api_organizations_organizationid_members_invitations**](OrganizationsApi.md#get_api_organizations_organizationid_members_invitations) | **GET** /api/organizations/{organizationId}/members/invitations | 
[**post_api_organizations**](OrganizationsApi.md#post_api_organizations) | **POST** /api/organizations | 
[**post_api_organizations_organizationid_members**](OrganizationsApi.md#post_api_organizations_organizationid_members) | **POST** /api/organizations/{organizationId}/members | 
[**put_api_organizations_organizationid**](OrganizationsApi.md#put_api_organizations_organizationid) | **PUT** /api/organizations/{organizationId} | 


# **delete_api_organizations_organizationid**
> delete_api_organizations_organizationid(organization_id)


Delete a specific organization, and all its associated objects. Calling this method with an api key will result in a 403 (forbidden) error.

#### Error Responses:
`404 Not Found` - If an organization with the specified id does not exist.

`403 Forbidden` - If the user does not have permission to delete this organization


### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://nuextract.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = numind.openapi_client.Configuration(
    host = "https://nuextract.ai"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
with numind.openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = numind.openapi_client.OrganizationsApi(api_client)
    organization_id = 'organization_id_example' # str | identifier for the organization

    try:
        api_instance.delete_api_organizations_organizationid(organization_id)
    except Exception as e:
        print("Exception when calling OrganizationsApi->delete_api_organizations_organizationid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_id** | **str**| identifier for the organization | 

### Return type

void (empty response body)

### Authorization

[oauth2Auth](../README.md#oauth2Auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_api_organizations_organizationid_members_invitations_invitationid**
> delete_api_organizations_organizationid_members_invitations_invitationid(organization_id, invitation_id)


Delete an invitation. Can be used to then create a new one for the user. Calling this method with an api key will result in a 403 (forbidden) error.

#### Error Responses:
`404 Not Found` - If an organization with the specified id does not exist,
or if the invitationId is not valid


### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://nuextract.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = numind.openapi_client.Configuration(
    host = "https://nuextract.ai"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
with numind.openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = numind.openapi_client.OrganizationsApi(api_client)
    organization_id = 'organization_id_example' # str | identifier for the organization
    invitation_id = 'invitation_id_example' # str | 

    try:
        api_instance.delete_api_organizations_organizationid_members_invitations_invitationid(organization_id, invitation_id)
    except Exception as e:
        print("Exception when calling OrganizationsApi->delete_api_organizations_organizationid_members_invitations_invitationid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_id** | **str**| identifier for the organization | 
 **invitation_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[oauth2Auth](../README.md#oauth2Auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_api_organizations_organizationid_members_userid**
> delete_api_organizations_organizationid_members_userid(organization_id, user_id)


Remove a member from an organization. Calling this method with an api key will result in a 403 (forbidden) error.

#### Error Responses:
`404 Not Found` - If an organization with the specified id does not exist,
or if the member with the given memberId does not exist.


### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://nuextract.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = numind.openapi_client.Configuration(
    host = "https://nuextract.ai"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
with numind.openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = numind.openapi_client.OrganizationsApi(api_client)
    organization_id = 'organization_id_example' # str | identifier for the organization
    user_id = 'user_id_example' # str | Unique identifier of the user.

    try:
        api_instance.delete_api_organizations_organizationid_members_userid(organization_id, user_id)
    except Exception as e:
        print("Exception when calling OrganizationsApi->delete_api_organizations_organizationid_members_userid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_id** | **str**| identifier for the organization | 
 **user_id** | **str**| Unique identifier of the user. | 

### Return type

void (empty response body)

### Authorization

[oauth2Auth](../README.md#oauth2Auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_api_organizations**
> List[OrganizationResponse] get_api_organizations()


Returns the organizations for the current user. Calling this method with an api key will result in a 403 (forbidden) error.


### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.organization_response import OrganizationResponse
from numind.openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://nuextract.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = numind.openapi_client.Configuration(
    host = "https://nuextract.ai"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
with numind.openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = numind.openapi_client.OrganizationsApi(api_client)

    try:
        api_response = api_instance.get_api_organizations()
        print("The response of OrganizationsApi->get_api_organizations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationsApi->get_api_organizations: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[OrganizationResponse]**](OrganizationResponse.md)

### Authorization

[oauth2Auth](../README.md#oauth2Auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_api_organizations_organizationid_members**
> List[MemberResponse] get_api_organizations_organizationid_members(organization_id)


List the members of an organization. Calling this method with an api key will result in a 403 (forbidden) error.

#### Error Responses:
`404 Not Found` - If an organization with the specified id does not exist.


### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.member_response import MemberResponse
from numind.openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://nuextract.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = numind.openapi_client.Configuration(
    host = "https://nuextract.ai"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
with numind.openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = numind.openapi_client.OrganizationsApi(api_client)
    organization_id = 'organization_id_example' # str | identifier for the organization

    try:
        api_response = api_instance.get_api_organizations_organizationid_members(organization_id)
        print("The response of OrganizationsApi->get_api_organizations_organizationid_members:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationsApi->get_api_organizations_organizationid_members: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_id** | **str**| identifier for the organization | 

### Return type

[**List[MemberResponse]**](MemberResponse.md)

### Authorization

[oauth2Auth](../README.md#oauth2Auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_api_organizations_organizationid_members_invitations**
> List[InvitationResponse] get_api_organizations_organizationid_members_invitations(organization_id)


List all the pending invitations for a given organization. Calling this method with an api key will result in a 403 (forbidden) error.

#### Error Responses:
`404 Not Found` - If an organization with the specified id does not exist


### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.invitation_response import InvitationResponse
from numind.openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://nuextract.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = numind.openapi_client.Configuration(
    host = "https://nuextract.ai"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
with numind.openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = numind.openapi_client.OrganizationsApi(api_client)
    organization_id = 'organization_id_example' # str | identifier for the organization

    try:
        api_response = api_instance.get_api_organizations_organizationid_members_invitations(organization_id)
        print("The response of OrganizationsApi->get_api_organizations_organizationid_members_invitations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationsApi->get_api_organizations_organizationid_members_invitations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_id** | **str**| identifier for the organization | 

### Return type

[**List[InvitationResponse]**](InvitationResponse.md)

### Authorization

[oauth2Auth](../README.md#oauth2Auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_api_organizations**
> OrganizationResponse post_api_organizations(create_organization_request)


Creates an organization with the current user as member.
The name does not need to be unique. Calling this method with an api key will result in a 403 (forbidden) error.

#### Response:
 Returns a JSON representing the created organization.


### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.create_organization_request import CreateOrganizationRequest
from numind.models.organization_response import OrganizationResponse
from numind.openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://nuextract.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = numind.openapi_client.Configuration(
    host = "https://nuextract.ai"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
with numind.openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = numind.openapi_client.OrganizationsApi(api_client)
    create_organization_request = {"name":"example organization"} # CreateOrganizationRequest | 

    try:
        api_response = api_instance.post_api_organizations(create_organization_request)
        print("The response of OrganizationsApi->post_api_organizations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationsApi->post_api_organizations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_organization_request** | [**CreateOrganizationRequest**](CreateOrganizationRequest.md)|  | 

### Return type

[**OrganizationResponse**](OrganizationResponse.md)

### Authorization

[oauth2Auth](../README.md#oauth2Auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, text/plain

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**400** | Invalid value for: body |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_api_organizations_organizationid_members**
> post_api_organizations_organizationid_members(organization_id, invite_member_request)


Invite someone to an organization. Calling this method with an api key will result in a 403 (forbidden) error.
The person to invite does not need to have an account when invited,
she will be added once the account is activated.


#### Error Responses:
`404 Not Found` - If an organization with the specified id does not exist.


### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.invite_member_request import InviteMemberRequest
from numind.openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://nuextract.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = numind.openapi_client.Configuration(
    host = "https://nuextract.ai"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
with numind.openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = numind.openapi_client.OrganizationsApi(api_client)
    organization_id = 'organization_id_example' # str | identifier for the organization
    invite_member_request = {"email":"user@example.com"} # InviteMemberRequest | 

    try:
        api_instance.post_api_organizations_organizationid_members(organization_id, invite_member_request)
    except Exception as e:
        print("Exception when calling OrganizationsApi->post_api_organizations_organizationid_members: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_id** | **str**| identifier for the organization | 
 **invite_member_request** | [**InviteMemberRequest**](InviteMemberRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

[oauth2Auth](../README.md#oauth2Auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: text/plain, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**400** | Invalid value for: body |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_api_organizations_organizationid**
> OrganizationResponse put_api_organizations_organizationid(organization_id, update_organization_request)


Update a specific organization. Calling this method with an api key will result in a 403 (forbidden) error.

#### Error Responses:
`404 Not Found` - If an organization with the specified id does not exist.

`403 Forbidden` - If the user does not have permission to change this organization


### Example

* OAuth Authentication (oauth2Auth):

```python
import numind.openapi_client
from numind.models.organization_response import OrganizationResponse
from numind.models.update_organization_request import UpdateOrganizationRequest
from numind.openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://nuextract.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = numind.openapi_client.Configuration(
    host = "https://nuextract.ai"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
with numind.openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = numind.openapi_client.OrganizationsApi(api_client)
    organization_id = 'organization_id_example' # str | identifier for the organization
    update_organization_request = {"name":"new name"} # UpdateOrganizationRequest | 

    try:
        api_response = api_instance.put_api_organizations_organizationid(organization_id, update_organization_request)
        print("The response of OrganizationsApi->put_api_organizations_organizationid:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationsApi->put_api_organizations_organizationid: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_id** | **str**| identifier for the organization | 
 **update_organization_request** | [**UpdateOrganizationRequest**](UpdateOrganizationRequest.md)|  | 

### Return type

[**OrganizationResponse**](OrganizationResponse.md)

### Authorization

[oauth2Auth](../README.md#oauth2Auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, text/plain

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**400** | Invalid value for: body |  -  |
**0** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

