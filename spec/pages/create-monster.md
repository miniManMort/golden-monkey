---
Name: Create Monster Page
Menu Option : Monsters / Create Monster
Status: Proposed
---

| Field | Format | Validation |
| --- | --- | --- |
| id | Hidden | Auto generated |
| Name | Text | Entered by user, must not exist in DB |
| Summary | Text | Entered by user, must be at least 60 characters long |
| HP | Text | Cannot be blank, must conform to format [0-9][0-9]*d[0-9][0-9]*[+-]*[0-9]* |
| AC | Integer | In range 5 to 25 |
| Save | Text | Cannot be blank, Must be of the format [FCMPT]:[0-9][0-9]* |
| Morale | Int | Must be in range 2  to 12 |
| Attacks | Text | Cannot be blank |
| Damage | Text | Cannot be blank |
| Trasure | Text | Single character or Nil |
| Specials | Multi-line Text | Defaults to "None" |
| Save | Button | Saves the data |
