# Work Plans Summary

This folder contains implementation plans and execution logs for the Golden Monkey
application. The plans below are ordered by task number.

## Task summary

| Task | Status | Summary |
| --- | --- | --- |
| [1](plans/task-1.md) | Proposed | Create the initial home page with a welcome message, application overview, navigation menu, and Help dialog. |
| [2](plans/task-2.md) | Completed | Add the monster data model and create-monster form, including persistence and validation. |
| [3](plans/task-3.md) | Completed | Add the monster list page and navigation entry, with the table view but without later view/edit actions. |
| [4](plans/task-4.md) | Completed | Add a view-details action for each monster record. |
| [5](plans/task-5.md) | Completed | Add monster editing and deletion, including save and confirmation behavior. |
| [6](plans/task-6.md) | Completed | Add regex search for monsters by name, level, or alignment and update the list specification. |
| [7](plans/task-7.md) | Completed | Add the monster `specials` field to create, modify, detail, and persistence flows. |
| [8](plans/task-8.md) | Completed | Add ODT extraction for monster profiles, including sort and output-location choices. |
| [9](plans/task-9.md) | Completed | Add the spell data model and create-spell form, including persistence and validation. |
| [10](plans/task-10.md) | Completed | Add the spell list page and navigation entry, initially without view/edit actions. |
| [11](plans/task-11.md) | Completed | Add a view-details action for each spell record. |
| [12](plans/task-12.md) | Completed | Add spell editing and deletion, including save and confirmation behavior. |
| [13](plans/task-13.md) | Proposed | Add ODT extraction for spell profiles, with sorting and an output file dialog. |
| [14](plans/task-14.md) | Completed | Rewrite the application as an active React web app backed by SQLite and a local HTTP API. |
| [15](plans/task-15.md) | Completed | Convert the React backend server to FastAPI while preserving routes and behavior. |
| [16](plans/task-16.md) | Completed | Refactor the FastAPI backend into database, schema, repository, router, service, and CLI modules. |
| [17](plans/task-17.md) | Completed | Document React/FastAPI as the active architecture and archive the legacy implementations. |
| [18](plans/task-18.md) | Completed | Add rich-text editing for long-text fields with supported formatting and ODT preservation. |
| [19](plans/task-19.md) | Completed | Replace the custom rich-text editor with TinyMCE while preserving data and supported HTML. |
| [20](plans/task-20.md) | Completed | Recommend and implement maintainability improvements across the frontend and backend. |
| [21](plans/task-21.md) | Completed | Add character class management: navigation, list/view/edit summaries, and create workflows. |
| [22](plans/task-22.md) | Completed | Add pages to manage rule section records, including navigation, listing, creation, viewing, editing, and deletion. |
| [23](plans/task-23.md) | Completed | Update the home page to summarize and provide actions for the complete application library. |
| [24](plans/task-24.md) | Completed | Reorder left-side menus and home-page widgets to show rules, classes, spells, and monsters. |
| [25](plans/task-25.md) | Completed | Allow headings in rule text by enabling heading insertion in the add/modify rule-segment editor. |

## Progress overview

- Tasks 1-12 cover the original desktop application's core monster and spell workflows.
- Tasks 13 proposes spell ODT extraction but is not marked completed.
- Tasks 14-17 establish and document the React/FastAPI implementation.
- Tasks 18-21 add rich-text support, architectural cleanup, and character class management.
- Task 22 adds rule section management pages and ODT export support.
- Task 23 updates the home page for the complete application library.
- Task 24 orders the left-side menus and home-page widgets as rules, classes, spells, and monsters.
- Task 25 enables heading insertion in rule-section rich-text editing and preserves headings in ODT exports.
