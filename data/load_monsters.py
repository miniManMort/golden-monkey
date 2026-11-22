#!/usr/bin/env python3
"""Load a sample set of classic B/X-style monsters into a SQLite database."""

from __future__ import annotations

import argparse
import sqlite3
import uuid
from contextlib import closing
from pathlib import Path


def monster_seed_data() -> list[dict]:
    return [
        {
            "name": "Goblin",
            "summary": "A skulking, cave-dwelling humanoid with a ruthless appetite for mischief, theft, and ambushes in the dark.",
            "level": 1,
            "hit_points": "2d6",
            "armour_class": 6,
            "save_as": "F:14",
            "morale": 7,
            "attacks": "1 short sword or spear",
            "damage": "1d6",
            "treasure": "C",
            "alignment": "Chaotic",
            "specials": "None",
        },
        {
            "name": "Orc",
            "summary": "A brutal, warlike humanoid that prefers raiding, intimidation, and close-quarters combat over subtlety.",
            "level": 1,
            "hit_points": "1d8+1",
            "armour_class": 6,
            "save_as": "F:13",
            "morale": 8,
            "attacks": "1 weapon",
            "damage": "1d8",
            "treasure": "C",
            "alignment": "Chaotic",
            "specials": "None",
        },
        {
            "name": "Kobold",
            "summary": "A diminutive reptilian creature with a cowardly temperament, but a nasty bite and a fondness for traps.",
            "level": 1,
            "hit_points": "1d4",
            "armour_class": 7,
            "save_as": "F:14",
            "morale": 6,
            "attacks": "1 short spear or bite",
            "damage": "1d4",
            "treasure": "Nil",
            "alignment": "Lawful",
            "specials": "None",
        },
        {
            "name": "Skeleton",
            "summary": "An animated pile of bones that keeps fighting with relentless discipline, especially in graveyards and crypts.",
            "level": 1,
            "hit_points": "1d8",
            "armour_class": 7,
            "save_as": "F:12",
            "morale": 12,
            "attacks": "1 club or sword",
            "damage": "1d6",
            "treasure": "Nil",
            "alignment": "Lawful",
            "specials": "None",
        },
        {
            "name": "Zombie",
            "summary": "A shambling undead horror that serves its master without reason, driven by hunger and decay.",
            "level": 1,
            "hit_points": "1d8",
            "armour_class": 8,
            "save_as": "F:12",
            "morale": 12,
            "attacks": "1 claw or slam",
            "damage": "1d6",
            "treasure": "Nil",
            "alignment": "Neutral",
            "specials": "None",
        },
        {
            "name": "Wolf",
            "summary": "A hungry predator of the wilds, known for speed, pack tactics, and a relentless stalking pursuit.",
            "level": 2,
            "hit_points": "2d6",
            "armour_class": 7,
            "save_as": "F:14",
            "morale": 8,
            "attacks": "1 bite",
            "damage": "1d6",
            "treasure": "Nil",
            "alignment": "Neutral",
            "specials": "None",
        },
        {
            "name": "Bandit",
            "summary": "A road-worn raider who survives by improvisation, intimidation, and opportunistic violence.",
            "level": 1,
            "hit_points": "1d6",
            "armour_class": 7,
            "save_as": "F:12",
            "morale": 7,
            "attacks": "1 weapon",
            "damage": "1d6",
            "treasure": "C",
            "alignment": "Chaotic",
            "specials": "None",
        },
        {
            "name": "Giant Rat",
            "summary": "A disease-ridden scavenger that thrives in ruins, sewers, and neglected hovels where the desperate gather.",
            "level": 1,
            "hit_points": "1d4",
            "armour_class": 7,
            "save_as": "F:14",
            "morale": 7,
            "attacks": "1 bite",
            "damage": "1d3",
            "treasure": "Nil",
            "alignment": "Neutral",
            "specials": "None",
        },
    ]


def load_monsters(db_path: str | None = None) -> int:
    target = Path(db_path) if db_path else Path(__file__).resolve().parent / "golden_monkey.db"
    target.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(target)) as database, database:
        database.execute(
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
        columns = {
            row[1] for row in database.execute('PRAGMA table_info("monster")')
        }
        if "save" in columns and "save_as" not in columns:
            database.execute('ALTER TABLE "monster" RENAME COLUMN "save" TO "save_as"')
        if "specials" not in columns:
            database.execute(
                'ALTER TABLE "monster" ADD COLUMN "specials" TEXT NOT NULL DEFAULT \'None\''
            )

        fields = (
            "id",
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
        rows = monster_seed_data()
        database.execute("DELETE FROM monster")
        database.executemany(
            f'INSERT INTO monster ({", ".join(fields)}) '
            f'VALUES ({", ".join("?" for _ in fields)})',
            [
                (uuid.uuid4().hex, *(row[field] for field in fields[1:]))
                for row in rows
            ],
        )
        count = database.execute("SELECT COUNT(*) FROM monster").fetchone()[0]
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description="Load sample B/X-style monsters into a SQLite database.")
    parser.add_argument(
        "db_path",
        nargs="?",
        default=str(Path(__file__).resolve().parent / "golden_monkey.db"),
        help="Destination SQLite database path. Defaults to data/golden_monkey.db.",
    )
    args = parser.parse_args()

    count = load_monsters(args.db_path)
    print(f"Loaded {count} monster records into {args.db_path}")


if __name__ == "__main__":
    main()
