---
Name: List Spells Page
Menu Option : Spells / List Spells
Status: Implemented
---

At the top of the page provide search facility:
- Search type selector with Name and Level options.
- Search text field accepting a regular expression.
- Search button to show only records whose selected field matches the expression.
- Matching is case-insensitive; an empty search expression shows all spells.
- Invalid regular expressions are reported to the user and do not replace the current results.

This is followed by a table of spells as follows
| Name | Level | Range | Duration | Save Allowed | Action |
| --- | --- | --- | --- | --- | --- | --- |
| spell.name | spell.level | spell.range | spell.duration | spell.save_allowed | View button and Edit button |