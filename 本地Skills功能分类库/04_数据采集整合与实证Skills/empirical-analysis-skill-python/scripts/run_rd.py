from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from common import DEFAULT_OUTPUT, add_common_io, export_table, import_matplotlib, parse_cols, read_data, require_columns, save_figure, write_json


def parse_float_list(value: str) -> list[float]:
    return [float(item.strip()) for item in value.split(",") if item.strip()]


def kernel_weights(x: pd.Series, bandwidth: float, kernel: str) -> np.ndarray:
    scaled = np.abs(x.to_numpy(dtype=float)) / bandwidth
    if kernel == "triangular":
        weights = np.maximum(1.0 - scaled, 0.0)
    elif kernel == "epanechnikov":
        weights = np.maximum(0.75 * (1.0 - scaled**2), 0.0)
    elif kernel == "uniform":
        weights = (scaled <= 1.0).astype(float)
    else:
        raise ValueError(f"Unsupported kernel: {kernel}")
    return weights


def choose_bandwidth(centered: pd.Series) -> float:
    abs_x = centered.abs()
    positive = abs_x[abs_x > 0]
    if positive.empty:
        raise ValueError("Running variable has no variation around the cutoff.")
    return float(positive.quantile(0.75))


def prepare_local_frame(df: pd.DataFrame, args: argparse.Namespace, bandwidth: float) -> pd.DataFrame:
    data = df.copy()
    data["_rd_x"] = pd.to_numeric(data[args.running], errors="coerce") - args.cutoff
    data["_rd_right"] = (data["_rd_x"] >= 0).astype(float)
    data = data.loc[data["_rd_x"].abs() <= bandwidth].copy()
    for power in range(1, args.order + 1):
        data[f"_rd_x{power}"] = data["_rd_x"] ** power
        data[f"_rd_right_x{power}"] = data["_rd_right"] * data[f"_rd_x{power}"]
    data["_rd_weight"] = kernel_weights(data["_rd_x"], bandwidth, args.kernel)
    return data.loc[data["_rd_weight"] > 0].copy()


def rd_formula(outcome: str, controls: list[str], order: int) -> str:
    terms = ["_rd_right"]
    for power in range(1, order + 1):
        terms.append(f"_rd_x{power}")
        terms.append(f"_rd_right_x{power}")
    terms.extend(controls)
    return f"{outcome} ~ {' + '.join(terms)}"


def fit_wls(data: pd.DataFrame, formula: str, args: argparse.Namespace) -> Any:
    import statsmodels.formula.api as smf

    model = smf.wls(formula, data=data, weights=data["_rd_weight"])
    if args.cluster:
        require_columns(data, [args.cluster], "cluster column")
        return model.fit(cov_type="cluster", cov_kwds={"groups": data[args.cluster]})
    return model.fit(cov_type=args.cov_type)


def sharp_row(result: Any, bandwidth: float, nobs: int, formula: str) -> dict[str, Any]:
    return {
        "method": "sharp_rd",
        "bandwidth": bandwidth,
        "term": "_rd_right",
        "estimate": float(result.params.get("_rd_right", np.nan)),
        "se": float(result.bse.get("_rd_right", np.nan)),
        "pvalue": float(result.pvalues.get("_rd_right", np.nan)),
        "nobs": nobs,
        "rsquared": float(getattr(result, "rsquared", np.nan)),
        "formula": formula,
    }


def fuzzy_row(outcome_result: Any, treatment_result: Any, bandwidth: float, nobs: int) -> dict[str, Any]:
    reduced = float(outcome_result.params.get("_rd_right", np.nan))
    first_stage = float(treatment_result.params.get("_rd_right", np.nan))
    reduced_se = float(outcome_result.bse.get("_rd_right", np.nan))
    first_stage_se = float(treatment_result.bse.get("_rd_right", np.nan))
    late = reduced / first_stage if np.isfinite(first_stage) and abs(first_stage) > 1e-12 else np.nan
    se = np.nan
    if np.isfinite(late) and np.isfinite(reduced_se) and np.isfinite(first_stage_se):
        se = float(np.sqrt((reduced_se / first_stage) ** 2 + ((reduced * first_stage_se) / (first_stage**2)) ** 2))
    return {
        "method": "fuzzy_rd_wald",
        "bandwidth": bandwidth,
        "term": "wald_late",
        "estimate": late,
        "se": se,
        "pvalue": np.nan,
        "nobs": nobs,
        "reduced_form_jump": reduced,
        "first_stage_jump": first_stage,
        "formula": "local Wald ratio: outcome jump / treatment jump",
    }


def prediction_frame(data: pd.DataFrame, args: argparse.Namespace, controls: list[str], side: str) -> pd.DataFrame:
    if side == "left":
        x_grid = np.linspace(data["_rd_x"].min(), min(0.0, data["_rd_x"].max()), 100)
    else:
        x_grid = np.linspace(max(0.0, data["_rd_x"].min()), data["_rd_x"].max(), 100)
    frame = pd.DataFrame({"_rd_x": x_grid, "_rd_right": (x_grid >= 0).astype(float)})
    for power in range(1, args.order + 1):
        frame[f"_rd_x{power}"] = frame["_rd_x"] ** power
        frame[f"_rd_right_x{power}"] = frame["_rd_right"] * frame[f"_rd_x{power}"]
    for control in controls:
        if pd.api.types.is_numeric_dtype(data[control]):
            frame[control] = data[control].mean()
        else:
            frame[control] = data[control].mode(dropna=True).iloc[0]
    return frame


def make_rd_plot(data: pd.DataFrame, result: Any, args: argparse.Namespace, controls: list[str], outdir: Path) -> list[str]:
    plt = import_matplotlib()
    fig, ax = plt.subplots(figsize=(7.5, 5.0))
    bins = pd.cut(data["_rd_x"], bins=args.bins)
    binned = data.groupby(bins, observed=True).agg(x=("_rd_x", "mean"), y=(args.outcome, "mean")).dropna()
    ax.scatter(binned["x"], binned["y"], s=24, alpha=0.8, label="Binned mean")
    for side, color in [("left", "#1f77b4"), ("right", "#d62728")]:
        frame = prediction_frame(data, args, controls, side)
        ax.plot(frame["_rd_x"], result.predict(frame), color=color, linewidth=2)
    ax.axvline(0, color="black", linestyle="--", linewidth=1)
    ax.set_xlabel(f"{args.running} centered at cutoff")
    ax.set_ylabel(args.outcome)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    written = save_figure(fig, outdir / "fig_rd_plot")
    plt.close(fig)
    return written


def run(args: argparse.Namespace) -> dict[str, Any]:
    df = read_data(args.input, args.sheet)
    controls = parse_cols(args.controls)
    required = [args.outcome, args.running] + controls
    if args.treatment:
        required.append(args.treatment)
    if args.cluster:
        required.append(args.cluster)
    require_columns(df, required, "RD columns")
    before = len(df)
    df = df.dropna(subset=required).copy()
    centered = pd.to_numeric(df[args.running], errors="coerce") - args.cutoff
    base_bandwidth = args.bandwidth or choose_bandwidth(centered)
    bandwidths = parse_float_list(args.bandwidth_grid) if args.bandwidth_grid else [base_bandwidth]
    if base_bandwidth not in bandwidths:
        bandwidths.insert(0, base_bandwidth)

    rows: list[dict[str, Any]] = []
    summaries: list[str] = []
    figure_files: list[str] = []
    main_result: Any | None = None
    main_data: pd.DataFrame | None = None
    main_formula = ""
    for bandwidth in bandwidths:
        data = prepare_local_frame(df, args, bandwidth)
        if len(data) < args.min_n:
            rows.append({"method": "rd", "bandwidth": bandwidth, "term": "_rd_right", "estimate": np.nan, "se": np.nan, "pvalue": np.nan, "nobs": len(data), "error": "Too few observations inside bandwidth."})
            continue
        formula = rd_formula(args.outcome, controls, args.order)
        outcome_result = fit_wls(data, formula, args)
        rows.append(sharp_row(outcome_result, bandwidth, int(outcome_result.nobs), formula))
        summaries.append(f"\n\n=== RD bandwidth={bandwidth} ===\n{outcome_result.summary()}")
        if args.treatment:
            treatment_formula = rd_formula(args.treatment, controls, args.order)
            treatment_result = fit_wls(data, treatment_formula, args)
            rows.append(fuzzy_row(outcome_result, treatment_result, bandwidth, int(outcome_result.nobs)))
            summaries.append(f"\n\n=== First stage bandwidth={bandwidth} ===\n{treatment_result.summary()}")
        if abs(bandwidth - base_bandwidth) < 1e-12:
            main_result = outcome_result
            main_data = data
            main_formula = formula

    outdir = Path(args.output_dir)
    results = pd.DataFrame(rows).round(6)
    written = export_table(results, outdir / "rd_results", parse_cols(args.formats))
    summary_path = outdir / "rd_summaries.txt"
    summary_path.write_text("\n".join(summaries), encoding="utf-8")
    written.append(str(summary_path))
    if not args.no_figures and main_result is not None and main_data is not None:
        figure_files = make_rd_plot(main_data, main_result, args, controls, outdir)

    manifest = {
        "input": str(args.input),
        "output_dir": str(outdir),
        "outcome": args.outcome,
        "running": args.running,
        "cutoff": args.cutoff,
        "treatment": args.treatment,
        "controls": controls,
        "order": args.order,
        "kernel": args.kernel,
        "bandwidths": bandwidths,
        "dropped_missing_rows": int(before - len(df)),
        "files": {"results": written, "figures": figure_files, "manifest": str(outdir / "rd_manifest.json")},
        "main_formula": main_formula,
    }
    write_json(manifest, outdir / "rd_manifest.json")
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run sharp or fuzzy regression discontinuity with fixed local-polynomial code.")
    add_common_io(parser)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT / "rd"))
    parser.add_argument("--outcome", required=True)
    parser.add_argument("--running", required=True)
    parser.add_argument("--cutoff", type=float, default=0.0)
    parser.add_argument("--treatment", default=None, help="Optional fuzzy-RD treatment variable.")
    parser.add_argument("--controls", default="")
    parser.add_argument("--bandwidth", type=float, default=None)
    parser.add_argument("--bandwidth-grid", default="", help="Comma-separated robustness bandwidths.")
    parser.add_argument("--order", type=int, default=1)
    parser.add_argument("--kernel", default="triangular", choices=["triangular", "epanechnikov", "uniform"])
    parser.add_argument("--cluster", default=None)
    parser.add_argument("--cov-type", default="HC3")
    parser.add_argument("--bins", type=int, default=40)
    parser.add_argument("--min-n", type=int, default=30)
    parser.add_argument("--no-figures", action="store_true")
    parser.add_argument("--formats", default="csv,xlsx,tex")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    print(json.dumps(run(args), indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
