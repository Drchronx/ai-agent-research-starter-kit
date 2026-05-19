---
name: manuscript-version-manager
description: "Manage academic manuscript versions and revision history. Use for manuscript_versions.md, version naming, draft comparison, change summaries, manuscript milestones, version logs, figure/table versioning, and paper draft continuity."
---

# Manuscript Version Manager

Use this skill when creating, comparing, or documenting manuscript drafts.

## Inputs

- Manuscript folder.
- Current draft and previous versions.
- Revision goals.
- Major changes and unresolved issues.

## Workflow

1. Identify current manuscript version and naming scheme.
2. Create a version record before major edits.
3. Summarize changes by section, table, figure, analysis, and references.
4. Track unresolved issues and reviewer risks.
5. Recommend next version name and archive policy.

## Hard Constraints

- Do not overwrite manuscript drafts without explicit approval.
- Do not claim a section changed unless evidence exists or user states it.
- Keep content edits separate from version metadata.

## Script

Use `scripts/create_manuscript_version_log.py` to create a version log template.

## Output

```text
Current version:
Version history:
Changes in this version:
Unresolved issues:
Next version plan:
Archive recommendations:
```

