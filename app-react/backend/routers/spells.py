"""Spell profile API routes."""

from fastapi import APIRouter, HTTPException, status

from ..repositories import spells
from ..schemas.spell import SpellCreate, SpellRead, SpellUpdate

router = APIRouter(prefix="/api/spells", tags=["spells"])


@router.get("", response_model=list[SpellRead])
def list_spells() -> list[SpellRead]:
    return spells.list_spells()


@router.get("/{record_id}", response_model=SpellRead)
def get_spell(record_id: str) -> SpellRead:
    record = spells.get_spell(record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="The selected record no longer exists.")
    return record


@router.post("", response_model=SpellRead, status_code=status.HTTP_201_CREATED)
def create_spell(value: SpellCreate) -> SpellRead:
    return spells.create_spell(value.model_dump())


@router.put("/{record_id}", response_model=SpellRead)
def update_spell(record_id: str, value: SpellUpdate) -> SpellRead:
    record = spells.update_spell(record_id, value.model_dump())
    if record is None:
        raise HTTPException(status_code=404, detail="The selected record no longer exists.")
    return record


@router.delete("/{record_id}")
def delete_spell(record_id: str) -> dict[str, bool]:
    if not spells.delete_spell(record_id):
        raise HTTPException(status_code=404, detail="The selected record no longer exists.")
    return {"deleted": True}
