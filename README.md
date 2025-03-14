# numind

API to interact with NuMind models.

## Requirements.

Python 3.8+

## Getting Started

### Installation

```sh
pip install numind
```

### Usage

```python
import numind
from numind.rest import ApiException

# Defining the host is optional and defaults to https://api.nuextract.ai/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = numind.Configuration(
    host = "https://api.nuextract.ai/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

configuration.access_token = os.environ["ACCESS_TOKEN"]


# Enter a context with an instance of the API client
with numind.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = numind.AuthenticationApi(api_client)
    user_token_id = 'user_token_id_example' # str | 

    try:
        api_instance.delete_api_auth_user_tokens_usertokenid(user_token_id)
    except ApiException as e:
        print("Exception when calling AuthenticationApi->delete_api_auth_user_tokens_usertokenid: %s\n" % e)
```

<a id="documentation-for-authorization"></a>
## Documentation For Authorization

Authentication schemes defined for the API:
<a id="oauth2Auth"></a>
### oauth2Auth

- **Type**: OAuth
- **Flow**: accessCode
- **Authorization URL**: https://users.numind.ai/realms/extract-platform/protocol/openid-connect/auth
- **Scopes**: 
 - **openid**: OpenID connect
 - **profile**: view profile
 - **email**: view email

