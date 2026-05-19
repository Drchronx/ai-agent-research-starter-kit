---
name: statistical-results-tables
description: "Create publication-style statistical tables and result interpretations. Use for regression tables, mediation tables, SEM tables, multilevel tables, DID/event-study tables, effect sizes, confidence intervals, exact p-values, APA tables, management journal tables, robustness tables, and Results writing."
---

# Statistical Results Tables

Use this skill to convert model outputs into journal-ready tables and text.

## Inputs

- Model outputs or CSV tables.
- Target journal style.
- Primary, mechanism, moderation, robustness, and appendix models.

## Workflow

1. Separate main, mechanism, heterogeneity, and robustness results.
2. Choose table columns and model order.
3. Include coefficient, standard error or confidence interval, p-value, N, fixed effects, controls, and model fit where appropriate.
4. Add notes explaining standard errors, clustering, variable coding, and significance notation.
5. Write a concise Results paragraph focused on effect direction, magnitude, uncertainty, and interpretation.

## Hard Constraints

- Do not change coefficients, standard errors, p-values, N, or model labels.
- Do not hide non-significant primary results.
- Do not use significance stars as the only evidence.
- Do not interpret unreported robustness checks as completed.

## Output

```text
Table plan:
Formatted result table:
Table notes:
Results paragraph:
Effect-size interpretation:
Missing information:
```

