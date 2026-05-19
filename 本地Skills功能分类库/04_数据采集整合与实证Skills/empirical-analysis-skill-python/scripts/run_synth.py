from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from common import DEFAULT_OUTPUT, add_common_io, export_table, import_matplotlib, parse_cols, read_data, require_columns, save_figure, write_json


def coerce_time_value(series: pd.Series, value: str) -> Any:
    if pd.api.types.is_numeric_dtype(series):
        return float(value)
    parsed_series = pd.to_datetime(series, errors="coerce")
    parsed_value = pd.to_datetime(value, errors="coerce")
    if parsed_series.notna().all() and not pd.isna(parsed_value):
        return parsed_value
    return value


def normalize_time(series: pd.Series) -> pd.Series:
    if pd.api.types.is_numeric_dtype(series):
        return pd.to_numeric(series, errors="coerce")
    parsed = pd.to_datetime(series, errors="coerce")
    if parsed.notna().all():
        return parsed
    return series.astype(str)


def solve_weights(x0: np.ndarray, x1: np.ndarray, ridge: float) -> tuple[np.ndarray, str]:
    n_donors = x0.shape[1]
    try:
        from scipy.optimize import minimize

        def objective(weights: np.ndarray) -> float:
            residual = x1 - x0 @ weights
            return float(residual @ residual + ridge * (weights @ weights))

        constraints = {"type": "eq", "fun": lambda weights: np.sum(weights) - 1.0}
        bounds = [(0.0, 1.0)] * n_donors
        start = np.repeat(1.0 / n_donors, n_donors)
        result = minimize(objective, start, method="SLSQP", bounds=bounds, constraints=constraints)
        if result.success:
            weights = np.maximum(result.x, 0.0)
            weights = weights / weights.sum()
            return weights, "scipy_slsqp"
    except Exception:
        pass
    gram = x0.T @ x0 + ridge * np.eye(n_donors)
    target = x0.T @ x1
    weights = np.linalg.solve(gram, target)
    weights = np.maximum(weights, 0.0)
    if weights.sum() == 0:
        weights = np.repeat(1.0 / n_donors, n_donors)
    else:
        weights = weights / weights.sum()
    return weights, "nonnegative_lstsq_fallback"


def make_plot(trajectory: pd.DataFrame, outdir: Path, treated_unit: str) -> list[str]:
    plt = import_matplotlib()
    fig, axes = plt.subplots(2, 1, figsize=(8.0, 6.5), sharex=True, gridspec_kw={"height_ratios": [2, 1]})
    axes[0].plot(trajectory["time"], trajectory["treated"], label=str(treated_unit), linewidth=2)
    axes[0].plot(trajectory["time"], trajectory["synthetic"], label="Synthetic", linewidth=2, linestyle="--")
    axes[0].axvline(trajectory.loc[trajectory["post"] == 1, "time"].min(), color="gray", linestyle=":", linewidth=1)
    axes[0].set_ylabel("Outcome")
    axes[0].legend(frameon=False)
    axes[1].plot(trajectory["time"], trajectory["gap"], color="#333333", linewidth=2)
    axes[1].axhline(0, color="gray", linewidth=0.8)
    axes[1].set_ylabel("Gap")
    axes[1].set_xlabel("Time")
    for ax in axes:
        ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    written = save_figure(fig, outdir / "fig_synth_trajectory")
    plt.close(fig)
    return written


def run(args: argparse.Namespace) -> dict[str, Any]:
    df = read_data(args.input, args.sheet)
    require_columns(df, [args.outcome, args.unit, args.time], "synthetic-control columns")
    df = df.dropna(subset=[args.outcome, args.unit, args.time]).copy()
    df["_synth_time"] = normalize_time(df[args.time])
    treatment_time = coerce_time_value(df["_synth_time"], args.treatment_time)
    panel = df.pivot_table(index="_synth_time", columns=args.unit, values=args.outcome, aggfunc="mean").sort_index()
    treated_matches = [col for col in panel.columns if str(col) == str(args.treated_unit)]
    if not treated_matches:
        raise ValueError(f"Treated unit not found: {args.treated_unit}")
    treated_col = treated_matches[0]
    donors = parse_cols(args.donors)
    donor_cols = [col for col in panel.columns if str(col) in donors] if donors else [col for col in panel.columns if col != treated_col]
    if not donor_cols:
        raise ValueError("No donor units available.")
    pre_mask = panel.index < treatment_time
    if pre_mask.sum() < args.min_pre_periods:
        raise ValueError("Too few pre-treatment periods for synthetic control.")
    pre = panel.loc[pre_mask, [treated_col] + donor_cols].dropna(axis=0, how="any")
    x1 = pre[treated_col].to_numpy(dtype=float)
    x0 = pre[donor_cols].to_numpy(dtype=float)
    weights, optimizer = solve_weights(x0, x1, args.ridge)
    synthetic = panel[donor_cols].to_numpy(dtype=float) @ weights
    trajectory = pd.DataFrame(
        {
            "time": panel.index,
            "treated": panel[treated_col].to_numpy(dtype=float),
            "synthetic": synthetic,
        }
    )
    trajectory["gap"] = trajectory["treated"] - trajectory["synthetic"]
    trajectory["post"] = (panel.index >= treatment_time).astype(int)
    weights_table = pd.DataFrame({"donor_unit": donor_cols, "weight": weights}).sort_values("weight", ascending=False)
    fit = {
        "pre_rmse": float(np.sqrt(np.nanmean(trajectory.loc[trajectory["post"] == 0, "gap"] ** 2))),
        "post_gap_mean": float(np.nanmean(trajectory.loc[trajectory["post"] == 1, "gap"])),
        "post_gap_rms": float(np.sqrt(np.nanmean(trajectory.loc[trajectory["post"] == 1, "gap"] ** 2))),
    }

    outdir = Path(args.output_dir)
    written: list[str] = []
    written += export_table(weights_table.round(6), outdir / "synthetic_weights", parse_cols(args.formats))
    written += export_table(trajectory.round(6), outdir / "synthetic_trajectory", parse_cols(args.formats))
    written += export_table(pd.DataFrame([fit]).round(6), outdir / "synthetic_fit", parse_cols(args.formats))
    figure_files: list[str] = []
    if not args.no_figures:
        figure_files = make_plot(trajectory, outdir, str(treated_col))
    manifest = {
        "input": str(args.input),
        "output_dir": str(outdir),
        "treated_unit": str(treated_col),
        "treatment_time": str(treatment_time),
        "donors": [str(col) for col in donor_cols],
        "optimizer": optimizer,
        "fit": fit,
        "files": {"tables": written, "figures": figure_files, "manifest": str(outdir / "synth_manifest.json")},
    }
    write_json(manifest, outdir / "synth_manifest.json")
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a fixed synthetic-control workflow.")
    add_common_io(parser)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT / "synth"))
    parser.add_argument("--outcome", required=True)
    parser.add_argument("--unit", required=True)
    parser.add_argument("--time", required=True)
    parser.add_argument("--treated-unit", required=True)
    parser.add_argument("--treatment-time", required=True)
    parser.add_argument("--donors", default="")
    parser.add_argument("--ridge", type=float, default=1e-8)
    parser.add_argument("--min-pre-periods", type=int, default=3)
    parser.add_argument("--no-figures", action="store_true")
    parser.add_argument("--formats", default="csv,xlsx,tex")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    print(json.dumps(run(args), indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
