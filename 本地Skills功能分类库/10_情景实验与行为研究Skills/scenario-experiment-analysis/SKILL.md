---
name: scenario-experiment-analysis
description: "Analyze scenario/vignette experiment datasets for behavioral research. Use for 情景实验数据分析, manipulation checks, randomization checks, exclusion rules, reliability, ANOVA/ANCOVA, regression, mediation, moderation, moderated mediation, simple slopes, bootstrap indirect effects, effect sizes, exact p-values, robustness checks, and top-journal-style results tables for JCR, JCP, JM, JMR, ISR, MISQ, JAP, OBHDP, JPSP, Psychological Science, UTD24, FT50, and AJG/ABS4-oriented manuscripts."
---

# Scenario Experiment Analysis

Use this skill when the user has scenario experiment data or wants an analysis plan.

## Core Principle

Separate confirmatory tests from exploratory checks. Do not change exclusion rules, dependent variables, or model specifications after seeing whether results are significant.

## Data Intake

Before analysis, identify:

- Condition columns and coding.
- Dependent variable.
- Manipulation check.
- Attention check.
- Mediator.
- Moderator.
- Covariates.
- Exclusion flags.
- Participant platform and timestamp fields.

Never overwrite raw data. Save all outputs to a new analysis folder.

## Standard Analysis Order

1. Data audit: rows, missingness, duplicates, duration, impossible values.
2. Exclusion report: preregistered rules first, then sensitivity with/without exclusions.
3. Randomization check: demographics or baseline variables by condition.
4. Manipulation check: treatment should move the perceived construct.
5. Reliability: Cronbach's alpha or composite reliability for multi-item scales.
6. Primary model: ANOVA/regression/ANCOVA as planned.
7. Effect size: Cohen's d, eta-squared/partial eta-squared, standardized beta, odds ratio, or marginal effect.
8. Mechanism: mediation or moderated mediation when theory requires it.
9. Robustness: alternative coding, covariates, nonparametric/sensitivity checks.
10. Report: estimates, standard errors, confidence intervals, exact p-values, effect sizes.

## Model Selection

| Research design | Default analysis |
|---|---|
| Two conditions, continuous DV | t-test and OLS regression |
| More than two conditions | ANOVA and planned contrasts |
| 2 x 2 design | OLS/ANOVA with interaction |
| Covariates planned ex ante | ANCOVA/OLS with covariates |
| Binary choice DV | Logistic regression |
| Mediation | Bootstrap indirect effect |
| Moderation | Interaction + simple slopes |
| Moderated mediation | Conditional indirect effects |

## Script Support

Use `scripts/analyze_scenario_experiment.py` for a first-pass analysis report.

Example:

```bash
python scripts/analyze_scenario_experiment.py --data data.csv --dv trust --ivs condition --mediators perceived_agency --moderators expertise --checks manipulation_check --scale trust:trust1,trust2,trust3 --outdir output/scenario_analysis
```

The script generates:

- `analysis_report.md`
- `descriptives.csv`
- `reliability.csv` when `--scale` is supplied
- `model_primary.csv`
- optional mediation/moderation summaries when fields are supplied.

Read and inspect the script before relying on it for publication analysis. It is a helper, not a substitute for statistical judgment.

## Reporting Rules

For top-journal style reporting:

- Report exact p-values when possible.
- Report standard errors or confidence intervals for estimates.
- Report effect sizes and explain substantive magnitude.
- Avoid binary language such as "marginally significant" unless the target journal permits it.
- Use plots for interactions and conditional effects.
- State whether manipulation checks are analyzed before or after exclusions.

## Output Template

```text
Data and exclusions:
Randomization check:
Manipulation check:
Reliability:
Primary effect:
Mediation:
Moderation:
Robustness:
Effect sizes:
Interpretation:
Limitations:
Tables and figures produced:
```

## Red Flags

- Manipulation check fails but hypothesis test is interpreted as causal.
- Mediator is measured with wording nearly identical to the manipulation.
- Exclusions are decided after checking results.
- Only p-values are reported, with no effect sizes.
- Multiple DVs are tested but only significant ones are discussed.
- A scenario about AI is confounded with competence, risk, novelty, or privacy.
