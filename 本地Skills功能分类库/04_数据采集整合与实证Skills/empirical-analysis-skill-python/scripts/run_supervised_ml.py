from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from common import DEFAULT_OUTPUT, add_common_io, export_table, import_matplotlib, parse_cols, read_data, require_columns, save_figure, write_json
from prepare_ml_data import choose_features, infer_categorical, preprocessing_params, split_data, transform_features


def default_models(task: str) -> list[str]:
    if task == "regression":
        return ["linear", "ridge", "lasso", "elasticnet", "decision_tree", "random_forest", "gbdt"]
    return ["logistic", "decision_tree", "random_forest", "gbdt"]


def build_model(name: str, task: str, args: argparse.Namespace) -> Any:
    if task == "regression":
        from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
        from sklearn.linear_model import ElasticNet, ElasticNetCV, Lasso, LassoCV, LinearRegression, Ridge, RidgeCV
        from sklearn.tree import DecisionTreeRegressor

        if name == "linear":
            return LinearRegression()
        if name == "ridge":
            return RidgeCV(alphas=parse_float_grid(args.alphas)) if args.cv else Ridge(alpha=args.alpha, random_state=args.random_state)
        if name == "lasso":
            return LassoCV(alphas=parse_float_grid(args.alphas), cv=args.cv_folds, random_state=args.random_state, max_iter=args.max_iter) if args.cv else Lasso(alpha=args.alpha, random_state=args.random_state, max_iter=args.max_iter)
        if name == "elasticnet":
            l1_grid = parse_float_grid(args.l1_ratios)
            return ElasticNetCV(alphas=parse_float_grid(args.alphas), l1_ratio=l1_grid, cv=args.cv_folds, random_state=args.random_state, max_iter=args.max_iter) if args.cv else ElasticNet(alpha=args.alpha, l1_ratio=args.l1_ratio, random_state=args.random_state, max_iter=args.max_iter)
        if name == "decision_tree":
            return DecisionTreeRegressor(max_depth=args.max_depth, min_samples_leaf=args.min_samples_leaf, random_state=args.random_state)
        if name == "random_forest":
            return RandomForestRegressor(n_estimators=args.n_estimators, max_depth=args.max_depth, min_samples_leaf=args.min_samples_leaf, random_state=args.random_state)
        if name == "gbdt":
            return GradientBoostingRegressor(n_estimators=args.n_estimators, learning_rate=args.learning_rate, max_depth=args.max_depth or 3, random_state=args.random_state)
    else:
        from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
        from sklearn.linear_model import LogisticRegression
        from sklearn.tree import DecisionTreeClassifier

        if name == "logistic":
            penalty = "elasticnet" if args.classifier_penalty == "elasticnet" else args.classifier_penalty
            solver = "saga" if penalty in {"l1", "elasticnet"} else "lbfgs"
            l1_ratio = args.l1_ratio if penalty == "elasticnet" else None
            return LogisticRegression(penalty=penalty, solver=solver, l1_ratio=l1_ratio, C=args.classifier_c, max_iter=args.max_iter, random_state=args.random_state)
        if name == "decision_tree":
            return DecisionTreeClassifier(max_depth=args.max_depth, min_samples_leaf=args.min_samples_leaf, random_state=args.random_state)
        if name == "random_forest":
            return RandomForestClassifier(n_estimators=args.n_estimators, max_depth=args.max_depth, min_samples_leaf=args.min_samples_leaf, random_state=args.random_state)
        if name == "gbdt":
            return GradientBoostingClassifier(n_estimators=args.n_estimators, learning_rate=args.learning_rate, max_depth=args.max_depth or 3, random_state=args.random_state)
    raise ValueError(f"Unsupported model for {task}: {name}")


def parse_float_grid(value: str) -> list[float]:
    return [float(item.strip()) for item in value.split(",") if item.strip()]


def prepare_xy(df: pd.DataFrame, args: argparse.Namespace) -> tuple[pd.DataFrame, pd.Series, pd.Series, dict[str, Any]]:
    features = choose_features(df, args.target, parse_cols(args.features), parse_cols(args.exclude))
    id_cols = parse_cols(args.id_cols)
    required = [args.target] + features + id_cols
    if args.split_col:
        required.append(args.split_col)
    require_columns(df, required, "supervised ML columns")
    data = df[required].dropna(subset=[args.target]).copy()
    if args.split_col:
        require_columns(data, [args.split_col], "split column")
        data["_split"] = data[args.split_col].astype(str).str.lower()
    else:
        data = split_data(data, args)
    numeric, categorical = infer_categorical(data, features, parse_cols(args.categorical))
    train = data.loc[data["_split"] == "train"]
    if train.empty:
        raise ValueError("Training split is empty.")
    params = preprocessing_params(train, numeric, categorical)
    x = transform_features(data, numeric, categorical, params, args.standardize)
    y = data[args.target]
    meta = {
        "features": features,
        "numeric_features": numeric,
        "categorical_features": categorical,
        "id_cols": id_cols,
        "preprocessing_params": params,
        "row_index": data.index.tolist(),
    }
    return x, y, data["_split"], meta


def regression_metrics(y_true: pd.Series, pred: np.ndarray) -> dict[str, float]:
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

    mae = mean_absolute_error(y_true, pred)
    mse = mean_squared_error(y_true, pred)
    return {"MAE": float(mae), "MSE": float(mse), "RMSE": float(np.sqrt(mse)), "R2": float(r2_score(y_true, pred))}


def classification_metrics(y_true: pd.Series, pred: np.ndarray, proba: np.ndarray | None, average: str) -> dict[str, float]:
    from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score

    metrics = {
        "accuracy": float(accuracy_score(y_true, pred)),
        "precision": float(precision_score(y_true, pred, average=average, zero_division=0)),
        "recall": float(recall_score(y_true, pred, average=average, zero_division=0)),
        "f1": float(f1_score(y_true, pred, average=average, zero_division=0)),
    }
    if proba is not None:
        try:
            if proba.ndim == 2 and proba.shape[1] == 2:
                metrics["roc_auc"] = float(roc_auc_score(y_true, proba[:, 1]))
            elif proba.ndim == 2 and proba.shape[1] > 2:
                metrics["roc_auc"] = float(roc_auc_score(y_true, proba, multi_class="ovr", average=average))
        except Exception:
            metrics["roc_auc"] = np.nan
    return metrics


def model_parameters(model: Any) -> dict[str, Any]:
    params: dict[str, Any] = {}
    for attr in ["alpha_", "l1_ratio_", "alpha", "l1_ratio", "C"]:
        if hasattr(model, attr):
            value = getattr(model, attr)
            if isinstance(value, np.ndarray):
                value = value.tolist()
            params[attr] = value
    return params


def coefficient_rows(model_name: str, model: Any, feature_names: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if hasattr(model, "coef_"):
        coef = np.asarray(model.coef_)
        if coef.ndim == 1:
            for feature, value in zip(feature_names, coef):
                rows.append({"model": model_name, "feature": feature, "coefficient": float(value), "abs_value": float(abs(value))})
        else:
            for class_idx, class_coef in enumerate(coef):
                for feature, value in zip(feature_names, class_coef):
                    rows.append({"model": model_name, "class": class_idx, "feature": feature, "coefficient": float(value), "abs_value": float(abs(value))})
    if hasattr(model, "feature_importances_"):
        for feature, value in zip(feature_names, np.asarray(model.feature_importances_)):
            rows.append({"model": model_name, "feature": feature, "importance": float(value), "abs_value": float(abs(value))})
    return rows


def plot_feature_table(table: pd.DataFrame, outdir: Path, top_n: int) -> list[str]:
    if table.empty or "abs_value" not in table.columns:
        return []
    plot_df = table.sort_values("abs_value", ascending=False).head(top_n).iloc[::-1]
    value_col = "importance" if "importance" in plot_df.columns and plot_df["importance"].notna().any() else "coefficient"
    plt = import_matplotlib()
    fig, ax = plt.subplots(figsize=(8.0, max(4.0, 0.28 * len(plot_df))))
    labels = plot_df["model"].astype(str) + ": " + plot_df["feature"].astype(str)
    ax.barh(labels, plot_df[value_col].astype(float))
    ax.axvline(0, color="gray", linewidth=0.8)
    ax.set_xlabel(value_col)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    written = save_figure(fig, outdir / "fig_ml_feature_effects")
    plt.close(fig)
    return written


def run(args: argparse.Namespace) -> dict[str, Any]:
    df = read_data(args.input, args.sheet)
    x, y, split, meta = prepare_xy(df, args)
    models = parse_cols(args.models) or default_models(args.task)
    outdir = Path(args.output_dir)
    feature_names = list(x.columns)
    train_mask = split == "train"
    metrics_rows: list[dict[str, Any]] = []
    prediction_rows: list[dict[str, Any]] = []
    coef_rows: list[dict[str, Any]] = []
    fitted_params: dict[str, Any] = {}

    for model_name in models:
        model = build_model(model_name, args.task, args)
        model.fit(x.loc[train_mask], y.loc[train_mask])
        fitted_params[model_name] = model_parameters(model)
        coef_rows.extend(coefficient_rows(model_name, model, feature_names))
        for split_name in ["train", "valid", "test"]:
            mask = split == split_name
            if not mask.any():
                continue
            pred = model.predict(x.loc[mask])
            row: dict[str, Any] = {"model": model_name, "split": split_name, "nobs": int(mask.sum())}
            if args.task == "regression":
                row.update(regression_metrics(y.loc[mask], pred))
                proba = None
            else:
                proba = model.predict_proba(x.loc[mask]) if hasattr(model, "predict_proba") else None
                row.update(classification_metrics(y.loc[mask], pred, proba, args.average))
            metrics_rows.append(row)
            for idx, actual, predicted in zip(np.where(mask)[0], y.loc[mask], pred):
                prediction_rows.append({"model": model_name, "split": split_name, "row_position": int(idx), "actual": actual, "prediction": predicted})

    metrics = pd.DataFrame(metrics_rows).round(6)
    predictions = pd.DataFrame(prediction_rows)
    coef_table = pd.DataFrame(coef_rows).sort_values(["model", "abs_value"], ascending=[True, False]) if coef_rows else pd.DataFrame()
    written: list[str] = []
    written += export_table(metrics, outdir / "ml_metrics", parse_cols(args.formats))
    written += export_table(predictions, outdir / "ml_predictions", ["csv"])
    if not coef_table.empty:
        written += export_table(coef_table.round(6), outdir / "ml_feature_effects", parse_cols(args.formats))
    figure_files: list[str] = []
    if not args.no_figures and not coef_table.empty:
        figure_files = plot_feature_table(coef_table, outdir, args.top_n)

    manifest = {
        "input": str(args.input),
        "output_dir": str(outdir),
        "task": args.task,
        "target": args.target,
        "models": models,
        "standardize": args.standardize,
        "cv": args.cv,
        "cv_folds": args.cv_folds,
        "selected_model_params": fitted_params,
        "feature_schema": {key: meta[key] for key in ["features", "numeric_features", "categorical_features", "id_cols"]},
        "files": {"tables": written, "figures": figure_files, "manifest": str(outdir / "supervised_ml_manifest.json")},
    }
    write_json(manifest, outdir / "supervised_ml_manifest.json")
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run fixed supervised ML models and evaluation metrics.")
    add_common_io(parser)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT / "ml"))
    parser.add_argument("--task", required=True, choices=["regression", "classification"])
    parser.add_argument("--target", required=True)
    parser.add_argument("--features", default="")
    parser.add_argument("--categorical", default="")
    parser.add_argument("--exclude", default="")
    parser.add_argument("--id-cols", default="")
    parser.add_argument("--split-col", default=None)
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--valid-size", type=float, default=0.0)
    parser.add_argument("--stratify", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--standardize", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--models", default="", help="Regression: linear,ridge,lasso,elasticnet,decision_tree,random_forest,gbdt. Classification: logistic,decision_tree,random_forest,gbdt.")
    parser.add_argument("--alpha", type=float, default=1.0)
    parser.add_argument("--alphas", default="0.001,0.01,0.1,1,10,100")
    parser.add_argument("--l1-ratio", type=float, default=0.5)
    parser.add_argument("--l1-ratios", default="0.1,0.5,0.9")
    parser.add_argument("--cv", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--cv-folds", type=int, default=5)
    parser.add_argument("--classifier-penalty", default="l2", choices=["l2", "l1", "elasticnet"])
    parser.add_argument("--classifier-c", type=float, default=1.0)
    parser.add_argument("--n-estimators", type=int, default=300)
    parser.add_argument("--learning-rate", type=float, default=0.05)
    parser.add_argument("--max-depth", type=int, default=None)
    parser.add_argument("--min-samples-leaf", type=int, default=5)
    parser.add_argument("--max-iter", type=int, default=10000)
    parser.add_argument("--average", default="binary", choices=["binary", "macro", "micro", "weighted"])
    parser.add_argument("--random-state", type=int, default=2025)
    parser.add_argument("--top-n", type=int, default=30)
    parser.add_argument("--no-figures", action="store_true")
    parser.add_argument("--formats", default="csv,xlsx,tex")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    print(json.dumps(run(args), indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
