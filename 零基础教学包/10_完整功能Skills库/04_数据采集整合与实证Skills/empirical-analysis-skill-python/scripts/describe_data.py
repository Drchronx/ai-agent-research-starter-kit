from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

from common import DEFAULT_OUTPUT, add_common_io, add_table_format_arg, export_table, import_matplotlib, numeric_columns, parse_cols, read_data, require_columns, save_figure, write_json


def table_summary(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    require_columns(df, cols)
    rows = []
    for col in cols:
        s = pd.to_numeric(df[col], errors="coerce")
        rows.append(
            {
                "variable": col,
                "N": int(s.notna().sum()),
                "Mean": s.mean(),
                "SD": s.std(),
                "Min": s.min(),
                "P25": s.quantile(0.25),
                "Median": s.median(),
                "P75": s.quantile(0.75),
                "Max": s.max(),
            }
        )
    return pd.DataFrame(rows).round(4)


def standardized_mean_difference(treat: pd.Series, control: pd.Series) -> float:
    pooled = math.sqrt((float(treat.var()) + float(control.var())) / 2.0)
    if pooled == 0 or not np.isfinite(pooled):
        return np.nan
    return float((treat.mean() - control.mean()) / pooled)


def table1_by_group(df: pd.DataFrame, group: str, cols: list[str]) -> pd.DataFrame:
    from scipy import stats

    require_columns(df, [group] + cols)
    groups = [g for g in sorted(df[group].dropna().unique().tolist())]
    if len(groups) < 2:
        raise ValueError("Group variable must contain at least two non-missing groups.")
    if len(groups) > 2:
        groups = groups[:2]
    g0, g1 = groups[0], groups[1]
    rows = []
    for col in cols:
        a = pd.to_numeric(df.loc[df[group] == g1, col], errors="coerce").dropna()
        b = pd.to_numeric(df.loc[df[group] == g0, col], errors="coerce").dropna()
        pvalue = stats.ttest_ind(a, b, equal_var=False, nan_policy="omit").pvalue if len(a) > 1 and len(b) > 1 else np.nan
        rows.append(
            {
                "variable": col,
                "group0": str(g0),
                "group1": str(g1),
                "N_group0": int(len(b)),
                "N_group1": int(len(a)),
                "mean_group0": b.mean(),
                "sd_group0": b.std(),
                "mean_group1": a.mean(),
                "sd_group1": a.std(),
                "difference": a.mean() - b.mean(),
                "SMD": standardized_mean_difference(a, b),
                "p_ttest": pvalue,
            }
        )
    return pd.DataFrame(rows).round(4)


def run(args: argparse.Namespace) -> dict[str, object]:
    df = read_data(args.input, args.sheet)
    outdir = Path(args.output_dir)
    cols = parse_cols(args.vars) or numeric_columns(df)[:25]
    if not cols:
        raise ValueError("No numeric variables available. Pass --vars explicitly.")

    written: list[str] = []
    written += export_table(table_summary(df, cols), outdir / "table1_summary", parse_cols(args.formats))

    if args.group:
        written += export_table(table1_by_group(df, args.group, cols), outdir / "table1_balance", parse_cols(args.formats))

    categorical = parse_cols(args.categorical_vars)
    if categorical:
        require_columns(df, categorical)
        rows = []
        for col in categorical:
            counts = df[col].value_counts(dropna=False)
            props = df[col].value_counts(dropna=False, normalize=True)
            for level, count in counts.items():
                rows.append({"variable": col, "level": str(level), "N": int(count), "share": float(props.loc[level])})
        written += export_table(pd.DataFrame(rows), outdir / "table1_categorical", parse_cols(args.formats))

    corr_cols = numeric_columns(df, cols)
    if len(corr_cols) >= 2:
        corr = df[corr_cols].corr()
        corr_path = outdir / "correlation_matrix.csv"
        corr_path.parent.mkdir(parents=True, exist_ok=True)
        corr.to_csv(corr_path)
        written.append(str(corr_path))
        if not args.no_figures:
            plt = import_matplotlib()
            fig, ax = plt.subplots(figsize=(max(6, len(corr_cols) * 0.45), max(4, len(corr_cols) * 0.35)))
            im = ax.imshow(corr, vmin=-1, vmax=1, cmap="coolwarm")
            ax.set_xticks(range(len(corr_cols)), labels=corr_cols, rotation=45, ha="right")
            ax.set_yticks(range(len(corr_cols)), labels=corr_cols)
            fig.colorbar(im, ax=ax, shrink=0.8)
            fig.tight_layout()
            written += save_figure(fig, outdir / "fig_corr_heatmap")
            plt.close(fig)

    if args.outcome and args.treatment and args.time:
        require_columns(df, [args.outcome, args.treatment, args.time], "trend plot columns")
        plot_df = (
            df.groupby([args.time, args.treatment], dropna=False)[args.outcome]
            .mean()
            .reset_index()
            .pivot(index=args.time, columns=args.treatment, values=args.outcome)
            .sort_index()
        )
        plot_df.to_csv(outdir / "trend_values.csv")
        if not args.no_figures:
            plt = import_matplotlib()
            fig, ax = plt.subplots(figsize=(7, 4))
            plot_df.plot(ax=ax)
            ax.set_xlabel(args.time)
            ax.set_ylabel(args.outcome)
            ax.spines[["top", "right"]].set_visible(False)
            fig.tight_layout()
            written += save_figure(fig, outdir / "fig1_trend")
            plt.close(fig)

    manifest = {"written": written}
    write_json(manifest, outdir / "describe_manifest.json")
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate empirical Table 1 and descriptive figures.")
    add_common_io(parser)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT / "tables"))
    parser.add_argument("--vars", default="")
    parser.add_argument("--group", default=None)
    parser.add_argument("--categorical-vars", default="")
    parser.add_argument("--outcome", default=None)
    parser.add_argument("--treatment", default=None)
    parser.add_argument("--time", default=None)
    parser.add_argument("--no-figures", action="store_true")
    add_table_format_arg(parser)
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    print(json.dumps(run(args), indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
