---
ID: 6
Objective: Add search capability to list-monsters page
Status: Completed
---

# Outline
This task adds a search type field, search text field and search button at the top of the [list-monster](spec/pages/list-monsters.md) page. 

- update the list-monsters spec to include fields and button
- the search type should list name, level, alignment as searchable fields
- add new field and button to the [list-monsters-page](app/list_monsters_page.py)
- on clicking on the search button list only those monsters where the chosen field matches the search text field.
- the search should support regex matching.
