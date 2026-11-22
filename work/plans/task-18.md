---
ID: 18
Objective: Enable rich-text formatting for fields identified as long text
Status: Completed
---

# Proposal

Replace plain textareas for schema fields marked `long text` with a rich-text
editor supporting bold, italic, bullet lists, and tables. Preserve formatting
when profiles are viewed and exported while keeping existing plain-text records
compatible.

# Acceptance criteria

- Long-text fields `summary`, `specials`, and `effect` provide bold, italic,
  bulleted-list, and table editing controls.
- Existing plain-text values remain editable and readable.
- Rendered profile content is restricted to supported formatting elements.
- ODT exports preserve supported formatting and tables.
- The frontend builds and existing backend API tests pass.
