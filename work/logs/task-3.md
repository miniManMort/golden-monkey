# Task 3 log

## Summary
Implemented the list-monster page for the Golden Monkey app, including a `Monsters / List Monsters` menu entry and a table view of persisted monster records.

## Work carried out
- Reviewed the architecture in [spec/README.md](../../spec/README.md) and the task requirements in [work/plans/task-3.md](../../work/plans/task-3.md).
- Added the list-monster dialog in [app/list_monsters_page.py](../../app/list_monsters_page.py).
- Wired the dialog into the main menu on the start page under `Monsters / List Monsters`.
- Loaded monster records from the SQLite database and displayed them in the requested table columns: Name, Level, AC, Save, Morale, Alignment, and Action.
- Left the Action column empty for now, as required, to defer view/edit button implementation to a later task.
- Validated the app compiles and the dialog can be instantiated in offscreen Qt mode.

## Result
The task is complete: the home page now includes the list-monsters option, and the app displays a monster table matching the specified layout without implementing the future action buttons.
