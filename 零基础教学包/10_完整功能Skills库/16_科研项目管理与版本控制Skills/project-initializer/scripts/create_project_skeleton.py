#!/usr/bin/env python
import argparse
from datetime import date
from pathlib import Path


DIRS = [
    "00_project_dashboard",
    "01_literature/pdfs",
    "01_literature/notes",
    "01_literature/matrix",
    "02_theory",
    "03_study_design/materials",
    "03_study_design/preregistration",
    "04_data/raw",
    "04_data/processed",
    "04_data/codebook",
    "05_analysis/scripts",
    "05_analysis/output",
    "06_manuscript/drafts",
    "06_manuscript/figures",
    "06_manuscript/tables",
    "07_submission",
    "08_logs",
    "09_archive",
]


def write_if_missing(path, text):
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Create an academic research project skeleton.")
    parser.add_argument("--root", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--methods", default="")
    args = parser.parse_args()

    root = Path(args.root)
    root.mkdir(parents=True, exist_ok=True)
    for d in DIRS:
        (root / d).mkdir(parents=True, exist_ok=True)

    today = date.today().isoformat()
    write_if_missing(root / "AGENTS.md", f"""# Project Agent Instructions

Project: {args.title}
Methods: {args.methods}

Rules:
- Read this file and `00_project_dashboard/project_status.md` before starting.
- Do not overwrite files in `04_data/raw`.
- Write new outputs to the relevant `output`, `logs`, or versioned folder.
- Separate verified findings from hypotheses or unverified notes.
- Update `08_logs/research_log.md` after meaningful work.
""")
    write_if_missing(root / "00_project_dashboard/project_status.md", f"""# Project Status

Project: {args.title}
Created: {today}

## Current Research Question

TBD

## Completed

- Project skeleton created.

## Active Work

- TBD

## Blockers

- TBD

## Next Three Priorities

1. Define research question.
2. Build literature matrix.
3. Specify study design and data needs.
""")
    write_if_missing(root / "08_logs/research_log.md", "# Research Log\n\n")
    write_if_missing(root / "08_logs/weekly_plan.md", "# Weekly Plan\n\n")
    write_if_missing(root / "04_data/codebook/data_lineage.csv", "raw_file,script_or_step,output_file,description,date,notes\n")
    write_if_missing(root / "06_manuscript/manuscript_versions.md", "# Manuscript Versions\n\n")
    write_if_missing(root / "07_submission/submission_tracker.csv", "journal,status,target_fit,submitted_date,decision_date,next_action,notes\n")
    print(root)


if __name__ == "__main__":
    main()

