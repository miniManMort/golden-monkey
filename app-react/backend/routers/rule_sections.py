"""Rule section API routes."""

from fastapi import APIRouter, HTTPException, status

from ..repositories import rule_sections
from ..schemas.rule_section import (
    RuleSectionCreate,
    RuleSectionRead,
    RuleSectionUpdate,
)

router = APIRouter(prefix="/api/rule-sections", tags=["rule-sections"])
alias_router = APIRouter(prefix="/api/rule_sections", tags=["rule-sections"])


@router.get("", response_model=list[RuleSectionRead])
def list_rule_sections() -> list[RuleSectionRead]:
    return rule_sections.list_rule_sections()


@router.get("/{record_id}", response_model=RuleSectionRead)
def get_rule_section(record_id: str) -> RuleSectionRead:
    record = rule_sections.get_rule_section(record_id)
    if record is None:
        raise HTTPException(404, "The selected record no longer exists.")
    return record


@router.post("", response_model=RuleSectionRead, status_code=status.HTTP_201_CREATED)
def create_rule_section(value: RuleSectionCreate) -> RuleSectionRead:
    return rule_sections.create_rule_section(value.model_dump())


@router.put("/{record_id}", response_model=RuleSectionRead)
def update_rule_section(record_id: str, value: RuleSectionUpdate) -> RuleSectionRead:
    record = rule_sections.update_rule_section(record_id, value.model_dump())
    if record is None:
        raise HTTPException(404, "The selected record no longer exists.")
    return record


@router.delete("/{record_id}")
def delete_rule_section(record_id: str) -> dict[str, bool]:
    if not rule_sections.delete_rule_section(record_id):
        raise HTTPException(404, "The selected record no longer exists.")
    return {"deleted": True}


@alias_router.get("", response_model=list[RuleSectionRead])
def list_rule_sections_alias() -> list[RuleSectionRead]:
    return rule_sections.list_rule_sections()


@alias_router.get("/{record_id}", response_model=RuleSectionRead)
def get_rule_section_alias(record_id: str) -> RuleSectionRead:
    return get_rule_section(record_id)


@alias_router.post("", response_model=RuleSectionRead, status_code=status.HTTP_201_CREATED)
def create_rule_section_alias(value: RuleSectionCreate) -> RuleSectionRead:
    return rule_sections.create_rule_section(value.model_dump())


@alias_router.put("/{record_id}", response_model=RuleSectionRead)
def update_rule_section_alias(
    record_id: str, value: RuleSectionUpdate
) -> RuleSectionRead:
    record = rule_sections.update_rule_section(record_id, value.model_dump())
    if record is None:
        raise HTTPException(404, "The selected record no longer exists.")
    return record


@alias_router.delete("/{record_id}")
def delete_rule_section_alias(record_id: str) -> dict[str, bool]:
    if not rule_sections.delete_rule_section(record_id):
        raise HTTPException(404, "The selected record no longer exists.")
    return {"deleted": True}
