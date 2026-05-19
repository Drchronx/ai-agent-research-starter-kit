---
name: eeg-deep-learning-bci
description: "Design EEG deep-learning workflows for BCI and neural decoding. Use for EEGNet, DeepConvNet, ShallowConvNet, CNN-LSTM, TCN, Transformer, self-supervised EEG models, data augmentation, subject-independent training, training logs, regularization, and deep model reporting."
---

# EEG Deep Learning For BCI

Use this skill when model capacity, data size, and validation design justify deep learning.

## Inputs

- Epoched EEG tensors or time-frequency tensors.
- Labels, subjects, sessions, and split plan.
- Target architecture and hardware constraints.

## Workflow

1. Decide whether deep learning is justified over classical baselines.
2. Define tensor shape: trials x channels x time or trials x channels x frequency x time.
3. Split data by the claimed generalization unit before augmentation.
4. Choose architecture: EEGNet, DeepConvNet, ShallowConvNet, CNN-LSTM, TCN, or Transformer.
5. Apply augmentation only to training data.
6. Track seeds, hyperparameters, early stopping, learning curves, and checkpoints.
7. Compare against classical baselines and report uncertainty.

## Hard Constraints

- Do not augment before train-test split.
- Do not let windows from the same trial appear in train and test.
- Do not claim cross-subject decoding from within-subject splits.
- Do not report only maximum validation accuracy.

## Output

```text
Deep-learning suitability:
Tensor schema:
Architecture candidates:
Training protocol:
Regularization and augmentation:
Evaluation design:
Baseline comparison:
Reporting paragraph:
```

