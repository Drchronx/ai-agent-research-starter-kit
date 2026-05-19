from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from common import DEFAULT_OUTPUT, add_common_io, export_table, import_matplotlib, parse_cols, read_data, require_columns, save_figure, write_json


def km_curve(df: pd.DataFrame, duration: str, event: str, group_col: str | None) -> pd.DataFrame:
    groups = [(None, df)] if not group_col else list(df.groupby(group_col, dropna=False))
    rows: list[dict[str, Any]] = []
    for group, data in groups:
        data = data.sort_values(duration)
        survival = 1.0
        rows.append({"group": "all" if group is None else group, "time": 0.0, "survival": 1.0, "n_at_risk": len(data), "events": 0})
        event_times = sorted(data.loc[data[event] == 1, duration].unique())
        for time in event_times:
            n_at_risk = int((data[duration] >= time).sum())
            events = int(((data[duration] == time) & (data[event] == 1)).sum())
            if n_at_risk > 0:
                survival *= 1.0 - events / n_at_risk
            rows.append({"group": "all" if group is None else group, "time": float(time), "survival": survival, "n_at_risk": n_at_risk, "events": events})
    return pd.DataFrame(rows)


def survival_plot(curve: pd.DataFrame, outdir: Path) -> list[str]:
    plt = import_matplotlib()
    fig, ax = plt.subplots(figsize=(7.5, 5.0))
    for group, data in curve.groupby("group"):
        ax.step(data["time"], data["survival"], where="post", label=str(group), linewidth=2)
    ax.set_xlabel("Time")
    ax.set_ylabel("Survival probability")
    ax.set_ylim(0, 1.03)
    ax.spines[["top", "right"]].set_visible(False)
    if curve["group"].nunique() > 1:
        ax.legend(frameon=False)
    fig.tight_layout()
    written = save_figure(fig, outdir / "fig_km_curve")
    plt.close(fig)
    return written


def fit_lifelines(df: pd.DataFrame, args: argparse.Namespace, covariates: list[str]) -> tuple[list[dict[str, Any]], list[str]]:
    rows: list[dict[str, Any]] = []
    summaries: list[str] = []
    try:
        from lifelines import CoxPHFitter, WeibullAFTFitter
    except ImportError:
        for method in parse_cols(args.methods):
            if method in {"cox", "aft"}:
                rows.append({"method": method, "term": "", "coef": np.nan, "se": np.nan, "pvalue": np.nan, "error": "Install lifelines to run Cox or AFT models."})
        return rows, summaries

    model_df = pd.get_dummies(df[[args.duration, args.event] + covariates], drop_first=True).apply(pd.to_numeric, errors="coerce").dropna()
    if "cox" in parse_cols(args.methods):
        cox = CoxPHFitter()
        cox.fit(model_df, duration_col=args.duration, event_col=args.event)
        for term, row in cox.summary.iterrows():
            rows.append({"method": "cox", "term": term, "coef": float(row["coef"]), "se": float(row["se(coef)"]), "pvalue": float(row["p"]), "nobs": len(model_df)})
        summaries.append(str(cox.summary))
    if "aft" in parse_cols(args.methods):
        aft = WeibullAFTFitter()
        aft.fit(model_df, duration_col=args.duration, event_col=args.event)
        for term, row in aft.summary.iterrows():
            rows.append({"method": "weibull_aft", "term": str(term), "coef": float(row["coef"]), "se": float(row["se(coef)"]), "pvalue": float(row["p"]), "nobs": len(model_df)})
        summaries.append(str(aft.summary))
    return rows, summaries


def run(args: argparse.Namespace) -> dict[str, Any]:
    df = read_data(args.input, args.sheet)
    covariates = parse_cols(args.covariates)
    required = [args.duration, args.event] + covariates
    if args.group_col:
        required.append(args.group_col)
    require_columns(df, required, "survival columns")
    before = len(df)
    df[args.duration] = pd.to_numeric(df[args.duration], errors="coerce")
    df[args.event] = pd.to_numeric(df[args.event], errors="coerce")
    df = df.dropna(subset=required).copy()
    df[args.event] = df[args.event].astype(int)

    outdir = Path(args.output_dir)
    written: list[str] = []
    figure_files: list[str] = []
    curve = pd.DataFrame()
    methods = parse_cols(args.methods)
    if "km" in methods:
        curve = km_curve(df, args.duration, args.event, args.group_col)
        written += export_table(curve.round(6), outdir / "km_curve", parse_cols(args.formats))
        if not args.no_figures:
            figure_files = survival_plot(curve, outdir)
    model_rows, summaries = fit_lifelines(df, args, covariates)
    if model_rows:
        written += export_table(pd.DataFrame(model_rows).round(6), outdir / "survival_model_results", parse_cols(args.formats))
    summary_path = outdir / "survival_summaries.txt"
    summary_path.write_text("\n\n".join(summaries), encoding="utf-8")
    written.append(str(summary_path))

    manifest = {
        "input": str(args.input),
        "output_dir": str(outdir),
        "methods": methods,
        "duration": args.duration,
        "event": args.event,
        "covariates": covariates,
        "group_col": args.group_col,
        "dropped_missing_rows": int(before - len(df)),
        "files": {"tables": written, "figures": figure_files, "manifest": str(outdir / "survival_manifest.json")},
    }
    write_json(manifest, outdir / "survival_manifest.json")
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run fixed Kaplan-Meier, Cox, and Weibull AFT survival workflows.")
    add_common_io(parser)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT / "survival"))
    parser.add_argument("--duration", required=True)
    parser.add_argument("--event", required=True)
    parser.add_argument("--covariates", default="")
    parser.add_argument("--group-col", default=None)
    parser.add_argument("--methods", default="km,cox", help="Comma-separated: km,cox,aft.")
    parser.add_argument("--no-figures", action="store_true")
    parser.add_argument("--formats", default="csv,xlsx,tex")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    print(json.dumps(run(args), indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
