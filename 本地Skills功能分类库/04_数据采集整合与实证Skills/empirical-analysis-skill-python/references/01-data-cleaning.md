# Step 1 - Data Cleaning

Use the fixed script `scripts/clean_data.py`.

Goal: turn a raw file into an analysis-ready dataset while creating a sample log, missingness report, dtype report, and duplicate report.

## Use When

- The user provides raw CSV, Excel, Parquet, JSON, JSONL, or Stata data.
- The workflow needs dtype coercion, string trimming, key-variable missingness handling, or deduplication.
- A paper-style sample construction log is required.

## Main Parameters

| Parameter | Use |
|---|---|
| `--input` | Raw data file path. |
| `--output` | Cleaned dataset path. |
| `--sheet` | Excel sheet when reading workbook files. |
| `--id-cols` | Unit, time, or primary key columns. |
| `--key-vars` | Outcome, treatment, id, time, and other variables that cannot be missing. |
| `--numeric-cols` | Columns to coerce with numeric parsing. |
| `--categorical-cols` | Columns to mark as categories. |
| `--date-cols` | Columns to parse as datetimes. |
| `--dedupe-cols` | Columns used to identify duplicate records. |
| `--drop-key-missing` | Drop rows with missing values on `--key-vars`. |
| `--drop-duplicates` | Drop duplicate records after counting them. |
| `--missing-threshold` | High-missingness threshold, default `1.0`. |
| `--drop-high-missing` | Drop columns above the missingness threshold. |
| `--report-dir` | Directory for reports, usually `output/empirical/tables`. |

## Typical Invocation

Use an inline command shaped like `python scripts/clean_data.py --input data/raw.csv --output output/empirical/data_clean.csv --id-cols firm_id,year --key-vars y,treat,firm_id,year --numeric-cols y,treat,age,assets --dedupe-cols firm_id,year --drop-key-missing --drop-duplicates --report-dir output/empirical/tables`.

## Outputs

- Cleaned dataset at `--output`.
- `missing_report.csv` and `missing_report.xlsx`.
- `dtype_report.csv` and `dtype_report.xlsx`.
- `sample_log.json` with row and column counts, dropped rows, duplicate counts, and coercions.

## Decision Rules

- Do not silently drop rows. Use `--drop-key-missing` only for outcome, treatment, id, time, or other non-negotiable variables.
- Do not blanket-impute in Step 1. Create clean types and reports first; transformations and imputations belong in later scripted steps.
- Prefer explicit `--dedupe-cols` for panel data. Use `unit,time` keys rather than full-row deduplication when possible.
- If the CLI cannot read the file type, convert the file externally or extend `read_data` in `scripts/empirical_cli.py`.
