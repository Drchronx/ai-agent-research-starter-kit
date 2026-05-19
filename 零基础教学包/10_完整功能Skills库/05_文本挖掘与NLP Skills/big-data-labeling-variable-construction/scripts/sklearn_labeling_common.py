import argparse
from pathlib import Path
from typing import Callable

import pandas as pd
from joblib import dump
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from labeling_common import ensure_dir, load_stopwords, load_table, require_columns, save_json, tokenize_text


class TokenizerAdapter:
    def __init__(self, stopwords: set[str]) -> None:
        self.stopwords = stopwords

    def __call__(self, text: str) -> list[str]:
        return tokenize_text(text, self.stopwords)


def parse_common_args(description: str) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("input_path", help="CSV or Excel file containing text and labels.")
    parser.add_argument("--text-col", default="text", help="Text column name.")
    parser.add_argument("--label-col", default="label", help="Label column name.")
    parser.add_argument("--id-col", default="doc_id", help="Document id column.")
    parser.add_argument("--test-size", type=float, default=0.2, help="Test set ratio between 0 and 1.")
    parser.add_argument("--random-state", type=int, default=42, help="Random seed.")
    parser.add_argument("--stopwords-path", help="Optional UTF-8 stopwords file.")
    parser.add_argument("--output-dir", required=True, help="Output directory.")
    return parser.parse_args()


def run_sklearn_labeling(
    args: argparse.Namespace,
    classifier_factory: Callable[[], object],
    method_name: str,
) -> None:
    output_dir = ensure_dir(Path(args.output_dir))
    df = load_table(Path(args.input_path)).copy()
    require_columns(df, [args.text_col, args.label_col])

    local = df.copy()
    if args.id_col not in local.columns:
        local[args.id_col] = range(1, len(local) + 1)
    local[args.text_col] = local[args.text_col].fillna("").astype(str)
    local[args.label_col] = local[args.label_col].fillna("").astype(str)
    local = local[local[args.label_col] != ""].reset_index(drop=True)
    if local[args.label_col].nunique() < 2:
        raise ValueError("At least two label classes are required.")

    stopwords = load_stopwords(args.stopwords_path)
    pipeline = Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    tokenizer=TokenizerAdapter(stopwords),
                    token_pattern=None,
                    lowercase=False,
                    min_df=1,
                    max_df=0.95,
                ),
            ),
            ("classifier", classifier_factory()),
        ]
    )

    stratify = local[args.label_col] if local[args.label_col].value_counts().min() >= 2 else None
    train_df, test_df = train_test_split(
        local,
        test_size=args.test_size,
        random_state=args.random_state,
        stratify=stratify,
    )
    pipeline.fit(train_df[args.text_col], train_df[args.label_col])
    predictions = pipeline.predict(test_df[args.text_col])

    labels = sorted(local[args.label_col].unique())
    metrics = {
        "method": method_name,
        "train_size": int(len(train_df)),
        "test_size": int(len(test_df)),
        "label_count": int(len(labels)),
        "accuracy": round(float(accuracy_score(test_df[args.label_col], predictions)), 6),
        "macro_f1": round(float(f1_score(test_df[args.label_col], predictions, average="macro")), 6),
        "weighted_f1": round(float(f1_score(test_df[args.label_col], predictions, average="weighted")), 6),
        "labels": labels,
    }

    report = classification_report(
        test_df[args.label_col],
        predictions,
        output_dict=True,
        zero_division=0,
    )
    report_df = pd.DataFrame(report).transpose().reset_index().rename(columns={"index": "label"})
    report_df.to_csv(output_dir / "classification_report.csv", index=False, encoding="utf-8-sig")

    matrix = confusion_matrix(test_df[args.label_col], predictions, labels=labels)
    matrix_df = pd.DataFrame(matrix, index=labels, columns=labels)
    matrix_df.index.name = "actual"
    matrix_df.to_csv(output_dir / "confusion_matrix.csv", encoding="utf-8-sig")

    predictions_df = test_df[[args.id_col, args.text_col, args.label_col]].copy()
    predictions_df["predicted_label"] = predictions
    predictions_df["is_correct"] = predictions_df[args.label_col] == predictions_df["predicted_label"]
    predictions_df.to_csv(output_dir / "test_predictions.csv", index=False, encoding="utf-8-sig")

    model_path = output_dir / "model.joblib"
    dump(pipeline, model_path)
    save_json(output_dir / "metrics.json", metrics)

    summary_lines = [
        f"# {method_name} Text Labeling Summary",
        "",
        f"- Train size: {len(train_df)}",
        f"- Test size: {len(test_df)}",
        f"- Accuracy: {metrics['accuracy']:.4f}",
        f"- Macro F1: {metrics['macro_f1']:.4f}",
        f"- Weighted F1: {metrics['weighted_f1']:.4f}",
        f"- Labels: {', '.join(labels)}",
        "",
        "## Output Files",
        "- metrics.json",
        "- classification_report.csv",
        "- confusion_matrix.csv",
        "- test_predictions.csv",
        "- model.joblib",
    ]
    (output_dir / "summary.md").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

    print(f"Method: {method_name}")
    print(f"Metrics: {output_dir / 'metrics.json'}")
    print(f"Classification report: {output_dir / 'classification_report.csv'}")
    print(f"Confusion matrix: {output_dir / 'confusion_matrix.csv'}")
    print(f"Predictions: {output_dir / 'test_predictions.csv'}")
    print(f"Model: {model_path}")
