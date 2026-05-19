---
name: project-initializer
description: "Initialize a structured academic research project workspace. Use for creating doctoral project folders, AGENTS.md, project dashboard, literature/data/analysis/manuscript/submission/log directories, research project templates, and reproducible project scaffolds for papers, experiments, EEG/BCI projects, or dissertations."
---

# Project Initializer

Use this skill when starting a new research project or converting a messy folder into a structured workspace.

## Inputs

- Project title and short slug.
- Research domain and methods.
- Planned outputs: paper, dissertation chapter, experiment, EEG/BCI project, dataset, or grant.
- Target journal or degree milestone if known.

## Workflow

1. Create or propose a stable project folder structure.
2. Generate `AGENTS.md` with project-specific rules.
3. Generate `00_project_dashboard/project_status.md`.
4. Generate starter files for weekly plan, research log, data lineage, manuscript versions, and submission tracker.
5. Explain where raw data, processed data, literature, scripts, outputs, and manuscript files should go.

## Hard Constraints

- Never move or delete existing raw data without explicit user approval.
- Do not overwrite existing files unless the user asks or a backup/version is created.
- Keep project instructions concise enough for an agent to read at the start of each task.

## Script

Use `scripts/create_project_skeleton.py` to create a new project skeleton.

## Output

```text
Project folder tree:
Created files:
How to start each session:
Next three setup tasks:
Risks or missing information:
```

