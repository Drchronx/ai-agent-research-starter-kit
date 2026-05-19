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


def build_regressor(args: argparse.Namespace) -> Any:
    if args.learner == "gbr":
        from sklearn.ensemble import GradientBoostingRegressor

        return GradientBoostingRegressor(n_estimators=args.n_estimators, max_depth=args.max_depth, random_state=args.random_state)
    from sklearn.ensemble import RandomForestRegressor

    return RandomForestRegressor(n_estimators=args.n_estimators, max_depth=args.max_depth, min_samples_leaf=args.min_samples_leaf, random_state=args.random_state)


def t_learner(y: np.ndarray, t: np.ndarray, x: pd.DataFrame, args: argparse.Namespace) -> np.ndarray:
    if t.sum() == 0 or (1 - t).sum() == 0:
        raise ValueError("T-learner requires treated and control observations.")
    model_treated = build_regressor(args)
    model_control = build_regressor(args)
    model_treated.fit(x.loc[t == 1], y[t == 1])
    model_control.fit(x.loc[t == 0], y[t == 0])
    return model_treated.predict(x) - model_control.predict(x)


def s_learner(y: np.ndarray, t: np.ndarray, x: pd.DataFrame, args: argparse.Namespace) -> np.ndarray:
    model = build_regressor(args)
    xt = x.copy()
    xt["_treatment"] = t
    model.fit(xt, y)
    x1 = x.copy()
    x1["_treatment"] = 1
    x0 = x.copy()
    x0["_treatment"] = 0
    return model.predict(x1) - model.predict(x0)


def causal_forest(y: np.ndarray, t: np.ndarray, x: pd.DataFrame, args: argparse.Namespace) -> np.ndarray:
    try:
        from econml.dml import CausalForestDML
        from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
    except ImportError as exc:
        raise RuntimeError("Install econml to run causal_forest. Use --method tlearner for the fixed sklearn fallback.") from exc
    model_y = RandomForestRegressor(n_estimators=args.n_estimators, max_depth=args.max_depth, min_samples_leaf=args.min_samples_leaf, random_state=args.random_state)
    model_t = RandomForestClassifier(n_estimators=args.n_estimators, max_depth=args.max_depth, min_samples_leaf=args.min_samples_leaf, random_state=args.random_state)
    forest = CausalForestDML(
        model_y=model_y,
        model_t=model_t,
        discrete_treatment=True,
        n_estimators=args.n_estimators,
        min_samples_leaf=args.min_samples_leaf,
        random_state=args.random_state,
    )
    forest.fit(y, t, X=x.to_numpy(dtype=float))
    return np.asarray(forest.effect(x.to_numpy(dtype=float)), dtype=float)


def summarize_cate(df: pd.DataFrame, cate: np.ndarray, modifiers: list[str]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = [
        {"group": "overall", "modifier": "", "level": "all", "nobs": len(cate), "cate_mean": float(np.mean(cate)), "cate_sd": float(np.std(cate, ddof=1)), "cate_p10": float(np.quantile(cate, 0.10)), "cate_p50": float(np.quantile(cate, 0.50)), "cate_p90": float(np.quantile(cate, 0.90))}
    ]
    temp = df.copy()
    temp["_cate"] = cate
    for modifier in modifiers:
        if pd.api.types.is_numeric_dtype(temp[modifier]):
            levels = pd.qcut(temp[modifier], q=min(4, temp[modifier].nunique()), duplicates="drop")
        else:
            levels = temp[modifier].astype(str)
        for level, data in temp.groupby(levels, observed=True):
            rows.append({"group": f"{modifier}={level}", "modifier": modifier, "level": str(level), "nobs": len(data), "cate_mean": float(data["_cate"].mean()), "cate_sd": float(data["_cate"].std(ddof=1))})
    return pd.DataFrame(rows)


def cate_plot(cate: np.ndarray, outdir: Path) -> list[str]:
    plt = import_matplotlib()
    fig, ax = plt.subplots(figsize=(7.5, 5.0))
    ax.hist(cate, bins=30, color="#4C78A8", alpha=0.85)
    ax.axvline(np.mean(cate), color="black", linestyle="--", linewidth=1, label="Mean CATE")
    ax.set_xlabel("Estimated CATE")
    ax.set_ylabel("Count")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False)
    fig.tight_layout()
    written = save_figure(fig, outdir / "fig_cate_distribution")
    plt.close(fig)
    return written


def run(args: argparse.Namespace) -> dict[str, Any]:
    df = read_data(args.input, args.sheet)
    controls = parse_cols(args.controls)
    modifiers = parse_cols(args.effect_modifiers)
    require_columns(df, [args.outcome, args.treatment] + controls + modifiers, "CATE columns")
    before = len(df)
    df = df.dropna(subset=[args.outcome, args.treatment] + controls + modifiers).copy()
    y = pd.to_numeric(df[args.outcome], errors="coerce").to_numpy(dtype=float)
    t = pd.to_numeric(df[args.treatment], errors="coerce").astype(int).to_numpy()
    x = make_design(df, controls)

    actual_method = args.method
    if args.method == "tlearner":
        cate = t_learner(y, t, x, args)
    elif args.method == "slearner":
        cate = s_learner(y, t, x, args)
    elif args.method == "causal_forest":
        cate = causal_forest(y, t, x, args)
    else:
        raise ValueError(f"Unsupported method: {args.method}")

    predictions = df[[args.outcome, args.treatment] + controls + modifiers].copy()
    predictions["_cate"] = cate
    summary = summarize_cate(df, cate, modifiers).round(6)
    outdir = Path(args.output_dir)
    written: list[str] = []
    written += export_table(predictions.round(6), outdir / "cate_predictions", ["csv"])
    written += export_table(summary, outdir / "cate_summary", parse_cols(args.formats))
    figure_files: list[str] = []
    if not args.no_figures:
        figure_files = cate_plot(cate, outdir)
    manifest = {
        "input": str(args.input),
        "output_dir": str(outdir),
        "method": actual_method,
        "learner": args.learner,
        "controls": controls,
        "effect_modifiers": modifiers,
        "dropped_missing_rows": int(before - len(df)),
        "files": {"tables": written, "figures": figure_files, "manifest": str(outdir / "cate_manifest.json")},
    }
    write_json(manifest, outdir / "cate_manifest.json")
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run CATE estimation with fixed T-learner, S-learner, or econml causal forest.")
    add_common_io(parser)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT / "cate"))
    parser.add_argument("--outcome", required=True)
    parser.add_argument("--treatment", required=True)
    parser.add_argument("--controls", required=True)
    parser.add_argument("--effect-modifiers", default="")
    parser.add_argument("--method", default="tlearner", choices=["tlearner", "slearner", "causal_forest"])
    parser.add_argument("--learner", default="rf", choices=["rf", "gbr"])
    parser.add_argument("--n-estimators", type=int, default=300)
    parser.add_argument("--max-depth", type=int, default=5)
    parser.add_argument("--min-samples-leaf", type=int, default=5)
    parser.add_argument("--random-state", type=int, default=2025)
    parser.add_argument("--no-figures", action="store_true")
    parser.add_argument("--formats", default="csv,xlsx,tex")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    print(json.dumps(run(args), indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
