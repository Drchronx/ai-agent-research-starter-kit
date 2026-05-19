---
name: eeg-cross-subject-transfer-bci
description: "Plan cross-subject, cross-session, transfer-learning, domain-adaptation, and few-shot BCI workflows. Use for subject-independent EEG decoding, leave-one-subject-out validation, calibration, alignment, CORAL, Riemannian alignment, adversarial domain adaptation, and transfer evaluation."
---

# EEG Cross-Subject Transfer For BCI

Use this skill when the goal is generalization to new subjects or sessions.

## Inputs

- Subject and session metadata.
- Source and target domains.
- Calibration data availability.
- Model type and features.

## Workflow

1. Define target deployment: new subject, new session, new device, or new task.
2. Choose validation: leave-one-subject-out, leave-one-session-out, cross-dataset, or calibration split.
3. Establish non-transfer baselines.
4. Choose transfer method: normalization, covariance alignment, Riemannian alignment, fine-tuning, domain adaptation, or few-shot calibration.
5. Keep target test labels unavailable during adaptation unless the method explicitly uses labeled calibration.
6. Report performance by subject and variance across subjects.

## Hard Constraints

- Do not use target-test labels for adaptation.
- Do not mix target subject trials into training when claiming zero-calibration.
- Do not hide subjects with failed transfer.
- Do not report only pooled accuracy when subject-level performance varies.

## Output

```text
Transfer setting:
Validation design:
Source/target split:
Adaptation method:
Calibration policy:
Subject-wise metrics:
Failure-case analysis:
Reporting paragraph:
```

