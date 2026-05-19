from __future__ import annotations

import argparse
import json
import warnings
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from common import DEFAULT_OUTPUT, add_common_io, export_table, parse_cols, read_data, require_columns, write_json


def build_model_y(args: argparse.Namespace) -> Any:
    if args.model_y == "gbr":
        from sklearn.ensemble import GradientBoostingRegressor

        return GradientBoostingRegressor(n_estimators=args.n_estimators_y, max_depth=args.max_depth_y, random_state=args.random_state)
    if args.model_y == "rf":
        from sklearn.ensemble import RandomForestRegressor

        return RandomForestRegressor(n_estimators=args.n_estimators_y, max_depth=args.max_depth_y, random_state=args.random_state)
    raise ValueError(f"Unsupported model_y: {args.model_y}")


def build_model_t(args: argparse.Namespace) -> Any:
    if args.discrete_treatment:
        if args.model_t == "rf":
            from sklearn.ensemble import RandomForestClassifier

            return RandomForestClassifier(n_estimators=args.n_estimators_t, max_depth=args.max_depth_t, random_state=args.random_state)
        if args.model_t == "gbc":
            from sklearn.ensemble import GradientBoostingClassifier

            return GradientBoostingClassifier(n_estimators=args.n_estimators_t, max_depth=args.max_depth_t, random_state=args.random_state)
        if args.model_t == "logit":
            from sklearn.linear_model import LogisticRegression

            return LogisticRegression(max_iter=args.max_iter)
    else:
        if args.model_t == "rf":
            from sklearn.ensemble import RandomForestRegressor

            return RandomForestRegressor(n_estimators=args.n_estimators_t, max_depth=args.max_depth_t, random_state=args.random_state)
        if args.model_t == "gbr":
            from sklearn.ensemble import GradientBoostingRegressor

            return GradientBoostingRegressor(n_estimators=args.n_estimators_t, max_depth=args.max_depth_t, random_state=args.random_state)
    raise ValueError(f"Unsupported model_t: {args.model_t} for discrete_treatment={args.discrete_treatment}")


def significance_stars(pvalue: float) -> str:
    if pvalue < 0.01:
        return "***"
    if pvalue < 0.05:
        return "**"
    if pvalue < 0.1:
        return "*"
    return ""


def make_design_matrix(df: pd.DataFrame, controls: list[str], spec: str, time_col: str | None) -> tuple[np.ndarray, list[str]]:
    base = df[controls].apply(pd.to_numeric, errors="coerce").to_numpy(dtype=float)
    parts = [base]
    columns = list(controls)

    if spec in {"squared", "time_fe_squared"}:
        parts.append(base**2)
        columns.extend([f"{col}_sq" for col in controls])

    if spec in {"time_fe", "time_fe_squared"}:
        if not time_col:
            raise ValueError(f"Spec {spec} requires --time-col.")
        dummies = pd.get_dummies(df[time_col], prefix=time_col, drop_first=True).astype(float)
        parts.append(dummies.to_numpy(dtype=float))
        columns.extend(list(dummies.columns))

    return np.hstack(parts), columns


def run_single_dml(
    df: pd.DataFrame,
    args: argparse.Namespace,
    spec: str,
    label: str,
    controls: list[str],
) -> tuple[dict[str, Any], list[str]]:
    try:
        from econml.dml import LinearDML
    except ImportError as exc:
        raise RuntimeError("Install econml to run DML workflows.") from exc
    from sklearn.model_selection import GroupKFold, KFold

    y = pd.to_numeric(df[args.outcome], errors="coerce").to_numpy(dtype=float)
    t_series = pd.to_numeric(df[args.treatment], errors="coerce")
    t = t_series.to_numpy(dtype=int if args.discrete_treatment else float)
    x, x_columns = make_design_matrix(df, controls, spec, args.time_col)
    groups = df[args.group_col].to_numpy() if args.group_col else None
    cv = GroupKFold(n_splits=args.n_splits) if args.group_col else KFold(n_splits=args.n_splits, shuffle=True, random_state=args.random_state)

    est = LinearDML(
        model_y=build_model_y(args),
        model_t=build_model_t(args),
        discrete_treatment=args.discrete_treatment,
        cv=cv,
        random_state=args.random_state,
    )
    est.fit(y, t, X=x, groups=groups)
    inf = est.ate_inference(X=x)
    ate = float(np.squeeze(inf.mean_point))
    se = float(np.squeeze(inf.stderr_mean))
    pvalue = float(np.squeeze(inf.pvalue()))
    row = {
        "model": label,
        "spec": spec,
        "ATE": ate,
        "StdErr": se,
        "Significance": significance_stars(pvalue),
        "p_value": pvalue,
        "N": int(len(y)),
        "n_features": int(x.shape[1]),
    }
    return row, x_columns


def run(args: argparse.Namespace) -> dict[str, Any]:
    warnings.filterwarnings("ignore")
    df = read_data(args.input, args.sheet)
    controls = parse_cols(args.controls)
    required = [args.outcome, args.treatment] + controls
    if args.group_col:
        required.append(args.group_col)
    if args.time_col:
        required.append(args.time_col)
    require_columns(df, required, "DML columns")

    before = len(df)
    df = df.dropna(subset=required).copy()
    specs = parse_cols(args.specs)
    labels = parse_cols(args.labels)
    if not labels:
        labels = specs
    if len(labels) != len(specs):
        raise ValueError("--labels must have the same number of items as --specs.")

    rows: list[dict[str, Any]] = []
    design_columns: dict[str, list[str]] = {}
    for spec, label in zip(specs, labels):
        row, x_columns = run_single_dml(df, args, spec, label, controls)
        rows.append(row)
        design_columns[spec] = x_columns

    outdir = Path(args.output_dir)
    results = pd.DataFrame(rows)
    export_table(results, outdir / "dml_results", ["csv"])
    transposed = results.set_index("model")[["ATE", "StdErr", "Significance", "p_value", "N"]].T.reset_index().rename(columns={"index": "metric"})
    export_table(transposed, outdir / "dml_results_transposed", ["csv"])

    manifest = {
        "input": str(args.input),
        "output_dir": str(outdir),
        "outcome": args.outcome,
        "treatment": args.treatment,
        "group_col": args.group_col,
        "time_col": args.time_col,
        "controls": controls,
        "specs": specs,
        "labels": labels,
        "model_y": args.model_y,
        "model_t": args.model_t,
        "random_state": args.random_state,
        "n_splits": args.n_splits,
        "dropped_missing_rows": int(before - len(df)),
        "design_columns": design_columns,
        "files": {
            "results": str(outdir / "dml_results.csv"),
            "transposed": str(outdir / "dml_results_transposed.csv"),
            "manifest": str(outdir / "dml_manifest.json"),
        },
    }
    write_json(manifest, outdir / "dml_manifest.json")
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run fixed LinearDML specifications.")
    add_common_io(parser)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT / "dml"))
    parser.add_argument("--outcome", required=True)
    parser.add_argument("--treatment", required=True)
    parser.add_argument("--controls", required=True)
    parser.add_argument("--group-col", default=None)
    parser.add_argument("--time-col", default=None)
    parser.add_argument("--specs", default="base", help="Comma-separated: base,time_fe,squared,time_fe_squared.")
    parser.add_argument("--labels", default="")
    parser.add_argument("--model-y", default="gbr", choices=["gbr", "rf"])
    parser.add_argument("--model-t", default="rf", choices=["rf", "gbc", "logit", "gbr"])
    parser.add_argument("--discrete-treatment", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--n-estimators-y", type=int, default=300)
    parser.add_argument("--n-estimators-t", type=int, default=300)
    parser.add_argument("--max-depth-y", type=int, default=3)
    parser.add_argument("--max-depth-t", type=int, default=3)
    parser.add_argument("--max-iter", type=int, default=5000)
    parser.add_argument("--random-state", type=int, default=2025)
    parser.add_argument("--n-splits", type=int, default=5)
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    print(json.dumps(run(args), indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
