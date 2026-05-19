---
name: bci-results-reporting
description: "Write BCI and EEG machine-learning results for papers. Use for subject-wise performance tables, accuracy, balanced accuracy, AUC, F1, confusion matrix, ITR, confidence intervals, permutation tests, baseline comparison, leakage disclosure, model architecture table, and BCI manuscript reporting."
---

# BCI Results Reporting

Use this skill to turn EEG/BCI modeling outputs into manuscript-ready results.

## Inputs

- Model outputs and metrics.
- Split design and leakage audit.
- Baselines and comparison models.
- Target journal or conference style.

## Workflow

1. Report the data split first, because it defines the claim.
2. Provide subject-wise and aggregate metrics.
3. Include baseline and chance-level comparison.
4. Report uncertainty: confidence intervals, standard deviation across subjects, or paired tests.
5. Include confusion matrix and class-level metrics for imbalanced tasks.
6. Disclose preprocessing, feature extraction, tuning, and leakage safeguards.
7. State deployment limits: within-subject, cross-session, cross-subject, offline, pseudo-online, or online.

## Hard Constraints

- Do not report only the best fold or best seed.
- Do not omit failed subjects.
- Do not describe offline results as real-time BCI.
- Do not hide leakage risks or post hoc model selection.

## Output

```text
Results table plan:
Subject-wise table:
Model-comparison table:
Figure plan:
Leakage and split disclosure:
Results paragraph:
Limitations paragraph:
```

