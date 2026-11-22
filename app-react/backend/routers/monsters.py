"""Monster profile API routes."""

from fastapi import APIRouter, HTTPException, status

from ..repositories import monsters
from ..schemas.monster import MonsterCreate, MonsterRead, MonsterUpdate

router = APIRouter(prefix="/api/monsters", tags=["monsters"])


@router.get("", response_model=list[MonsterRead])
def list_monsters() -> list[MonsterRead]:
    return monsters.list_monsters()


@router.get("/{record_id}", response_model=MonsterRead)
def get_monster(record_id: str) -> MonsterRead:
    record = monsters.get_monster(record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="The selected record no longer exists.")
    return record


@router.post("", response_model=MonsterRead, status_code=status.HTTP_201_CREATED)
def create_monster(value: MonsterCreate) -> MonsterRead:
    return monsters.create_monster(value.model_dump())


@router.put("/{record_id}", response_model=MonsterRead)
def update_monster(record_id: str, value: MonsterUpdate) -> MonsterRead:
    record = monsters.update_monster(record_id, value.model_dump())
    if record is None:
        raise HTTPException(status_code=404, detail="The selected record no longer exists.")
    return record


@router.delete("/{record_id}")
def delete_monster(record_id: str) -> dict[str, bool]:
    if not monsters.delete_monster(record_id):
        raise HTTPException(status_code=404, detail="The selected record no longer exists.")
    return {"deleted": True}
