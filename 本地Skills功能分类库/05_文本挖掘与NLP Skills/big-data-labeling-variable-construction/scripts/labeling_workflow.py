import argparse
from pathlib import Path

from labeling_common import ensure_dir, save_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Recommend a labeling route and list only the truly necessary user inputs.")
    parser.add_argument("--task-description", required=True, help="User labeling request in natural language.")
    parser.add_argument(
        "--label-status",
        choices=["none", "partial", "labeled"],
        default="none",
        help="Whether labeled data already exists.",
    )
    parser.add_argument("--sample-size", type=int, default=0, help="Approximate sample size.")
    parser.add_argument("--need-topic-discovery", action="store_true", help="Need unsupervised topic discovery.")
    parser.add_argument("--need-highest-accuracy", action="store_true", help="Prefer stronger supervised models.")
    parser.add_argument("--use-api", action="store_true", help="Want to call a remote LLM API for labeling.")
    parser.add_argument("--output-dir", default="reports/labeling-workflow", help="Output directory.")
    return parser.parse_args()


def recommend_method(args: argparse.Namespace) -> dict:
    description = args.task_description.lower()
    if args.need_topic_discovery or "主题" in args.task_description or "topic" in description:
        return {
            "recommended_category": "LDA主题建模",
            "recommended_script": "scripts/lda_topic_model.py",
            "why": "当前目标更接近无监督主题发现，而不是监督分类标注。",
            "user_only_needs_to_provide": ["数据文件"],
            "auto_infer_or_default": ["文本列名", "文档ID列名", "候选主题数范围"],
        }
    if args.use_api or "大模型" in args.task_description or "openai" in description:
        return {
            "recommended_category": "调用大语言模型标注数据",
            "recommended_script": "scripts/openai_llm_labeling.py",
            "why": "当前需求更适合直接调用远程大模型进行初始标注。",
            "user_only_needs_to_provide": ["数据文件", "标签集合", "base_url", "api_key", "模型名称"],
            "auto_infer_or_default": ["文本列名", "文档ID列名", "系统提示词"],
        }
    if args.label_status == "labeled" and args.need_highest_accuracy:
        return {
            "recommended_category": "预训练模型",
            "recommended_script": "scripts/bert_labeling.py 或 scripts/ernie_labeling.py",
            "why": "你已经有标注数据，且更关注分类效果，优先考虑预训练模型微调。",
            "user_only_needs_to_provide": ["数据文件", "模型名称"],
            "auto_infer_or_default": ["文本列名", "标签列名", "文档ID列名", "训练测试比例", "epoch", "batch size"],
        }
    if args.label_status == "labeled":
        return {
            "recommended_category": "sklearn常见机器学习方法",
            "recommended_script": "scripts/sklearn_svm_labeling.py",
            "why": "你已经有标签，先跑轻量基线更稳，便于快速比较模型。",
            "user_only_needs_to_provide": ["数据文件"],
            "auto_infer_or_default": ["文本列名", "标签列名", "文档ID列名", "训练测试比例"],
        }
    return {
        "recommended_category": "调用大语言模型标注数据",
        "recommended_script": "scripts/openai_llm_labeling.py",
        "why": "当前没有标注集，先用大模型生成初始标签通常更实用。",
        "user_only_needs_to_provide": ["数据文件", "标签集合", "base_url", "api_key", "模型名称"],
        "auto_infer_or_default": ["文本列名", "文档ID列名", "系统提示词"],
    }


def main() -> None:
    args = parse_args()
    output_dir = ensure_dir(Path(args.output_dir))
    recommendation = recommend_method(args)
    payload = {
        "task_description": args.task_description,
        "label_status": args.label_status,
        "sample_size": args.sample_size,
        "need_topic_discovery": args.need_topic_discovery,
        "need_highest_accuracy": args.need_highest_accuracy,
        "use_api": args.use_api,
        **recommendation,
        "confirmation_phrase": "确认无误，请执行",
    }
    save_json(output_dir / "recommendation.json", payload)
    print(f"Recommended category: {payload['recommended_category']}")
    print(f"Recommended script: {payload['recommended_script']}")
    print(f"Why: {payload['why']}")
    print("User only needs to provide:")
    for item in payload["user_only_needs_to_provide"]:
        print(f"- {item}")
    print("The skill should auto infer or use defaults for:")
    for item in payload["auto_infer_or_default"]:
        print(f"- {item}")
    print(f"Confirmation phrase: {payload['confirmation_phrase']}")
    print(f"Saved: {output_dir / 'recommendation.json'}")


if __name__ == "__main__":
    main()
