# Step 7 - Further Analysis

Use `scripts/run_further_analysis.py` for mechanism, heterogeneity, and simple mediation; use `scripts/run_cate.py` for ML CATE; use `scripts/run_survival.py` for survival workflows.

Goal: run scripted mechanism, heterogeneity, and simple mediation analyses after the main estimate is established.

## Use When

- The user asks for mechanism analysis, outcome ladders, heterogeneity, subgroup logic, treatment interactions, mediation, moderation-style checks, CATE, causal forest, Kaplan-Meier, Cox, or AFT models.

## Main Parameters

| Parameter | Use |
|---|---|
| `--input` | Analysis dataset path. |
| `--outcome` and `--treatment` | Main outcome and treatment. |
| `--controls` | Baseline controls. |
| `--fixed-effects` | Fixed effects. |
| `--cluster` | Cluster variable. |
| `--cov-type` | Robust covariance type. |
| `--model-type` | `ols`, `logit`, `probit`, or `poisson`. |
| `--heterogeneity-vars` | Variables interacted with treatment. |
| `--mechanism-outcomes` | Outcome-ladder variables. |
| `--mediators` | Candidate mediators for Baron-Kenny style decomposition. |
| `--formats` | Table export formats. |
| `--output-dir` | Output directory. |

## Typical Invocation

Use an inline command shaped like `python scripts/run_further_analysis.py --input output/empirical/data_analysis.csv --outcome log_wage --treatment training --controls age,edu,tenure --fixed-effects worker_id,year --cluster worker_id --heterogeneity-vars female,region_high --mechanism-outcomes hours_worked,job_quality --mediators skill_score --output-dir output/empirical/tables`.

For CATE with a fixed T-learner, use an inline command shaped like `python scripts/run_cate.py --input output/empirical/data_analysis.csv --outcome y --treatment treated --controls x1,x2,x3 --effect-modifiers gender,baseline_y --method tlearner --output-dir output/empirical/cate`.

For causal forest, use `python scripts/run_cate.py --input output/empirical/data_analysis.csv --outcome y --treatment treated --controls x1,x2,x3 --effect-modifiers gender,baseline_y --method causal_forest --output-dir output/empirical/cate`; this requires `econml`.

For survival analysis, use an inline command shaped like `python scripts/run_survival.py --input output/empirical/survival.csv --duration followup_days --event event --covariates treated,age,sex,baseline_risk --group-col treated --methods km,cox,aft --output-dir output/empirical/survival`.

## Outputs

- `table4_heterogeneity` when heterogeneity variables are provided.
- `table3_mechanism` when mechanism outcomes are provided.
- `mediation_baron_kenny` when mediators are provided.
- `further_manifest.json`.
- `cate_predictions`, `cate_summary`, `fig_cate_distribution`, and `cate_manifest.json` from `scripts/run_cate.py`.
- `km_curve`, `survival_model_results`, `fig_km_curve`, and `survival_manifest.json` from `scripts/run_survival.py`.

## Decision Rules

- Heterogeneity should be motivated by theory or pre-analysis plans, not by fishing through every column.
- Mechanism outcomes should represent a plausible causal chain from treatment to final outcome.
- Simple Baron-Kenny mediation is descriptive and linear. If the user needs modern causal mediation, extend the fixed CLI first.
- For high-dimensional ML CATE or causal forest, use `scripts/run_cate.py`.
- For policy learning, add scripted support before running; do not paste custom estimator code in markdown.
