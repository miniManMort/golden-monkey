"""Character class profile persistence."""

import sqlite3
import uuid
from collections.abc import Mapping
from typing import Any

from ..database import database_connection
from ..errors import ApiError
from ..schemas.character_class import (
    CHARACTER_CLASS_FIELDS,
    CharacterClassRead,
    prepare_character_class,
    prepare_character_class_update,
)


def list_character_classes(sort_order: str = "Name") -> list[CharacterClassRead]:
    if sort_order == "Name":
        order = "name"
    elif sort_order == "Hit Dice / Name":
        order = "hit_dice, name"
    else:
        raise ApiError(
            400, f"Unsupported character class sort order: {sort_order}"
        )
    with database_connection() as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            f"SELECT * FROM character_class ORDER BY {order}"
        ).fetchall()
    return [CharacterClassRead.model_validate(dict(row)) for row in rows]


def get_character_class(record_id: str) -> CharacterClassRead | None:
    with database_connection() as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute(
            "SELECT * FROM character_class WHERE id = ?", (record_id,)
        ).fetchone()
    return (
        CharacterClassRead.model_validate(dict(row)) if row is not None else None
    )


def create_character_class(value: Mapping[str, Any]) -> CharacterClassRead:
    record = prepare_character_class(value)
    record_id = uuid.uuid4().hex
    with database_connection() as connection:
        _ensure_unique_name(connection, record.name)
        fields = ("id", *CHARACTER_CLASS_FIELDS)
        connection.execute(
            f'INSERT INTO character_class ({", ".join(fields)}) '
            f'VALUES ({", ".join("?" for _ in fields)})',
            (
                record_id,
                *(getattr(record, field) for field in CHARACTER_CLASS_FIELDS),
            ),
        )
    return CharacterClassRead(id=record_id, **record.model_dump())


def update_character_class(
    record_id: str, value: Mapping[str, Any]
) -> CharacterClassRead | None:
    with database_connection() as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute(
            "SELECT * FROM character_class WHERE id = ?", (record_id,)
        ).fetchone()
        if row is None:
            return None
        record = prepare_character_class_update(value, dict(row))
        _ensure_unique_name(connection, record.name, record_id)
        connection.execute(
            "UPDATE character_class SET "
            + ", ".join(f"{field} = ?" for field in CHARACTER_CLASS_FIELDS)
            + " WHERE id = ?",
            (
                *(getattr(record, field) for field in CHARACTER_CLASS_FIELDS),
                record_id,
            ),
        )
    return CharacterClassRead(id=record_id, **record.model_dump())


def delete_character_class(record_id: str) -> bool:
    with database_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM character_class WHERE id = ?", (record_id,)
        )
        return cursor.rowcount > 0


def _ensure_unique_name(
    connection: sqlite3.Connection, name: str, exclude_id: str | None = None
) -> None:
    query = "SELECT id FROM character_class WHERE name = ?"
    parameters: tuple[str, ...] = (name,)
    if exclude_id is not None:
        query += " AND id != ?"
        parameters = (name, exclude_id)
    if connection.execute(query, parameters).fetchone():
        raise ApiError(
            409, f"A character class named '{name}' already exists."
        )
