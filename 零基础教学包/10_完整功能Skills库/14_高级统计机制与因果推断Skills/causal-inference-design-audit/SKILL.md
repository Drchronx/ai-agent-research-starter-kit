---
name: causal-inference-design-audit
description: "Audit and design causal inference strategies for management, information systems, marketing, psychology, and text-mining empirical research. Use for causal claims, DAGs, confounding, identification, DID, PSM, IV, RDD, DML, matching, controls, mechanisms, heterogeneity, and what cannot be interpreted causally."
---

# Causal Inference Design Audit

Use this skill before writing causal claims or running quasi-experimental analyses.

Use `references/causal-claim-ladder.md` when deciding how strong the manuscript language can be.

## Inputs

- Research question.
- Treatment/exposure, outcome, timing, and data source.
- Proposed design: experiment, DID, PSM, IV, RDD, DML, panel, or observational regression.
- Variables, confounders, mediators, moderators, and measurement timing.

## Workflow

1. State the causal estimand.
2. Draw or describe a DAG.
3. Identify confounders, colliders, mediators, bad controls, and post-treatment variables.
4. Evaluate identification assumptions.
5. Choose an analysis strategy that matches the design.
6. Define robustness checks and falsification tests.
7. Rewrite claims to match the design strength.

## Hard Constraints

- Do not let robustness checks substitute for identification.
- Do not control for post-treatment variables when estimating total effects.
- Do not call observational correlations causal without identification.
- Do not overinterpret text-mining variables as exogenous treatments without design support.

## Output

```text
Causal estimand:
DAG/confounding audit:
Identification assumptions:
Recommended method:
Bad controls:
Robustness and falsification:
Permitted claims:
Claims to avoid:
```
