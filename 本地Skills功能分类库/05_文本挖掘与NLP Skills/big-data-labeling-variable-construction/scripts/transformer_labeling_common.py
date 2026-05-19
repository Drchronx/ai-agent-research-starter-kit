import argparse
import subprocess
from pathlib import Path

import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import train_test_split

from labeling_common import ensure_dir, load_table, require_columns, save_json


PYTORCH_HOME = "https://pytorch.org/"
PYTORCH_INSTALL = "https://pytorch.org/get-started/locally/"


def parse_common_args(description: str) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("input_path", help="CSV or Excel file containing text and labels.")
    parser.add_argument("--text-col", default="text", help="Text column name.")
    parser.add_argument("--label-col", default="label", help="Label column name.")
    parser.add_argument("--id-col", default="doc_id", help="Document id column.")
    parser.add_argument("--model-name", required=True, help="HuggingFace model name or local checkpoint.")
    parser.add_argument("--test-size", type=float, default=0.2, help="Test set ratio between 0 and 1.")
    parser.add_argument("--max-length", type=int, default=256, help="Tokenizer max sequence length.")
    parser.add_argument("--epochs", type=int, default=2, help="Training epochs.")
    parser.add_argument("--train-batch-size", type=int, default=8, help="Training batch size.")
    parser.add_argument("--eval-batch-size", type=int, default=8, help="Evaluation batch size.")
    parser.add_argument("--learning-rate", type=float, default=2e-5, help="Learning rate.")
    parser.add_argument("--random-state", type=int, default=42, help="Random seed.")
    parser.add_argument("--output-dir", required=True, help="Output directory.")
    return parser.parse_args()


def compute_metrics(eval_prediction: tuple) -> dict[str, float]:
    logits = getattr(eval_prediction, "predictions", eval_prediction[0])
    labels = getattr(eval_prediction, "label_ids", eval_prediction[1])
    predictions = logits.argmax(axis=1)
    return {
        "accuracy": float(accuracy_score(labels, predictions)),
        "macro_f1": float(f1_score(labels, predictions, average="macro")),
        "weighted_f1": float(f1_score(labels, predictions, average="weighted")),
    }


def detect_torch_runtime(torch_module) -> dict[str, object]:
    runtime = {
        "torch_version": torch_module.__version__,
        "torch_cuda_version": torch_module.version.cuda,
        "cuda_available": bool(torch_module.cuda.is_available()),
        "cuda_device_count": int(torch_module.cuda.device_count()),
        "device": "cpu",
        "device_name": "CPU",
        "device_reason": "PyTorch did not detect a CUDA-capable runtime.",
        "gpu_visible_to_system": False,
        "nvidia_smi_summary": None,
    }

    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
            capture_output=True,
            text=True,
            check=True,
        )
        gpu_names = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        if gpu_names:
            runtime["gpu_visible_to_system"] = True
            runtime["nvidia_smi_summary"] = gpu_names
    except Exception:
        runtime["gpu_visible_to_system"] = False

    if runtime["cuda_available"]:
        runtime["device"] = "cuda"
        runtime["device_name"] = str(torch_module.cuda.get_device_name(0))
        runtime["device_reason"] = "CUDA is available and PyTorch can use the GPU."
    elif runtime["gpu_visible_to_system"] and runtime["torch_cuda_version"] is None:
        runtime["device_reason"] = (
            "A GPU is visible via nvidia-smi, but this Python environment uses a CPU-only PyTorch build."
        )
    elif runtime["gpu_visible_to_system"]:
        runtime["device_reason"] = (
            "A GPU is visible via nvidia-smi, but PyTorch still cannot initialize CUDA in this environment."
        )
    return runtime


def run_transformer_labeling(args: argparse.Namespace, method_name: str) -> None:
    try:
        import torch
    except Exception as exc:
        raise RuntimeError(
            "未检测到 PyTorch。预训练模型路线需要先安装 torch。\n"
            f"PyTorch 官网：{PYTORCH_HOME}\n"
            f"官方安装页：{PYTORCH_INSTALL}\n"
            "请根据你的系统和是否有 NVIDIA GPU 选择对应安装命令，安装完成后再重试。"
        ) from exc

    try:
        from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments
    except Exception as exc:
        raise RuntimeError(
            "未检测到 transformers。请先安装 transformers 后再使用预训练模型路线。\n"
            f"PyTorch 官网：{PYTORCH_HOME}\n"
            f"官方安装页：{PYTORCH_INSTALL}"
        ) from exc

    class TextClassificationDataset(torch.utils.data.Dataset):
        def __init__(self, encodings: dict, labels: list[int]) -> None:
            self.encodings = encodings
            self.labels = labels

        def __len__(self) -> int:
            return len(self.labels)

        def __getitem__(self, idx: int) -> dict[str, torch.Tensor]:
            item = {key: torch.tensor(value[idx]) for key, value in self.encodings.items()}
            item["labels"] = torch.tensor(self.labels[idx])
            return item

    output_dir = ensure_dir(Path(args.output_dir))
    runtime = detect_torch_runtime(torch)
    save_json(output_dir / "runtime_diagnosis.json", runtime)
    df = load_table(Path(args.input_path)).copy()
    require_columns(df, [args.text_col, args.label_col])

    if args.id_col not in df.columns:
        df[args.id_col] = range(1, len(df) + 1)
    df[args.text_col] = df[args.text_col].fillna("").astype(str)
    df[args.label_col] = df[args.label_col].fillna("").astype(str)
    df = df[df[args.label_col] != ""].reset_index(drop=True)
    if df[args.label_col].nunique() < 2:
        raise ValueError("At least two label classes are required.")

    labels = sorted(df[args.label_col].unique())
    label_to_id = {label: idx for idx, label in enumerate(labels)}
    id_to_label = {idx: label for label, idx in label_to_id.items()}
    df["label_id"] = df[args.label_col].map(label_to_id)

    stratify = df[args.label_col] if df[args.label_col].value_counts().min() >= 2 else None
    train_df, test_df = train_test_split(
        df,
        test_size=args.test_size,
        random_state=args.random_state,
        stratify=stratify,
    )

    tokenizer = AutoTokenizer.from_pretrained(args.model_name)
    model = AutoModelForSequenceClassification.from_pretrained(
        args.model_name,
        num_labels=len(labels),
        id2label=id_to_label,
        label2id=label_to_id,
    )

    train_encodings = tokenizer(
        train_df[args.text_col].tolist(),
        truncation=True,
        padding=True,
        max_length=args.max_length,
    )
    test_encodings = tokenizer(
        test_df[args.text_col].tolist(),
        truncation=True,
        padding=True,
        max_length=args.max_length,
    )
    train_dataset = TextClassificationDataset(train_encodings, train_df["label_id"].tolist())
    test_dataset = TextClassificationDataset(test_encodings, test_df["label_id"].tolist())

    training_args = TrainingArguments(
        output_dir=str(output_dir / "trainer"),
        num_train_epochs=args.epochs,
        learning_rate=args.learning_rate,
        per_device_train_batch_size=args.train_batch_size,
        per_device_eval_batch_size=args.eval_batch_size,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="macro_f1",
        greater_is_better=True,
        logging_dir=str(output_dir / "logs"),
        report_to=[],
        seed=args.random_state,
        use_cpu=runtime["device"] != "cuda",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
        compute_metrics=compute_metrics,
    )
    trainer.train()
    eval_metrics = trainer.evaluate()
    prediction_output = trainer.predict(test_dataset)
    predicted_ids = prediction_output.predictions.argmax(axis=1)
    predicted_labels = [id_to_label[int(label_id)] for label_id in predicted_ids]

    metrics = {
        "method": method_name,
        "model_name": args.model_name,
        "runtime": runtime,
        "train_size": int(len(train_df)),
        "test_size": int(len(test_df)),
        "label_count": int(len(labels)),
        "accuracy": round(float(eval_metrics["eval_accuracy"]), 6),
        "macro_f1": round(float(eval_metrics["eval_macro_f1"]), 6),
        "weighted_f1": round(float(eval_metrics["eval_weighted_f1"]), 6),
        "labels": labels,
    }
    save_json(output_dir / "metrics.json", metrics)
    save_json(output_dir / "label_mapping.json", {"label_to_id": label_to_id, "id_to_label": id_to_label})

    report = classification_report(
        test_df[args.label_col],
        predicted_labels,
        output_dict=True,
        zero_division=0,
    )
    pd.DataFrame(report).transpose().reset_index().rename(columns={"index": "label"}).to_csv(
        output_dir / "classification_report.csv",
        index=False,
        encoding="utf-8-sig",
    )

    predictions_df = test_df[[args.id_col, args.text_col, args.label_col]].copy()
    predictions_df["predicted_label"] = predicted_labels
    predictions_df["is_correct"] = predictions_df[args.label_col] == predictions_df["predicted_label"]
    predictions_df.to_csv(output_dir / "test_predictions.csv", index=False, encoding="utf-8-sig")

    final_model_dir = output_dir / "fine_tuned_model"
    trainer.save_model(str(final_model_dir))
    tokenizer.save_pretrained(str(final_model_dir))

    summary_lines = [
        f"# {method_name} Text Labeling Summary",
        "",
        f"- Base model: {args.model_name}",
        f"- Runtime device: {runtime['device']}",
        f"- Runtime device name: {runtime['device_name']}",
        f"- Runtime reason: {runtime['device_reason']}",
        f"- Train size: {len(train_df)}",
        f"- Test size: {len(test_df)}",
        f"- Accuracy: {metrics['accuracy']:.4f}",
        f"- Macro F1: {metrics['macro_f1']:.4f}",
        f"- Weighted F1: {metrics['weighted_f1']:.4f}",
        "",
        "## Output Files",
        "- metrics.json",
        "- label_mapping.json",
        "- classification_report.csv",
        "- test_predictions.csv",
        "- fine_tuned_model/",
    ]
    (output_dir / "summary.md").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

    print(f"Method: {method_name}")
    print(f"Runtime device: {runtime['device']}")
    print(f"Runtime detail: {runtime['device_reason']}")
    print(f"Runtime diagnosis: {output_dir / 'runtime_diagnosis.json'}")
    print(f"Metrics: {output_dir / 'metrics.json'}")
    print(f"Label mapping: {output_dir / 'label_mapping.json'}")
    print(f"Predictions: {output_dir / 'test_predictions.csv'}")
    print(f"Model dir: {final_model_dir}")
