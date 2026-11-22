---
ID: 13
Objective: Extract spell details to open document format file
Status: Proposed
---

# Outline
This task adds the ability to extract spell profiles to an open document format file.

- Add menu option Extract to spell menu on home page
- On choosing Extract show dialog asking how the data is to be sorted (options are by Name or by Level/Name) and the location/name for the file to be created
- All spell details are then added to the new file in the order requested.

The format/layout for each spell is as follows

### {name}
| Level | Range | Duration | Save Allowed |
| --- | --- | --- | --- | 
| {level} | {range} | {duration} | {save_allowed} |

{effect}