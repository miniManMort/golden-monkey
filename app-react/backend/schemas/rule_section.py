"""Rule section request and response models, normalization, and validation."""

from collections.abc import Mapping
from typing import Any

from pydantic import BaseModel

from ..errors import ApiError
from .common import plain_text

RULE_SECTION_FIELDS = ("name", "section_text")


class RuleSectionCreate(BaseModel):
    name: str
    section_text: str = "None"


class RuleSectionUpdate(RuleSectionCreate):
    pass


class RuleSectionRead(RuleSectionCreate):
    id: str


def prepare_rule_section(
    value: Mapping[str, Any], existing: Mapping[str, Any] | None = None
) -> RuleSectionCreate:
    return RuleSectionCreate.model_validate(
        _prepare_rule_section_data(value, existing)
    )


def prepare_rule_section_update(
    value: Mapping[str, Any], existing: Mapping[str, Any]
) -> RuleSectionUpdate:
    return RuleSectionUpdate.model_validate(
        _prepare_rule_section_data(value, existing)
    )


def _prepare_rule_section_data(
    value: Mapping[str, Any], existing: Mapping[str, Any] | None
) -> dict[str, Any]:
    data = dict(existing or {})
    data.update(
        {field: value[field] for field in RULE_SECTION_FIELDS if field in value}
    )
    data.setdefault("name", "")
    data.setdefault("section_text", "None")

    data["name"] = str(data["name"] if data["name"] is not None else "").strip()
    data["section_text"] = str(
        data["section_text"] if data["section_text"] is not None else ""
    ).strip()

    if not data["name"]:
        raise ApiError(400, "Name cannot be blank.")
    if not plain_text(data["section_text"]).strip():
        raise ApiError(400, "Section text cannot be blank.")
    return data
