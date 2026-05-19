---
name: data-lineage-tracker
description: "Track data lineage and reproducibility for academic projects. Use for raw-to-processed data flow, data cleaning logs, script-to-output mapping, analysis provenance, dataset versioning, data dictionaries, non-overwrite raw data rules, and reproducibility audit trails."
---

# Data Lineage Tracker

Use this skill whenever raw data are cleaned, transformed, merged, analyzed, or exported.

## Inputs

- Raw data folder.
- Processed data folder.
- Scripts or notebooks.
- Output files.
- Cleaning and exclusion rules.

## Workflow

1. Inventory raw, intermediate, processed, and output files.
2. Map each processed file to its raw inputs and script.
3. Record cleaning rules, exclusion rules, variable construction, and dates.
4. Identify orphan outputs and untracked transformations.
5. Produce a data lineage table and reproducibility checklist.

## Hard Constraints

- Never overwrite raw data.
- Do not describe a dataset as reproducible if scripts or inputs are missing.
- Do not hide manual edits; mark them clearly.

## Script

Use `scripts/create_data_lineage_template.py` to create a lineage CSV.

## Output

```text
Data inventory:
Lineage table:
Untracked transformations:
Raw data protection check:
Reproducibility gaps:
Next fixes:
```

