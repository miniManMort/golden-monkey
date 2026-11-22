"""Rule section persistence."""

import sqlite3
import uuid
from collections.abc import Mapping
from typing import Any

from ..database import database_connection
from ..errors import ApiError
from ..schemas.rule_section import (
    RULE_SECTION_FIELDS,
    RuleSectionRead,
    prepare_rule_section,
    prepare_rule_section_update,
)


def list_rule_sections(sort_order: str = "Name") -> list[RuleSectionRead]:
    if sort_order != "Name":
        raise ApiError(400, f"Unsupported rule section sort order: {sort_order}")
    with database_connection() as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            "SELECT * FROM rule_section ORDER BY name"
        ).fetchall()
    return [RuleSectionRead.model_validate(dict(row)) for row in rows]


def get_rule_section(record_id: str) -> RuleSectionRead | None:
    with database_connection() as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute(
            "SELECT * FROM rule_section WHERE id = ?", (record_id,)
        ).fetchone()
    return RuleSectionRead.model_validate(dict(row)) if row is not None else None


def create_rule_section(value: Mapping[str, Any]) -> RuleSectionRead:
    record = prepare_rule_section(value)
    record_id = uuid.uuid4().hex
    with database_connection() as connection:
        _ensure_unique_name(connection, record.name)
        fields = ("id", *RULE_SECTION_FIELDS)
        connection.execute(
            f'INSERT INTO rule_section ({", ".join(fields)}) '
            f'VALUES ({", ".join("?" for _ in fields)})',
            (
                record_id,
                *(getattr(record, field) for field in RULE_SECTION_FIELDS),
            ),
        )
    return RuleSectionRead(id=record_id, **record.model_dump())


def update_rule_section(
    record_id: str, value: Mapping[str, Any]
) -> RuleSectionRead | None:
    with database_connection() as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute(
            "SELECT * FROM rule_section WHERE id = ?", (record_id,)
        ).fetchone()
        if row is None:
            return None
        record = prepare_rule_section_update(value, dict(row))
        _ensure_unique_name(connection, record.name, record_id)
        connection.execute(
            "UPDATE rule_section SET "
            + ", ".join(f"{field} = ?" for field in RULE_SECTION_FIELDS)
            + " WHERE id = ?",
            (
                *(getattr(record, field) for field in RULE_SECTION_FIELDS),
                record_id,
            ),
        )
    return RuleSectionRead(id=record_id, **record.model_dump())


def delete_rule_section(record_id: str) -> bool:
    with database_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM rule_section WHERE id = ?", (record_id,)
        )
        return cursor.rowcount > 0


def _ensure_unique_name(
    connection: sqlite3.Connection, name: str, exclude_id: str | None = None
) -> None:
    query = "SELECT id FROM rule_section WHERE name = ?"
    parameters: tuple[str, ...] = (name,)
    if exclude_id is not None:
        query += " AND id != ?"
        parameters = (name, exclude_id)
    if connection.execute(query, parameters).fetchone():
        raise ApiError(409, f"A rule section named '{name}' already exists.")
