"""Monster profile persistence."""

import sqlite3
import uuid
from collections.abc import Mapping
from typing import Any

from ..database import database_connection
from ..errors import ApiError
from ..schemas.monster import (
    MONSTER_FIELDS,
    MonsterRead,
    prepare_monster,
    prepare_monster_update,
)


def list_monsters(sort_order: str = "Name") -> list[MonsterRead]:
    if sort_order == "Name":
        order = "name"
    elif sort_order == "Level / Name":
        order = "level, name"
    else:
        raise ApiError(400, f"Unsupported monster sort order: {sort_order}")
    with database_connection() as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(f"SELECT * FROM monster ORDER BY {order}").fetchall()
    return [MonsterRead.model_validate(dict(row)) for row in rows]


def get_monster(record_id: str) -> MonsterRead | None:
    with database_connection() as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute(
            "SELECT * FROM monster WHERE id = ?", (record_id,)
        ).fetchone()
    return MonsterRead.model_validate(dict(row)) if row is not None else None


def create_monster(value: Mapping[str, Any]) -> MonsterRead:
    record = prepare_monster(value)
    record_id = uuid.uuid4().hex
    with database_connection() as connection:
        _ensure_unique_name(connection, record.name)
        fields = ("id", *MONSTER_FIELDS)
        connection.execute(
            f'INSERT INTO monster ({", ".join(fields)}) '
            f'VALUES ({", ".join("?" for _ in fields)})',
            (record_id, *(getattr(record, field) for field in MONSTER_FIELDS)),
        )
    return MonsterRead(id=record_id, **record.model_dump())


def update_monster(record_id: str, value: Mapping[str, Any]) -> MonsterRead | None:
    with database_connection() as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute(
            "SELECT * FROM monster WHERE id = ?", (record_id,)
        ).fetchone()
        if row is None:
            return None
        record = prepare_monster_update(value, dict(row))
        _ensure_unique_name(connection, record.name, record_id)
        connection.execute(
            "UPDATE monster SET "
            + ", ".join(f"{field} = ?" for field in MONSTER_FIELDS)
            + " WHERE id = ?",
            (*(getattr(record, field) for field in MONSTER_FIELDS), record_id),
        )
    return MonsterRead(id=record_id, **record.model_dump())


def delete_monster(record_id: str) -> bool:
    with database_connection() as connection:
        cursor = connection.execute("DELETE FROM monster WHERE id = ?", (record_id,))
        return cursor.rowcount > 0


def _ensure_unique_name(
    connection: sqlite3.Connection, name: str, exclude_id: str | None = None
) -> None:
    query = "SELECT id FROM monster WHERE name = ?"
    parameters: tuple[str, ...] = (name,)
    if exclude_id is not None:
        query += " AND id != ?"
        parameters = (name, exclude_id)
    if connection.execute(query, parameters).fetchone():
        raise ApiError(409, f"A monster named '{name}' already exists.")
