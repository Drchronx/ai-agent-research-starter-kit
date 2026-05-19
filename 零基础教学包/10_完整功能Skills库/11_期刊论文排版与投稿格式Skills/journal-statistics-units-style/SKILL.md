---
name: journal-statistics-units-style
description: "Audit and standardize statistical reporting, mathematical notation, p-values, confidence intervals, effect sizes, and measurement units for manuscripts. Use for APA 7 statistics style, SI units, exact p-value formatting, italic statistical symbols, unit consistency, and numeric-format compliance without changing values."
---

# Journal Statistics And Units Style

Use this skill to standardize statistical and unit reporting.

## Inputs

- Manuscript text, tables, figure notes, and results section.
- Target journal statistical style.
- Unit standard such as SI or journal-specific units.

## Workflow

1. Detect statistical symbols, test statistics, p-values, confidence intervals, effect sizes, sample sizes, and units.
2. Apply style rules for symbols, spacing, decimals, leading zeroes, exact p-values, and confidence intervals.
3. Check unit consistency and SI compliance.
4. Flag inconsistent or impossible statistical syntax.
5. Return formatted text and an audit table.

## Hard Constraints

- Never change numeric values, signs, confidence intervals, sample sizes, degrees of freedom, or p-values.
- Do not infer missing statistics.
- If a value appears inconsistent, flag it rather than correcting it.

## Output

```text
Formatted statistical text:
Statistics audit table:
Unit audit table:
Potential inconsistencies:
Manual verification items:
```

