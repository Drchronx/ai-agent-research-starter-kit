---
name: eeg-model-evaluation-leakage
description: "Audit EEG/BCI model evaluation and prevent data leakage. Use for subject-wise splits, session-wise splits, trial-window leakage, nested cross-validation, permutation tests, confidence intervals, chance level, repeated runs, class imbalance, and reproducible EEG ML evaluation."
---

# EEG Model Evaluation And Leakage Audit

Use this skill before trusting any EEG/BCI accuracy number.

Use `scripts/create_bci_evaluation_audit.py` to create an evaluation and leakage audit sheet.

## Inputs

- Dataset structure.
- Feature extraction and preprocessing steps.
- Split strategy and model outputs.
- Claimed generalization level.

## Workflow

1. Identify all possible leakage paths: preprocessing, filtering, normalization, feature selection, windows, augmentation, hyperparameters, and early stopping.
2. Match validation split to claim: within-subject, cross-session, cross-subject, or online.
3. Require nested CV when tuning hyperparameters.
4. Compute appropriate metrics: balanced accuracy, AUC, F1, confusion matrix, kappa, ITR when relevant.
5. Estimate uncertainty with subject-level confidence intervals or paired tests.
6. Run permutation or label-shuffle tests when needed.

## Hard Constraints

- Do not evaluate on data used for tuning.
- Do not split overlapping windows randomly.
- Do not aggregate across subjects without subject-level reporting.
- Do not compare against chance without class-balance adjustment.

## Output

```text
Claimed generalization:
Split audit:
Leakage risks:
Required fixes:
Metrics:
Uncertainty and statistical tests:
Accept/reject current evaluation:
```
