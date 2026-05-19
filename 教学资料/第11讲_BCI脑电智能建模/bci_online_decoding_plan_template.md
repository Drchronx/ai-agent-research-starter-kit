# BCI Online Decoding Plan Template

## System Type

- Offline:
- Pseudo-online:
- Real online:

## Streaming Constraints

- Sampling rate:
- Window length:
- Step size:
- Buffer:
- Hardware:

## Causal Preprocessing

- Filter:
- Referencing:
- Artifact handling:
- Feature extraction:
- Future samples used? Must be no.

## Decision Rule

- Model:
- Probability threshold:
- Smoothing:
- Majority voting:
- Rejection class:
- Feedback timing:

## Latency Budget

| Component | Expected ms |
|---|---:|
| Acquisition buffer |  |
| Preprocessing |  |
| Feature extraction |  |
| Inference |  |
| Decision smoothing |  |
| Feedback display |  |

## Online Metrics

- Accuracy:
- Balanced accuracy:
- False positive rate:
- Time-to-decision:
- ITR:
- User fatigue:

## Offline-Online Gap

Explain why offline performance may not transfer to online deployment.
