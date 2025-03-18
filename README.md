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
import os

from numind import NuMind

# Create a client object to interact with the API
# Providing the `api_key` is not required if the `NUMIND_API_KEY` environment variable
# is already set.
client = NuMind(api_key=os.environ["NUMIND_API_KEY"])

input_schema = {
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
project_id = client.post_api_reference_projects(input_schema)
input_text = """My dream vacation would be a month-long escape to the stunning islands of Tahiti.
I’d stay in an overwater bungalow in Bora Bora, waking up to crystal-clear turquoise waters and breathtaking sunrises.
Days would be spent snorkeling with vibrant marine life, paddleboarding over coral gardens, and basking on pristine white-sand beaches.
I’d explore lush rainforests, hidden waterfalls, and the rich Polynesian culture through traditional dance, music, and cuisine.
Evenings would be filled with romantic beachside dinners under the stars, with the soothing sound of waves as the perfect backdrop."""
output_schema = client.post_api_reference_projects_projectid_infer_text(project_id=project_id, text_request=input_text)
print(output_schema)
```

```json
{
    "destination": {
        "name": "Tahiti",
        "zip_code": null,
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

