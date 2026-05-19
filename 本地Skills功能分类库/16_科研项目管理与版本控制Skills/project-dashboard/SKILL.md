---
name: project-dashboard
description: "Maintain a research project dashboard and status summary. Use for project_status.md, current research question, completed tasks, blockers, next actions, active files, current manuscript version, experiment status, data status, and weekly research dashboard updates."
---

# Project Dashboard

Use this skill at the start or end of a research session to keep the project state visible.

## Inputs

- `AGENTS.md`.
- Existing `project_status.md`.
- Recent research logs.
- Folder tree and recent modified files.

## Workflow

1. Read project instructions and current status.
2. Summarize the current research question, theory, data, analysis, manuscript, and submission state.
3. List recently completed work and unresolved blockers.
4. Identify the next three high-priority actions.
5. Update or propose updates to the project dashboard.

## Hard Constraints

- Do not mark tasks completed unless there is file evidence or explicit user confirmation.
- Separate verified project facts from inferred status.
- Do not silently change project scope.

## Output

```text
Current status:
Evidence used:
Completed:
Blockers:
Next three priorities:
Files to update:
Questions for user:
```

