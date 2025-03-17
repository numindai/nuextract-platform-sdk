"""Test the NuMind client programmatically"""


if __name__ == "__main__":
    from argparse import ArgumentParser

    from numind import NuMind

    parser = ArgumentParser(description="Dataset creation script")
    parser.add_argument("--numind-api-key", type=str, required=False)
    args = vars(parser.parse_args())

    client = NuMind(api_key=args["numind_api_key"])

    input_text = """My dream vacation would be a month-long escape to the stunning islands of Tahiti.
    I’d stay in an overwater bungalow in Bora Bora, waking up to crystal-clear turquoise waters and breathtaking sunrises.
    Days would be spent snorkeling with vibrant marine life, paddleboarding over coral gardens, and basking on pristine white-sand beaches.
    I’d explore lush rainforests, hidden waterfalls, and the rich Polynesian culture through traditional dance, music, and cuisine.
    Evenings would be filled with romantic beachside dinners under the stars, with the soothing sound of waves as the perfect backdrop."""
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
    project_ids = client.get_api_reference_projects(shared=False)
    output_schema = client.post_api_reference_projects_projectid_infer_text(project_id="my_project_id", text_request=input_text)
    t = 0
