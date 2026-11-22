# Golden Monkey Architecture

Golden Monkey is a React web application for managing monsters, spells,
character classes, and rule sections. The application is under
[app-react](../app-react).

## Active application

The frontend is a React/Vite single-page application in
[app-react/src](../app-react/src). It provides the overview and registries for
monsters, spells, character classes, and rule sections, including profile forms,
searches, detail views, and ODT export controls.

The FastAPI backend is organized as a Python package in
[app-react/backend](../app-react/backend):

- `app.py` creates the FastAPI application, initializes the database through
  the lifespan, registers shared middleware and error handlers, and serves the
  built frontend.
- `database.py` owns SQLite connections, schema creation, and legacy schema
  migrations.
- `schemas/` defines Pydantic monster and spell create, update, and read
  records, including input normalization and validation.
- `repositories/` owns record-specific SQLite queries and persistence.
- `routers/` exposes the health, monster, spell, and export API endpoints.
- `services/odt.py` generates the OpenDocument Text exports.
- [server.py](../app-react/server.py) is the compatibility command-line
  launcher for the application.

The backend uses Python's SQLite support and the FastAPI/Uvicorn dependencies
listed in [app-react/requirements.txt](../app-react/requirements.txt). It reads
and writes the shared [data/golden_monkey.db](../data/golden_monkey.db) file.
Database startup creates missing tables and migrates the former `save` column
to `save_as` and adds `specials` when needed.

For development, install the Python requirements, start `python
app-react/server.py`, then run Vite from `app-react` with `npm install` and
`npm run dev`. For a built deployment, run `npm run build` in `app-react` and
start the same Python launcher. Detailed commands are in
[app-react/README.md](../app-react/README.md).

Data-structure and page requirements remain documented in
[data-structures](data-structures) and [pages](pages). Project work plans and
implementation logs are kept in [work](../work).
