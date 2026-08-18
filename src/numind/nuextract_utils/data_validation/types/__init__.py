"""Base types for the NuExtract models."""

import csv
import re
from pathlib import Path

from .base import SemanticType
from .bic import BIC
from .country import Country
from .currency import Currency
from .date_time import Date, DateTime, Time
from .duration import Duration
from .email_address import EmailAddress
from .geolocation import Geolocation
from .iban import IBAN
from .integer import Integer
from .language import Language
from .language_tag import LanguageTag
from .number import Number
from .phone_number import PhoneNumber
from .region import REGIONS_TYPES
from .script import Script
from .string_ import String
from .unit_code import UnitCode
from .url import URL
from .verbatim_string import VerbatimString

# Default types for NuExtract
NUEXTRACT_DEFAULT_TYPES = {
    "integer": Integer,
    "number": Number,
    "string": String,
    "verbatim-string": VerbatimString,
    "date": Date,
    "time": Time,
    "date-time": DateTime,
    "duration": Duration,
    "boolean": bool,
    "country": Country,
    "currency": Currency,
    "language": Language,
    "language-tag": LanguageTag,
    "script": Script,
    "url": URL,
    "email-address": EmailAddress,
    "phone-number": PhoneNumber,
    "iban": IBAN,
    "bic": BIC,
    "unit-code": UnitCode,
    **REGIONS_TYPES,
}


_FIELD_RE = re.compile(r"^\s*:(\w[\w-]*):\s*(.*)")


def _parse_docstring(docstring: str) -> tuple[str, str]:
    """
    Return ``(description, examples)`` parsed from an rST docstring.

    The description is the text before any ``:examples:`` field.  The examples
    value is the content of that field, with multi-line continuations joined into
    a single string.  Returns ``(description, None)`` when no ``:examples:``
    field is present.
    """
    lines = docstring.splitlines()

    examples_start: int | None = None
    for i, line in enumerate(lines):
        if re.match(r"\s*:examples:", line):
            examples_start = i
            break

    # --- description ---
    desc_lines = lines if examples_start is None else lines[:examples_start]
    description = " ".join(line.strip() for line in desc_lines).strip()

    if examples_start is None:
        return description, None

    # --- examples: collect the field line + non-empty continuation lines ---
    raw = [lines[examples_start]]
    for line in lines[examples_start + 1 :]:
        stripped = line.strip()
        if not stripped or _FIELD_RE.match(line):
            break
        raw.append(line)

    joined = " ".join(line.strip() for line in raw)
    m = re.match(r":examples:\s*(.*)", joined.strip())
    examples = m.group(1).strip() if m else None
    return description, examples or None


def _process_docstring(docstring: str) -> str:
    description, _ = _parse_docstring(docstring)
    return description


NUEXTRACT_DEFAULT_TYPES_DOCS = {
    type_name: _process_docstring(type_cls.__doc__)
    for type_name, type_cls in NUEXTRACT_DEFAULT_TYPES.items()
}
NUEXTRACT_DEFAULT_TYPES_DOCS["boolean"] = "A boolean being either `true` or `false`."

NUEXTRACT_DEFAULT_TYPES_EXAMPLES: dict[str, str] = {
    type_name: _parse_docstring(type_cls.__doc__)[1]
    for type_name, type_cls in NUEXTRACT_DEFAULT_TYPES.items()
}
NUEXTRACT_DEFAULT_TYPES_EXAMPLES["boolean"] = "`true`, `false`"


def export_types_csv(path: Path) -> None:
    """Export type metadata to a CSV file."""
    rows = [
        {
            "name": type_name,
            "description": NUEXTRACT_DEFAULT_TYPES_DOCS[type_name],
            "examples": NUEXTRACT_DEFAULT_TYPES_EXAMPLES.get(type_name) or "",
        }
        for type_name in NUEXTRACT_DEFAULT_TYPES
    ]
    with Path(path).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "description", "examples"])
        writer.writeheader()
        writer.writerows(rows)


# export_types_csv(Path("types.csv"))


__all__ = [
    "BIC",
    "IBAN",
    "NUEXTRACT_DEFAULT_TYPES",
    "URL",
    "Country",
    "Currency",
    "Date",
    "DateTime",
    "Duration",
    "EmailAddress",
    "Geolocation",
    "Integer",
    "Language",
    "LanguageTag",
    "Number",
    "PhoneNumber",
    "Script",
    "SemanticType",
    "String",
    "Time",
    "UnitCode",
    "VerbatimString",
]
