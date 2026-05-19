from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from common import DEFAULT_OUTPUT, add_table_format_arg, export_table, parse_cols, read_data, write_json


def stars(pvalue: float) -> str:
    if not np.isfinite(pvalue):
        return ""
    if pvalue < 0.01:
        return "***"
    if pvalue < 0.05:
        return "**"
    if pvalue < 0.1:
        return "*"
    return ""


def format_tidy_regression(df: pd.DataFrame, digits: int) -> pd.DataFrame:
    required = {"model", "term", "coef", "se"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Input table is missing required columns: {sorted(missing)}")
    data = df.copy()
    data["stars"] = data["pvalue"].astype(float).map(stars) if "pvalue" in data.columns else ""
    data["estimate"] = data["coef"].astype(float).round(digits).astype(str) + data["stars"]
    data["stderr"] = "(" + data["se"].astype(float).round(digits).astype(str) + ")"
    rows = []
    for term, group in data.groupby("term", sort=False):
        coef_row = {"term": term}
        se_row = {"term": ""}
        for _, row in group.iterrows():
            coef_row[row["model"]] = row["estimate"]
            se_row[row["model"]] = row["stderr"]
        rows.extend([coef_row, se_row])
    return pd.DataFrame(rows)


def run(args: argparse.Namespace) -> dict[str, object]:
    df = read_data(args.input, args.sheet)
    outdir = Path(args.output_dir)
    if args.kind == "regression":
        table = format_tidy_regression(df, args.digits)
    elif args.kind == "wide":
        index = parse_cols(args.index)
        table = df.pivot_table(index=index, columns=args.columns, values=args.values, aggfunc="first").reset_index()
    else:
        table = df
    written = export_table(table, outdir / args.stem, parse_cols(args.formats))
    manifest = {"input": args.input, "kind": args.kind, "written": written}
    write_json(manifest, outdir / f"{args.stem}_manifest.json")
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Format empirical result tables.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--sheet", default=None)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT / "tables"))
    parser.add_argument("--kind", default="regression", choices=["regression", "wide", "copy"])
    parser.add_argument("--stem", default="formatted_table")
    parser.add_argument("--digits", type=int, default=3)
    parser.add_argument("--index", default="term")
    parser.add_argument("--columns", default="model")
    parser.add_argument("--values", default="coef")
    add_table_format_arg(parser)
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    print(json.dumps(run(args), indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
