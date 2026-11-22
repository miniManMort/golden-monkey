"""Character class profile API routes."""

from fastapi import APIRouter, HTTPException, status

from ..repositories import character_classes
from ..schemas.character_class import (
    CharacterClassCreate,
    CharacterClassRead,
    CharacterClassUpdate,
)

router = APIRouter(prefix="/api/character-classes", tags=["character-classes"])
alias_router = APIRouter(prefix="/api/character_classes", tags=["character-classes"])


@router.get("", response_model=list[CharacterClassRead])
def list_character_classes() -> list[CharacterClassRead]:
    return character_classes.list_character_classes()


@router.get("/{record_id}", response_model=CharacterClassRead)
def get_character_class(record_id: str) -> CharacterClassRead:
    record = character_classes.get_character_class(record_id)
    if record is None:
        raise HTTPException(
            status_code=404, detail="The selected record no longer exists."
        )
    return record


@router.post("", response_model=CharacterClassRead, status_code=status.HTTP_201_CREATED)
def create_character_class(value: CharacterClassCreate) -> CharacterClassRead:
    return character_classes.create_character_class(value.model_dump())


@router.put("/{record_id}", response_model=CharacterClassRead)
def update_character_class(
    record_id: str, value: CharacterClassUpdate
) -> CharacterClassRead:
    record = character_classes.update_character_class(
        record_id, value.model_dump()
    )
    if record is None:
        raise HTTPException(
            status_code=404, detail="The selected record no longer exists."
        )
    return record


@router.delete("/{record_id}")
def delete_character_class(record_id: str) -> dict[str, bool]:
    if not character_classes.delete_character_class(record_id):
        raise HTTPException(
            status_code=404, detail="The selected record no longer exists."
        )
    return {"deleted": True}


@alias_router.get("", response_model=list[CharacterClassRead])
def list_character_classes_alias() -> list[CharacterClassRead]:
    return character_classes.list_character_classes()


@alias_router.get("/{record_id}", response_model=CharacterClassRead)
def get_character_class_alias(record_id: str) -> CharacterClassRead:
    return get_character_class(record_id)


@alias_router.post("", response_model=CharacterClassRead, status_code=status.HTTP_201_CREATED)
def create_character_class_alias(value: CharacterClassCreate) -> CharacterClassRead:
    return character_classes.create_character_class(value.model_dump())


@alias_router.put("/{record_id}", response_model=CharacterClassRead)
def update_character_class_alias(
    record_id: str, value: CharacterClassUpdate
) -> CharacterClassRead:
    record = character_classes.update_character_class(record_id, value.model_dump())
    if record is None:
        raise HTTPException(
            status_code=404, detail="The selected record no longer exists."
        )
    return record


@alias_router.delete("/{record_id}")
def delete_character_class_alias(record_id: str) -> dict[str, bool]:
    if not character_classes.delete_character_class(record_id):
        raise HTTPException(
            status_code=404, detail="The selected record no longer exists."
        )
    return {"deleted": True}
