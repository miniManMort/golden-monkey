# Task 6 log

## Summary
Added regex-based filtering for monster name, level, and alignment to the list-monsters page.

## Work carried out
- Reviewed the architecture in [spec/README.md](../../spec/README.md) and requirements in [work/plans/task-6.md](../../work/plans/task-6.md).
- Added a search-type selector, regex search field, and Search button to the list dialog.
- Implemented case-insensitive regex filtering for the selected field; an empty expression displays all monsters.
- Invalid regex expressions show a warning and leave the displayed results intact.
- Updated [spec/pages/list-monsters.md](../../spec/pages/list-monsters.md) to document the search controls and behavior.
- Verified compilation and searched test data using each supported field and an invalid regex.

## Result
Task 6 is complete. Users can filter the monster list with regular expressions against Name, Level, or Alignment.
