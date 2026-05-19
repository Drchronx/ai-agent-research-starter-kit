import argparse
import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib import font_manager
from sklearn.linear_model import LinearRegression


FONT_PATH_CANDIDATES = [
    os.getenv("OPENCLAW_CJK_FONT", "").strip(),
    r"C:\Program Files\Microsoft Office\root\vfs\Fonts\private\STSONG.TTF",
    r"C:\Windows\Fonts\msyh.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
]
FONT_NAME_CANDIDATES = [
    "STSong",
    "Microsoft YaHei",
    "SimHei",
    "Noto Sans CJK SC",
    "Source Han Sans SC",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze research datasets and generate publication-ready figures.")
    parser.add_argument("input_path", help="Path to a CSV or Excel dataset.")
    parser.add_argument("--output-dir", default="reports/research-data-analysis", help="Directory for reports and figures.")
    parser.add_argument("--group-col", help="Optional grouping column for comparative boxplots.")
    parser.add_argument("--target-col", help="Optional numeric target column for linear regression.")
    return parser.parse_args()


def load_table(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    raise ValueError(f"Unsupported file type: {path.suffix}")


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def set_style() -> None:
    sns.set_theme(style="whitegrid", context="paper")
    plt.rcParams["figure.dpi"] = 180
    plt.rcParams["savefig.dpi"] = 300
    plt.rcParams["axes.unicode_minus"] = False

    installed_names = {font.name for font in font_manager.fontManager.ttflist}
    for raw_font_path in FONT_PATH_CANDIDATES:
        if not raw_font_path:
            continue
        font_path = Path(raw_font_path)
        if font_path.exists() and font_path.is_file():
            font_manager.fontManager.addfont(str(font_path))
            font_name = font_manager.FontProperties(fname=str(font_path)).get_name()
            plt.rcParams["font.family"] = font_name
            plt.rcParams["font.sans-serif"] = [font_name, *FONT_NAME_CANDIDATES, "DejaVu Sans"]
            return

    for font_name in FONT_NAME_CANDIDATES:
        if font_name in installed_names:
            plt.rcParams["font.family"] = font_name
            plt.rcParams["font.sans-serif"] = [font_name, *FONT_NAME_CANDIDATES, "DejaVu Sans"]
            return

    plt.rcParams["font.family"] = "DejaVu Sans"


def save_missingness(df: pd.DataFrame, output_dir: Path) -> Path:
    missing = (
        df.isna()
        .mean()
        .mul(100)
        .round(2)
        .rename("missing_pct")
        .reset_index()
        .rename(columns={"index": "column"})
        .sort_values("missing_pct", ascending=False)
    )
    output = output_dir / "missingness.csv"
    missing.to_csv(output, index=False, encoding="utf-8-sig")
    return output


def save_summary_stats(df: pd.DataFrame, output_dir: Path) -> tuple[pd.DataFrame, Path]:
    numeric = df.select_dtypes(include="number")
    if numeric.empty:
        raise ValueError("The dataset does not contain numeric columns for statistical analysis.")
    summary = numeric.describe().T.round(4)
    summary["missing_count"] = numeric.isna().sum()
    summary["missing_pct"] = (numeric.isna().mean() * 100).round(2)
    output = output_dir / "summary_statistics.csv"
    summary.to_csv(output, encoding="utf-8-sig")
    return summary, output


def save_distribution_plots(df: pd.DataFrame, output_dir: Path) -> list[Path]:
    numeric = df.select_dtypes(include="number")
    figure_dir = ensure_dir(output_dir / "figures")
    outputs: list[Path] = []
    for column in numeric.columns[:4]:
        fig, ax = plt.subplots(figsize=(6.4, 4.8))
        sns.histplot(df[column].dropna(), kde=True, ax=ax, color="#1f5aa6")
        ax.set_title(f"Distribution of {column}")
        ax.set_xlabel(column)
        ax.set_ylabel("Count")
        fig.tight_layout()
        path = figure_dir / f"distribution_{column}.png"
        fig.savefig(path, bbox_inches="tight")
        plt.close(fig)
        outputs.append(path)
    return outputs


def save_correlation_heatmap(df: pd.DataFrame, output_dir: Path) -> Path | None:
    numeric = df.select_dtypes(include="number")
    if numeric.shape[1] < 2:
        return None
    corr = numeric.corr(numeric_only=True)
    fig, ax = plt.subplots(figsize=(7.2, 5.8))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="Blues", linewidths=0.5, ax=ax)
    ax.set_title("Correlation Heatmap")
    fig.tight_layout()
    path = ensure_dir(output_dir / "figures") / "correlation_heatmap.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def save_group_boxplot(df: pd.DataFrame, group_col: str, output_dir: Path) -> Path | None:
    if group_col not in df.columns:
        raise ValueError(f"group column '{group_col}' not found.")
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    numeric_cols = [col for col in numeric_cols if col != group_col]
    if not numeric_cols:
        return None
    preferred = [col for col in numeric_cols if col.lower() not in {"year", "dose"}]
    metric = preferred[0] if preferred else numeric_cols[0]
    fig, ax = plt.subplots(figsize=(7.2, 5.2))
    sns.boxplot(data=df, x=group_col, y=metric, hue=group_col, ax=ax, palette="Set2", legend=False)
    sns.stripplot(data=df, x=group_col, y=metric, ax=ax, color="#333333", size=3, alpha=0.6)
    ax.set_title(f"{metric} by {group_col}")
    fig.tight_layout()
    path = ensure_dir(output_dir / "figures") / f"boxplot_{metric}_by_{group_col}.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def run_regression(df: pd.DataFrame, target_col: str, output_dir: Path) -> tuple[Path, Path] | tuple[None, None]:
    if target_col not in df.columns:
        raise ValueError(f"target column '{target_col}' not found.")
    numeric = df.select_dtypes(include="number").copy()
    feature_cols = [col for col in numeric.columns if col != target_col]
    if len(feature_cols) < 1:
        return None, None
    model_df = numeric[[target_col] + feature_cols].dropna()
    if len(model_df) < 3:
        return None, None

    x = model_df[feature_cols]
    y = model_df[target_col]
    model = LinearRegression()
    model.fit(x, y)
    predictions = model.predict(x)

    coef_table = pd.DataFrame({"feature": feature_cols, "coefficient": model.coef_.round(6)})
    coef_table = coef_table.sort_values("coefficient", key=lambda series: series.abs(), ascending=False)
    coef_table.loc[len(coef_table)] = {"feature": "intercept", "coefficient": round(float(model.intercept_), 6)}
    coef_path = output_dir / "regression_coefficients.csv"
    coef_table.to_csv(coef_path, index=False, encoding="utf-8-sig")

    fig, ax = plt.subplots(figsize=(6.4, 4.8))
    sns.scatterplot(x=y, y=predictions, ax=ax, color="#1f5aa6")
    min_val = min(float(y.min()), float(predictions.min()))
    max_val = max(float(y.max()), float(predictions.max()))
    ax.plot([min_val, max_val], [min_val, max_val], linestyle="--", color="#cc4c39", linewidth=1)
    ax.set_title(f"Observed vs Predicted: {target_col}")
    ax.set_xlabel("Observed")
    ax.set_ylabel("Predicted")
    fig.tight_layout()
    fig_path = ensure_dir(output_dir / "figures") / f"regression_{target_col}.png"
    fig.savefig(fig_path, bbox_inches="tight")
    plt.close(fig)
    return coef_path, fig_path


def build_report(df: pd.DataFrame, summary: pd.DataFrame, missing_path: Path, output_dir: Path, group_col: str | None, target_col: str | None) -> Path:
    lines = [
        "# Research Data Analysis Report",
        "",
        f"- Rows: {len(df)}",
        f"- Columns: {df.shape[1]}",
        f"- Numeric columns analyzed: {len(summary)}",
        f"- Missingness table: `{missing_path.name}`",
        "",
        "## Key Summary Statistics",
    ]
    top_means = summary["mean"].sort_values(ascending=False).head(5)
    for column, value in top_means.items():
        lines.append(f"- `{column}` mean = {value:.3f}")

    lines.extend(["", "## Recommended Figure Set"])
    lines.append("- Distribution plots for the first four numeric indicators.")
    if len(summary) >= 2:
        lines.append("- Correlation heatmap for numeric variables.")
    if group_col:
        lines.append(f"- Comparative boxplot using `{group_col}` as the grouping factor.")
    if target_col:
        lines.append(f"- Linear regression diagnostic figure using `{target_col}` as the dependent variable.")

    lines.extend(["", "## Interpretation Notes"])
    highest_variance = summary["std"].sort_values(ascending=False).head(3)
    for column, value in highest_variance.items():
        lines.append(f"- `{column}` shows substantial dispersion (std = {value:.3f}).")
    if group_col:
        lines.append(f"- Inspect the `{group_col}` boxplot for heterogeneity and outlier separation across groups.")
    if target_col:
        lines.append(f"- Review `regression_coefficients.csv` before treating associations with `{target_col}` as substantive findings.")

    report_path = output_dir / "analysis_report.md"
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_path


def main() -> None:
    args = parse_args()
    input_path = Path(args.input_path)
    output_dir = ensure_dir(Path(args.output_dir))
    set_style()

    df = load_table(input_path)
    summary, summary_path = save_summary_stats(df, output_dir)
    missing_path = save_missingness(df, output_dir)
    distribution_paths = save_distribution_plots(df, output_dir)
    heatmap_path = save_correlation_heatmap(df, output_dir)
    group_plot = save_group_boxplot(df, args.group_col, output_dir) if args.group_col else None
    regression_outputs = run_regression(df, args.target_col, output_dir) if args.target_col else (None, None)
    report_path = build_report(df, summary, missing_path, output_dir, args.group_col, args.target_col)

    print(f"Summary statistics: {summary_path}")
    print(f"Missingness table: {missing_path}")
    print(f"Report: {report_path}")
    for path in distribution_paths:
        print(f"Figure: {path}")
    if heatmap_path:
        print(f"Figure: {heatmap_path}")
    if group_plot:
        print(f"Figure: {group_plot}")
    if regression_outputs[0]:
        print(f"Regression coefficients: {regression_outputs[0]}")
    if regression_outputs[1]:
        print(f"Figure: {regression_outputs[1]}")


if __name__ == "__main__":
    main()
