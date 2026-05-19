---
name: multilevel-longitudinal-modeling
description: "Design, analyze, and report multilevel, mixed-effects, repeated-measures, diary, panel, and longitudinal models. Use for nested data, participants within teams, repeated observations, random intercepts, random slopes, cross-level interactions, growth models, ICC, and management or psychology longitudinal reporting."
---

# Multilevel Longitudinal Modeling

Use this skill when observations are nested or repeated.

## Inputs

- Data hierarchy: trials, days, participants, teams, organizations, time.
- Outcome type.
- Predictors at each level.
- Repeated-measures or panel structure.

## Workflow

1. Identify the nesting structure and unit of analysis.
2. Compute or request ICC when relevant.
3. Specify random intercepts and random slopes based on design and theory.
4. Center predictors appropriately: grand-mean, group-mean, person-mean, or no centering.
5. Test cross-level interactions and time trends when theoretically justified.
6. Report fixed effects, random effects, variance components, and model comparison.

## Hard Constraints

- Do not ignore clustering when observations are not independent.
- Do not choose centering only to obtain significance.
- Do not claim within-person effects from between-person associations.
- Do not fit overly complex random effects when data cannot support them without caveats.

## Output

```text
Data hierarchy:
Model choice:
Centering plan:
Random-effects plan:
Model formula:
Results table:
Interpretation by level:
Reporting paragraph:
```

