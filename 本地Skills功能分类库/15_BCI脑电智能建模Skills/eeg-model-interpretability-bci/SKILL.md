---
name: eeg-model-interpretability-bci
description: "Interpret EEG/BCI machine-learning and deep-learning models. Use for spatial patterns, CSP patterns, saliency maps, frequency importance, temporal importance, SHAP, permutation importance, topographies, model explanation limits, and neural interpretation cautions."
---

# EEG Model Interpretability For BCI

Use this skill after model evaluation is leakage-safe.

## Inputs

- Trained model and evaluation results.
- Feature names or tensor dimensions.
- Channels, time windows, frequency bands, and task timing.

## Workflow

1. Choose interpretation method that matches the model and feature type.
2. For classical models, inspect coefficients, CSP patterns, permutation importance, or SHAP with caution.
3. For deep models, inspect saliency, occlusion, temporal/frequency/channel importance, and learned filters.
4. Map importance to channels, time, and frequency.
5. Check whether patterns are stable across subjects and folds.
6. Separate predictive importance from neural mechanism claims.

## Hard Constraints

- Do not interpret leakage-driven performance.
- Do not treat model saliency as proof of brain mechanism.
- Do not report cherry-picked subject maps as general effects.
- Do not ignore preprocessing and reference effects on spatial patterns.

## Output

```text
Interpretability method:
Channel/time/frequency findings:
Stability checks:
Figures:
Mechanistic interpretation limits:
Reporting paragraph:
```

