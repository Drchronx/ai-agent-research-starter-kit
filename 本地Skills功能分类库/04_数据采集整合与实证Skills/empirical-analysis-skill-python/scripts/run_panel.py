from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from common import DEFAULT_OUTPUT, add_common_io, add_table_format_arg, export_table, parse_cols, read_data, require_columns, write_json
from model_utils import fit_model, fit_result_rows


def build_panel_formula(outcome: str, rhs: list[str], entity: str | None, time: str | None, entity_fe: bool, time_fe: bool) -> str:
    terms = list(rhs)
    if entity_fe and entity:
        terms.append(f"C({entity})")
    if time_fe and time:
        terms.append(f"C({time})")
    return f"{outcome} ~ {' + '.join(terms) if terms else '1'}"


def run_statsmodels_panel(df: pd.DataFrame, args: argparse.Namespace, method: str) -> Any:
    rhs = [args.treatment] + parse_cols(args.controls)
    if method == "fe":
        formula = build_panel_formula(args.outcome, rhs, args.entity, args.time, True, False)
        return fit_model(df, formula, "ols", args.cluster or args.entity, args.cov_type, "entity_fe")
    if method == "twfe":
        formula = build_panel_formula(args.outcome, rhs, args.entity, args.time, True, True)
        return fit_model(df, formula, "ols", args.cluster or args.entity, args.cov_type, "two_way_fe")
    if method == "between":
        cols = [args.outcome] + rhs
        between = df[[args.entity] + cols].groupby(args.entity, as_index=False).mean(numeric_only=True)
        formula = f"{args.outcome} ~ {' + '.join(rhs)}"
        return fit_model(between, formula, "ols", None, args.cov_type, "between")
    if method == "fd":
        cols = [args.outcome] + rhs
        data = df[[args.entity, args.time] + cols].sort_values([args.entity, args.time]).copy()
        diffed = data.groupby(args.entity)[cols].diff().dropna()
        formula = f"{args.outcome} ~ {' + '.join(rhs)} - 1"
        return fit_model(diffed, formula, "ols", None, args.cov_type, "first_difference")
    raise ValueError(f"Unsupported panel method: {method}")


def run_random_effects(df: pd.DataFrame, args: argparse.Namespace) -> dict[str, Any]:
    try:
        from linearmodels.panel import RandomEffects
    except ImportError as exc:
        raise RuntimeError("Install linearmodels to run random effects.") from exc
    rhs = [args.treatment] + parse_cols(args.controls)
    data = df.set_index([args.entity, args.time])
    formula = f"{args.outcome} ~ 1 + {' + '.join(rhs)}"
    result = RandomEffects.from_formula(formula, data=data).fit(cov_type="clustered", cluster_entity=True)
    return {
        "name": "random_effects",
        "formula": formula,
        "params": result.params,
        "bse": result.std_errors,
        "pvalues": result.pvalues,
        "nobs": float(result.nobs),
        "rsquared": float(result.rsquared) if result.rsquared is not None else np.nan,
        "text_summary": str(result.summary),
    }


def result_rows(result: Any, keep_terms: list[str]) -> list[dict[str, Any]]:
    if hasattr(result, "params"):
        return fit_result_rows(result, keep_terms or None)
    rows = []
    terms = keep_terms or list(result["params"].index)
    for term in terms:
        if term in result["params"].index:
            rows.append(
                {
                    "model": result["name"],
                    "term": term,
                    "coef": float(result["params"][term]),
                    "se": float(result["bse"][term]),
                    "pvalue": float(result["pvalues"][term]),
                    "nobs": result["nobs"],
                    "rsquared": result["rsquared"],
                    "formula": result["formula"],
                }
            )
    return rows


def run(args: argparse.Namespace) -> dict[str, Any]:
    df = read_data(args.input, args.sheet)
    controls = parse_cols(args.controls)
    required = [args.outcome, args.treatment, args.entity, args.time] + controls
    if args.cluster:
        required.append(args.cluster)
    require_columns(df, required, "panel columns")

    methods = parse_cols(args.methods)
    keep_terms = parse_cols(args.keep_terms) or [args.treatment]
    rows: list[dict[str, Any]] = []
    summaries: list[str] = []
    for method in methods:
        if method == "re":
            result = run_random_effects(df, args)
            rows.extend(result_rows(result, keep_terms))
            summaries.append(f"[random_effects]\n{result['text_summary']}")
        else:
            result = run_statsmodels_panel(df, args, method)
            rows.extend(result_rows(result, keep_terms))
            summaries.append(f"[{result.name}] {result.formula}\n{result.text_summary}")

    outdir = Path(args.output_dir)
    export_table(pd.DataFrame(rows).round(6), outdir / "panel_results", parse_cols(args.formats))
    summary_path = outdir / "panel_summaries.txt"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text("\n\n".join(summaries), encoding="utf-8")
    manifest = {"methods": methods, "output_dir": str(outdir), "summary": str(summary_path)}
    write_json(manifest, outdir / "panel_manifest.json")
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run fixed panel estimators.")
    add_common_io(parser)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT / "tables"))
    parser.add_argument("--outcome", required=True)
    parser.add_argument("--treatment", required=True)
    parser.add_argument("--controls", default="")
    parser.add_argument("--entity", required=True)
    parser.add_argument("--time", required=True)
    parser.add_argument("--methods", default="twfe", help="Comma-separated: fe,twfe,between,fd,re.")
    parser.add_argument("--cluster", default=None)
    parser.add_argument("--cov-type", default="HC3")
    parser.add_argument("--keep-terms", default="")
    add_table_format_arg(parser)
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    print(json.dumps(run(args), indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
