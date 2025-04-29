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

Most of the code of this SDK is generated from our [OpenAPI specification](https://nuextract.ai/docs) with [OpenAPI generator](https://openapi-generator.tech).
The documentation of the generated models and routes can be found in the [docs](docs) directory.
