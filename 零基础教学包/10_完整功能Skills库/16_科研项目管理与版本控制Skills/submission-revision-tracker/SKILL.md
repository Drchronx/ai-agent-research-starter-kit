---
name: submission-revision-tracker
description: "Track journal submission, reviewer comments, revisions, and response letters. Use for submission_tracker.csv, target journal pipeline, desk reject risk, reviewer comment extraction, response letter task table, revision status, resubmission checklist, and publication workflow management."
---

# Submission Revision Tracker

Use this skill when preparing submission, tracking journals, or responding to reviews.

## Inputs

- Target journals.
- Manuscript version.
- Submission requirements.
- Reviewer comments or decision letter.
- Response letter draft if available.

## Workflow

1. Create or update a journal submission tracker.
2. Record target journal fit, status, dates, files, and next action.
3. If reviewer comments are provided, split them into actionable items.
4. Classify comments by theory, methods, data, analysis, writing, formatting, or ethics.
5. Track response status and manuscript changes.

## Hard Constraints

- Do not mark reviewer issues resolved unless there is a response and manuscript evidence.
- Do not fabricate journal requirements; verify current author guidelines when needed.
- Keep confidential reviewer materials inside the project.

## Script

Use `scripts/create_submission_tracker.py` to create a submission tracker CSV.

## Output

```text
Submission tracker:
Reviewer issue table:
Response priorities:
Files needed:
Risks before resubmission:
Next actions:
```

