"""Spell profile persistence."""

import sqlite3
import uuid
from collections.abc import Mapping
from typing import Any

from ..database import database_connection
from ..errors import ApiError
from ..schemas.spell import (
    SPELL_FIELDS,
    SpellRead,
    prepare_spell,
    prepare_spell_update,
)


def list_spells(sort_order: str = "Name") -> list[SpellRead]:
    if sort_order == "Name":
        order = "name"
    elif sort_order == "Level / Name":
        order = "level, name"
    else:
        raise ApiError(400, f"Unsupported spell sort order: {sort_order}")
    with database_connection() as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(f"SELECT * FROM spell ORDER BY {order}").fetchall()
    return [SpellRead.model_validate(dict(row)) for row in rows]


def get_spell(record_id: str) -> SpellRead | None:
    with database_connection() as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute(
            "SELECT * FROM spell WHERE id = ?", (record_id,)
        ).fetchone()
    return SpellRead.model_validate(dict(row)) if row is not None else None


def create_spell(value: Mapping[str, Any]) -> SpellRead:
    record = prepare_spell(value)
    record_id = uuid.uuid4().hex
    with database_connection() as connection:
        _ensure_unique_name(connection, record.name)
        fields = ("id", *SPELL_FIELDS)
        connection.execute(
            f'INSERT INTO spell ({", ".join(fields)}) '
            f'VALUES ({", ".join("?" for _ in fields)})',
            (record_id, *(getattr(record, field) for field in SPELL_FIELDS)),
        )
    return SpellRead(id=record_id, **record.model_dump())


def update_spell(record_id: str, value: Mapping[str, Any]) -> SpellRead | None:
    with database_connection() as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute(
            "SELECT * FROM spell WHERE id = ?", (record_id,)
        ).fetchone()
        if row is None:
            return None
        record = prepare_spell_update(value, dict(row))
        _ensure_unique_name(connection, record.name, record_id)
        connection.execute(
            "UPDATE spell SET "
            + ", ".join(f"{field} = ?" for field in SPELL_FIELDS)
            + " WHERE id = ?",
            (*(getattr(record, field) for field in SPELL_FIELDS), record_id),
        )
    return SpellRead(id=record_id, **record.model_dump())


def delete_spell(record_id: str) -> bool:
    with database_connection() as connection:
        cursor = connection.execute("DELETE FROM spell WHERE id = ?", (record_id,))
        return cursor.rowcount > 0


def _ensure_unique_name(
    connection: sqlite3.Connection, name: str, exclude_id: str | None = None
) -> None:
    query = "SELECT id FROM spell WHERE name = ?"
    parameters: tuple[str, ...] = (name,)
    if exclude_id is not None:
        query += " AND id != ?"
        parameters = (name, exclude_id)
    if connection.execute(query, parameters).fetchone():
        raise ApiError(409, f"A spell named '{name}' already exists.")
