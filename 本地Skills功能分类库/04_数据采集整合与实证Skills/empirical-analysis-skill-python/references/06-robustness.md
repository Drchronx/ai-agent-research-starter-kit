# Step 6 - Robustness Checks

Use `scripts/run_robustness.py` for specification batteries and `scripts/run_sensitivity.py` for formal sensitivity analyses.

Goal: run a controlled battery of robustness specifications and export a single robustness table plus sensitivity figure.

## Use When

- The user asks for alternative controls, alternative clustering, subsamples, placebo tests, specification curves, robustness tables, Oster delta, E-value, or randomization inference.

## Main Parameters

| Parameter | Use |
|---|---|
| `--input` | Analysis dataset path. |
| `--outcome` and `--treatment` | Main estimate to stress-test. |
| `--controls` | Baseline controls. |
| `--progressive` | Add progressive control-set checks. |
| `--control-sets` | Semicolon-separated custom control sets. |
| `--fixed-effects` | Fixed effects for all generated formulas. |
| `--formula` | Exact baseline formula override. |
| `--cluster` | Baseline cluster variable. |
| `--cluster-vars` | Alternative cluster variables. |
| `--filters` | Semicolon-separated pandas query expressions for subsample checks. |
| `--placebo-vars` | Alternative placebo treatment variables. |
| `--plot-term` | Coefficient term for the sensitivity plot. |
| `--min-n` | Minimum sample size for a robustness variant, default `20`. |
| `--formats` | Table export formats. |
| `--output-dir` | Output directory. |

## Typical Invocation

Use an inline command shaped like `python scripts/run_robustness.py --input output/empirical/data_analysis.csv --outcome log_wage --treatment training --controls age,edu,tenure --fixed-effects worker_id,year --cluster worker_id --cluster-vars firm_id,region --filters "year>=2010;female==1" --placebo-vars placebo_training --plot-term training --output-dir output/empirical/tables`.

For Oster delta, use an inline command shaped like `python scripts/run_sensitivity.py --input output/empirical/data_analysis.csv --modes oster --outcome log_wage --treatment training --restricted-controls age,edu --controls age,edu,tenure,firm_size --fixed-effects year --cluster worker_id --output-dir output/empirical/sensitivity`.

For E-value from a risk ratio, use an inline command shaped like `python scripts/run_sensitivity.py --modes evalue --effect-rr 1.8 --ci-low 1.2 --ci-high 2.4 --output-dir output/empirical/sensitivity`.

For randomization inference, use an inline command shaped like `python scripts/run_sensitivity.py --input output/empirical/data_analysis.csv --modes randomization --outcome y --treatment treated --controls x1,x2 --permutations 1000 --output-dir output/empirical/sensitivity`.

## Outputs

- `table5_robustness` in requested formats.
- `fig4_sensitivity` when valid coefficients and SEs are available.
- `robustness_manifest.json`.
- `sensitivity_results` and `sensitivity_manifest.json` from `scripts/run_sensitivity.py`.
- `randomization_distribution.csv` when randomization inference is requested.

## Decision Rules

- Keep robustness variants close to the identifying design; do not add arbitrary checks that change the estimand.
- Subsample filters are parameters, not code. Use clear pandas query strings in `--filters`.
- Placebo variables should already exist in the dataset. Create them with `transform` or a scripted extension before running this step.
- Report failed variants in the output table instead of silently omitting them.
- Use `run_sensitivity.py` for formal sensitivity metrics rather than mixing those calculations into `run_robustness.py`.
