---
name: did-psm-iv-rdd-dml-event-study
description: "Plan, implement, and report DID, event study, PSM, IV, RDD, and DML analyses. Use for quasi-experimental management and information systems studies, parallel trends, matching balance, first stage, exclusion restriction, bandwidth, double machine learning, robustness checks, and causal results tables."
---

# DID PSM IV RDD DML Event Study

Use this skill for common quasi-experimental and causal ML designs.

## Inputs

- Treatment timing, treated/control units, outcome, panel structure.
- Candidate covariates and confounders.
- Proposed design.
- Data granularity and sample restrictions.

## Workflow

1. Match the design to the data-generating setting.
2. For DID/event study, test pre-trends, timing, staggered adoption risks, and control group definition.
3. For PSM, report balance before/after matching and avoid claiming identification from matching alone.
4. For IV, evaluate relevance, exclusion, monotonicity, and first-stage strength.
5. For RDD, justify cutoff, bandwidth, manipulation tests, and local interpretation.
6. For DML, define nuisance models, cross-fitting, target estimand, and interpretability limits.
7. Report assumptions, diagnostics, and robustness alongside effect estimates.

## Hard Constraints

- Do not use two-way fixed effects blindly with problematic staggered adoption.
- Do not treat PSM as a causal design without unconfoundedness assumptions.
- Do not use weak or invalid instruments.
- Do not generalize RDD effects far from the cutoff.
- Do not use DML as a black box to bypass design logic.

## Output

```text
Design fit:
Assumption checklist:
Diagnostics:
Model specification:
Robustness checks:
Results table plan:
Interpretation limits:
Reviewer-risk checklist:
```

