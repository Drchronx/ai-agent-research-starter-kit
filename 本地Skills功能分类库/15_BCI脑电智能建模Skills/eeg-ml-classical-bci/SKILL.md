---
name: eeg-ml-classical-bci
description: "Build classical machine-learning workflows for EEG/BCI classification and regression. Use for LDA, logistic regression, SVM, random forest, XGBoost, CSP+LDA, FBCSP, Riemannian classifiers, calibration, hyperparameter tuning, and baseline BCI models."
---

# EEG Classical ML For BCI

Use this skill before deep learning unless data volume and validation justify deep models.

## Inputs

- Feature matrix with metadata.
- Labels and class balance.
- Split design.
- Baseline and candidate models.

## Workflow

1. Establish a chance-level and simple baseline.
2. Choose classical models: LDA, logistic regression, SVM, random forest, XGBoost, CSP+LDA, Riemannian classifiers.
3. Use pipelines so scaling, CSP, feature selection, and model fitting happen inside each training fold.
4. Use nested cross-validation for hyperparameter tuning when possible.
5. Report subject-wise and aggregate metrics.
6. Compare models using paired statistics or permutation tests when appropriate.

## Hard Constraints

- Do not tune hyperparameters on the test set.
- Do not report only the best run without repeated or nested validation.
- Do not ignore subject-level variance.
- Do not compare models on different splits.

## Output

```text
Model candidates:
Pipeline design:
Cross-validation design:
Hyperparameter plan:
Metrics:
Model-comparison plan:
Reporting paragraph:
```

