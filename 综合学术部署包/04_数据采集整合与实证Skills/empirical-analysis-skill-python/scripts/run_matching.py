from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from common import DEFAULT_OUTPUT, add_common_io, export_table, import_matplotlib, parse_cols, read_data, require_columns, save_figure, write_json


def make_design(df: pd.DataFrame, controls: list[str]) -> pd.DataFrame:
    design = pd.get_dummies(df[controls], drop_first=True)
    return design.apply(pd.to_numeric, errors="coerce").astype(float)


def fit_propensity(design: pd.DataFrame, treatment: pd.Series, args: argparse.Namespace) -> np.ndarray:
    if args.propensity_model == "rf":
        from sklearn.ensemble import RandomForestClassifier

        model = RandomForestClassifier(n_estimators=args.n_estimators, max_depth=args.max_depth, random_state=args.random_state)
        model.fit(design, treatment)
        pscore = model.predict_proba(design)[:, 1]
    else:
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import make_pipeline
        from sklearn.preprocessing import StandardScaler

        model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=args.max_iter, random_state=args.random_state))
        model.fit(design, treatment)
        pscore = model.predict_proba(design)[:, 1]
    return np.clip(pscore, args.trim, 1.0 - args.trim)


def weighted_mean(values: pd.Series, weights: np.ndarray) -> float:
    weights = np.asarray(weights, dtype=float)
    return float(np.sum(values.to_numpy(dtype=float) * weights) / np.sum(weights))


def weighted_var(values: pd.Series, weights: np.ndarray) -> float:
    mean = weighted_mean(values, weights)
    weights = np.asarray(weights, dtype=float)
    return float(np.sum(weights * (values.to_numpy(dtype=float) - mean) ** 2) / np.sum(weights))


def smd_rows(design: pd.DataFrame, treatment: pd.Series, weights: np.ndarray | None, label: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    t = treatment.to_numpy(dtype=int)
    if weights is None:
        weights = np.ones(len(design))
    for col in design.columns:
        treated = design.loc[t == 1, col]
        control = design.loc[t == 0, col]
        wt = weights[t == 1]
        wc = weights[t == 0]
        mt = weighted_mean(treated, wt)
        mc = weighted_mean(control, wc)
        vt = weighted_var(treated, wt)
        vc = weighted_var(control, wc)
        pooled = np.sqrt((vt + vc) / 2.0)
        rows.append({"sample": label, "covariate": col, "smd": (mt - mc) / pooled if pooled > 0 else 0.0})
    return rows


def ipw_effect(df: pd.DataFrame, args: argparse.Namespace, pscore: np.ndarray) -> dict[str, Any]:
    y = pd.to_numeric(df[args.outcome], errors="coerce")
    t = pd.to_numeric(df[args.treatment], errors="coerce").to_numpy(dtype=int)
    if args.estimand == "att":
        weights = np.where(t == 1, 1.0, pscore / (1.0 - pscore))
    else:
        weights = np.where(t == 1, 1.0 / pscore, 1.0 / (1.0 - pscore))
    y1 = weighted_mean(y[t == 1], weights[t == 1])
    y0 = weighted_mean(y[t == 0], weights[t == 0])
    return {"method": f"ipw_{args.estimand}", "estimate": y1 - y0, "treated_mean": y1, "control_mean": y0, "nobs": len(df), "n_treated": int(t.sum())}


def nearest_neighbor_effect(df: pd.DataFrame, args: argparse.Namespace, pscore: np.ndarray) -> tuple[dict[str, Any], pd.DataFrame]:
    from sklearn.neighbors import NearestNeighbors

    y = pd.to_numeric(df[args.outcome], errors="coerce").to_numpy(dtype=float)
    t = pd.to_numeric(df[args.treatment], errors="coerce").to_numpy(dtype=int)
    treated_idx = np.where(t == 1)[0]
    control_idx = np.where(t == 0)[0]
    if len(treated_idx) == 0 or len(control_idx) == 0:
        raise ValueError("Matching requires both treated and control observations.")
    nn = NearestNeighbors(n_neighbors=args.neighbors)
    nn.fit(pscore[control_idx].reshape(-1, 1))
    distances, neighbors = nn.kneighbors(pscore[treated_idx].reshape(-1, 1))
    pairs: list[dict[str, Any]] = []
    effects: list[float] = []
    for row_pos, treated_pos in enumerate(treated_idx):
        matched_controls = control_idx[neighbors[row_pos]]
        if args.caliper is not None:
            keep = distances[row_pos] <= args.caliper
            matched_controls = matched_controls[keep]
        if len(matched_controls) == 0:
            continue
        matched_y = float(np.mean(y[matched_controls]))
        effect = float(y[treated_pos] - matched_y)
        effects.append(effect)
        pairs.append(
            {
                "treated_index": int(treated_pos),
                "control_indices": ",".join(str(int(idx)) for idx in matched_controls),
                "treated_pscore": float(pscore[treated_pos]),
                "matched_control_pscore_mean": float(np.mean(pscore[matched_controls])),
                "effect": effect,
            }
        )
    estimate = float(np.mean(effects)) if effects else np.nan
    se = float(np.std(effects, ddof=1) / np.sqrt(len(effects))) if len(effects) > 1 else np.nan
    row = {"method": "nearest_neighbor_att", "estimate": estimate, "se": se, "nobs": len(df), "n_treated_matched": len(effects)}
    return row, pd.DataFrame(pairs)


def love_plot(balance: pd.DataFrame, outdir: Path) -> list[str]:
    plt = import_matplotlib()
    pivot = balance.pivot_table(index="covariate", columns="sample", values="smd", aggfunc="first").fillna(0.0)
    pivot["max_abs"] = pivot.abs().max(axis=1)
    pivot = pivot.sort_values("max_abs")
    fig, ax = plt.subplots(figsize=(7.5, max(4.0, 0.28 * len(pivot))))
    for sample in pivot.columns.drop("max_abs"):
        ax.scatter(pivot[sample].abs(), np.arange(len(pivot)), label=sample, s=22)
    ax.axvline(0.1, color="gray", linestyle="--", linewidth=1)
    ax.set_yticks(np.arange(len(pivot)), labels=pivot.index)
    ax.set_xlabel("Absolute standardized mean difference")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False)
    fig.tight_layout()
    written = save_figure(fig, outdir / "fig_love_plot")
    plt.close(fig)
    return written


def run(args: argparse.Namespace) -> dict[str, Any]:
    df = read_data(args.input, args.sheet)
    controls = parse_cols(args.controls)
    require_columns(df, [args.outcome, args.treatment] + controls, "matching columns")
    before = len(df)
    df = df.dropna(subset=[args.outcome, args.treatment] + controls).copy()
    df[args.treatment] = pd.to_numeric(df[args.treatment], errors="coerce").astype(int)
    design = make_design(df, controls)
    pscore = fit_propensity(design, df[args.treatment], args)
    df["_pscore"] = pscore
    if args.common_support:
        lo = max(df.loc[df[args.treatment] == 1, "_pscore"].min(), df.loc[df[args.treatment] == 0, "_pscore"].min())
        hi = min(df.loc[df[args.treatment] == 1, "_pscore"].max(), df.loc[df[args.treatment] == 0, "_pscore"].max())
        df = df.loc[df["_pscore"].between(lo, hi)].copy()
        design = design.loc[df.index]
        pscore = df["_pscore"].to_numpy()

    rows: list[dict[str, Any]] = []
    matched_pairs = pd.DataFrame()
    if args.method in {"ipw", "both"}:
        rows.append(ipw_effect(df, args, pscore))
    if args.method in {"matching", "both"}:
        match_row, matched_pairs = nearest_neighbor_effect(df, args, pscore)
        rows.append(match_row)

    t = df[args.treatment]
    if args.estimand == "att":
        weights = np.where(t.to_numpy(dtype=int) == 1, 1.0, pscore / (1.0 - pscore))
    else:
        weights = np.where(t.to_numpy(dtype=int) == 1, 1.0 / pscore, 1.0 / (1.0 - pscore))
    balance = pd.DataFrame(smd_rows(design, t, None, "raw") + smd_rows(design, t, weights, "weighted")).round(6)

    outdir = Path(args.output_dir)
    written: list[str] = []
    written += export_table(pd.DataFrame(rows).round(6), outdir / "matching_effects", parse_cols(args.formats))
    written += export_table(df.drop(columns=[]), outdir / "propensity_scores", ["csv"])
    written += export_table(balance, outdir / "balance_smd", parse_cols(args.formats))
    if not matched_pairs.empty:
        written += export_table(matched_pairs.round(6), outdir / "matched_pairs", ["csv"])
    figure_files: list[str] = []
    if not args.no_figures:
        figure_files = love_plot(balance, outdir)

    manifest = {
        "input": str(args.input),
        "output_dir": str(outdir),
        "method": args.method,
        "estimand": args.estimand,
        "controls": controls,
        "propensity_model": args.propensity_model,
        "dropped_missing_rows": int(before - len(df)),
        "files": {"tables": written, "figures": figure_files, "manifest": str(outdir / "matching_manifest.json")},
    }
    write_json(manifest, outdir / "matching_manifest.json")
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run propensity-score IPW and nearest-neighbor matching.")
    add_common_io(parser)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT / "matching"))
    parser.add_argument("--outcome", required=True)
    parser.add_argument("--treatment", required=True)
    parser.add_argument("--controls", required=True)
    parser.add_argument("--method", default="both", choices=["ipw", "matching", "both"])
    parser.add_argument("--estimand", default="att", choices=["att", "ate"])
    parser.add_argument("--propensity-model", default="logit", choices=["logit", "rf"])
    parser.add_argument("--neighbors", type=int, default=1)
    parser.add_argument("--caliper", type=float, default=None)
    parser.add_argument("--trim", type=float, default=0.01)
    parser.add_argument("--common-support", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--n-estimators", type=int, default=300)
    parser.add_argument("--max-depth", type=int, default=4)
    parser.add_argument("--max-iter", type=int, default=5000)
    parser.add_argument("--random-state", type=int, default=2025)
    parser.add_argument("--no-figures", action="store_true")
    parser.add_argument("--formats", default="csv,xlsx,tex")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    print(json.dumps(run(args), indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
