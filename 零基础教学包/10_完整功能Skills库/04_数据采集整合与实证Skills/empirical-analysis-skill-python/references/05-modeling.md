# Step 5 - Empirical Modeling

Use fixed modeling scripts:

| Task | Script |
|---|---|
| OLS/logit/probit/poisson formulas | `scripts/run_model.py` |
| Panel FE/RE/between/first-difference | `scripts/run_panel.py` |
| DID/TWFE/event study | `scripts/run_did.py` |
| IV/2SLS/LIML/GMM | `scripts/run_iv.py` |
| RD/sharp/fuzzy regression discontinuity | `scripts/run_rd.py` |
| Propensity-score matching or IPW | `scripts/run_matching.py` |
| Synthetic control | `scripts/run_synth.py` |
| Double machine learning | `scripts/run_dml.py` |

Goal: estimate the main empirical model and export paper-ready regression tables without writing ad hoc Python code in markdown.

## Use When

- The user asks for OLS, logit, probit, poisson, IV, panel fixed effects, DID, event-study-style formulas, RD, matching/IPW, synthetic control, double machine learning, ML causal inference, or a multi-column main regression table.

## Main Parameters

| Parameter | Use |
|---|---|
| `--input` | Analysis dataset path. |
| `--outcome` and `--treatment` | Standard outcome-treatment interface. |
| `--controls` | Comma-separated controls. |
| `--progressive` | Build progressive columns from treatment-only through full controls. |
| `--control-sets` | Semicolon-separated control sets for custom progressive columns. |
| `--fixed-effects` | Categorical fixed effects appended to generated formulas. |
| `--formula` | One exact formula. |
| `--formulas` | Semicolon-separated exact formulas for multiple model columns. |
| `--model-names` | Comma-separated names matching formula count. |
| `--model-type` | One of `ols`, `logit`, `probit`, `poisson`, or `iv`. |
| `--cluster` | Cluster variable. |
| `--cov-type` | Covariance type, default `HC3`. |
| `--keep-terms` | Terms to keep in tidy output. |
| `--plot-term` | Coefficient to plot. |
| `--formats` | Table export formats. |
| `--output-dir` | Output directory. |

## Typical Invocations

For a progressive economics Table 2, use an inline command shaped like `python scripts/run_model.py --input output/empirical/data_analysis.csv --outcome log_wage --treatment training --controls age,edu,tenure,firm_size --progressive --fixed-effects worker_id,year --cluster worker_id --keep-terms training --plot-term training --output-dir output/empirical/tables`.

For exact DID or event-study formulas, pass formula strings through `--formulas` and model names through `--model-names`. Keep the formula as a parameter, not as Python code in markdown.

For IV, use `--model-type iv` with a linearmodels-compatible formula string through `--formula` or `--formulas`; the script requires `linearmodels` to be installed.

For DML, use an inline command shaped like `python scripts/run_dml.py --input data/DML/dml_dataset.csv --output-dir output/dml_reproduction --outcome Dig_Innov --treatment Data --controls Size,Age,Lev,Roa,Rd,Growth,Cash,Eps,TobinQ --group-col Stkcd --time-col Year --specs base,time_fe,time_fe_squared --labels direct_effect,time_fixed_effect,time_fixed_effect_squared_controls --model-y gbr --model-t rf --discrete-treatment --random-state 2025 --n-splits 5`.

For panel models, use an inline command shaped like `python scripts/run_panel.py --input data/panel.csv --outcome y --treatment treat --controls x1,x2 --entity firm_id --time year --methods fe,twfe,between,fd --cluster firm_id --output-dir output/empirical/tables`.

For DID, use an inline command shaped like `python scripts/run_did.py --input data/panel.csv --outcome y --treated treated --post post --entity firm_id --time year --controls x1,x2 --mode twfe --cluster firm_id --output-dir output/empirical/tables`.

For event study, use an inline command shaped like `python scripts/run_did.py --input data/panel.csv --outcome y --treated treated --rel-time rel_time --entity firm_id --time year --controls x1,x2 --mode event --cluster firm_id --ref-period -1 --output-dir output/empirical/tables`.

For IV, use an inline command shaped like `python scripts/run_iv.py --input data/analysis.csv --outcome y --endog treatment --instruments z1,z2 --controls x1,x2 --fixed-effects year --cluster firm_id --methods 2sls,liml,gmm --output-dir output/empirical/tables`.

For RD, use an inline command shaped like `python scripts/run_rd.py --input data/analysis.csv --outcome y --running score --cutoff 0 --controls x1,x2 --bandwidth-grid 2,4,6 --cluster school_id --output-dir output/empirical/rd`.

For fuzzy RD, add the treatment received variable: `python scripts/run_rd.py --input data/analysis.csv --outcome y --running score --cutoff 0 --treatment takeup --controls x1,x2 --bandwidth 5 --output-dir output/empirical/rd`.

For matching/IPW, use an inline command shaped like `python scripts/run_matching.py --input data/analysis.csv --outcome y --treatment treated --controls age,edu,income,baseline_y --method both --estimand att --output-dir output/empirical/matching`.

For synthetic control, use an inline command shaped like `python scripts/run_synth.py --input data/panel.csv --outcome y --unit state --time year --treated-unit California --treatment-time 2010 --output-dir output/empirical/synth`.

## Outputs

- `table2_main_tidy` with model, term, coefficient, SE, p-value, N, R-squared, and formula.
- `table2_main` wide coefficient table.
- `model_summaries.txt`.
- `fig3_coefplot` when `--plot-term` or treatment coefficient is available.
- `model_manifest.json`.

Panel outputs from `scripts/run_panel.py`:

- `panel_results.csv/.xlsx/.tex` depending on `--formats`.
- `panel_summaries.txt`.
- `panel_manifest.json`.

DID outputs from `scripts/run_did.py`:

- `did_results.csv/.xlsx/.tex` depending on `--formats`.
- `did_summaries.txt`.
- `did_manifest.json` including event-study pretrend test metadata when available.

IV outputs from `scripts/run_iv.py`:

- `iv_results.csv/.xlsx/.tex` depending on `--formats`.
- `iv_summaries.txt`.
- `iv_manifest.json` including first-stage and overidentification diagnostics where available.

DML outputs from `scripts/run_dml.py`:

- `dml_results.csv` with model, spec, ATE, StdErr, Significance, p-value, N, and feature count.
- `dml_results_transposed.csv` matching the common notebook-style transposed table.
- `dml_manifest.json` with variable choices, model choices, specs, and output paths.

RD outputs from `scripts/run_rd.py`:

- `rd_results.csv/.xlsx/.tex` depending on `--formats`.
- `rd_summaries.txt`.
- `fig_rd_plot.png/.pdf` unless `--no-figures` is set.
- `rd_manifest.json`.

Matching/IPW outputs from `scripts/run_matching.py`:

- `matching_effects.csv/.xlsx/.tex`.
- `propensity_scores.csv`.
- `balance_smd.csv/.xlsx/.tex`.
- `matched_pairs.csv` when nearest-neighbor matching is requested.
- `fig_love_plot.png/.pdf` unless `--no-figures` is set.
- `matching_manifest.json`.

Synthetic-control outputs from `scripts/run_synth.py`:

- `synthetic_weights.csv/.xlsx/.tex`.
- `synthetic_trajectory.csv/.xlsx/.tex`.
- `synthetic_fit.csv/.xlsx/.tex`.
- `fig_synth_trajectory.png/.pdf` unless `--no-figures` is set.
- `synth_manifest.json`.

## Design Routing

- Use generated formulas for ordinary applied-economics specifications.
- Use explicit `--formula` or `--formulas` for DID, event studies, high-dimensional interactions, IV, or other special designs.
- Use `run_panel.py` for panel FE/RE/between/first-difference instead of encoding every panel estimator manually in `run_model.py`.
- Use `run_did.py` when treatment timing, pre/post treatment, or relative event time is central to identification.
- Use `run_iv.py` when the treatment is endogenous and the user provides instruments.
- Use `run_rd.py` when assignment changes discontinuously at a cutoff in a running variable.
- Use `run_matching.py` when the design requires observed-covariate balance through propensity scores, matching, or weighting.
- Use `run_synth.py` for one or a few treated aggregate units with pre/post panel outcomes and donor units.
- Use `scripts/run_dml.py` when the user asks for DML, double machine learning, `LinearDML`, grouped cross-fitting, or ML causal inference with nuisance models.
- Use `--fixed-effects unit,time` for moderate fixed effects. For very high-dimensional fixed effects, consider extending the CLI to use `pyfixest` rather than writing temporary code in markdown.
- Use `--keep-terms` to keep tables compact and prevent accidental reporting of hundreds of fixed-effect dummy coefficients.

## Decision Rules

- Main economics tables should have multiple columns; do not collapse Table 2 to one headline coefficient unless the user explicitly asks.
- Cluster at the treatment assignment or sampling level when applicable.
- Keep the formula strings in `model_manifest.json` so reported estimates remain reproducible.
