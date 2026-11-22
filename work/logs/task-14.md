# Task 14 log

## Summary
Created a React web rewrite in `app-react/` while preserving the original Python
desktop app under `app/`.

## Work carried out
- Reviewed the app architecture and existing model, screen, and export behavior.
- Added a responsive React/Vite interface with overview, monster and spell
  registries, create/edit/view/delete dialogs, and regular-expression search.
- Added a standard-library Python HTTP API that validates records and reads and
  writes the shared `data/golden_monkey.db` SQLite database.
- Added ODT downloads for monster and spell profiles, including name and
  level/name sorting.
- Added app setup/run documentation, package configuration, and isolated API
  tests.
- Updated the project and architecture READMEs to describe the React app.

## Verification
- `npm run build` completed successfully.
- `python -W error::ResourceWarning -m unittest discover -s tests -v` passed
  all four API, validation, CRUD, and export tests.
- Browser smoke checks confirmed the existing 12 monsters and 3 spells render,
  invalid regex input preserves results, details open, and spell ODT downloads
  are generated with the correct MIME type by the export endpoint.
- Confirmed the shared database retains its existing 12 monster and 3 spell
  records.

## Result
Task 14 is complete. The React web app is available separately in `app-react/`.
