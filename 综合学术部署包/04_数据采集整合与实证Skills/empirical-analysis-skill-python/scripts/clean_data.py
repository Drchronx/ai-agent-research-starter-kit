from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from common import DEFAULT_OUTPUT, add_common_io, ensure_dir, export_table, parse_cols, read_data, require_columns, write_data, write_json


def run(args: argparse.Namespace) -> dict[str, object]:
    df = read_data(args.input, args.sheet)
    outdir = ensure_dir(Path(args.report_dir or DEFAULT_OUTPUT / "tables"))
    original_shape = {"rows": int(df.shape[0]), "columns": int(df.shape[1])}

    if not args.no_trim_strings:
        for col in df.select_dtypes(include=["object", "string"]).columns:
            df[col] = df[col].astype("string").str.strip().str.replace(r"\s+", " ", regex=True)

    numeric_cols = parse_cols(args.numeric_cols)
    date_cols = parse_cols(args.date_cols)
    categorical_cols = parse_cols(args.categorical_cols)
    require_columns(df, numeric_cols + date_cols + categorical_cols, "coercion columns")

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    for col in categorical_cols:
        df[col] = df[col].astype("category")

    key_vars = parse_cols(args.key_vars)
    require_columns(df, key_vars, "key variables")
    dropped_key_missing = 0
    if args.drop_key_missing and key_vars:
        before = len(df)
        df = df.dropna(subset=key_vars)
        dropped_key_missing = before - len(df)

    missing = (
        df.isna()
        .agg(["sum", "mean"])
        .T.reset_index()
        .rename(columns={"index": "variable", "sum": "missing_n", "mean": "missing_rate"})
        .sort_values("missing_rate", ascending=False)
    )
    missing["missing_n"] = missing["missing_n"].astype(int)
    high_missing = missing.loc[missing["missing_rate"] > args.missing_threshold, "variable"].tolist()
    if args.drop_high_missing and high_missing:
        df = df.drop(columns=high_missing)

    dedupe_cols = parse_cols(args.dedupe_cols) or parse_cols(args.id_cols)
    require_columns(df, dedupe_cols, "dedupe columns")
    duplicate_rows = int(df.duplicated(subset=dedupe_cols).sum()) if dedupe_cols else int(df.duplicated().sum())
    if args.drop_duplicates:
        df = df.drop_duplicates(subset=dedupe_cols or None, keep="first")

    dtype_report = pd.DataFrame(
        [{"variable": col, "dtype": str(dtype), "n_unique": int(df[col].nunique(dropna=False))} for col, dtype in df.dtypes.items()]
    )
    export_table(missing, outdir / "missing_report", ["csv", "xlsx"])
    export_table(dtype_report, outdir / "dtype_report", ["csv", "xlsx"])

    sample_log = {
        "input": str(args.input),
        "output": str(args.output),
        "original_shape": original_shape,
        "final_shape": {"rows": int(df.shape[0]), "columns": int(df.shape[1])},
        "dropped_key_missing": int(dropped_key_missing),
        "duplicate_rows_detected": duplicate_rows,
        "dropped_high_missing_columns": high_missing if args.drop_high_missing else [],
        "numeric_coercions": numeric_cols,
        "date_coercions": date_cols,
        "categorical_coercions": categorical_cols,
    }
    write_json(sample_log, outdir / "sample_log.json")
    write_data(df, args.output)
    return sample_log


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Clean empirical raw data and write audit reports.")
    add_common_io(parser)
    parser.add_argument("--output", required=True)
    parser.add_argument("--report-dir", default=None)
    parser.add_argument("--id-cols", default="")
    parser.add_argument("--key-vars", default="")
    parser.add_argument("--numeric-cols", default="")
    parser.add_argument("--categorical-cols", default="")
    parser.add_argument("--date-cols", default="")
    parser.add_argument("--dedupe-cols", default="")
    parser.add_argument("--missing-threshold", type=float, default=1.0)
    parser.add_argument("--drop-key-missing", action="store_true")
    parser.add_argument("--drop-high-missing", action="store_true")
    parser.add_argument("--drop-duplicates", action="store_true")
    parser.add_argument("--no-trim-strings", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    print(json.dumps(run(args), indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
