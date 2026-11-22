import json
import socket
import sqlite3
import tempfile
import threading
import time
import unittest
import urllib.error
import urllib.request
import zipfile
from contextlib import closing
from io import BytesIO
from pathlib import Path

import server
import uvicorn
from backend import database


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_database = database.DATABASE_PATH
        database.DATABASE_PATH = Path(self.temp_dir.name) / "golden_monkey.db"
        database.initialize_database()
        self.socket = socket.socket()
        self.socket.bind(("127.0.0.1", 0))
        self.base_url = f"http://127.0.0.1:{self.socket.getsockname()[1]}"
        self.uvicorn_server = uvicorn.Server(
            uvicorn.Config(server.app, log_level="critical")
        )
        self.thread = threading.Thread(
            target=self.uvicorn_server.run,
            kwargs={"sockets": [self.socket]},
            daemon=True,
        )
        self.thread.start()
        deadline = time.monotonic() + 10
        while not self.uvicorn_server.started and self.thread.is_alive():
            if time.monotonic() >= deadline:
                self.uvicorn_server.should_exit = True
                self.thread.join()
                self.fail("Uvicorn did not start in time.")
            time.sleep(0.01)

    def tearDown(self):
        self.uvicorn_server.should_exit = True
        self.thread.join(timeout=10)
        self.socket.close()
        database.DATABASE_PATH = self.original_database
        self.temp_dir.cleanup()

    def call_api(self, path, method="GET", body=None):
        payload = None if body is None else json.dumps(body).encode("utf-8")
        request = urllib.request.Request(
            self.base_url + path,
            data=payload,
            method=method,
            headers={"Content-Type": "application/json"},
        )
        try:
            response = urllib.request.urlopen(request)
        except urllib.error.HTTPError as error:
            response = error
        content_type = response.headers.get("Content-Type", "")
        content = response.read()
        status = response.status
        response.close()
        return status, json.loads(content) if "application/json" in content_type else content

    def test_fastapi_health_and_frontend_routes(self):
        status, health = self.call_api("/api/health")
        self.assertEqual(status, 200)
        self.assertEqual(health, {"status": "ok"})
        status, content = self.call_api("/")
        self.assertEqual(status, 200)
        self.assertIn(b"Golden Monkey", content)

        request = urllib.request.Request(
            self.base_url + "/api/spells",
            data=b"{",
            method="POST",
            headers={"Content-Type": "application/json"},
        )
        with self.assertRaises(urllib.error.HTTPError) as response:
            urllib.request.urlopen(request)
        self.assertEqual(response.exception.code, 400)
        self.assertEqual(
            json.loads(response.exception.read())["error"],
            "Request body must be valid JSON.",
        )

    def test_database_initialization_migrates_legacy_monster_columns(self):
        legacy_path = Path(self.temp_dir.name) / "legacy.db"
        with closing(sqlite3.connect(legacy_path)) as connection, connection:
            connection.execute(
                """CREATE TABLE monster (
                    id TEXT NOT NULL PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE,
                    summary TEXT NOT NULL,
                    level INTEGER NOT NULL,
                    hit_points TEXT NOT NULL,
                    armour_class INTEGER NOT NULL,
                    save TEXT NOT NULL,
                    morale INTEGER NOT NULL,
                    attacks TEXT NOT NULL,
                    damage TEXT NOT NULL,
                    treasure TEXT NOT NULL,
                    alignment TEXT NOT NULL
                )"""
            )
            connection.execute(
                """INSERT INTO monster VALUES (
                    'legacy-id', 'Goblin',
                    'A creature description long enough to meet the minimum length.',
                    1, '2d8', 6, 'F:1', 7, '1 weapon', '1d6', 'B', 'Chaotic'
                )"""
            )

        current_path = database.DATABASE_PATH
        database.DATABASE_PATH = legacy_path
        try:
            database.initialize_database()
        finally:
            database.DATABASE_PATH = current_path

        with closing(sqlite3.connect(legacy_path)) as connection:
            columns = {
                row[1] for row in connection.execute('PRAGMA table_info("monster")')
            }
            row = connection.execute(
                "SELECT id, name, save_as, specials FROM monster WHERE id = 'legacy-id'"
            ).fetchone()
        self.assertIn("save_as", columns)
        self.assertIn("specials", columns)
        self.assertEqual(row, ("legacy-id", "Goblin", "F:1", "None"))

    def test_spell_crud_and_duplicate_name_error(self):
        spell = {
            "name": "  Lantern  ",
            "level": 1,
            "save_allowed": "None",
            "range": "Touch",
            "duration": "1 hour",
            "effect": "Creates warm light.",
        }
        status, created = self.call_api("/api/spells", "POST", spell)
        self.assertEqual(status, 201)
        self.assertEqual(created["name"], "Lantern")

        status, duplicate = self.call_api("/api/spells", "POST", spell)
        self.assertEqual(status, 409)
        self.assertIn("already exists", duplicate["error"])

        created["level"] = 2
        status, updated = self.call_api(
            f"/api/spells/{created['id']}", "PUT", created
        )
        self.assertEqual(status, 200)
        self.assertEqual(updated["level"], 2)

        status, rows = self.call_api("/api/spells")
        self.assertEqual(status, 200)
        self.assertEqual([row["name"] for row in rows], ["Lantern"])

        status, result = self.call_api(
            f"/api/spells/{created['id']}", "DELETE"
        )
        self.assertEqual(status, 200)
        self.assertTrue(result["deleted"])

    def test_monster_validation_returns_actionable_error(self):
        status, result = self.call_api(
            "/api/monsters",
            "POST",
            {
                "name": "Goblin",
                "summary": "Too short",
                "level": 1,
                "hit_points": "2d8",
                "armour_class": 6,
                "save_as": "F:1",
                "morale": 7,
                "attacks": "1 weapon",
                "damage": "1d6",
                "treasure": "B",
                "alignment": "Chaotic",
            },
        )
        self.assertEqual(status, 400)
        self.assertEqual(result["error"], "Summary must be at least 60 characters long.")

    def test_rich_text_spell_effect_persists_and_exports_formatting(self):
        effect = (
            "<p>A <strong>bright</strong> and <em>steady</em> light.</p>"
            "<ul><li>Reveals hidden doors</li><li>Guides travelers</li></ul>"
            "<table><tbody><tr><td>First</td><td>Second</td></tr></tbody></table>"
        )
        spell = {
            "name": "Rich Lantern",
            "level": 1,
            "save_allowed": "None",
            "range": "Touch",
            "duration": "1 hour",
            "effect": effect,
        }
        status, created = self.call_api("/api/spells", "POST", spell)
        self.assertEqual(status, 201)
        self.assertEqual(created["effect"], effect)

        status, payload = self.call_api("/api/export/spells")
        self.assertEqual(status, 200)
        with zipfile.ZipFile(BytesIO(payload)) as archive:
            content = archive.read("content.xml").decode("utf-8")
            styles = archive.read("styles.xml").decode("utf-8")
        self.assertIn('text:style-name="Bold">bright</text:span>', content)
        self.assertIn('text:style-name="Italic">steady</text:span>', content)
        self.assertIn("<text:list>", content)
        self.assertIn("<table:table-cell", content)
        self.assertIn('style:name="Bold"', styles)
        self.assertIn('style:name="Italic"', styles)

    def test_rule_section_crud_validation_and_export(self):
        rule_section = {
            "name": "  Combat  ",
            "section_text": "<h2>Actions</h2><p>Use <strong>initiative</strong>.</p>",
        }
        status, created = self.call_api(
            "/api/rule-sections", "POST", rule_section
        )
        self.assertEqual(status, 201)
        self.assertEqual(created["name"], "Combat")
        self.assertIn("initiative", created["section_text"])

        status, duplicate = self.call_api(
            "/api/rule-sections", "POST", rule_section
        )
        self.assertEqual(status, 409)
        self.assertIn("already exists", duplicate["error"])

        invalid = {"name": "Exploration", "section_text": "<p><br></p>"}
        status, result = self.call_api(
            "/api/rule-sections", "POST", invalid
        )
        self.assertEqual(status, 400)
        self.assertEqual(result["error"], "Section text cannot be blank.")

        created["section_text"] = "<p>Updated <em>combat rules</em>.</p>"
        status, updated = self.call_api(
            f"/api/rule-sections/{created['id']}", "PUT", created
        )
        self.assertEqual(status, 200)
        self.assertIn("combat rules", updated["section_text"])

        status, rows = self.call_api("/api/rule-sections")
        self.assertEqual(status, 200)
        self.assertEqual([row["name"] for row in rows], ["Combat"])

        status, payload = self.call_api(
            "/api/export/rule-sections?sort=Name"
        )
        self.assertEqual(status, 200)
        with zipfile.ZipFile(BytesIO(payload)) as archive:
            content = archive.read("content.xml").decode("utf-8")
            styles = archive.read("styles.xml").decode("utf-8")
        self.assertIn("Combat", content)
        self.assertIn("combat rules", content)
        self.assertIn('style:name="Italic"', styles)

        status, result = self.call_api(
            f"/api/rule-sections/{created['id']}", "DELETE"
        )
        self.assertEqual(status, 200)
        self.assertTrue(result["deleted"])

    def test_character_class_crud_validation_and_export(self):
        character_class = {
            "name": "  Ranger  ",
            "outline": "A wilderness specialist.",
            "requirements": "Dexterity 9",
            "hit_dice": "d8",
            "combat_skills": "Medium armor and martial weapons",
            "other_skills": "Tracking and survival",
            "progression_table": "<p>Gains <strong>level benefits</strong>.</p>"
            "<table><tbody><tr><td>Level</td><td>1</td></tr></tbody></table>",
        }
        status, created = self.call_api(
            "/api/character-classes", "POST", character_class
        )
        self.assertEqual(status, 201)
        self.assertEqual(created["name"], "Ranger")
        self.assertEqual(created["hit_dice"], "d8")

        status, duplicate = self.call_api(
            "/api/character-classes", "POST", character_class
        )
        self.assertEqual(status, 409)
        self.assertIn("already exists", duplicate["error"])

        invalid = dict(character_class)
        invalid["name"] = "Druid"
        invalid["hit_dice"] = "d12"
        status, result = self.call_api("/api/character-classes", "POST", invalid)
        self.assertEqual(status, 400)
        self.assertEqual(
            result["error"], "Hit dice must be d4, d6, d8 or d10."
        )

        created["requirements"] = "Dexterity 12"
        status, updated = self.call_api(
            f"/api/character-classes/{created['id']}", "PUT", created
        )
        self.assertEqual(status, 200)
        self.assertEqual(updated["requirements"], "Dexterity 12")

        status, rows = self.call_api("/api/character-classes")
        self.assertEqual(status, 200)
        self.assertEqual([row["name"] for row in rows], ["Ranger"])

        status, payload = self.call_api(
            "/api/export/character-classes?sort=Name"
        )
        self.assertEqual(status, 200)
        with zipfile.ZipFile(BytesIO(payload)) as archive:
            content = archive.read("content.xml").decode("utf-8")
            styles = archive.read("styles.xml").decode("utf-8")
        self.assertIn("Ranger", content)
        self.assertIn("Hit Dice: d8", content)
        self.assertIn("Progression Table:", content)
        self.assertIn('text:style-name="Bold">level benefits</text:span>', content)
        self.assertIn("<table:table-cell", content)
        self.assertIn('style:name="Bold"', styles)

        status, result = self.call_api(
            f"/api/character-classes/{created['id']}", "DELETE"
        )
        self.assertEqual(status, 200)
        self.assertTrue(result["deleted"])

    def test_rich_text_summary_minimum_uses_visible_characters(self):
        status, result = self.call_api(
            "/api/monsters",
            "POST",
            {
                "name": "Short Summary",
                "summary": "<p>" + ("Visible text " * 4) + "</p>",
                "level": 1,
                "hit_points": "2d8",
                "armour_class": 6,
                "save_as": "F:1",
                "morale": 7,
                "attacks": "1 weapon",
                "damage": "1d6",
                "treasure": "B",
                "alignment": "Chaotic",
            },
        )
        self.assertEqual(status, 400)
        self.assertEqual(result["error"], "Summary must be at least 60 characters long.")

    def test_monster_export_includes_all_profile_fields(self):
        monster = {
            "name": "Goblin",
            "summary": "A cave-dwelling creature with a fierce temper and a taste for shiny things.",
            "level": 1,
            "hit_points": "2d8+1",
            "armour_class": 6,
            "save_as": "F:1",
            "morale": 7,
            "attacks": "1 weapon",
            "damage": "1d6",
            "treasure": "B",
            "alignment": "Chaotic",
            "specials": "Ambush",
        }
        self.assertEqual(self.call_api("/api/monsters", "POST", monster)[0], 201)
        status, payload = self.call_api("/api/export/monsters?sort=Name")
        self.assertEqual(status, 200)
        with zipfile.ZipFile(BytesIO(payload)) as archive:
            content = archive.read("content.xml").decode("utf-8")
        for field in ("Goblin", "Summary:", "Hit Points: 2d8+1", "Save As: F:1", "Specials: Ambush"):
            self.assertIn(field, content)

    def test_odt_exports_contain_profiles_in_requested_sort_order(self):
        spells = [
            {"name": "Zeta", "level": 2, "save_allowed": "None", "range": "Near", "duration": "Instant", "effect": "Last spell."},
            {"name": "Alpha", "level": 1, "save_allowed": "Half", "range": "Touch", "duration": "1 hour", "effect": "First spell."},
        ]
        for spell_data in spells:
            self.assertEqual(self.call_api("/api/spells", "POST", spell_data)[0], 201)

        status, payload = self.call_api("/api/export/spells?sort=Level%20%2F%20Name")
        self.assertEqual(status, 200)
        with zipfile.ZipFile(BytesIO(payload)) as archive:
            self.assertEqual(archive.namelist()[0], "mimetype")
            content = archive.read("content.xml").decode("utf-8")
        self.assertLess(content.index(">Alpha<"), content.index(">Zeta<"))
        self.assertIn("Save Allowed", content)
        self.assertIn("First spell.", content)


if __name__ == "__main__":
    unittest.main()
