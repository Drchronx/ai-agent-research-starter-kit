# Method Index

Use this file first when the user describes an empirical task in natural language. It maps common requests to fixed scripts.

| User intent | Fixed script |
|---|---|
| clean raw data, coerce types, missingness report, sample log | `scripts/clean_data.py` |
| construct variables, winsorize, standardize, lags, event time | `scripts/transform_data.py` |
| ML feature matrix X, target vector y, train/valid/test split | `scripts/prepare_ml_data.py` |
| Table 1, balance table, summary statistics, trend plot | `scripts/describe_data.py` |
| residual diagnostics, Breusch-Pagan, White, VIF | `scripts/run_diagnostics.py` |
| ordinary OLS/logit/probit/poisson formulas | `scripts/run_model.py` |
| panel FE/RE/between/first-difference | `scripts/run_panel.py` |
| DID, TWFE, treatment x post, event study, pretrend | `scripts/run_did.py` |
| IV, 2SLS, LIML, GMM, first stage | `scripts/run_iv.py` |
| LinearRegression, Ridge, Lasso, ElasticNet, tree models, random forest, GBDT, ML metrics | `scripts/run_supervised_ml.py` |
| RD, regression discontinuity, fuzzy RD, bandwidth checks | `scripts/run_rd.py` |
| propensity-score matching, IPW, love plot, balance after weighting | `scripts/run_matching.py` |
| synthetic control, SCM, treated-vs-synthetic trajectory | `scripts/run_synth.py` |
| DML, double machine learning, LinearDML | `scripts/run_dml.py` |
| CATE, causal forest, T-learner, S-learner | `scripts/run_cate.py` |
| robustness variants, clusters, placebo, subsamples | `scripts/run_robustness.py` |
| Oster delta, E-value, randomization inference | `scripts/run_sensitivity.py` |
| heterogeneity, mechanism, simple mediation | `scripts/run_further_analysis.py` |
| survival analysis, Kaplan-Meier, Cox, AFT | `scripts/run_survival.py` |
| regression table formatting | `scripts/table_factory.py` |
| coefficient/event-study/binscatter/love plots | `scripts/plot_factory.py` |
| artifact manifest | `scripts/render_manifest.py` |

If a method is listed in the original skill but has no fixed script yet, do not write ad hoc Python in markdown. Add a dedicated script first.
