---
Name: Create Spell Page
Menu Option : Spells / Create Spell
Status: Implemented
---

| Field | Format | Validation |
| --- | --- | --- |
| id | Hidden | Auto generated |
| Name | Text | Entered by user, must not exist in DB |
| Level | Integer | In range 1 to 6 |
| Save Allowed | Text | Cannot be blank |
| Range | Text | Cannot be blank |
| Duraction | Text | Cannot be blank |
| Effect | Multi-line text, 60 characters wide by 5 lines high | Cannot be blank |
| Save | Button | Saves the data |
