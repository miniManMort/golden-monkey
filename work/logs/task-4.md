# Task 4 log

## Summary
Added a per-row View button to the list-monster table and implemented a details dialog that shows the full record for the selected monster.

## Work carried out
- Reviewed the architecture in [spec/README.md](../../spec/README.md) and the requirements in [work/plans/task-4.md](../../work/plans/task-4.md).
- Extended the monster table in [app/list_monsters_page.py](../../app/list_monsters_page.py) so each row includes a View button in the Action column.
- Added a `MonsterDetailsDialog` that presents all saved monster fields, including summary, HP, AC, save, morale, attacks, damage, treasure, and alignment.
- Wired the button click to open the details dialog for the selected record.
- Verified the project still compiles and the list page/dialog instantiate correctly in offscreen Qt mode.

## Result
The task is complete: each row in the monster list now has a working View action that opens a details page for that monster.
