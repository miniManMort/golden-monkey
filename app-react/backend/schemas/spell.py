"""Spell request and response models, normalization, and validation."""

from collections.abc import Mapping
from typing import Any

from pydantic import BaseModel

from ..errors import ApiError
from .common import parse_integer, plain_text

SPELL_FIELDS = ("name", "level", "save_allowed", "range", "duration", "effect")
_TEXT_FIELDS = ("name", "save_allowed", "range", "duration", "effect")


class SpellCreate(BaseModel):
    name: str
    level: int
    save_allowed: str
    range: str
    duration: str
    effect: str


class SpellUpdate(SpellCreate):
    pass


class SpellRead(SpellCreate):
    id: str


def prepare_spell(
    value: Mapping[str, Any], existing: Mapping[str, Any] | None = None
) -> SpellCreate:
    return SpellCreate.model_validate(_prepare_spell_data(value, existing))


def prepare_spell_update(
    value: Mapping[str, Any], existing: Mapping[str, Any]
) -> SpellUpdate:
    return SpellUpdate.model_validate(_prepare_spell_data(value, existing))


def _prepare_spell_data(
    value: Mapping[str, Any], existing: Mapping[str, Any] | None
) -> dict[str, Any]:
    data = dict(existing or {})
    data.update({field: value[field] for field in SPELL_FIELDS if field in value})
    for field in SPELL_FIELDS:
        data.setdefault(field, "")

    for field in _TEXT_FIELDS:
        data[field] = str(data[field] if data[field] is not None else "").strip()
    data["level"] = parse_integer(data["level"], "Level")

    _validate_spell(data)
    return data


def _validate_spell(data: Mapping[str, Any]) -> None:
    if not data["name"]:
        raise ApiError(400, "Name cannot be blank.")
    if not 1 <= data["level"] <= 6:
        raise ApiError(400, "Level must be between 1 and 6.")
    for field, label in (
        ("save_allowed", "Save Allowed"),
        ("range", "Range"),
        ("duration", "Duration"),
        ("effect", "Effect"),
    ):
        if not plain_text(data[field]).strip():
            raise ApiError(400, f"{label} cannot be blank.")
