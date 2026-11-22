---
ID: 15
Objective: Convert the app-react backend to FastAPI
Status: Completed
---

# Outline
Replace the standard-library HTTP server in `app-react/server.py` with FastAPI.

- Preserve the existing CRUD, health, export, and built-frontend routes and their response formats.
- Keep SQLite validation, migration, and ODT generation behavior intact.
- Add backend dependencies and update run/test documentation.
- Adapt the API tests to exercise the FastAPI application.
