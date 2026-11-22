---
ID: 20
Objective: Improve application code structure and maintainability
Status: Completed
---

# Proposal

Add a staged architecture cleanup for the React frontend and FastAPI backend.
This is a recommendation and implementation task, not a behavior rewrite.
Preserve the existing API, SQLite records, rich-text HTML format, ODT exports,
and user workflows.

# Recommendations

## 1. Split the frontend application by responsibility

[App.jsx](/home/mort/Projects/golden-monkey/app-react/src/App.jsx) currently
combines application state, API calls, navigation, tables, forms, dialogs,
export handling, and page rendering. Split it into feature-oriented modules:

- `src/app/App.jsx` or `src/App.jsx` as the shell only.
- `src/api/client.js` for the shared HTTP request wrapper.
- `src/features/monsters/` for monster columns, fields, table, details, and dialog.
- `src/features/spells/` for spell columns, fields, table, details, and dialog.
- `src/components/` for reusable layout, modal, fields, buttons, and alerts.
- `src/pages/` for overview and registry pages.
- `src/constants/` or `src/config/` for shared empty records and column definitions.

Keep local search state in the registry component and keep server collection
state in one app-level data hook or store.

## 2. Centralize frontend data access

Replace direct `request()` calls scattered across pages and dialogs with hooks
or a small API module:

- `getMonsters`, `createMonster`, `updateMonster`, and `deleteMonster`.
- `getSpells`, `createSpell`, `updateSpell`, and `deleteSpell`.
- `exportMonsters` and `exportSpells`.

Each operation should return data or a typed application error and provide one
consistent refresh/invalidation path.

## 3. Move validation into reusable form definitions

The monster and spell dialogs duplicate field metadata and contain form logic
that is difficult to test. Define field/section configuration per profile type,
then keep `Field` as a generic renderer.

Also replace DOM queries for TinyMCE required-field validation. Required rich
text should have an explicit value/ref API or register with the form state.
This avoids relying on `[contenteditable="true"]`, which no longer represents
TinyMCE's iframe implementation.

## 4. Split styles by feature

One 200+ line stylesheet with global page rules makes ownership unclear and
TinyMCE overrides easy to miss. Split CSS by concern:

- `styles/base.css` for reset, tokens, and typography.
- `styles/layout.css` for shell, navigation, footer, and modal.
- `styles/components.css` for buttons, tables, alerts, and fields.
- Feature CSS for monster/spell and homepage-specific layouts.

Keep the TinyMCE iframe content styles in the editor configuration or an
explicit editor stylesheet instead of mixing it with the main app rules.

## 5. Add routes and testable frontend boundaries

Use a real client-side router or a small route abstraction so Overview,
Monsters, Spells, and dialog state can be addressed and tested independently.
Add Vitest and React Testing Library for:

- Rich text conversion and sanitization.
- Monster/spell form validation.
- Search behavior.
- CRUD loading/error states.
- Required fields and save flows.

## 6. Tighten backend boundaries

The backend already has useful router, repository, schema, and service layers,
but duplicate CRUD patterns remain.

- Change request routes from `dict[str, Any]` to create/update Pydantic models.
- Move `prepare_*` normalization and validation ahead of repository writes.
- Keep repositories limited to SQL and return Pydantic read models.
- Centralize exception-to-response handling where possible.
- Make sort order and export sort parameters typed/validated.
- Move static frontend serving and API application assembly into named modules
  if route count continues to grow.

## 7. Add a single rich-text contract

Keep the accepted rich-text tag and attribute set in one backend and frontend
contract. The frontend currently owns sanitization while the backend only
relies on model text handling and export parsing. Add contract tests for:

- Allowed tags and dropped unsafe content.
- Plain-text compatibility.
- Visible character counts.
- Exported ODT formatting.
- Persistence round trips.

## 8. Package and build cleanup

- Move `@vitejs/plugin-react` and `vite` to `devDependencies`.
- Keep TinyMCE assets generated into `public/tinymce` reproducibly.
- Add an asset-generation or prebuild check that fails clearly if npm dependencies
  are missing.
- Consider a route/build test to verify the FastAPI fallback does not expose
  filesystem paths outside `dist`.

# Recommended implementation order

1. Fix or test rich-text required-field validation.
2. Extract frontend API and shared UI primitives.
3. Split monster/spell feature modules and dialog/table components.
4. Split global CSS and add frontend tests.
5. Replace raw route dictionaries with typed request schemas.
6. Centralize rich-text and sort contracts.

# Acceptance criteria

- `App.jsx` is reduced to application shell, routing/page selection, and
  top-level data orchestration.
- Monster and spell behavior is grouped in feature modules.
- API calls and error handling are centralized.
- Shared form and rich-text validation works without DOM-specific selectors.
- Frontend unit/component tests cover core data transformations and workflows.
- Backend request models are typed and repository SQL remains isolated.
- Existing API tests and production build continue to pass.
