---
Name: Modify Spell Page
Status: Proposed
---

| Field | Format | Validation |
| --- | --- | --- |
| id | Hidden |  |
| Name | Text | Entered by user, must not exist in DB |
| Level | Integer | In range 1 to 6 |
| Save Allowed | Text | Cannot be blank |
| Range | Text | Cannot be blank |
| Duration | Text | Cannot be blank |
| Effect | Multi-line text, 60 characters wide by 5 lines high | Cannot be blank |
| Save | Button | Saves the data |
| Delete | Button | Deletes the spell |

