# BCI Project Checklist

Use this checklist before modeling.

## Data

- Raw EEG files are read-only.
- Subject, session, run, trial, and window IDs are explicit.
- Labels are traceable to events or behavioral logs.
- Class balance is checked by subject and session.
- Split unit is decided before feature engineering.

## Modeling

- Baselines are defined before deep models.
- Feature transforms are fit inside training folds.
- Hyperparameters are tuned inside nested CV or validation folds.
- Subject-wise metrics are reported.
- Cross-subject claims use subject-level splits.

## Reporting

- Offline, pseudo-online, and online performance are separated.
- Chance level and uncertainty are reported.
- Failed subjects and high-variance subjects are not hidden.
- Interpretability is not overstated as neural mechanism.

