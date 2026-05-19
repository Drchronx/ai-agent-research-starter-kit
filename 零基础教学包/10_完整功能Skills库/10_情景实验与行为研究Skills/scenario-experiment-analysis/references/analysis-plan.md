# Scenario Experiment Analysis Plan

## Minimum Variables

| Variable type | Examples |
|---|---|
| Condition | `condition`, `ai_agent`, `explainability`, `autonomy` |
| DV | `trust`, `purchase_intention`, `adoption_intention`, `blame`, `creativity` |
| Manipulation check | `mc_autonomy`, `mc_anthropomorphism`, `mc_risk` |
| Mediator | `perceived_agency`, `cognitive_load`, `psychological_ownership` |
| Moderator | `expertise`, `need_for_cognition`, `task_complexity` |
| Exclusion | `attention_pass`, `duration`, `duplicate_id` |

## Primary Models

- Two-condition design: `DV ~ condition`
- 2 x 2 design: `DV ~ factor1 * factor2`
- Covariate model: `DV ~ condition + covariates`
- Mediation: `M ~ X`; `Y ~ X + M`; bootstrap indirect effect.
- Moderation: `Y ~ X * W`
- Moderated mediation: conditional indirect effects at low/mean/high W.

## Robustness

- With and without covariates.
- With and without exclusions.
- Nonparametric alternative if severe non-normality.
- Alternative DV coding if theoretically justified.
- Correction or transparent discussion for multiple testing.

