---
Name: monster
Description: A monster profile
DB Table Name: monsters
Model Name: Monster
Status: Proposed
---


| attribute | type | constraints |
| --- | --- | --- |
| id | Text | default=uuid4.hex |
| name | Text | not null |
| summary | Text | not null long text; supports bold, italic, bulleted lists, and tables |
| level | Int | not null range 1-20 |
| hit_points | Text | not null | 
| armour_class | Int | not null |
| save_as | Text | not null |
| morale | Int | not null range 2-12 |
| attacks | Text | not null |
| damage | Text | not null |
| treasure | Text | not null |
| alignment | Text | not null allowed values = ['Lawful','Chaotic','Neutral'] |
| specials | Text | not null default "None" long text; supports bold, italic, bulleted lists, and tables |
