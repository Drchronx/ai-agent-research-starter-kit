# BCI Leakage Audit Template

| Risk | Question | Evidence | Status | Required Fix |
|---|---|---|---|---|
| Window leakage | Same trial windows split across train/test? |  | pass/revise/fail |  |
| Subject leakage | Same subject in train/test for cross-subject claim? |  | pass/revise/fail |  |
| Session leakage | Same session mixed when claiming cross-session? |  | pass/revise/fail |  |
| Normalization leakage | Scaler fit on all data? |  | pass/revise/fail |  |
| CSP/PCA leakage | CSP/PCA fit outside training fold? |  | pass/revise/fail |  |
| Feature selection leakage | Selected features using all labels? |  | pass/revise/fail |  |
| Tuning leakage | Test set used for hyperparameter selection? |  | pass/revise/fail |  |
| Augmentation leakage | Augmented samples cross split boundary? |  | pass/revise/fail |  |
| Target label leakage | Target test labels used in adaptation? |  | pass/revise/fail |  |
| Benchmark mismatch | Compared results use incompatible split? |  | pass/revise/fail |  |

## Final Decision

- Overall: pass / revise / fail
- Must fix before modeling:
- Must fix before manuscript:
