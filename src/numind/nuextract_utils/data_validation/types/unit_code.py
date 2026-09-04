"""Unit type."""

from __future__ import annotations

import importlib.resources
from typing import TYPE_CHECKING
from xml.etree import ElementTree as ET

from .base import SemanticType

if TYPE_CHECKING:
    from numind.nuextract_utils.data_validation.models import ErrorJson

# UCUM units
UNITS = {}
PREFIXES = {}
with (
    importlib.resources.files("numind.nuextract_utils._iso_data")
    .joinpath("ucum-essence.xml")
    .open("rb") as _file
):
    tree = ET.parse(_file)  # noqa: S314 - trusted bundled XML
    root = tree.getroot()

    ns = {"ucum": "http://unitsofmeasure.org/ucum-essence"}
    # Find the base-unit element
    base_units = root.findall("ucum:base-unit", namespaces=ns) + root.findall(
        "ucum:unit", namespaces=ns
    )
    # Extract values
    for unit in base_units:
        unit_class = unit.attrib.get("class", "base-units")
        if unit_class is not None and unit_class in {"dimless", "const"}:
            continue
        is_metric = unit.attrib.get("isMetric", "yes").lower() != "no"
        unit_code = unit.attrib["Code"]
        if unit_code.startswith("["):
            unit_code = unit_code[1:-1]
        UNITS[unit_code] = {
            "name": unit.find("ucum:name", namespaces=ns).text,
            "property": unit.find("ucum:property", namespaces=ns).text,
            "class": unit_class,
            "is_metric": is_metric,
            "print_symbol": unit.attrib.get("printSymbol", None),
        }

    # Prefixes
    prefixes = root.findall("ucum:prefix", namespaces=ns)
    for prefix in prefixes:
        PREFIXES[prefix.attrib["Code"]] = {
            "name": prefix.find("ucum:name", namespaces=ns).text,
            "print_symbol": prefix.find("ucum:printSymbol", namespaces=ns).text,
            "value": float(prefix.find("ucum:value", namespaces=ns).attrib["value"]),
        }


class UnitCode(SemanticType):
    """
    A UCUM (Unified Code for Units of Measure) unit code.

    :examples: `m` (meter), `kg` (kilogram), `s` (second), `Hz` (hertz)
    """

    json_schema_format = "ucum-unit-code"

    @classmethod
    def coerce(
        cls,
        value: str,
        input_text: str | None = None,
        error: ErrorJson | None = None,
    ) -> str | None:
        """
        Try to convert a value to its string type.

        :param value: value to convert to string if it can, otherwise ``None``.
        :param input_text: input text.
        :param error: error associated to the value to convert. This argument
            can help to convert the value by targeting to the appropriate methods
            (default: ``None``).
        :return: a string value if the provided value can be converted, otherwise
            ``None``.
        """
        _ = input_text
        # No fix possible
        if error is not None:
            return None
        return value

    @classmethod
    def validate(cls, value: str, _: str | None = None) -> str | None:
        """
        Check that a string is not considered "null" (and thus should be ``None``).

        :param value: string value to assess.
        :param _: input text.
        :return: error message if the value should be ``None``, otherwise ``None``.
        """
        # Check that the value follows the predefined template
        try:
            cls.validate_code(value)
        except ValueError as e:
            return str(e)
        return None

    @staticmethod
    def validate_code(v: str) -> str:
        """Ensure code is UCUM."""
        if v not in UNITS:
            if v.lower() in UNITS:
                msg = "Unit code is in UCUM but not with the right casing"
            else:
                msg = "Unit code is not in UCUM units"
            raise ValueError(msg)
        return v
