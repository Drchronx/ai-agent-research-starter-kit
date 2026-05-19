---
name: eeg-feature-engineering-bci
description: "Create EEG/BCI feature-engineering plans. Use for band power, PSD, ERP features, CSP, FBCSP, Riemannian covariance features, connectivity features, time-window features, normalization, feature scaling, and feature extraction inside cross-validation."
---

# EEG Feature Engineering For BCI

Use this skill when converting EEG trials or windows into model-ready features.

## Inputs

- Cleaned EEG or epochs.
- Task type: motor imagery, P300, SSVEP, workload, emotion, attention, neuromarketing, or HCI.
- Frequency bands, time windows, channels, and labels.
- Evaluation design.

## Workflow

1. Choose features based on task physiology and timing.
2. Define windows and channels before seeing model performance.
3. Extract baseline features: time-domain statistics, band power, PSD, ERP amplitude/latency.
4. Add BCI features when relevant: CSP, FBCSP, Riemannian covariance, connectivity.
5. Fit scaling, feature selection, CSP, PCA, or normalization only on training folds.
6. Export feature matrix with subject/session/trial metadata.

## Hard Constraints

- Do not fit feature selection or normalization on the full dataset before cross-validation.
- Do not choose windows after inspecting test performance.
- Do not use future samples in online or pseudo-online features.
- Do not report feature importance as neural mechanism without caution.

## Output

```text
Feature set:
Window and channel plan:
Training-fold-only transforms:
Feature matrix schema:
Baseline features:
Advanced features:
Leakage audit:
```

