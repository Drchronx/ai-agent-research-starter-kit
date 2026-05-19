---
name: scale-reliability-validity
description: "Analyze reliability and validity of questionnaire scales. Use for Cronbach alpha, McDonald's omega, composite reliability, AVE, convergent validity, discriminant validity, Fornell-Larcker, HTMT, item-total correlations, scale purification, and management or psychology measurement reporting."
---

# Scale Reliability And Validity

Use this skill after collecting scale data.

Use `scripts/create_scale_codebook.py` to create a construct-item codebook before analysis.

## Inputs

- Item-level dataset.
- Construct-to-item mapping.
- Reverse-coded item list.
- Target reporting style.

## Workflow

1. Audit missingness, coding, anchors, and reverse-coded items.
2. Compute descriptive statistics and item-total correlations.
3. Estimate reliability: alpha, omega, and composite reliability when appropriate.
4. Assess convergent validity using AVE or factor loadings.
5. Assess discriminant validity using Fornell-Larcker, HTMT, or model comparison.
6. Decide whether item removal is theoretically justified.
7. Produce a measurement-quality report.

## Hard Constraints

- Do not remove items solely to improve alpha without theoretical rationale.
- Do not hide poor reliability or validity.
- Do not compute construct scores before reverse coding is verified.
- Do not claim validity from reliability alone.

## Output

```text
Data audit:
Reliability table:
Validity table:
Problematic items:
Scale-scoring instructions:
Reporting paragraph:
Reviewer risks:
```
