---
name: eeg-ml-classification
description: "Build EEG machine learning and deep learning classification workflows. Use for feature extraction, train-test split, cross-validation, leakage prevention, ERP/frequency features, CSP, Riemannian features, CNN/RNN/Transformer EEG models, BCI classification, metrics, and model reporting."
---

# EEG Machine Learning Classification

Use this skill for predictive modeling from EEG data.

## Inputs

- Feature type: ERP amplitudes, band power, time-frequency maps, connectivity, raw epochs, or learned representations.
- Labels and class balance.
- Participant structure and repeated measures.
- Model family and validation plan.

## Workflow

1. Define the prediction target and label source.
2. Prevent leakage: split by participant when generalization across participants is claimed.
3. Extract features using only training data transformations inside cross-validation.
4. Choose baseline models before deep models.
5. Report accuracy, balanced accuracy, AUC, F1, confusion matrix, and confidence intervals.
6. Use permutation tests or nested cross-validation when appropriate.
7. Interpret models cautiously; prediction is not mechanism by itself.

## Hard Constraints

- Do not mix epochs from the same participant across train and test when claiming subject-independent performance.
- Do not tune hyperparameters on the test set.
- Do not report a single accuracy without baseline, chance level, and uncertainty.

## Output

```text
Prediction target:
Feature plan:
Validation design:
Leakage audit:
Model candidates:
Metrics:
Interpretation limits:
Reporting paragraph:
```

