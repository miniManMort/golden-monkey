---
Name: spell
Description: A spell profile
DB Table Name: spell
Model Name: Spell
Status: Implemented
---

| attribute | type | constraints |
| --- | --- | --- |
| id | Text | primary key default=uuid4.hex |
| name | Text | not null |
| level | Int | not null range 1-6 |
| save_allowed | Text | not null |
| range | Text | not null |
| duration | Text | not null |
| effect | Text | not null default "None" long text; supports bold, italic, bulleted lists, and tables |
