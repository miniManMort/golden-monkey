"""Monster request and response models, normalization, and validation."""

import re
from collections.abc import Mapping
from typing import Any

from pydantic import BaseModel

from ..errors import ApiError
from .common import parse_integer, plain_text

MONSTER_FIELDS = (
    "name",
    "summary",
    "level",
    "hit_points",
    "armour_class",
    "save_as",
    "morale",
    "attacks",
    "damage",
    "treasure",
    "alignment",
    "specials",
)
_TEXT_FIELDS = (
    "name",
    "summary",
    "hit_points",
    "save_as",
    "attacks",
    "damage",
    "treasure",
    "alignment",
    "specials",
)


class MonsterCreate(BaseModel):
    name: str
    summary: str
    level: int
    hit_points: str
    armour_class: int
    save_as: str
    morale: int
    attacks: str
    damage: str
    treasure: str
    alignment: str
    specials: str = "None"


class MonsterUpdate(MonsterCreate):
    pass


class MonsterRead(MonsterCreate):
    id: str


def prepare_monster(
    value: Mapping[str, Any], existing: Mapping[str, Any] | None = None
) -> MonsterCreate:
    return MonsterCreate.model_validate(_prepare_monster_data(value, existing))


def prepare_monster_update(
    value: Mapping[str, Any], existing: Mapping[str, Any]
) -> MonsterUpdate:
    return MonsterUpdate.model_validate(_prepare_monster_data(value, existing))


def _prepare_monster_data(
    value: Mapping[str, Any], existing: Mapping[str, Any] | None
) -> dict[str, Any]:
    data = dict(existing or {})
    data.update({field: value[field] for field in MONSTER_FIELDS if field in value})
    for field in MONSTER_FIELDS:
        data.setdefault(field, "")

    for field in _TEXT_FIELDS:
        data[field] = str(data[field] if data[field] is not None else "").strip()
    data["level"] = parse_integer(data["level"], "Level")
    data["armour_class"] = parse_integer(data["armour_class"], "AC")
    data["morale"] = parse_integer(data["morale"], "Morale")
    data["treasure"] = data["treasure"] or "Nil"
    data["specials"] = data["specials"] or "None"

    _validate_monster(data)
    return data


def _validate_monster(data: Mapping[str, Any]) -> None:
    if not data["name"]:
        raise ApiError(400, "Name cannot be blank.")
    if len(plain_text(data["summary"])) < 60:
        raise ApiError(400, "Summary must be at least 60 characters long.")
    if not 1 <= data["level"] <= 20:
        raise ApiError(400, "Level must be between 1 and 20.")
    if not re.fullmatch(r"[0-9]+d[0-9]+[+-]?[0-9]*", data["hit_points"]):
        raise ApiError(400, "HP must match the format [0-9]+d[0-9]+[+-]?[0-9]*.")
    if not 5 <= data["armour_class"] <= 25:
        raise ApiError(400, "AC must be between 5 and 25.")
    if not re.fullmatch(r"[FCMPT]:[0-9]+", data["save_as"]):
        raise ApiError(400, "Save must match the format [FCMPT]:[0-9]+.")
    if not 2 <= data["morale"] <= 12:
        raise ApiError(400, "Morale must be between 2 and 12.")
    if not data["attacks"]:
        raise ApiError(400, "Attacks cannot be blank.")
    if not data["damage"]:
        raise ApiError(400, "Damage cannot be blank.")
    if data["treasure"] != "Nil" and len(data["treasure"]) != 1:
        raise ApiError(400, "Treasure must be a single character or 'Nil'.")
    if data["alignment"] not in {"Lawful", "Chaotic", "Neutral"}:
        raise ApiError(400, "Alignment must be Lawful, Chaotic or Neutral.")
