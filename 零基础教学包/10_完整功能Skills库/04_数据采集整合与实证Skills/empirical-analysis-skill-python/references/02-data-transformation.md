# Step 2 - Data Transformation

Use the fixed script `scripts/transform_data.py`.

Goal: construct analysis variables deterministically from a cleaned dataset.

## Use When

- The workflow needs logs, IHS transforms, winsorization, standardization, dummies, lags, leads, differences, or DID timing variables.
- The user asks to "winsorize", "standardize", "create lag", "make event time", or "construct variables".

## Main Parameters

| Parameter | Use |
|---|---|
| `--input` | Cleaned dataset path. |
| `--output` | Transformed dataset path. |
| `--log-cols` | Positive variables to transform into `log_col`. |
| `--ihs-cols` | Variables to transform into `ihs_col`. |
| `--winsorize-cols` | Variables to clip into `col_w`. |
| `--winsor-lower` and `--winsor-upper` | Quantile cutoffs, default `0.01` and `0.99`. |
| `--standardize-cols` | Variables to convert into `col_z`. |
| `--dummy-cols` | Categorical variables to one-hot encode. |
| `--dummy-na` | Create a dummy for missing category values. |
| `--drop-first-dummy` | Drop first category to avoid collinearity. |
| `--panel-id` and `--time-col` | Required for lag, lead, and difference operations. |
| `--lag-cols`, `--lead-cols`, `--diff-cols` | Panel operators with `--periods`. |
| `--treat-start-col` | Column containing first treatment period. |
| `--rel-time-name` and `--post-name` | Names for event-time and post-treatment columns. |
| `--report-dir` | Directory for `transform_log.json`. |

## Typical Invocation

Use an inline command shaped like `python scripts/transform_data.py --input output/empirical/data_clean.csv --output output/empirical/data_analysis.csv --log-cols wage,assets --winsorize-cols wage,assets --standardize-cols age,assets --panel-id firm_id --time-col year --lag-cols wage --treat-start-col first_treat_year --report-dir output/empirical/tables`.

## Outputs

- Transformed dataset at `--output`.
- `transform_log.json` listing created columns and winsorization limits.

## Decision Rules

- Use generated suffixes consistently: `log_`, `ihs_`, `_w`, `_z`, `_lagN`, `_leadN`, `_diffN`.
- Log transforms produce missing values for non-positive inputs. Use IHS when zeros or negatives are meaningful.
- Winsorization creates new columns instead of overwriting originals.
- Panel operators require sorted `--panel-id` and `--time-col`; do not create lags without both.
- For staggered DID, create `rel_time` and `post` with `--treat-start-col` rather than writing custom dataframe code.
