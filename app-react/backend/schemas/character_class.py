"""Character class request and response models, normalization, and validation."""

from collections.abc import Mapping
from typing import Any

from pydantic import BaseModel

from ..errors import ApiError
from .common import plain_text

CHARACTER_CLASS_FIELDS = (
    "name",
    "outline",
    "requirements",
    "hit_dice",
    "combat_skills",
    "other_skills",
    "progression_table",
)
_TEXT_FIELDS = CHARACTER_CLASS_FIELDS


class CharacterClassCreate(BaseModel):
    name: str
    outline: str
    requirements: str
    hit_dice: str
    combat_skills: str
    other_skills: str
    progression_table: str


class CharacterClassUpdate(CharacterClassCreate):
    pass


class CharacterClassRead(CharacterClassCreate):
    id: str


def prepare_character_class(
    value: Mapping[str, Any], existing: Mapping[str, Any] | None = None
) -> CharacterClassCreate:
    return CharacterClassCreate.model_validate(
        _prepare_character_class_data(value, existing)
    )


def prepare_character_class_update(
    value: Mapping[str, Any], existing: Mapping[str, Any]
) -> CharacterClassUpdate:
    return CharacterClassUpdate.model_validate(
        _prepare_character_class_data(value, existing)
    )


def _prepare_character_class_data(
    value: Mapping[str, Any], existing: Mapping[str, Any] | None
) -> dict[str, Any]:
    data = dict(existing or {})
    data.update(
        {field: value[field] for field in CHARACTER_CLASS_FIELDS if field in value}
    )
    for field in CHARACTER_CLASS_FIELDS:
        data.setdefault(field, "")

    for field in _TEXT_FIELDS:
        data[field] = str(data[field] if data[field] is not None else "").strip()

    _validate_character_class(data)
    return data


def _validate_character_class(data: Mapping[str, Any]) -> None:
    if not data["name"]:
        raise ApiError(400, "Name cannot be blank.")
    for field, label in (
        ("outline", "Outline"),
        ("requirements", "Requirements"),
        ("combat_skills", "Combat skills"),
        ("other_skills", "Other skills"),
        ("progression_table", "Progression table"),
    ):
        if not plain_text(data[field]).strip():
            raise ApiError(400, f"{label} cannot be blank.")
    if data["hit_dice"] not in {"d4", "d6", "d8", "d10"}:
        raise ApiError(400, "Hit dice must be d4, d6, d8 or d10.")
