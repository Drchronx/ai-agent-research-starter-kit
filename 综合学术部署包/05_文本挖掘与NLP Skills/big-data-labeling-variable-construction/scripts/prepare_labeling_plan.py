import argparse
from pathlib import Path

from labeling_common import (
    ensure_dir,
    infer_id_column,
    infer_label_column,
    infer_text_column,
    load_table,
    save_json,
)

from check_pretrained_env import PYTORCH_HOME, PYTORCH_INSTALL


def inspect_pretrained_env() -> dict:
    result = {
        "pytorch_home": PYTORCH_HOME,
        "pytorch_install": PYTORCH_INSTALL,
        "torch_installed": False,
        "transformers_installed": False,
        "torch_version": None,
        "transformers_version": None,
        "torch_cuda_version": None,
        "cuda_available": False,
        "device": "cpu",
        "status": "missing_dependencies",
        "message": "",
    }

    try:
        import torch  # type: ignore

        result["torch_installed"] = True
        result["torch_version"] = torch.__version__
        result["torch_cuda_version"] = torch.version.cuda
        result["cuda_available"] = bool(torch.cuda.is_available())
        result["device"] = "cuda" if result["cuda_available"] else "cpu"
    except Exception:
        pass

    try:
        import transformers  # type: ignore

        result["transformers_installed"] = True
        result["transformers_version"] = transformers.__version__
    except Exception:
        pass

    if result["torch_installed"] and result["transformers_installed"]:
        result["status"] = "ready"
        if result["cuda_available"]:
            result["message"] = "预训练模型环境已就绪，当前可使用 GPU。"
        else:
            result["message"] = "预训练模型环境已就绪，但当前将使用 CPU。"
    else:
        missing = []
        if not result["torch_installed"]:
            missing.append("torch")
        if not result["transformers_installed"]:
            missing.append("transformers")
        result["message"] = (
            "预训练模型路线缺少依赖："
            + ", ".join(missing)
            + "。请优先使用 PyTorch 官方安装页选择与你机器匹配的安装命令。"
        )
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect the first rows of a dataset and prepare a labeling plan for user confirmation.")
    parser.add_argument("input_path", help="CSV or Excel dataset path.")
    parser.add_argument(
        "--category",
        required=True,
        choices=["lda", "sklearn", "pretrained", "openai"],
        help="Chosen labeling category.",
    )
    parser.add_argument("--model-name", help="Optional model name for pretrained or OpenAI routes.")
    parser.add_argument("--labels", help="Comma-separated candidate labels for OpenAI route.")
    parser.add_argument("--output-dir", default="reports/labeling-plan", help="Output directory.")
    return parser.parse_args()


def build_defaults(category: str, row_count: int) -> dict:
    if category == "lda":
        upper = 10 if row_count < 2000 else 15
        return {"topic_range": f"2-{upper}", "passes": 20, "iterations": 200}
    if category == "sklearn":
        return {"recommended_method": "sklearn_svm", "test_size": 0.2}
    if category == "pretrained":
        batch_size = 16 if row_count <= 2000 else 8
        return {"test_size": 0.2, "epochs": 2, "train_batch_size": batch_size, "eval_batch_size": batch_size}
    if category == "openai":
        return {"system_prompt": "你是一个严格的中文文本标注助手，只返回 JSON。", "batch_size": 1}
    return {}


def main() -> None:
    args = parse_args()
    output_dir = ensure_dir(Path(args.output_dir))
    df = load_table(Path(args.input_path))
    preview = df.head(10).copy()

    id_column = infer_id_column(df)
    text_column = infer_text_column(preview)
    label_column = infer_label_column(preview, text_column=text_column) if args.category in {"sklearn", "pretrained"} else None
    defaults = build_defaults(args.category, len(df))
    pretrained_env = inspect_pretrained_env() if args.category == "pretrained" else None

    missing_user_inputs = []
    if args.category == "openai":
        if not args.labels:
            missing_user_inputs.append("标签集合")
        if not args.model_name:
            missing_user_inputs.append("模型名称")
        missing_user_inputs.extend(["base_url", "api_key"])
    if args.category == "pretrained" and not args.model_name:
        missing_user_inputs.append("模型名称")

    payload = {
        "input_path": args.input_path,
        "category": args.category,
        "row_count": int(len(df)),
        "column_names": [str(column) for column in df.columns],
        "preview_records": preview.fillna("").astype(str).to_dict(orient="records"),
        "inferred_columns": {
            "text_col": text_column,
            "label_col": label_column,
            "id_col": id_column or "auto_generated_doc_id",
        },
        "default_parameters": defaults,
        "pretrained_env": pretrained_env,
        "model_name": args.model_name,
        "labels": [item.strip() for item in args.labels.split(",")] if args.labels else None,
        "missing_user_inputs": missing_user_inputs,
        "next_step": "请先向用户展示这份推断结果。只有在用户明确回复【确认无误，请执行】后，才允许调用实际运行脚本。",
        "confirmation_phrase": "确认无误，请执行",
    }
    save_json(output_dir / "labeling_plan.json", payload)

    print(f"Category: {args.category}")
    print(f"Rows: {len(df)}")
    print(f"Inferred text_col: {text_column}")
    print(f"Inferred label_col: {label_column}")
    print(f"Inferred id_col: {id_column or 'auto_generated_doc_id'}")
    print("Default parameters:")
    for key, value in defaults.items():
        print(f"- {key}: {value}")
    if pretrained_env:
        print("Pretrained environment:")
        print(f"- status: {pretrained_env['status']}")
        print(f"- device: {pretrained_env['device']}")
        print(f"- message: {pretrained_env['message']}")
        print(f"- pytorch_home: {pretrained_env['pytorch_home']}")
        print(f"- pytorch_install: {pretrained_env['pytorch_install']}")
    if missing_user_inputs:
        print("Still need from user:")
        for item in missing_user_inputs:
            print(f"- {item}")
    print("Execution gate: only run after user replies with【确认无误，请执行】")
    print(f"Saved: {output_dir / 'labeling_plan.json'}")


if __name__ == "__main__":
    main()
