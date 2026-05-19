import argparse
import json
from pathlib import Path

import pandas as pd

from labeling_common import ensure_dir, load_table, require_columns


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Label text data with an OpenAI-compatible large language model.")
    parser.add_argument("input_path", help="CSV or Excel file containing text data.")
    parser.add_argument("--text-col", default="text", help="Text column name.")
    parser.add_argument("--id-col", default="doc_id", help="Document id column.")
    parser.add_argument("--output-col", default="predicted_label", help="Predicted label column name.")
    parser.add_argument("--labels", required=True, help="Comma-separated candidate labels.")
    parser.add_argument("--base-url", required=True, help="OpenAI-compatible base_url.")
    parser.add_argument("--api-key", required=True, help="API key.")
    parser.add_argument("--model", required=True, help="Model name.")
    parser.add_argument("--system-prompt", default="你是一个严格的中文文本标注助手，只返回 JSON。", help="System prompt.")
    parser.add_argument("--batch-size", type=int, default=1, help="Reserved for future batching. Currently only 1 is supported.")
    parser.add_argument("--max-samples", type=int, help="Only label the first N rows for smoke testing.")
    parser.add_argument("--output-dir", required=True, help="Output directory.")
    return parser.parse_args()


def build_user_prompt(text: str, labels: list[str]) -> str:
    return (
        "请在给定标签集中为文本选择最合适的一个标签，并给出简短理由。"
        "只返回 JSON，格式为"
        '{"label":"标签","reason":"一句话理由"}。'
        f"\n标签集：{labels}\n文本：{text}"
    )


def main() -> None:
    from openai import OpenAI

    args = parse_args()
    if args.batch_size != 1:
        raise ValueError("Current version only supports batch-size 1.")

    output_dir = ensure_dir(Path(args.output_dir))
    df = load_table(Path(args.input_path)).copy()
    require_columns(df, [args.text_col])
    if args.id_col not in df.columns:
        df[args.id_col] = range(1, len(df) + 1)

    if args.max_samples:
        df = df.head(args.max_samples).copy()

    labels = [item.strip() for item in args.labels.split(",") if item.strip()]
    if len(labels) < 2:
        raise ValueError("At least two labels must be provided.")

    client = OpenAI(base_url=args.base_url, api_key=args.api_key)
    rows = []
    for _, row in df.iterrows():
        completion = client.chat.completions.create(
            model=args.model,
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": args.system_prompt},
                {"role": "user", "content": build_user_prompt(str(row[args.text_col]), labels)},
            ],
        )
        payload = json.loads(completion.choices[0].message.content)
        rows.append(
            {
                args.id_col: row[args.id_col],
                args.text_col: row[args.text_col],
                args.output_col: payload.get("label", ""),
                "reason": payload.get("reason", ""),
            }
        )

    result = pd.DataFrame(rows)
    result_path = output_dir / "llm_labeled_output.csv"
    result.to_csv(result_path, index=False, encoding="utf-8-sig")
    summary = {
        "method": "openai_llm_labeling",
        "model": args.model,
        "base_url": args.base_url,
        "sample_count": int(len(result)),
        "labels": labels,
        "output_file": str(result_path),
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Labeled output: {result_path}")
    print(f"Summary: {output_dir / 'summary.json'}")


if __name__ == "__main__":
    main()
