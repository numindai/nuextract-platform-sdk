"""Tests for error detection."""

from __future__ import annotations

import pytest

from numind.nuextract_utils.data_validation import (
    correct_output_json_and_input_template,
    detect_errors_in_input_template,
    detect_errors_in_output_json,
)
from numind.nuextract_utils.data_validation.constants import (
    ERR_INPUT_SCHEMA_LEAF_TYPE_INVALID,
    ERR_LABEL_ENUM_VALUE_NOT_IN_INPUT_SCHEMA,
    ERR_LABEL_LEAF_TYPE_INVALID,
    ERR_LABEL_MISSING_NODE_FROM_INPUT_SCHEMA,
    ERR_LABEL_NODE_NOT_IN_INPUT_SCHEMA,
)
from numind.nuextract_utils.data_validation.models import ErrorJson
from numind.nuextract_utils.data_validation.types import NUEXTRACT_DEFAULT_TYPES
from numind.nuextract_utils.data_validation.types.country import (
    ERR_LABEL_COUNTRY_ISO_3166_COMPLIANT_BUT_CASE_INSENSITIVE,
    ERR_LABEL_COUNTRY_NOT_ISO_3166_COMPLIANT,
)
from numind.nuextract_utils.data_validation.types.currency import (
    ERR_LABEL_CURRENCY_CODE_NOT_ISO_4217_COMPLIANT,
    ERR_LABEL_CURRENCY_ISO_4217_COMPLIANT_BUT_CASE_INSENSITIVE,
)
from numind.nuextract_utils.data_validation.types.email_address import (
    ERR_LABEL_EMAIL_ADDRESS_IS_MALFORMED,
)
from numind.nuextract_utils.data_validation.types.geolocation import (
    ERR_LABEL_LEAF_VALUE_IS_GEOLOCATION_BUT_IN_MESSY_STRING,
    ERR_LABEL_LEAF_VALUE_IS_NOT_A_GEOLOCATION,
    Geolocation,
)
from numind.nuextract_utils.data_validation.types.language import (
    ERR_LABEL_LANGUAGE_CODE_NOT_ISO_639_COMPLIANT,
    ERR_LABEL_LANGUAGE_ISO_639_COMPLIANT_BUT_CASE_INSENSITIVE,
)
from numind.nuextract_utils.data_validation.types.language_tag import (
    ERR_LABEL_LANGUAGE_TAG_NOT_RFC_5646_COMPLIANT,
)
from numind.nuextract_utils.data_validation.types.phone_number import (
    ERR_LABEL_PHONE_NUMBER_IS_VALID_BUT_IN_MESSY_STRING,
)
from numind.nuextract_utils.data_validation.types.region import (
    ERR_LABEL_REGION_ISO_3166_COMPLIANT_BUT_CASE_INSENSITIVE,
    ERR_LABEL_REGION_NOT_ISO_3166_COMPLIANT,
)
from numind.nuextract_utils.data_validation.types.script import (
    ERR_LABEL_SCRIPT_CODE_NOT_ISO_15924_COMPLIANT,
    ERR_LABEL_SCRIPT_ISO_15924_COMPLIANT_BUT_CASE_INSENSITIVE,
)
from numind.nuextract_utils.data_validation.types.url import ERR_LABEL_URL_IS_MALFORMED
from numind.nuextract_utils.data_validation.types.verbatim_string import (
    ERR_LABEL_VERBATIM_STRING_ABSENT_FROM_INPUT,
)

NUEXTRACT_DEFAULT_TYPES.update({"geolocation": Geolocation})

# schema_input,
# schema_output,
# text_input,
# expected_input_errors,
# expected_output_errors,
# expected_corrected_input_schema,
# expected_corrected_output_schema,
TEST_CASES = [
    (
        {
            "test1": "string",
            "int1": "integer",
            "verbstr1": "verbatim-string",
            "verbstr2": "verbatim-string",
            "countries": ["country"],
            "regions": ["region:US"],
            "currencies": ["currency"],
            "languages": ["language"],
            "scripts": ["script"],
            "language-tags": ["language-tag"],
            "urls": ["url"],
            "email-addresses": ["email-address"],
            "phone-numbers": ["phone-number"],
            "geolocations": ["geolocation"],
            "ibans": ["iban"],
            "bics": ["bic"],
            "bool": "boolean",
        },
        {
            "test1": "a text",
            "int1": "2.0",
            "verbstr1": "cat",
            "verbstr2": "map",
            "countries": ["PF", "USB", "Portugal", "us", "fra"],
            "regions": ["CA", "ny", "michigan", "hawaii🌊"],
            "currencies": ["EUR", "EURO", "New Zealand Dollar", "usD", "BYR"],
            "languages": ["haw", "Gumuz", "notal", "french", "ENG", "Spanish"],
            "scripts": ["Thai", "Tibetan", "notas", "latin", "KORE"],
            "urls": ["https://numind.ai", "google.com"],
            "email-addresses": ["user@example.com", "user2 at example dot com"],
            "phone-numbers": ["Mon numéro : 06 77 83 04 29", "+442071234567"],
            "language-tags": ["en-US", "en_gb", "fr_FR", "fzdfdzgq"],
            "geolocations": [
                "-17.022844-149.595818",
                "40.7128, -74.0060",
                "40° 65' 46\" N, 74° 0' 21\" W",
            ],
            "ibans": ["FR7630006000011234567890189"],
            "bics": ["BNPAFRPP"],
            "bool": True,
        },
        "The cat sat on the mat.",
        [],
        [
            (["int1"], ERR_LABEL_LEAF_TYPE_INVALID, "2.0"),
            (["verbstr2"], ERR_LABEL_VERBATIM_STRING_ABSENT_FROM_INPUT, "map"),
            (["countries", 1], ERR_LABEL_COUNTRY_NOT_ISO_3166_COMPLIANT, "USB"),
            (["countries", 2], ERR_LABEL_COUNTRY_NOT_ISO_3166_COMPLIANT, "Portugal"),
            (
                ["countries", 3],
                ERR_LABEL_COUNTRY_ISO_3166_COMPLIANT_BUT_CASE_INSENSITIVE,
                "us",
            ),
            (["countries", 4], ERR_LABEL_COUNTRY_NOT_ISO_3166_COMPLIANT, "fra"),
            (
                ["regions", 1],
                ERR_LABEL_REGION_ISO_3166_COMPLIANT_BUT_CASE_INSENSITIVE,
                "ny",
            ),
            (["regions", 2], ERR_LABEL_REGION_NOT_ISO_3166_COMPLIANT, "michigan"),
            (["regions", 3], ERR_LABEL_REGION_NOT_ISO_3166_COMPLIANT, "hawaii🌊"),
            (["currencies", 1], ERR_LABEL_CURRENCY_CODE_NOT_ISO_4217_COMPLIANT, "EURO"),
            (
                ["currencies", 2],
                ERR_LABEL_CURRENCY_CODE_NOT_ISO_4217_COMPLIANT,
                "New Zealand Dollar",
            ),
            (
                ["currencies", 3],
                ERR_LABEL_CURRENCY_ISO_4217_COMPLIANT_BUT_CASE_INSENSITIVE,
                "usD",
            ),
            (["languages", 1], ERR_LABEL_LANGUAGE_CODE_NOT_ISO_639_COMPLIANT, "Gumuz"),
            (["languages", 2], ERR_LABEL_LANGUAGE_CODE_NOT_ISO_639_COMPLIANT, "notal"),
            (["languages", 3], ERR_LABEL_LANGUAGE_CODE_NOT_ISO_639_COMPLIANT, "french"),
            (
                ["languages", 4],
                ERR_LABEL_LANGUAGE_ISO_639_COMPLIANT_BUT_CASE_INSENSITIVE,
                "ENG",
            ),
            (
                ["languages", 5],
                ERR_LABEL_LANGUAGE_CODE_NOT_ISO_639_COMPLIANT,
                "Spanish",
            ),
            (["scripts", 1], ERR_LABEL_SCRIPT_CODE_NOT_ISO_15924_COMPLIANT, "Tibetan"),
            (["scripts", 2], ERR_LABEL_SCRIPT_CODE_NOT_ISO_15924_COMPLIANT, "notas"),
            (["scripts", 3], ERR_LABEL_SCRIPT_CODE_NOT_ISO_15924_COMPLIANT, "latin"),
            (
                ["scripts", 4],
                ERR_LABEL_SCRIPT_ISO_15924_COMPLIANT_BUT_CASE_INSENSITIVE,
                "KORE",
            ),
            (["urls", 1], ERR_LABEL_URL_IS_MALFORMED, "google.com"),
            (
                ["email-addresses", 1],
                ERR_LABEL_EMAIL_ADDRESS_IS_MALFORMED,
                "user2 at example dot com",
            ),
            (
                ["phone-numbers", 0],
                ERR_LABEL_PHONE_NUMBER_IS_VALID_BUT_IN_MESSY_STRING,
                "Mon numéro : 06 77 83 04 29",
            ),
            (
                ["language-tags", 1],
                ERR_LABEL_LANGUAGE_TAG_NOT_RFC_5646_COMPLIANT,
                "en_gb",
            ),
            (
                ["language-tags", 2],
                ERR_LABEL_LANGUAGE_TAG_NOT_RFC_5646_COMPLIANT,
                "fr_FR",
            ),
            (
                ["language-tags", 3],
                ERR_LABEL_LANGUAGE_TAG_NOT_RFC_5646_COMPLIANT,
                "fzdfdzgq",
            ),
            (
                ["geolocations", 1],
                ERR_LABEL_LEAF_VALUE_IS_GEOLOCATION_BUT_IN_MESSY_STRING,
                "40.7128, -74.0060",
            ),
            (
                ["geolocations", 2],
                ERR_LABEL_LEAF_VALUE_IS_NOT_A_GEOLOCATION,
                "40° 65' 46\" N, 74° 0' 21\" W",
            ),
        ],
        None,  # identical corrected schema (no errors)
        {
            "test1": "a text",
            "int1": 2,
            "verbstr1": "cat",
            "verbstr2": "mat",
            "countries": ["PF", "PT", "US", "FR"],
            "regions": ["CA", "NY", "MI"],
            "currencies": ["EUR", "NZD", "USD", "BYR"],
            "languages": ["haw", "guk", "fra", "eng", "spa"],
            "scripts": ["Thai", "Tibt", "Latn", "Kore"],
            "urls": ["https://numind.ai", "https://google.com"],
            "email-addresses": ["user@example.com", "user2@example.com"],
            "phone-numbers": ["0677830429", "+442071234567"],
            "language-tags": ["en-US", "en-GB", "fr-FR"],
            "geolocations": ["-17.022844-149.595818", "+40.712800-074.006000"],
            "ibans": ["FR7630006000011234567890189"],
            "bics": ["BNPAFRPP"],
            "bool": True,
        },
    ),
    (
        {
            "test1": "string",
            "test2": "Integer",
            "regions_invalid": "region:fr",
            "enum": ["item1", "item54", "something else"],
            "level": {"node_a": "integer"},
        },
        {
            "test1": "a text",
            "foo": "bar",
            "enum": "item",  # value missing from input list
            "level": {"node_b": 4},  # node name missing from input schema
        },
        None,
        [
            (["test2"], ERR_INPUT_SCHEMA_LEAF_TYPE_INVALID, "Integer"),
            (["regions_invalid"], ERR_INPUT_SCHEMA_LEAF_TYPE_INVALID, "region:fr"),
        ],
        [
            (["test2"], ERR_LABEL_MISSING_NODE_FROM_INPUT_SCHEMA, None),
            (["regions_invalid"], ERR_LABEL_MISSING_NODE_FROM_INPUT_SCHEMA, None),
            (["foo"], ERR_LABEL_NODE_NOT_IN_INPUT_SCHEMA, "foo"),
            (["enum"], ERR_LABEL_ENUM_VALUE_NOT_IN_INPUT_SCHEMA, "item"),
            (["level", "node_a"], ERR_LABEL_MISSING_NODE_FROM_INPUT_SCHEMA, None),
            (["level", "node_b"], ERR_LABEL_NODE_NOT_IN_INPUT_SCHEMA, "node_b"),
        ],
        {
            "test1": "string",
            "test2": "integer",
            "enum": ["item1", "item54", "something else"],
            "level": {"node_a": "integer"},
        },
        {
            "test1": "a text",
            "test2": None,
            "enum": "item1",
            "level": {"node_a": 4},
        },
    ),
]


@pytest.mark.parametrize(
    (
        "schema_input",
        "schema_output",
        "text_input",
        "input_errors_expected",
        "output_errors_expected",
    ),
    [case[:5] for case in TEST_CASES],
)
def test_error_detection(
    schema_input: dict,
    schema_output: dict,
    text_input: str | None,
    input_errors_expected: list[tuple[list[str | int], str]],
    output_errors_expected: list[tuple[list[str | int], str]],
) -> None:
    input_errors = detect_errors_in_input_template(schema_input)
    assert {err.to_json() for err in input_errors} == {
        ErrorJson(path, msg, val_err).to_json()
        for path, msg, val_err in input_errors_expected
    }
    output_errors = detect_errors_in_output_json(schema_input, schema_output, text_input)
    assert {err.to_json() for err in output_errors} == {
        ErrorJson(path, msg, val_err).to_json()
        for path, msg, val_err in output_errors_expected
    }


@pytest.mark.parametrize(
    (
        "schema_input",
        "schema_output",
        "text_input",
        "schema_input_corrected_expected",
        "schema_output_corrected_expected",
    ),
    [case[:3] + case[5:] for case in TEST_CASES],
)
def test_error_correction(
    schema_input: dict,
    schema_output: dict,
    text_input: str | None,
    schema_input_corrected_expected: dict | None,
    schema_output_corrected_expected: dict | None,
) -> None:
    if schema_input_corrected_expected is None:
        schema_input_corrected_expected = schema_input.copy()
    if schema_output_corrected_expected is None:
        schema_output_corrected_expected = schema_output.copy()
    schema_input_corrected, schema_output_corrected = correct_output_json_and_input_template(
        schema_input, schema_output, text_input, deduplicate_arrays_entries=True
    )[:2]  # excluding fixed errors lists
    assert schema_input_corrected == schema_input_corrected_expected
    assert schema_output_corrected == schema_output_corrected_expected

