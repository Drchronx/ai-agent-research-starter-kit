# Step 4 - Statistical Tests and Diagnostics

Use the fixed script `scripts/run_diagnostics.py`.

Goal: diagnose residual behavior, heteroskedasticity, autocorrelation, multicollinearity, and scaling problems for the baseline formula.

## Use When

- The user asks for Breusch-Pagan, White, Durbin-Watson, Ljung-Box, VIF, normality tests, or regression diagnostics.
- A baseline regression is ready but before the result is treated as a paper-ready estimate.

## Main Parameters

| Parameter | Use |
|---|---|
| `--input` | Analysis dataset path. |
| `--outcome` | Dependent variable. |
| `--treatment` | Main explanatory variable. |
| `--controls` | Comma-separated controls. |
| `--fixed-effects` | Fixed effects inserted as categorical terms. |
| `--formula` | Exact formula override for special designs. |
| `--cluster` | Cluster variable for robust summary fitting. |
| `--cov-type` | Robust covariance type, default `HC3`. |
| `--formats` | Table export formats. |
| `--no-figures` | Skip residual plot. |
| `--output-dir` | Output directory. |

## Typical Invocation

Use an inline command shaped like `python scripts/run_diagnostics.py --input output/empirical/data_analysis.csv --outcome log_wage --treatment training --controls age,edu,tenure --fixed-effects worker_id,year --cluster worker_id --output-dir output/empirical/tables`.

## Outputs

- `diagnostic_tests` in requested table formats.
- `vif` in requested table formats.
- `fig_residuals` when figures are enabled.
- `diagnostics_manifest.json`.

## Decision Rules

- If Breusch-Pagan or White p-value is below `0.05`, report robust or clustered SEs in the main model.
- If VIF is large, inspect whether fixed effects, interactions, or redundant controls are causing near-collinearity.
- Diagnostics are warning lights, not automatic deletion rules. Keep the model specification tied to the research design.
- Use `--formula` when the diagnostic baseline differs from the standard outcome-treatment-controls layout.
