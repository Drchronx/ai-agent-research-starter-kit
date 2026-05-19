# BCI Results Report Template

## Split Disclosure

Describe the split first. State whether the result is within-subject, cross-session, cross-subject, cross-dataset, pseudo-online, or online.

## Baseline And Chance

| Model | Split | Chance | Balanced Accuracy | AUC | F1 | Notes |
|---|---|---:|---:|---:|---:|---|

## Subject-Wise Metrics

| Subject | Accuracy | Balanced Accuracy | AUC | F1 | Failed? | Notes |
|---|---:|---:|---:|---:|---|---|

## Confusion Matrix

Fill one matrix per main model. Include class labels and sample size.

## Statistical Comparison

- Paired test or permutation test:
- Correction:
- Effect size:
- CI:

## Leakage Safeguards

- Split rule:
- Fold-internal preprocessing:
- Tuning:
- Augmentation:
- Transfer policy:

## Limitations

- Offline/online boundary:
- Subject variability:
- Dataset limitation:
- Model interpretability limitation:
- Claim not supported:
