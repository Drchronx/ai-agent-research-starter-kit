---
name: eeg-preprocessing-pipeline
description: "Design and audit EEG preprocessing workflows. Use for raw EEG import, channel montage, filtering, referencing, bad channel detection, ICA, artifact rejection, ocular artifacts, epoching preparation, quality control, MNE-Python, EEGLAB, BrainVision, Neuroscan, EDF, BDF, and preprocessing reports."
---

# EEG Preprocessing Pipeline

Use this skill when raw EEG data must be cleaned reproducibly.

Use `references/eeg-qc-checklist.md` for quality-control criteria. Use `scripts/create_eeg_qc_template.py` to create a participant-level QC sheet.

## Inputs

- File format and acquisition system.
- Montage and channel locations.
- Sampling rate.
- Event marker file.
- Target analysis: ERP, time-frequency, connectivity, or classification.

## Workflow

1. Preserve raw data and create a processed-data folder.
2. Import raw data and verify channel names, montage, sampling rate, and events.
3. Apply filtering appropriate to the downstream analysis.
4. Detect bad channels and interpolate only with documented rationale.
5. Re-reference according to the analysis plan.
6. Use ICA or artifact correction when justified; document removed components.
7. Epoch only after event integrity is checked.
8. Create a quality-control report: retained trials, rejected trials, bad channels, ICA decisions.

## Hard Constraints

- Never overwrite raw EEG data.
- Do not choose filters after seeing hypothesis results.
- Do not remove ICA components without documented rationale.
- Do not mix preprocessing choices across conditions unless explicitly justified.

## Output

```text
Preprocessing plan:
Recommended parameters:
QC metrics:
Artifact policy:
Folder structure:
Reproducible script plan:
Reviewer-facing preprocessing paragraph:
```
