---
name: erp-segmentation-analysis
description: "Run and report ERP segmentation and component analysis. Use for epoching, baseline correction, artifact rejection, averaging, component windows, ROI electrodes, peak and mean amplitude, latency, topography, ERP statistics, and ERP Results writing."
---

# ERP Segmentation And Analysis

Use this skill for event-related potential analysis after preprocessing.

## Inputs

- Cleaned EEG data.
- Event codes and condition labels.
- Epoch window and baseline window.
- Components and regions of interest.
- Statistical model plan.

## Workflow

1. Verify event markers and condition counts.
2. Define epoch and baseline windows before inspecting effects.
3. Reject or mark bad epochs using predefined criteria.
4. Average by condition and participant.
5. Extract component metrics: mean amplitude, peak amplitude, peak latency, or area under curve.
6. Analyze components with appropriate within/between-subject models.
7. Create waveforms, scalp maps, and component summary tables.

## Hard Constraints

- Do not redefine time windows based on where effects look strongest unless labeled exploratory.
- Do not report only significant electrodes when the ROI was not preregistered.
- Do not interpret noise or low-trial averages as stable ERP effects.

## Output

```text
ERP processing decisions:
Epoch and baseline settings:
Trial-retention table:
Component extraction table:
Statistical model:
Figures needed:
Results paragraph:
Limitations:
```

