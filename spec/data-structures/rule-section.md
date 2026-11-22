---
Name: rule-section
Description: A Rule Section text block
DB Table Name: rule_section
Model Name: RuleSection
Status: Proposed
---

| attribute | type | constraints |
| --- | --- | --- |
| id | Text | primary key default=uuid4.hex |
| name | Text | not null |
| section_text | Text | not null default "None" long text; supports headings, bold, italic, bulleted lists, and tables |
