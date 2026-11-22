---
ID: 16
Objective: Refactor the app-react FastAPI backend into model-focused modules
Status: Completed
---

# Proposal

`app-react/server.py` is currently 572 lines and combines SQLite schema setup,
record normalization/validation, CRUD SQL, ODT generation, FastAPI exception
handling, routes, static file delivery, and the Uvicorn CLI. Split these
responsibilities into a small backend package while keeping the existing React
client, SQLite file, and API contract unchanged.

## Proposed layout

```text
app-react/
  backend/
    __init__.py
    app.py                 # FastAPI app, lifespan, middleware, error handlers
    database.py            # database path, connection context, schema/migrations
    errors.py              # shared API error type
    schemas/
      __init__.py
      monster.py           # monster create/update/read Pydantic models
      spell.py             # spell create/update/read Pydantic models
    repositories/
      __init__.py
      monsters.py          # monster SQLite queries and persistence
      spells.py            # spell SQLite queries and persistence
    routers/
      __init__.py
      health.py            # /api/health
      monsters.py          # /api/monsters CRUD
      spells.py            # /api/spells CRUD
      exports.py           # /api/export/monsters and /api/export/spells
    services/
      __init__.py
      odt.py               # shared ODT XML/ZIP generation
    cli.py                 # Uvicorn host/port command
  server.py                # backwards-compatible CLI entry point
```

## Responsibilities and boundaries

- Keep SQL, row mapping, unique-name checks, and persistence in the
  resource-specific repositories. Put shared connection setup and the existing
  legacy-column migration in `database.py`.
- Use separate Pydantic input and output schemas for monsters and spells.
  Preserve the current validation rules and user-facing messages; keep
  uniqueness checks in the repositories, where the database constraint is
  authoritative.
- Put each resource's endpoints in its own `APIRouter`. Keep shared exception
  mapping, request-size middleware, lifespan initialization, router
  registration, and frontend fallback in `app.py`.
- Move ODT package writing and profile formatting out of the routes and into
  `services/odt.py`; export routes should only load sorted records and return
  the download response.
- Retain `python app-react/server.py` as the supported command. Make
  `server.py` a thin shim that imports the package app and invokes the CLI,
  avoiding a breaking change to the README instructions.

## Suggested implementation sequence

1. Extract the database connection and initialization without changing SQL or
   the shared database path.
2. Add the Pydantic schemas and move monster/spell validation and CRUD
   persistence into repositories.
3. Extract the health, monster, spell, and export routers and register them
   from the FastAPI app module.
4. Move ODT generation, then leave static serving, shared middleware/error
   handling, and app lifespan in the app module.
5. Reduce `server.py` to the CLI/import shim and update tests and documentation.

## Acceptance criteria

- Existing frontend endpoints, response shapes/status codes, validation
  messages, regex-independent listing order, export sorting, and ODT contents
  remain compatible.
- The app continues using `data/golden_monkey.db`; initialization preserves
  existing records and the legacy `save` to `save_as` / `specials` migrations.
- Existing API tests pass, with focused coverage for schema validation,
  repository CRUD and duplicate names, ODT output, and static frontend serving.
- `python app-react/server.py` still starts the FastAPI app, and the React UI
  continues to work through the same `/api` routes.
- No changes are made to the original desktop implementation in `app/`.
