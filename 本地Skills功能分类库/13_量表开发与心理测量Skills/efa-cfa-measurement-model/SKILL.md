---
name: efa-cfa-measurement-model
description: "Plan, run, and report exploratory factor analysis and confirmatory factor analysis for academic scales. Use for EFA, CFA, factor loadings, model fit indices, CFI, TLI, RMSEA, SRMR, chi-square, modification indices, cross-loadings, latent variable measurement models, and questionnaire validation."
---

# EFA CFA Measurement Model

Use this skill for factor-structure evaluation.

## Inputs

- Item-level data.
- Expected factor structure.
- Sample size and population.
- Software preference: R, Python, Mplus, lavaan, AMOS, jamovi, SPSS.

## Workflow

1. Check data suitability: sample size, missingness, item distributions, correlations.
2. Use EFA only when structure is uncertain or being explored.
3. Use CFA when testing a theoretically specified measurement model.
4. Report factor loadings, fit indices, residual issues, and correlated errors only when justified.
5. Compare alternative models if discriminant validity is a concern.
6. Produce tables and a reporting paragraph.

## Hard Constraints

- Do not use EFA and CFA on the same sample as if it were independent validation unless labeled exploratory.
- Do not add correlated errors only to chase fit.
- Do not delete items without theory and transparent reporting.
- Do not overclaim construct validity from a single CFA.

## Output

```text
Analysis choice:
Model specification:
Fit-index table:
Loading table:
Model comparison:
Modification risks:
Reporting paragraph:
```

