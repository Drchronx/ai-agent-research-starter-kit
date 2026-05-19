from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from common import DEFAULT_OUTPUT, add_common_io, add_table_format_arg, export_table, parse_cols, read_data, require_columns, write_json
from model_utils import build_formula, fit_model, fit_result_rows


def run(args: argparse.Namespace) -> dict[str, object]:
    df = read_data(args.input, args.sheet)
    outdir = Path(args.output_dir)
    controls = parse_cols(args.controls)
    fixed_effects = parse_cols(args.fixed_effects)
    require_columns(df, [args.outcome, args.treatment] + controls + fixed_effects, "further-analysis columns")

    written: list[str] = []
    hetero_rows: list[dict[str, object]] = []
    for var in parse_cols(args.heterogeneity_vars):
        require_columns(df, [var])
        formula = build_formula(args.outcome, f"{args.treatment}*{var}", controls, fixed_effects)
        fitted = fit_model(df, formula, args.model_type, args.cluster, args.cov_type, f"interaction_{var}")
        hetero_rows.extend(fit_result_rows(fitted, [args.treatment, f"{args.treatment}:{var}", f"{var}:{args.treatment}"]))
    if hetero_rows:
        written += export_table(pd.DataFrame(hetero_rows).round(6), outdir / "table4_heterogeneity", parse_cols(args.formats))

    mechanism_rows: list[dict[str, object]] = []
    for outcome in parse_cols(args.mechanism_outcomes):
        require_columns(df, [outcome])
        formula = build_formula(outcome, args.treatment, controls, fixed_effects)
        fitted = fit_model(df, formula, args.model_type, args.cluster, args.cov_type, f"outcome_{outcome}")
        mechanism_rows.extend(fit_result_rows(fitted, [args.treatment]))
    if mechanism_rows:
        written += export_table(pd.DataFrame(mechanism_rows).round(6), outdir / "table3_mechanism", parse_cols(args.formats))

    mediation_rows: list[dict[str, object]] = []
    for mediator in parse_cols(args.mediators):
        require_columns(df, [mediator])
        m_formula = build_formula(mediator, args.treatment, controls, fixed_effects)
        y_formula = build_formula(args.outcome, args.treatment, [mediator] + controls, fixed_effects)
        m_fit = fit_model(df, m_formula, "ols", args.cluster, args.cov_type, f"mediator_{mediator}")
        y_fit = fit_model(df, y_formula, "ols", args.cluster, args.cov_type, f"outcome_with_{mediator}")
        b = float(m_fit.params.get(args.treatment, np.nan))
        d = float(y_fit.params.get(mediator, np.nan))
        mediation_rows.append(
            {
                "mediator": mediator,
                "treat_to_mediator": b,
                "mediator_to_outcome": d,
                "indirect_effect_product": b * d if np.isfinite(b) and np.isfinite(d) else np.nan,
                "direct_effect": float(y_fit.params.get(args.treatment, np.nan)),
                "m_formula": m_formula,
                "y_formula": y_formula,
            }
        )
    if mediation_rows:
        written += export_table(pd.DataFrame(mediation_rows).round(6), outdir / "mediation_baron_kenny", parse_cols(args.formats))

    manifest = {"written": written}
    write_json(manifest, outdir / "further_manifest.json")
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run mechanism, heterogeneity, and simple mediation analyses.")
    add_common_io(parser)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT / "tables"))
    parser.add_argument("--outcome", required=True)
    parser.add_argument("--treatment", required=True)
    parser.add_argument("--controls", default="")
    parser.add_argument("--fixed-effects", default="")
    parser.add_argument("--cluster", default=None)
    parser.add_argument("--cov-type", default="HC3")
    parser.add_argument("--model-type", default="ols", choices=["ols", "logit", "probit", "poisson"])
    parser.add_argument("--heterogeneity-vars", default="")
    parser.add_argument("--mechanism-outcomes", default="")
    parser.add_argument("--mediators", default="")
    add_table_format_arg(parser)
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    print(json.dumps(run(args), indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
