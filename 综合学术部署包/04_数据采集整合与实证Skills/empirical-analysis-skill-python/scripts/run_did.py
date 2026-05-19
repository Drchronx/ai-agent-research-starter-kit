from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd

from common import DEFAULT_OUTPUT, add_common_io, add_table_format_arg, export_table, parse_cols, read_data, require_columns, write_json
from model_utils import fit_model, fit_result_rows


def safe_event_name(k: Any) -> str:
    value = float(k)
    text = str(int(value)) if value.is_integer() else str(value).replace(".", "_")
    return "event_m" + text[1:] if text.startswith("-") else "event_p" + text


def run_twfe(df: pd.DataFrame, args: argparse.Namespace) -> tuple[list[dict[str, Any]], str, str]:
    controls = parse_cols(args.controls)
    require_columns(df, [args.outcome, args.treated, args.post, args.entity, args.time] + controls, "DID columns")
    formula = f"{args.outcome} ~ {args.treated} * {args.post}"
    if controls:
        formula += " + " + " + ".join(controls)
    formula += f" + C({args.entity}) + C({args.time})"
    result = fit_model(df, formula, "ols", args.cluster or args.entity, args.cov_type, "twfe_did")
    terms = parse_cols(args.keep_terms) or [f"{args.treated}:{args.post}", f"{args.post}:{args.treated}"]
    return fit_result_rows(result, terms), formula, result.text_summary


def run_event_study(df: pd.DataFrame, args: argparse.Namespace) -> tuple[list[dict[str, Any]], str, str, dict[str, Any]]:
    controls = parse_cols(args.controls)
    require_columns(df, [args.outcome, args.treated, args.rel_time, args.entity, args.time] + controls, "event-study columns")
    data = df.copy()
    rel_values = sorted(v for v in data[args.rel_time].dropna().unique() if float(v) != args.ref_period)
    event_cols = []
    event_map = {}
    for k in rel_values:
        name = safe_event_name(k)
        data[name] = ((data[args.rel_time] == k) & (data[args.treated] == 1)).astype(int)
        event_cols.append(name)
        event_map[name] = float(k)
    formula = f"{args.outcome} ~ {' + '.join(event_cols)}"
    if controls:
        formula += " + " + " + ".join(controls)
    formula += f" + C({args.entity}) + C({args.time})"
    result = fit_model(data, formula, "ols", args.cluster or args.entity, args.cov_type, "event_study")
    rows = fit_result_rows(result, event_cols)
    for row in rows:
        row["rel_time"] = event_map.get(row["term"])

    pre_cols = [col for col, rel in event_map.items() if rel < args.ref_period]
    pretrend: dict[str, Any] = {"tested_terms": pre_cols}
    if pre_cols:
        import statsmodels.formula.api as smf

        fitted = smf.ols(formula, data=data).fit(cov_type="cluster", cov_kwds={"groups": data[args.cluster or args.entity]})
        try:
            test = fitted.f_test(" = 0, ".join(pre_cols) + " = 0")
            pretrend.update({"statistic": float(test.fvalue), "pvalue": float(test.pvalue)})
        except Exception as exc:
            pretrend.update({"error": str(exc)})
    return rows, formula, result.text_summary, pretrend


def run(args: argparse.Namespace) -> dict[str, Any]:
    df = read_data(args.input, args.sheet)
    outdir = Path(args.output_dir)
    rows: list[dict[str, Any]] = []
    summaries: list[str] = []
    formulas: dict[str, str] = {}
    pretrend: dict[str, Any] = {}

    if args.mode in {"twfe", "both"}:
        twfe_rows, formula, summary = run_twfe(df, args)
        rows.extend(twfe_rows)
        formulas["twfe"] = formula
        summaries.append(f"[twfe_did] {formula}\n{summary}")
    if args.mode in {"event", "both"}:
        event_rows, formula, summary, pretrend = run_event_study(df, args)
        rows.extend(event_rows)
        formulas["event_study"] = formula
        summaries.append(f"[event_study] {formula}\n{summary}")

    export_table(pd.DataFrame(rows).round(6), outdir / "did_results", parse_cols(args.formats))
    summary_path = outdir / "did_summaries.txt"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text("\n\n".join(summaries), encoding="utf-8")
    manifest = {"mode": args.mode, "formulas": formulas, "pretrend": pretrend, "summary": str(summary_path)}
    write_json(manifest, outdir / "did_manifest.json")
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run fixed DID and event-study specifications.")
    add_common_io(parser)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT / "tables"))
    parser.add_argument("--outcome", required=True)
    parser.add_argument("--treated", required=True)
    parser.add_argument("--post", default=None)
    parser.add_argument("--rel-time", default=None)
    parser.add_argument("--ref-period", type=float, default=-1)
    parser.add_argument("--entity", required=True)
    parser.add_argument("--time", required=True)
    parser.add_argument("--controls", default="")
    parser.add_argument("--cluster", default=None)
    parser.add_argument("--cov-type", default="HC3")
    parser.add_argument("--mode", default="twfe", choices=["twfe", "event", "both"])
    parser.add_argument("--keep-terms", default="")
    add_table_format_arg(parser)
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    if args.mode in {"twfe", "both"} and not args.post:
        raise ValueError("--post is required for twfe DID.")
    if args.mode in {"event", "both"} and not args.rel_time:
        raise ValueError("--rel-time is required for event-study DID.")
    print(json.dumps(run(args), indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
