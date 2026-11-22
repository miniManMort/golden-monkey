# Task 17 log

## Summary
Updated the architecture documentation to describe React/FastAPI as the active
application and moved the legacy desktop applications to `archive/`.

## Work carried out
- Rewrote `spec/README.md` to document the React frontend, FastAPI modules,
  SQLite persistence, migrations, and current run commands.
- Updated the root and React READMEs to mark both desktop implementations as
  archived reference material.
- Moved the Python desktop app and Rust desktop app to `archive/app/` and
  `archive/app-rust/`, with archive-level reference-only documentation.
- Updated `run.sh` to launch the active FastAPI application.
- Removed the sample monster loader's dependency on the archived Python
  package by switching it to SQLite directly.

## Verification
- The six FastAPI API tests passed.
- The standalone sample loader created its expected eight records in a
  temporary database.
- Pylance reported no diagnostics for the updated sample loader.
- `./run.sh --port 8102` served `/api/health` and the built React frontend.

## Result
Task 17 is complete. `app-react` is the documented active app; the legacy
folders remain available for reference under `archive/`.
