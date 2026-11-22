---
Name: Character Class
Description: A character class description
DB Table Name: character_class
Model Name: CharacterClass
Status: Proposed
---

| attribute | type | constraints |
| --- | --- | --- |
| id | Text | primary key default=uuid4.hex |
| name | Text | not null |
| outline | Text | not null |
| requirements | Text | not null |
| hit_dice | Text | not null format d(4|6|8|10)|
| combat_skills | Text | not null |
| other_skills | Text | not null |
| progression_table | Text | not null long text; supports bold, italic, bulleted lists, and tables |
