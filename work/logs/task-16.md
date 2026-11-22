# Task 16 log

## Summary
Split the FastAPI backend into focused database, schema, repository, router,
service, app, and CLI modules.

## Work carried out
- Reviewed the app architecture and the Task 16 proposal in
  [task-16.md](../plans/task-16.md).
- Extracted SQLite schema initialization, connection management, and legacy
  column migration into `backend/database.py`.
- Added typed monster and spell create/update/read schemas with normalization
  and validation, and moved CRUD SQL into resource repositories.
- Split health, monster, spell, and export endpoints into FastAPI routers.
- Moved ODT XML/ZIP generation into `backend/services/odt.py`.
- Moved app lifecycle, middleware, error handlers, router setup, and frontend
  serving to `backend/app.py`; kept `server.py` as the CLI compatibility
  launcher.
- Updated the README with the backend module layout and kept the original
  desktop app untouched.

## Verification
- `python -W error::ResourceWarning -m unittest discover -s tests -v` passed
  all six API, validation, CRUD, export, and legacy migration tests.
- Python compilation passed for the modular backend and tests.
- Pylance reported no diagnostics in the new backend modules; unrelated
  pre-existing desktop-app diagnostics remain outside this task.
- `python app-react/server.py --port 8101` served the health route, existing
  monster records, and built React frontend.

## Result
Task 16 is complete. The modular backend preserves the existing launch command
and `/api` route contract.
