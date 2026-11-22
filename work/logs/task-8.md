# Task 8 log

## Summary
Added export of monster profiles to OpenDocument Text (`.odt`) files.

## Work carried out
- Reviewed the architecture in [spec/README.md](../../spec/README.md) and task requirements in [work/plans/task-8.md](../../work/plans/task-8.md).
- Added an Extract action to the Monsters menu and a dialog for sort order and destination path.
- Implemented ODT creation using Python's standard library, including the ODF package structure and every monster field.
- Added Name and Level / Name ordering and preserved multiline field content in the exported document.
- Documented the export dialog in [spec/pages/extract-monsters.md](../../spec/pages/extract-monsters.md).
- Verified generated ODT structure, XML contents, ordering, and Qt dialog/menu initialization.

## Result
Task 8 is complete. Users can export all monster profiles to an ODT document sorted by name or by level and name.
