---
name: research-data-auto-analysis-plotting
description: Automatically analyze research datasets and generate publication-ready statistical tables, correlation figures, grouped comparison plots, and regression diagnostics. Use when the user wants科研数据自动分析、学术绘图、实证数据可视化、可发表级图表输出, or needs a CSV/Excel dataset turned into summary statistics and clean PNG figures.
---

# Research Data Auto Analysis Plotting

Use this skill from `F:\Python\课程\OpenClaw\cnki\skills\research-data-auto-analysis-plotting`.

## Workflow

1. Install dependencies:

```powershell
python -m pip install -r scripts/requirements.txt
```

2. Run the analysis script on a CSV or Excel dataset:

```powershell
python scripts/analyze_research_data.py assets/sample_research_dataset.csv --group-col treatment_group --target-col response_score --output-dir reports/research-analysis-demo
```

3. Read the generated outputs:
- `summary_statistics.csv`
- `missingness.csv`
- `analysis_report.md`
- `figures/*.png`

## Behavior

- The script automatically reads `csv/xlsx/xls`.
- It computes summary statistics and missingness rates for numeric variables.
- It generates up to four distribution plots for the first numeric indicators.
- It creates a correlation heatmap when at least two numeric columns exist.
- It creates a grouped boxplot when `--group-col` is provided.
- It fits a simple linear regression and exports coefficients when `--target-col` is provided.

## Parameters

Run without grouped or regression analysis:

```powershell
python scripts/analyze_research_data.py path\to\data.xlsx --output-dir reports\my-study
```

Add grouped comparison plots:

```powershell
python scripts/analyze_research_data.py path\to\data.csv --group-col industry
```

Add regression diagnostics:

```powershell
python scripts/analyze_research_data.py path\to\data.csv --target-col roa
```
