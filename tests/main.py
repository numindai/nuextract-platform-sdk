"""Test the NuMind client programmatically"""

if __name__ == "__main__":
    from argparse import ArgumentParser
    from pathlib import Path

    from numind import NuMind
    from numind.openapi_client.models import TextRequest, CreateOrUpdateProjectRequest

    parser = ArgumentParser(description="Dataset creation script")
    parser.add_argument("--numind-api-key", type=str, required=False)
    args = vars(parser.parse_args())

    client = NuMind(api_key=args["numind_api_key"])
    projects = client.get_api_reference_projects(shared=True)

    # Create a project
    input_schema = {
        "destination": {
            "name": "verbatim-string",
            "zip_code": "string",
            "country": "string",
        },
        "accommodation": "verbatim-string",
        "activities": ["verbatim-string"],
        "duration": {
            "time_unit": ["day", "week", "month", "year"],
            "time_quantity": "integer",
        },
    }
    project_creation_response = client.post_api_reference_projects(
        CreateOrUpdateProjectRequest(
            name="vacation", description="", template=input_schema
        )
    )
    project_id = project_creation_response.id
    # project_id = "7218c55b-dc6e-4567-b816-cb6c34919fba"

    # Infer with text
    input_text = """My dream vacation would be a month-long escape to the stunning islands of Tahiti.
    I’d stay in an overwater bungalow in Bora Bora, waking up to crystal-clear turquoise waters and breathtaking sunrises.
    Days would be spent snorkeling with vibrant marine life, paddleboarding over coral gardens, and basking on pristine white-sand beaches.
    I’d explore lush rainforests, hidden waterfalls, and the rich Polynesian culture through traditional dance, music, and cuisine.
    Evenings would be filled with romantic beachside dinners under the stars, with the soothing sound of waves as the perfect backdrop."""
    text_request = TextRequest(text=input_text)
    # TODO make it usable without using TextRequest/FileRequest
    output_response = client.post_api_reference_projects_projectid_infer_text(
        project_id, text_request=text_request
    )

    # Infer with file
    input_file_path = Path("tests/test_cases/vacation/files/vacation.docx")
    with input_file_path.open("rb") as file:
        intput_file = file.read()
    o = client.post_api_reference_projects_projectid_infer_file(
        project_id, input_file_path.name, intput_file
    )
    t = 0
