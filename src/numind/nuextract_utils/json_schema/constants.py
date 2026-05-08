"""Constants for JSON schema."""

from __future__ import annotations

NUEXTRACT_TYPE_TO_JSON_SCHEMA_FORMAT = {
    "integer": "integer",
    "number": "number",
    "string": "string",
    "verbatim-string": "verbatim-string",
    "date": "date",
    "time": "time",
    "date-time": "date-time",
    "duration": "duration",
    "boolean": "boolean",
    "country": ("country-code-ISO_3166-1_2chars", "country-code"),
    "currency": ("currency-code-ISO_4217_3chars", "currency-code"),
    "language": ("language-code-ISO_639-3_3chars", "language-code"),
    "language-tag": ("language-tag-IETF-BCP-47", "language-tag"),
    "script": ("script-code-ISO_15924-4chars", "script-code"),
    "url": ("iri", "uri", "url"),
    "email-address": ("idn-email", "email", "email-address"),
    "phone-number": ("phone-number-E.164", "phone-number"),
    "iban": "iban-ISO_13616-1",
    "bic": "bice-code-ISO_9362",
    "unit-code": "ucum-unit-code",
}

REGION_COUNTRIES = (
    "US",
    "FR",
    "IE",
    "GB",
    "IT",
    "ES",
    "DE",
    "PT",
    "CA",
    "MX",
    "BR",
    "AU",
    "JP",
    "KR",
    "CN",
    "IN",
    "VN",
    "TH",
    "RU",
    "PL",
)
for region_country in REGION_COUNTRIES:
    NUEXTRACT_TYPE_TO_JSON_SCHEMA_FORMAT[f"region:{region_country}"] = (
        f"region-code-ISO_3166-2:{region_country}"
    )

JSON_SCHEMA_PRIMITIVES = {
    "string",
    "number",
    "integer",
    "boolean",
    "object",
    "array",
    "null",
}

ERR_INPUT_SCHEMA_NOT_JSON_DESERIALIZABLE = (
    "input schema JSON is not deserializable / RFC 8259 compliant"
)
ERR_INPUT_LINT_DANGLING_DEPENDENCY = (
    "input schema contains property in 'dependentRequired' is not defined in "
    "'properties'."
)
