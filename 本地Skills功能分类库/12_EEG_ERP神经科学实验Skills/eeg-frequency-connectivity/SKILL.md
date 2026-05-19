---
name: eeg-frequency-connectivity
description: "Analyze EEG frequency-domain, time-frequency, ERSP, power, phase, and functional connectivity outcomes. Use for alpha beta theta gamma power, wavelet/STFT, baseline normalization, coherence, PLV, wPLI, graph metrics, source-space caveats, and neurophysiology reporting."
---

# EEG Frequency And Connectivity

Use this skill when EEG hypotheses concern oscillatory power, time-frequency dynamics, or connectivity.

## Inputs

- Cleaned continuous or epoched EEG.
- Frequency bands or time-frequency parameters.
- Baseline period.
- Conditions, ROIs, and analysis model.

## Workflow

1. Define frequency bands or time-frequency method.
2. Choose baseline correction or normalization.
3. Compute power, ERSP, ITC, phase metrics, or connectivity.
4. Aggregate by ROI, time window, and frequency band.
5. Control multiple comparisons or use planned ROIs.
6. Create time-frequency plots, band-power topographies, and connectivity visuals.

## Hard Constraints

- Do not interpret frequency bands without task timing and theoretical justification.
- Connectivity is not causal direction unless the method supports it and assumptions are satisfied.
- Avoid circular ROI and time-window selection.

## Output

```text
Frequency/connectivity plan:
Parameter table:
Baseline and normalization:
ROI and time-window decisions:
Statistical model:
Figure plan:
Results paragraph:
Reviewer risks:
```

