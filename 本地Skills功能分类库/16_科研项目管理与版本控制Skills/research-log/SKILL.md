---
name: research-log
description: "Maintain research logs and decision records for academic projects. Use for research_log.md, experiment logs, modeling decisions, literature decisions, analysis decisions, daily work records, decision rationale, output file inventory, and reproducibility notes."
---

# Research Log

Use this skill after meaningful project work to preserve continuity.

## Inputs

- What was done.
- Files read, created, or modified.
- Decisions made and rationale.
- Reliable findings and uncertain findings.
- Next steps.

## Workflow

1. Identify the session date, task, inputs, outputs, and tools used.
2. Record decisions and why they were made.
3. Record generated files and their purposes.
4. Separate confirmed conclusions from items needing verification.
5. Update next actions and blockers.

## Hard Constraints

- Do not record fabricated progress.
- Do not claim data or citations are verified unless verification happened.
- Preserve analysis caveats and failed attempts.

## Script

Use `scripts/append_research_log.py` for appending a structured log entry.

## Output

```text
Log entry:
Files changed:
Decisions:
Findings:
Unverified items:
Next actions:
```

