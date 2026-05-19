---
name: empirical-analysis-skill-python
description: Parameterized Python empirical-analysis and machine-learning workflow for applied economics, public health epidemiology, supervised ML, and ML causal inference. Use when the user asks for data cleaning, feature engineering, train/test/validation splits, feature matrix X and target y, Table 1, diagnostic tests, OLS/panel/IV-style formulas, LinearRegression, Ridge, Lasso, ElasticNet, decision trees, random forests, GBDT, regression/classification metrics, DID/event-study formulas, DML/double machine learning with LinearDML, causal forests, robustness checks, mechanism or heterogeneity analysis, mediation, publication-ready tables, figures, or an end-to-end empirical paper pipeline. The skill must route execution through fixed step scripts under scripts/ instead of writing ad hoc Python code in markdown.
triggers:
  - full empirical analysis in Python
  - classical econometrics pipeline
  - applied economics paper replication
  - end-to-end empirical workflow
  - data cleaning empirical
  - winsorize and standardize
  - variable construction
  - machine learning basics
  - supervised learning
  - feature matrix X
  - target vector y
  - train validation test split
  - validation set
  - regression metrics
  - classification metrics
  - MAE
  - MSE
  - RMSE
  - R2
  - accuracy
  - precision
  - recall
  - F1
  - LinearRegression
  - Ridge regression
  - Lasso regression
  - ElasticNet
  - Elastic Net
  - decision tree
  - random forest
  - GBDT
  - Table 1 summary statistics
  - balance table
  - correlation matrix
  - normality test
  - heteroskedasticity test
  - autocorrelation test
  - multicollinearity VIF
  - baseline regression
  - panel fixed effects
  - PanelOLS
  - random effects
  - first difference panel
  - DID workflow Python
  - difference in differences
  - event study
  - pretrend test
  - instrumental variables regression
  - 2SLS
  - LIML
  - GMM IV
  - double machine learning
  - DML
  - LinearDML
  - causal forest
  - meta learner
  - regression discontinuity
  - propensity score matching
  - synthetic control python
  - robustness checks
  - placebo test
  - specification curve
  - alternative clustering
  - heterogeneity analysis
  - mechanism analysis
  - mediation analysis
  - moderation analysis
  - publication-ready regression table
  - coefplot
  - binscatter
  - event study plot
  - target trial emulation
  - IPTW
  - TMLE
  - Mendelian randomization
  - survival analysis
  - Cox model
  - AFT model
  - E-value sensitivity
  - policy tree
  - conformal causal
  - fairness audit
---

# Empirical Analysis Skill - Python

This skill runs a full empirical workflow through fixed, decoupled Python scripts. The agent may choose variables, formulas, modes, and arguments, but must not invent Python snippets inside markdown responses or reference files.

## Hard Rules

- Run the fixed step scripts under `scripts/` for analysis work.
- Use CLI parameters, formula strings, and input/output paths to customize behavior.
- Do not paste new Python code into markdown as the primary solution.
- If the fixed scripts do not support a requested estimator, either express it through `--formula` or `--formulas`, or state the limitation and ask whether to extend the relevant script.
- Keep generated outputs on disk under the project output directory, usually `output/empirical`.
- Use reference files only to decide which subcommand and parameters to call.

## Script Layout

Use the per-step scripts directly:

| Step | Script | Purpose | Reference |
|---|---|---|---|
| 1 | `scripts/clean_data.py` | Inspect, coerce dtypes, trim strings, handle key missingness, deduplicate, and log sample construction. | `references/01-data-cleaning.md` |
| 2 | `scripts/transform_data.py` | Create logs, IHS variables, winsorized columns, z-scores, dummies, lags, leads, differences, and treatment timing. | `references/02-data-transformation.md` |
| 2M | `scripts/prepare_ml_data.py` | Build supervised ML feature matrix X, target vector y, train/valid/test splits, imputation, and standardization. | `references/09-machine-learning.md` |
| 3 | `scripts/describe_data.py` | Generate Table 1, balance table, categorical frequencies, correlation matrix, heatmap, and trend plot. | `references/03-descriptive-stats.md` |
| 4 | `scripts/run_diagnostics.py` | Run residual normality, heteroskedasticity, autocorrelation, condition-number, and VIF diagnostics. | `references/04-statistical-tests.md` |
| 5 | `scripts/run_model.py` | Fit OLS, logit, probit, poisson, or IV formulas; export regression tables and coefficient plots. | `references/05-modeling.md` |
| 5A | `scripts/run_panel.py` | Run panel FE/RE/between/first-difference models with clustered covariance support. | `references/05-modeling.md` |
| 5A | `scripts/run_did.py` | Run 2x2/TWFE DID and event-study specifications with pretrend tests. | `references/05-modeling.md` |
| 5A | `scripts/run_iv.py` | Run 2SLS/LIML/GMM IV estimates with first-stage and overidentification diagnostics where available. | `references/05-modeling.md` |
| 5A | `scripts/run_rd.py` | Run sharp/fuzzy regression-discontinuity estimates, bandwidth checks, and RD plots. | `references/05-modeling.md` |
| 5A | `scripts/run_matching.py` | Run propensity-score IPW, nearest-neighbor matching, and covariate balance diagnostics. | `references/05-modeling.md` |
| 5A | `scripts/run_synth.py` | Run synthetic-control weights, trajectory, gap, and fit diagnostics. | `references/05-modeling.md` |
| 5M | `scripts/run_supervised_ml.py` | Run LinearRegression, Ridge, Lasso, ElasticNet, tree models, random forest, GBDT, and classification models with fixed metrics. | `references/09-machine-learning.md` |
| 5B | `scripts/run_dml.py` | Run fixed `econml.dml.LinearDML` specifications for double machine learning and ML causal inference. | `references/05-modeling.md` |
| 5B | `scripts/run_cate.py` | Run T-learner, S-learner, or econml causal forest CATE estimation. | `references/07-further-analysis.md` |
| 6 | `scripts/run_robustness.py` | Run fixed robustness variants: alternative SEs, clusters, filters, placebo variables, and control sets. | `references/06-robustness.md` |
| 6 | `scripts/run_sensitivity.py` | Run Oster delta, E-value, and randomization-inference sensitivity analyses. | `references/06-robustness.md` |
| 7 | `scripts/run_further_analysis.py` | Run heterogeneity, mechanism/outcome-ladder, and simple Baron-Kenny mediation tables. | `references/07-further-analysis.md` |
| 7E | `scripts/run_survival.py` | Run Kaplan-Meier, Cox, and Weibull AFT survival-analysis workflows. | `references/07-further-analysis.md` |
| 8 | `scripts/table_factory.py` | Format tidy model results into publication-oriented wide tables with significance stars. | `references/08-tables-plots.md` |
| 8 | `scripts/plot_factory.py` | Create coefficient, event-study, binscatter, and love plots from fixed input files. | `references/08-tables-plots.md` |
| 8 | `scripts/render_manifest.py` | Collect tables and figures into an artifact manifest. | `references/08-tables-plots.md` |

Shared support files:

- `scripts/common.py`: shared file I/O, export, plotting, and argument helpers.
- `scripts/model_utils.py`: shared formula construction and model-fitting helpers.
- `scripts/empirical_cli.py`: thin compatibility dispatcher only. Prefer direct step scripts.

Use `references/method-index.md` to map a user request to the correct fixed script. Discover supported parameters with inline commands such as `python scripts/run_model.py --help`.

## Default Workflow

1. Start with `scripts/clean_data.py` on the raw data. Always pass key variables and dedupe columns when known.
2. Use `scripts/transform_data.py` to create analysis variables rather than doing inline dataframe mutations.
3. Use `scripts/describe_data.py` to generate Table 1 and the main exploratory figures.
4. Use `scripts/run_diagnostics.py` on the baseline formula before reporting results.
5. Use `scripts/run_model.py` for the main results. Prefer progressive model columns with `--progressive` or explicit semicolon-separated `--formulas`.
6. Use `scripts/run_robustness.py` for alternative controls, clusters, subsamples, and placebo checks.
7. Use `scripts/run_further_analysis.py` for mechanism, heterogeneity, and mediation.
8. Use `scripts/render_manifest.py` to produce the final manifest of tables and figures.

## Domain Modes

Default applied economics mode uses `run_model.py`, `run_robustness.py`, and `run_further_analysis.py` with OLS or IV formula strings. Fixed effects are expressed with `--fixed-effects` or explicit `C(variable)` terms in formula strings.

Epidemiology and public-health mode still uses the same cleaning, transformation, descriptives, and diagnostics steps. Use `scripts/run_survival.py` for Kaplan-Meier, Cox, and Weibull AFT work. For TMLE, target-trial, or Mendelian-randomization work that is not covered by fixed step scripts, add or extend a dedicated script first rather than placing code into markdown.

Supervised ML mode uses `scripts/prepare_ml_data.py` for X/y construction and `scripts/run_supervised_ml.py` for LinearRegression, Ridge, Lasso, ElasticNet, decision tree, random forest, GBDT, logistic classification, and regression/classification metrics.

ML causal inference mode uses the same file layout and reporting contract. For double machine learning, use `scripts/run_dml.py` directly. For CATE work, use `scripts/run_cate.py` with T-learner, S-learner, or econml causal forest. For policy-learning estimators not yet covered by fixed scripts, add a separate step script before use.

## Output Contract

Default output root: `output/empirical`.

Tables should be exported as CSV, XLSX, and LaTeX unless the user specifies otherwise. Use `--formats csv,xlsx,tex` or add `docx` if `python-docx` is available.

Figures should be exported as PNG at 300 dpi and PDF when figure creation is enabled.

Core economics-style deliverables:

| Artifact | File stem |
|---|---|
| Table 1 summary statistics | `table1_summary` |
| Table 1 balance table | `table1_balance` |
| Main regression table | `table2_main` and `table2_main_tidy` |
| Supervised ML metrics | `ml_metrics` |
| Supervised ML coefficients/importances | `ml_feature_effects` |
| Mechanism table | `table3_mechanism` |
| Heterogeneity table | `table4_heterogeneity` |
| Robustness table | `table5_robustness` |
| Sensitivity table | `sensitivity_results` |
| Trend figure | `fig1_trend` |
| RD plot | `fig_rd_plot` |
| Synthetic-control trajectory | `fig_synth_trajectory` |
| KM survival curve | `fig_km_curve` |
| CATE distribution | `fig_cate_distribution` |
| ML feature effect plot | `fig_ml_feature_effects` |
| Coefficient plot | `fig3_coefplot` |
| Sensitivity/specification figure | `fig4_sensitivity` |
| Final artifact index | `artifact_manifest.json` and `artifact_manifest.md` |

## Parameter Conventions

- Column lists are comma-separated, for example `age,edu,tenure`.
- Multiple formulas or filters are semicolon-separated.
- Use exact formula strings when the design is special. The script accepts formulas through `--formula` or `--formulas`.
- Use `--cluster firm_id` for clustered standard errors in supported model subcommands.
- Use `--fixed-effects worker_id,year` for categorical fixed effects in statsmodels formulas.
- Use `--output-dir` for tables and figures; use `--output` for transformed datasets.

## When To Read References

Read only the relevant reference file before running a subcommand. The references do not contain Python implementation code. They explain parameter choices, outputs, and checks.

## Maintenance Rule

When adding new empirical behavior, modify the relevant step script or shared helper and document only the invocation pattern in `references/`. Do not add executable Python code blocks to `SKILL.md`, `README.md`, or any `references/*.md` file.
