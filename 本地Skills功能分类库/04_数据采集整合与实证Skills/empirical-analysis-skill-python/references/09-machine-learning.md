# Step 9 - Machine Learning Models

Use fixed machine-learning scripts:

| Task | Script |
|---|---|
| Build feature matrix X, target vector y, split train/valid/test | `scripts/prepare_ml_data.py` |
| LinearRegression, Ridge, Lasso, ElasticNet | `scripts/run_supervised_ml.py --task regression` |
| Decision tree, random forest, GBDT regression | `scripts/run_supervised_ml.py --task regression` |
| Logistic classifier, decision tree, random forest, GBDT classification | `scripts/run_supervised_ml.py --task classification` |
| DML / DDML with EconML LinearDML | `scripts/run_dml.py` |
| Causal forest / T-learner / S-learner CATE | `scripts/run_cate.py` |
| Three-line academic tables | `scripts/table_factory.py --formats tex` |

Goal: cover the introductory ML workflow without writing ad hoc sklearn code in markdown.

## Concept Routing

- Supervised learning: the user provides features X and label y. Use `prepare_ml_data.py` and `run_supervised_ml.py`.
- Unsupervised learning: not yet covered by a fixed script. Add a dedicated script before running clustering or dimensionality reduction.
- Regression: continuous target. Use `--task regression`.
- Classification: discrete class label. Use `--task classification`.
- Training, validation, testing: use `--test-size`, `--valid-size`, `--random-state`, and optionally `--split-col`.
- Feature matrix X and target y: use `--features` and `--target`.
- Missing values and standardization: handled by the fixed preprocessing path in both ML scripts.

## Supported Regression Models

`scripts/run_supervised_ml.py --task regression` supports:

- `linear`: sklearn `LinearRegression`.
- `ridge`: L2 regularized regression.
- `lasso`: L1 regularized regression with sparse feature selection.
- `elasticnet`: mixed L1 and L2 regularized regression.
- `decision_tree`: decision-tree regressor.
- `random_forest`: random-forest regressor.
- `gbdt`: gradient-boosting decision-tree regressor.

Use the `--models` parameter to select a subset, for example `--models linear,ridge,lasso,elasticnet`.

## Supported Classification Models

`scripts/run_supervised_ml.py --task classification` supports:

- `logistic`: logistic classifier with optional L1, L2, or elastic-net penalty.
- `decision_tree`: decision-tree classifier.
- `random_forest`: random-forest classifier.
- `gbdt`: gradient-boosting decision-tree classifier.

Use `--classifier-penalty l1`, `--classifier-penalty l2`, or `--classifier-penalty elasticnet` for regularized logistic classification.

## Metrics

Regression metrics:

- MAE.
- MSE.
- RMSE.
- R2.

Classification metrics:

- Accuracy.
- Precision.
- Recall.
- F1.
- ROC AUC when model probabilities are available.

## Typical Invocations

For feature preparation, use an inline command shaped like `python scripts/prepare_ml_data.py --input data/analysis.csv --target y --features x1,x2,x3,industry --categorical industry --test-size 0.2 --valid-size 0.1 --output-dir output/empirical/ml`.

For LinearRegression, Ridge, Lasso, and ElasticNet, use an inline command shaped like `python scripts/run_supervised_ml.py --input data/analysis.csv --task regression --target y --features x1,x2,x3 --models linear,ridge,lasso,elasticnet --cv --output-dir output/empirical/ml`.

For tree models, use an inline command shaped like `python scripts/run_supervised_ml.py --input data/analysis.csv --task regression --target y --features x1,x2,x3 --models decision_tree,random_forest,gbdt --n-estimators 300 --output-dir output/empirical/ml`.

For classification, use an inline command shaped like `python scripts/run_supervised_ml.py --input data/analysis.csv --task classification --target default --features x1,x2,x3 --models logistic,decision_tree,random_forest,gbdt --stratify --average binary --output-dir output/empirical/ml`.

For DML / DDML, use `scripts/run_dml.py`. For causal forest, use `scripts/run_cate.py --method causal_forest`.

For a LaTeX three-line table, use `scripts/table_factory.py` with `--formats tex` on the generated tidy results.

## Outputs

`prepare_ml_data.py` writes:

- `ml_dataset_split`.
- `ml_X_train.csv`, `ml_X_valid.csv`, `ml_X_test.csv`.
- `ml_y_train.csv`, `ml_y_valid.csv`, `ml_y_test.csv`.
- `ml_feature_summary`.
- `ml_ml_data_manifest.json`.

`run_supervised_ml.py` writes:

- `ml_metrics` with train/valid/test metrics.
- `ml_predictions.csv`.
- `ml_feature_effects` with coefficients or feature importances.
- `fig_ml_feature_effects.png/.pdf` unless `--no-figures` is set.
- `supervised_ml_manifest.json`.

## Decision Rules

- Use regularized models when features are many, multicollinearity is likely, or the user explicitly asks for Lasso, Ridge, or Elastic Net.
- Use Lasso when automatic feature selection is important.
- Use Ridge when multicollinearity is the main problem and feature selection is not required.
- Use ElasticNet when correlated predictors make pure Lasso unstable.
- Use tree models when nonlinearity or interactions are important.
- Use random forest for robust nonlinear prediction; use GBDT when stronger predictive performance is needed and tuning is acceptable.
- Use DML for causal estimation with ML nuisance models, not for ordinary prediction.
- Use causal forest or CATE scripts when heterogeneous treatment effects are the target.
