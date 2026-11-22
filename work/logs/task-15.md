# Task 15 log

## Summary
Replaced the `app-react` standard-library HTTP server with FastAPI and Uvicorn.

## Work carried out
- Preserved the health, monster/spell CRUD, validation, ODT export, and built
  React frontend routes.
- Added FastAPI exception handlers to keep the API's `{ "error": ... }`
  response shape and status codes.
- Initialized and migrated the shared SQLite database in the FastAPI lifespan.
- Declared FastAPI and Uvicorn dependencies and updated the app setup guide.
- Reworked the API tests to exercise the FastAPI app through Uvicorn over HTTP.

## Verification
- `python -W error::ResourceWarning -m unittest discover -s tests -v` passed
  all five API, validation, CRUD, and export tests.
- Pylance reported no diagnostics for `server.py` or its tests after the
  migration.
- The documented CLI started successfully and served `/api/health` and the
  built frontend.

## Result
Task 15 is complete. `app-react/server.py` now runs the API and built frontend
with FastAPI.
