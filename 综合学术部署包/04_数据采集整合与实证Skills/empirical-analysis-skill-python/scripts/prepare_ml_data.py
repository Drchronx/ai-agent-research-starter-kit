from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from common import DEFAULT_OUTPUT, add_common_io, export_table, parse_cols, read_data, require_columns, write_json


def choose_features(df: pd.DataFrame, target: str, features: list[str], exclude: list[str]) -> list[str]:
    if features:
        return features
    excluded = {target, "_split", *exclude}
    return [col for col in df.columns if col not in excluded]


def infer_categorical(df: pd.DataFrame, features: list[str], categorical: list[str]) -> tuple[list[str], list[str]]:
    if categorical:
        require_columns(df, categorical, "categorical features")
        cat = categorical
    else:
        cat = [col for col in features if not pd.api.types.is_numeric_dtype(df[col])]
    num = [col for col in features if col not in cat]
    return num, cat


def split_data(df: pd.DataFrame, args: argparse.Namespace) -> pd.DataFrame:
    from sklearn.model_selection import train_test_split

    data = df.copy()
    stratify_col = args.target if args.stratify else None
    stratify = data[stratify_col] if stratify_col else None
    train_valid, test = train_test_split(data, test_size=args.test_size, random_state=args.random_state, stratify=stratify)
    if args.valid_size > 0:
        valid_ratio = args.valid_size / (1.0 - args.test_size)
        valid_stratify = train_valid[stratify_col] if stratify_col else None
        train, valid = train_test_split(train_valid, test_size=valid_ratio, random_state=args.random_state, stratify=valid_stratify)
    else:
        train = train_valid
        valid = train_valid.iloc[0:0].copy()
    train = train.copy()
    valid = valid.copy()
    test = test.copy()
    train["_split"] = "train"
    valid["_split"] = "valid"
    test["_split"] = "test"
    return pd.concat([train, valid, test], axis=0).sort_index()


def preprocessing_params(train: pd.DataFrame, numeric: list[str], categorical: list[str]) -> dict[str, Any]:
    params: dict[str, Any] = {"numeric": {}, "categorical": {}}
    for col in numeric:
        series = pd.to_numeric(train[col], errors="coerce")
        mean = float(series.mean()) if series.notna().any() else 0.0
        std = float(series.std(ddof=0)) if series.notna().any() else 1.0
        if not np.isfinite(std) or std == 0:
            std = 1.0
        params["numeric"][col] = {
            "median": float(series.median()) if series.notna().any() else 0.0,
            "mean": mean,
            "std": std,
        }
    for col in categorical:
        mode = train[col].mode(dropna=True)
        params["categorical"][col] = {"mode": str(mode.iloc[0]) if not mode.empty else "__missing__"}
    return params


def transform_features(df: pd.DataFrame, numeric: list[str], categorical: list[str], params: dict[str, Any], standardize: bool) -> pd.DataFrame:
    parts: list[pd.DataFrame] = []
    if numeric:
        num = df[numeric].apply(pd.to_numeric, errors="coerce").copy()
        for col in numeric:
            info = params["numeric"][col]
            num[col] = num[col].fillna(info["median"])
            if standardize:
                num[col] = (num[col] - info["mean"]) / info["std"]
        parts.append(num)
    if categorical:
        cat = df[categorical].copy()
        for col in categorical:
            cat[col] = cat[col].astype("object").where(cat[col].notna(), params["categorical"][col]["mode"]).astype(str)
        parts.append(pd.get_dummies(cat, prefix=categorical, dtype=float))
    if not parts:
        raise ValueError("No features are available after preprocessing.")
    return pd.concat(parts, axis=1)


def export_split_matrices(
    x: pd.DataFrame,
    y: pd.Series,
    split: pd.Series,
    outdir: Path,
    prefix: str,
) -> list[str]:
    written: list[str] = []
    for name in ["train", "valid", "test"]:
        mask = split == name
        if not mask.any():
            continue
        x_path = outdir / f"{prefix}_X_{name}.csv"
        y_path = outdir / f"{prefix}_y_{name}.csv"
        x.loc[mask].to_csv(x_path, index=False)
        y.loc[mask].to_frame("target").to_csv(y_path, index=False)
        written.extend([str(x_path), str(y_path)])
    return written


def run(args: argparse.Namespace) -> dict[str, Any]:
    df = read_data(args.input, args.sheet)
    exclude = parse_cols(args.exclude)
    features = choose_features(df, args.target, parse_cols(args.features), exclude)
    id_cols = parse_cols(args.id_cols)
    require_columns(df, [args.target] + features + id_cols, "ML data columns")
    before = len(df)
    if args.drop_missing_target:
        df = df.dropna(subset=[args.target]).copy()
    split_df = split_data(df[[args.target] + features + id_cols].copy(), args)
    numeric, categorical = infer_categorical(split_df, features, parse_cols(args.categorical))
    train = split_df.loc[split_df["_split"] == "train"]
    params = preprocessing_params(train, numeric, categorical)
    x = transform_features(split_df, numeric, categorical, params, args.standardize)
    y = split_df[args.target]

    outdir = Path(args.output_dir)
    selected = split_df[[*id_cols, "_split", args.target] + features]
    written = export_table(selected, outdir / f"{args.prefix}_dataset_split", parse_cols(args.formats))
    written += export_split_matrices(x, y, split_df["_split"], outdir, args.prefix)
    feature_summary = pd.DataFrame(
        [{"feature": col, "role": "numeric" if col in numeric else "categorical", "missing": int(split_df[col].isna().sum()), "dtype": str(split_df[col].dtype)} for col in features]
    )
    written += export_table(feature_summary, outdir / f"{args.prefix}_feature_summary", parse_cols(args.formats))

    manifest = {
        "input": str(args.input),
        "output_dir": str(outdir),
        "target": args.target,
        "features": features,
        "numeric_features": numeric,
        "categorical_features": categorical,
        "id_cols": id_cols,
        "standardize": args.standardize,
        "test_size": args.test_size,
        "valid_size": args.valid_size,
        "random_state": args.random_state,
        "dropped_missing_target_rows": int(before - len(df)),
        "preprocessing_params": params,
        "files": {
            "written": written,
            "manifest": str(outdir / f"{args.prefix}_ml_data_manifest.json"),
        },
    }
    write_json(manifest, outdir / f"{args.prefix}_ml_data_manifest.json")
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prepare fixed ML feature matrices X and target vector y.")
    add_common_io(parser)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT / "ml"))
    parser.add_argument("--target", required=True)
    parser.add_argument("--features", default="", help="Comma-separated features. Defaults to all columns except target and excluded columns.")
    parser.add_argument("--categorical", default="", help="Comma-separated categorical features. Defaults to object/category columns.")
    parser.add_argument("--exclude", default="")
    parser.add_argument("--id-cols", default="")
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--valid-size", type=float, default=0.0)
    parser.add_argument("--stratify", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--drop-missing-target", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--standardize", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--random-state", type=int, default=2025)
    parser.add_argument("--prefix", default="ml")
    parser.add_argument("--formats", default="csv")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    print(json.dumps(run(args), indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
