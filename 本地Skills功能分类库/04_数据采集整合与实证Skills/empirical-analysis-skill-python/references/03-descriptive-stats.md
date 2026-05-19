# Step 3 - Descriptive Statistics and Table 1

Use the fixed script `scripts/describe_data.py`.

Goal: produce the descriptive tables and motivation figures that precede regression results.

## Use When

- The user asks for Table 1, balance table, summary statistics, correlation matrix, treatment-control descriptives, or treated/control trend plots.

## Main Parameters

| Parameter | Use |
|---|---|
| `--input` | Analysis dataset path. |
| `--vars` | Numeric variables for summary and balance rows. |
| `--group` | Treatment or grouping variable for balance table. |
| `--categorical-vars` | Categorical variables for frequency tables. |
| `--outcome`, `--treatment`, `--time` | Required together for trend figure values and `fig1_trend`. |
| `--formats` | Table formats, default `csv,xlsx,tex`. |
| `--no-figures` | Skip PNG/PDF figures when only tables are needed. |
| `--output-dir` | Output directory, usually `output/empirical/tables`. |

## Typical Invocation

Use an inline command shaped like `python scripts/describe_data.py --input output/empirical/data_analysis.csv --vars log_wage,training,age,edu,tenure --group training --categorical-vars female,region --outcome log_wage --treatment training --time year --output-dir output/empirical/tables`.

## Outputs

- `table1_summary` in requested table formats.
- `table1_balance` when `--group` is provided.
- `table1_categorical` when categorical variables are provided.
- `correlation_matrix.csv` and `fig_corr_heatmap` when at least two numeric variables are available.
- `trend_values.csv` and `fig1_trend` when outcome, treatment, and time are provided.
- `describe_manifest.json`.

## Decision Rules

- Always include the headline outcome, treatment, and core controls in `--vars`.
- For treatment-control comparisons, pass the treatment indicator as `--group`.
- Interpret standardized mean differences as balance diagnostics: below `0.1` is usually balanced, above `0.25` is severe imbalance.
- If a cross-section has no time variable, skip the trend figure with `--no-figures` or omit the trend parameters.
