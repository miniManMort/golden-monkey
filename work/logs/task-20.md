# Task 20 log

## Summary
Reviewed the application structure and recorded prioritized architecture
recommendations in a new task plan.

## Review findings
- The frontend is small in file count but [App.jsx](/home/mort/Projects/golden-monkey/app-react/src/App.jsx)
  combines global state, API access, navigation, list/search UI, profile
  dialogs, export UI, and page rendering.
- A single stylesheet combines base typography, layout, components, modals,
  and TinyMCE overrides.
- Monster and spell CRUD already have separate backend routers, repositories,
  and schemas, providing a good existing foundation.
- Backend routes accept raw dictionaries instead of create/update Pydantic
  request models.
- Rich-text HTML is preserved consistently in the frontend and ODT export
  pipeline, but sanitization and supported-tag rules are not centralized as a
  documented contract.
- The frontend has no component/unit test tooling beyond the production build.
- TinyMCE required-field submission still queries old
  `[contenteditable="true"][data-required="true"]` DOM elements, which is not
  reliable for the iframe-based editor.
- `vite` and `@vitejs/plugin-react` should be development dependencies.

## Recommendation
Use an incremental feature extraction: centralize API access and rich-text
validation first, split monster/spell modules and reusable UI, then split CSS
and introduce frontend tests. The backend already follows useful layers and
needs typed request models and richer contract tests rather than a rewrite.

## Work carried out
- Added a shared `src/api/client.js` library API module for list, CRUD, delete,
  and export operations.
- Extracted shared record defaults and table column configuration.
- Added reusable `Modal` and `Field` components.
- Split the overview page, record table, profile dialogs, export/help dialogs,
  monster fields, and spell fields into dedicated modules.
- Reduced `App.jsx` to application shell state and top-level dialog/page
  orchestration.
- Replaced DOM-based rich-text required-field checks with value-based visible
  text validation.
- Changed monster and spell create/update routes to accept typed Pydantic
  create/update models.
- Moved Vite and the React plugin to development dependencies.
- Preserved omitted monster `specials` as `"None"` for API compatibility.

## Verification
- `npm run build` passed after the frontend extraction.
- All eight backend API tests passed after typed route models were added.
- `npm audit --omit=dev` reported zero production dependency vulnerabilities.
- Fixed save submission by removing `.trim()` calls on numeric rich-text character
  counts in monster summary and spell effect validation.
- Browser repro confirmed create/edit for both monsters and spells was broken
  by `countRichTextCharacters(...).trim()` throwing `Ho(...).trim is not a function`.
  Replaced those guards with numeric zero checks.
- Rebuilt and verified monster create/edit and spell create/edit in the browser.
- Cleaned up temporary browser repro records and reran all eight backend tests.
- Made edit-dialog delete actions explicitly identify monsters and spells and
  clarified the native confirmation text, including the irreversible action.
