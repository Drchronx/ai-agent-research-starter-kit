from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from common import DEFAULT_OUTPUT, add_common_io, parse_cols, read_data, require_columns, write_data, write_json


def run(args: argparse.Namespace) -> dict[str, object]:
    df = read_data(args.input, args.sheet)
    log: dict[str, object] = {"input": str(args.input), "output": str(args.output), "created_columns": []}
    created: list[str] = log["created_columns"]  # type: ignore[assignment]

    for col in parse_cols(args.log_cols):
        require_columns(df, [col])
        new_col = f"log_{col}"
        values = pd.to_numeric(df[col], errors="coerce")
        df[new_col] = np.where(values > 0, np.log(values), np.nan)
        created.append(new_col)

    for col in parse_cols(args.ihs_cols):
        require_columns(df, [col])
        new_col = f"ihs_{col}"
        df[new_col] = np.arcsinh(pd.to_numeric(df[col], errors="coerce"))
        created.append(new_col)

    for col in parse_cols(args.winsorize_cols):
        require_columns(df, [col])
        values = pd.to_numeric(df[col], errors="coerce")
        lo = values.quantile(args.winsor_lower)
        hi = values.quantile(args.winsor_upper)
        new_col = f"{col}_w"
        df[new_col] = values.clip(lo, hi)
        created.append(new_col)
        log.setdefault("winsor_limits", {})[col] = {"lower": float(lo), "upper": float(hi)}  # type: ignore[index]

    for col in parse_cols(args.standardize_cols):
        require_columns(df, [col])
        values = pd.to_numeric(df[col], errors="coerce")
        sd = values.std(ddof=0)
        new_col = f"{col}_z"
        df[new_col] = (values - values.mean()) / sd if sd and np.isfinite(sd) else np.nan
        created.append(new_col)

    dummy_cols = parse_cols(args.dummy_cols)
    require_columns(df, dummy_cols, "dummy columns")
    for col in dummy_cols:
        dummies = pd.get_dummies(df[col], prefix=col, dummy_na=args.dummy_na, drop_first=args.drop_first_dummy)
        df = pd.concat([df, dummies.astype(int)], axis=1)
        created.extend(list(dummies.columns))

    panel_ops = parse_cols(args.lag_cols) + parse_cols(args.lead_cols) + parse_cols(args.diff_cols)
    require_columns(df, panel_ops, "panel operator columns")
    if panel_ops:
        require_columns(df, [args.panel_id, args.time_col], "panel id/time columns")
        df = df.sort_values([args.panel_id, args.time_col]).copy()
        grouped = df.groupby(args.panel_id, sort=False)
        for col in parse_cols(args.lag_cols):
            new_col = f"{col}_lag{args.periods}"
            df[new_col] = grouped[col].shift(args.periods)
            created.append(new_col)
        for col in parse_cols(args.lead_cols):
            new_col = f"{col}_lead{args.periods}"
            df[new_col] = grouped[col].shift(-args.periods)
            created.append(new_col)
        for col in parse_cols(args.diff_cols):
            new_col = f"{col}_diff{args.periods}"
            df[new_col] = grouped[col].diff(args.periods)
            created.append(new_col)

    if args.treat_start_col:
        require_columns(df, [args.treat_start_col, args.time_col], "treatment timing columns")
        df[args.rel_time_name] = pd.to_numeric(df[args.time_col], errors="coerce") - pd.to_numeric(df[args.treat_start_col], errors="coerce")
        df[args.post_name] = (df[args.rel_time_name] >= 0).astype(int)
        created.extend([args.rel_time_name, args.post_name])

    write_data(df, args.output)
    write_json(log, Path(args.report_dir or DEFAULT_OUTPUT / "tables") / "transform_log.json")
    return log


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create deterministic empirical analysis variables.")
    add_common_io(parser)
    parser.add_argument("--output", required=True)
    parser.add_argument("--report-dir", default=None)
    parser.add_argument("--log-cols", default="")
    parser.add_argument("--ihs-cols", default="")
    parser.add_argument("--winsorize-cols", default="")
    parser.add_argument("--winsor-lower", type=float, default=0.01)
    parser.add_argument("--winsor-upper", type=float, default=0.99)
    parser.add_argument("--standardize-cols", default="")
    parser.add_argument("--dummy-cols", default="")
    parser.add_argument("--dummy-na", action="store_true")
    parser.add_argument("--drop-first-dummy", action="store_true")
    parser.add_argument("--panel-id", default=None)
    parser.add_argument("--time-col", default=None)
    parser.add_argument("--lag-cols", default="")
    parser.add_argument("--lead-cols", default="")
    parser.add_argument("--diff-cols", default="")
    parser.add_argument("--periods", type=int, default=1)
    parser.add_argument("--treat-start-col", default=None)
    parser.add_argument("--rel-time-name", default="rel_time")
    parser.add_argument("--post-name", default="post")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    print(json.dumps(run(args), indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
