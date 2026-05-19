---
name: bci-benchmark-datasets
description: "Select and use public BCI and EEG benchmark datasets. Use for BCI Competition, MOABB, PhysioNet EEG, OpenNeuro EEG, motor imagery, P300, SSVEP, workload, emotion, dataset documentation, licensing, subject splits, and benchmark comparability."
---

# BCI Benchmark Datasets

Use this skill when choosing public datasets or comparing methods against benchmarks.

## Inputs

- Research task: motor imagery, P300, SSVEP, workload, attention, emotion, HCI, neuromarketing, or clinical BCI.
- Target model and evaluation design.
- Dataset constraints: license, channels, sampling rate, subjects, sessions, labels.

## Workflow

1. Define the task and target population.
2. Search candidate datasets using reliable sources such as dataset repositories, MOABB-compatible datasets, PhysioNet, OpenNeuro, or BCI Competition archives.
3. Compare datasets by subjects, sessions, channels, labels, paradigm, sampling rate, and license.
4. Decide whether the benchmark supports the desired claim.
5. Document preprocessing and split rules to keep results comparable.
6. Flag dataset-specific caveats.

## Hard Constraints

- Do not claim a dataset supports a task if labels or paradigm do not match.
- Do not ignore license or citation requirements.
- Do not compare benchmark results with different split rules as if equivalent.
- Verify current dataset URLs and documentation before final citation.

## Output

```text
Dataset candidates:
Dataset comparison table:
Recommended dataset:
Split and preprocessing rules:
Citation/licensing needs:
Benchmark limitations:
```

