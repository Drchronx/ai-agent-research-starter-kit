from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from common import DEFAULT_OUTPUT, export_table, parse_cols, read_data, require_columns, write_json
from model_utils import build_formula, fit_model


def e_value(effect: float) -> float:
    rr = effect if effect >= 1 else 1.0 / effect
    return float(rr + np.sqrt(rr * (rr - 1.0))) if rr >= 1 else np.nan


def run_evalue(args: argparse.Namespace) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if args.effect_rr:
        rows.append({"method": "e_value", "term": "point_estimate", "estimate": args.effect_rr, "sensitivity_value": e_value(args.effect_rr)})
    if args.ci_low:
        rows.append({"method": "e_value", "term": "ci_low", "estimate": args.ci_low, "sensitivity_value": e_value(args.ci_low)})
    if args.ci_high:
        rows.append({"method": "e_value", "term": "ci_high", "estimate": args.ci_high, "sensitivity_value": e_value(args.ci_high)})
    return rows


def run_oster(df: pd.DataFrame, args: argparse.Namespace) -> list[dict[str, Any]]:
    restricted_controls = parse_cols(args.restricted_controls)
    full_controls = parse_cols(args.controls)
    fixed_effects = parse_cols(args.fixed_effects)
    require_columns(df, [args.outcome, args.treatment] + restricted_controls + full_controls + fixed_effects, "Oster columns")
    restricted_formula = args.restricted_formula or build_formula(args.outcome, args.treatment, restricted_controls, fixed_effects)
    full_formula = args.formula or build_formula(args.outcome, args.treatment, full_controls, fixed_effects)
    restricted = fit_model(df, restricted_formula, "ols", args.cluster, args.cov_type, "restricted")
    full = fit_model(df, full_formula, "ols", args.cluster, args.cov_type, "full")
    beta_restricted = float(restricted.params.get(args.treatment, np.nan))
    beta_full = float(full.params.get(args.treatment, np.nan))
    r_restricted = float(restricted.rsquared or np.nan)
    r_full = float(full.rsquared or np.nan)
    rmax = args.rmax if args.rmax is not None else min(1.0, 1.3 * r_full)
    numerator = (beta_full - args.target_beta) * (r_full - r_restricted)
    denominator = (beta_restricted - beta_full) * (rmax - r_full)
    delta = numerator / denominator if abs(denominator) > 1e-12 else np.nan
    return [
        {
            "method": "oster_delta",
            "term": args.treatment,
            "estimate": delta,
            "beta_restricted": beta_restricted,
            "beta_full": beta_full,
            "r2_restricted": r_restricted,
            "r2_full": r_full,
            "rmax": rmax,
            "target_beta": args.target_beta,
            "restricted_formula": restricted_formula,
            "full_formula": full_formula,
        }
    ]


def run_randomization(df: pd.DataFrame, args: argparse.Namespace, outdir: Path) -> tuple[list[dict[str, Any]], str | None]:
    controls = parse_cols(args.controls)
    fixed_effects = parse_cols(args.fixed_effects)
    require_columns(df, [args.outcome, args.treatment] + controls + fixed_effects, "randomization-inference columns")
    formula = args.formula or build_formula(args.outcome, args.treatment, controls, fixed_effects)
    actual = fit_model(df, formula, args.model_type, args.cluster, args.cov_type, "actual")
    actual_coef = float(actual.params.get(args.treatment, np.nan))
    rng = np.random.default_rng(args.random_state)
    permuted_rows: list[dict[str, Any]] = []
    values = df[args.treatment].to_numpy().copy()
    for idx in range(args.permutations):
        shuffled = df.copy()
        shuffled[args.treatment] = rng.permutation(values)
        try:
            fitted = fit_model(shuffled, formula, args.model_type, args.cluster, args.cov_type, f"perm_{idx + 1}")
            coef = float(fitted.params.get(args.treatment, np.nan))
            permuted_rows.append({"iteration": idx + 1, "coef": coef})
        except Exception as exc:
            permuted_rows.append({"iteration": idx + 1, "coef": np.nan, "error": str(exc)})
    distribution = pd.DataFrame(permuted_rows)
    valid = distribution["coef"].dropna()
    pvalue = float((np.abs(valid) >= abs(actual_coef)).mean()) if len(valid) else np.nan
    path = outdir / "randomization_distribution.csv"
    export_table(distribution.round(6), outdir / "randomization_distribution", ["csv"])
    row = {"method": "randomization_inference", "term": args.treatment, "estimate": actual_coef, "pvalue": pvalue, "permutations": args.permutations, "valid_permutations": int(len(valid)), "formula": formula}
    return [row], str(path)


def run(args: argparse.Namespace) -> dict[str, Any]:
    modes = parse_cols(args.modes)
    outdir = Path(args.output_dir)
    rows: list[dict[str, Any]] = []
    extra_files: list[str] = []
    df: pd.DataFrame | None = None
    if any(mode in {"oster", "randomization"} for mode in modes):
        if not args.input:
            raise ValueError("--input is required for Oster or randomization inference.")
        df = read_data(args.input, args.sheet).dropna().copy()
    if "evalue" in modes:
        rows.extend(run_evalue(args))
    if "oster" in modes:
        assert df is not None
        rows.extend(run_oster(df, args))
    if "randomization" in modes:
        assert df is not None
        random_rows, distribution_file = run_randomization(df, args, outdir)
        rows.extend(random_rows)
        if distribution_file:
            extra_files.append(distribution_file)

    results = pd.DataFrame(rows).round(6)
    written = export_table(results, outdir / "sensitivity_results", parse_cols(args.formats)) + extra_files
    manifest = {
        "input": str(args.input) if args.input else None,
        "output_dir": str(outdir),
        "modes": modes,
        "files": {"tables": written, "manifest": str(outdir / "sensitivity_manifest.json")},
    }
    write_json(manifest, outdir / "sensitivity_manifest.json")
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run fixed sensitivity analyses: E-value, Oster delta, and randomization inference.")
    parser.add_argument("--input", default=None)
    parser.add_argument("--sheet", default=None)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT / "sensitivity"))
    parser.add_argument("--modes", default="oster", help="Comma-separated: oster,evalue,randomization.")
    parser.add_argument("--outcome", default=None)
    parser.add_argument("--treatment", default=None)
    parser.add_argument("--controls", default="")
    parser.add_argument("--restricted-controls", default="")
    parser.add_argument("--fixed-effects", default="")
    parser.add_argument("--formula", default=None)
    parser.add_argument("--restricted-formula", default=None)
    parser.add_argument("--cluster", default=None)
    parser.add_argument("--cov-type", default="HC3")
    parser.add_argument("--model-type", default="ols", choices=["ols", "logit", "probit", "poisson"])
    parser.add_argument("--rmax", type=float, default=None)
    parser.add_argument("--target-beta", type=float, default=0.0)
    parser.add_argument("--effect-rr", type=float, default=None)
    parser.add_argument("--ci-low", type=float, default=None)
    parser.add_argument("--ci-high", type=float, default=None)
    parser.add_argument("--permutations", type=int, default=500)
    parser.add_argument("--random-state", type=int, default=2025)
    parser.add_argument("--formats", default="csv,xlsx,tex")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    print(json.dumps(run(args), indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
