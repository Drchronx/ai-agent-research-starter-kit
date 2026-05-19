---
name: bci-data-structure
description: "Design and audit BCI and EEG machine-learning data structures. Use for subject/session/run/trial organization, labels, metadata, train-test split units, BIDS-like EEG folders, feature tables, event logs, class balance, and reproducible BCI project structure."
---

# BCI Data Structure

Use this skill before building any EEG/BCI model. Most BCI failures start with unclear subject, session, trial, and label structure.

Use `scripts/create_bci_metadata_template.py` to create a metadata template. Use `references/bci-project-checklist.md` for the project-level checklist.

## Inputs

- Raw EEG files, event logs, behavioral files, and labels.
- Participants, sessions, runs, blocks, trials, and conditions.
- Intended evaluation: within-subject, cross-session, cross-subject, or online.

## Workflow

1. Define the unit hierarchy: subject -> session -> run -> trial -> window.
2. Create a metadata table with subject, session, run, trial, label, condition, timestamp, and file path.
3. Decide split units before modeling: trial-level, session-level, or subject-level.
4. Audit class balance by subject and session.
5. Define raw, processed, features, models, reports, and logs folders.
6. Produce a data dictionary and leakage-risk notes.

## Hard Constraints

- Never overwrite raw EEG files.
- Do not split sliding windows from the same trial across train and test.
- Do not mix subjects across train and test when claiming subject-independent BCI.
- Do not create labels from information unavailable at prediction time.

## Output

```text
Project folder structure:
Metadata schema:
Label schema:
Split unit:
Class-balance audit:
Leakage risks:
Next modeling step:
```
