"""SQLite connection and schema management."""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

ROOT_DIR = Path(__file__).resolve().parents[2]
DATABASE_PATH = ROOT_DIR / "data" / "golden_monkey.db"


@contextmanager
def database_connection() -> Generator[sqlite3.Connection, None, None]:
    connection = sqlite3.connect(DATABASE_PATH)
    try:
        with connection:
            yield connection
    finally:
        connection.close()


def initialize_database() -> None:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with database_connection() as connection:
        connection.execute(
            """CREATE TABLE IF NOT EXISTS monster (
                id TEXT NOT NULL PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                summary TEXT NOT NULL,
                level INTEGER NOT NULL,
                hit_points TEXT NOT NULL,
                armour_class INTEGER NOT NULL,
                save_as TEXT NOT NULL,
                morale INTEGER NOT NULL,
                attacks TEXT NOT NULL,
                damage TEXT NOT NULL,
                treasure TEXT NOT NULL,
                alignment TEXT NOT NULL,
                specials TEXT NOT NULL DEFAULT 'None'
            )"""
        )
        connection.execute(
            """CREATE TABLE IF NOT EXISTS spell (
                id TEXT NOT NULL PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                level INTEGER NOT NULL,
                save_allowed TEXT NOT NULL,
                range TEXT NOT NULL,
                duration TEXT NOT NULL,
                effect TEXT NOT NULL DEFAULT 'None'
            )"""
        )
        connection.execute(
            """CREATE TABLE IF NOT EXISTS character_class (
                id TEXT NOT NULL PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                outline TEXT NOT NULL,
                requirements TEXT NOT NULL,
                hit_dice TEXT NOT NULL,
                combat_skills TEXT NOT NULL,
                other_skills TEXT NOT NULL,
                progression_table TEXT NOT NULL
            )"""
        )
        columns = {
            row[1] for row in connection.execute('PRAGMA table_info("monster")')
        }
        if "save" in columns and "save_as" not in columns:
            connection.execute('ALTER TABLE "monster" RENAME COLUMN "save" TO "save_as"')
        if "specials" not in columns:
            connection.execute(
                'ALTER TABLE "monster" ADD COLUMN "specials" TEXT NOT NULL DEFAULT \'None\''
            )
