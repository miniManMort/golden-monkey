---
ID: 19
Objective: Replace the custom rich text editor with TinyMCE
Status: Completed
---

# Proposal

Replace the hand-built contentEditable rich-text field with the TinyMCE React
editor while preserving the existing rich HTML data format and supported
formatting contract.

# Acceptance criteria

- Long-text fields use TinyMCE instead of the custom toolbar/contentEditable.
- Bold, italic, bulleted lists, and tables remain available.
- Existing plain-text and rich-text values remain editable.
- Output remains restricted to the existing supported HTML elements.
- The frontend builds and existing backend API tests pass.
