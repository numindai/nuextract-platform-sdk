"""Tests for conversion between NuExtract templates and Pydantic models."""

from __future__ import annotations

from datetime import date, datetime  # noqa: TC003
from enum import Enum
from typing import Annotated, Literal

import pytest
from pydantic import AnyUrl, BaseModel, Field, ValidationError

from numind.nuextract_utils.template_conversion import (
    convert_nuextract_template_to_pydantic_model,
    convert_pydantic_model_to_nuextract_template,
)


class InvoiceStatus(str, Enum):
    """Supported invoice workflow states."""

    DRAFT = "draft"
    APPROVED = "approved"
    PAID = "paid"


class Supplier(BaseModel):
    """Supplier details nested in an invoice."""

    name: str
    country: Annotated[
        str,
        Field(json_schema_extra={"format": "country-code-ISO_3166-1_2chars"}),
    ]
    established_on: date | None


class LineItem(BaseModel):
    """One invoiced product or service."""

    sku: str
    description: str
    quantity: int
    unit_price: float
    labels: list[Literal["fragile", "gift", "subscription"]]


class CompleteInvoice(BaseModel):
    """Large model covering every supported Pydantic schema shape."""

    document_id: Annotated[str, Field(json_schema_extra={"x-verbatim": True})]
    internal_reference: str = Field(alias="reference-id")
    source_url: AnyUrl
    issued_at: datetime
    due_date: date | None
    page_count: int
    total_amount: float
    paid: bool
    status: InvoiceStatus
    reviewers: list[str]
    tags: list[Literal["urgent", "finance", "international"]]
    supplier: Supplier
    related_suppliers: list[Supplier]
    line_items: list[LineItem]
    primary_bbox: tuple[int, int, int, int, int]
    notes: str | None = None


COMPLETE_NUEXTRACT_TEMPLATE = {
    "title": "string",
    "page_count": "integer",
    "confidence": "float",
    "paid": "boolean",
    "issued_at": "date-time",
    "status": ["draft", "approved", "paid"],
    "reviewers": ["string"],
    "tags": [["urgent", "finance", "international"]],
    "supplier": {
        "name": "string",
        "country": "string",
    },
    "line_items": [
        {
            "description": "string",
            "quantity": "integer",
        }
    ],
}


def test_nuextract_template_to_pydantic_supports_complete_nested_template() -> None:
    model = convert_nuextract_template_to_pydantic_model(
        COMPLETE_NUEXTRACT_TEMPLATE,
        class_name="GeneratedInvoice",
    )

    invoice = model(
        title="August invoice",
        page_count=3,
        confidence=0.98,
        paid=False,
        issued_at="2026-08-17T12:00:00Z",
        status="approved",
        reviewers=["Alice", "Bob"],
        tags=["urgent", "finance"],
        supplier={"name": "Paper Corp", "country": "FR"},
        line_items=[{"description": "Paper", "quantity": 10}],
    )

    assert model.__name__ == "GeneratedInvoice"
    assert invoice.status == "approved"
    assert invoice.tags == ["urgent", "finance"]
    assert invoice.supplier.name == "Paper Corp"
    assert invoice.line_items[0].quantity == 10


@pytest.mark.parametrize(
    ("field_name", "invalid_value"),
    [
        ("status", "cancelled"),
        ("tags", ["unknown"]),
        ("line_items", [{"description": "Paper"}]),
    ],
)
def test_nuextract_template_to_pydantic_rejects_invalid_nested_values(
    field_name: str,
    invalid_value: object,
) -> None:
    model = convert_nuextract_template_to_pydantic_model(COMPLETE_NUEXTRACT_TEMPLATE)
    values = {
        "title": "August invoice",
        "page_count": 3,
        "confidence": 0.98,
        "paid": False,
        "issued_at": "2026-08-17T12:00:00Z",
        "status": "approved",
        "reviewers": ["Alice", "Bob"],
        "tags": ["urgent", "finance"],
        "supplier": {"name": "Paper Corp", "country": "FR"},
        "line_items": [{"description": "Paper", "quantity": 10}],
    }
    values[field_name] = invalid_value

    with pytest.raises(ValidationError):
        model(**values)


def test_pydantic_to_nuextract_template_supports_complete_nested_model() -> None:
    template = convert_pydantic_model_to_nuextract_template(CompleteInvoice)

    assert template == {
        "document_id": "verbatim-string",
        "reference-id": "string",
        "source_url": "url",
        "issued_at": "date-time",
        "due_date": "date",
        "page_count": "integer",
        "total_amount": "number",
        "paid": "boolean",
        "status": ["draft", "approved", "paid"],
        "reviewers": ["string"],
        "tags": [["urgent", "finance", "international"]],
        "supplier": {
            "name": "string",
            "country": "country",
            "established_on": "date",
        },
        "related_suppliers": [
            {
                "name": "string",
                "country": "country",
                "established_on": "date",
            }
        ],
        "line_items": [
            {
                "sku": "string",
                "description": "string",
                "quantity": "integer",
                "unit_price": "number",
                "labels": [["fragile", "gift", "subscription"]],
            }
        ],
        "primary_bbox": ["integer"],
        "notes": "string",
    }


def test_pydantic_to_nuextract_template_rejects_primitive_union() -> None:
    class ModelWithPrimitiveUnion(BaseModel):
        value: str | int

    with pytest.raises(ValueError, match="ambiguous"):
        convert_pydantic_model_to_nuextract_template(ModelWithPrimitiveUnion)
