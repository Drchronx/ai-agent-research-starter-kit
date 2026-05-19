---
name: bci-online-decoding
description: "Design online or pseudo-online BCI decoding workflows. Use for sliding windows, real-time inference, latency, calibration, feedback, adaptive thresholds, stream processing, online metrics, offline-to-online gap, and deployment safety."
---

# BCI Online Decoding

Use this skill when moving from offline EEG classification to real-time or pseudo-online BCI.

## Inputs

- Sampling rate and streaming system.
- Window length, step size, and prediction target.
- Model and preprocessing pipeline.
- Feedback and decision rule.

## Workflow

1. Define online constraints: latency, window length, update rate, and hardware.
2. Specify causal preprocessing that uses only past and current samples.
3. Define calibration and model loading.
4. Design smoothing, confidence thresholds, rejection class, or majority voting.
5. Track online metrics: accuracy, latency, false positives, time-to-decision, ITR, and user fatigue.
6. Separate offline, pseudo-online, and real online results.

## Hard Constraints

- Do not use future samples in online filters or features.
- Do not tune thresholds on online test data.
- Do not present offline accuracy as online performance.
- Do not ignore latency and user feedback timing.

## Output

```text
Online decoding architecture:
Windowing plan:
Causal preprocessing:
Decision rule:
Latency budget:
Online metrics:
Offline-online gap:
Deployment risks:
```

