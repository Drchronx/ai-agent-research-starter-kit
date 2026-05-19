import argparse
import json
import os
import time
from pathlib import Path


def load_table(path, text_column=None):
    try:
        import pandas as pd
    except ImportError as exc:
        raise SystemExit("Missing dependency: install pandas.") from exc
    suffix = Path(path).suffix.lower()
    if suffix == ".txt":
        texts = [line.strip() for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
        return pd.DataFrame({"text": texts}), "text"
    if suffix == ".csv":
        df = pd.read_csv(path)
    elif suffix in {".xlsx", ".xls"}:
        df = pd.read_excel(path)
    else:
        raise SystemExit(f"Unsupported input: {path}")
    col = text_column or ("text" if "text" in df.columns else None)
    if not col or col not in df.columns:
        raise SystemExit(f"Specify --text-column. Available columns: {list(df.columns)}")
    return df, col


def classify(client, model, text, labels, temperature):
    prompt = (
        "You are a sentiment classifier. Return only JSON with keys "
        "`label`, `confidence`, and `reason`. "
        f"Allowed labels: {labels}. Text: {text}"
    )
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Classify sentiment accurately and concisely."},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
    )
    content = response.choices[0].message.content.strip()
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {"label": "parse_error", "confidence": 0, "reason": content}


def main():
    parser = argparse.ArgumentParser(description="LLM-based sentiment classification with an OpenAI-compatible API.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--text-column")
    parser.add_argument("--model", required=True)
    parser.add_argument("--base-url", help="OpenAI-compatible base URL.")
    parser.add_argument("--api-key-env", default="OPENAI_API_KEY")
    parser.add_argument("--labels", default="positive,negative,neutral")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--sleep", type=float, default=0.0)
    parser.add_argument("--max-rows", type=int, default=0)
    args = parser.parse_args()

    try:
        import pandas as pd
        from openai import OpenAI
    except ImportError as exc:
        raise SystemExit("Missing dependency: install openai and pandas.") from exc

    api_key = os.getenv(args.api_key_env)
    if not api_key:
        raise SystemExit(f"Missing API key environment variable: {args.api_key_env}")
    client = OpenAI(api_key=api_key, base_url=args.base_url) if args.base_url else OpenAI(api_key=api_key)
    df, col = load_table(args.input, args.text_column)
    if args.max_rows and args.max_rows > 0:
        df = df.head(args.max_rows).copy()
    labels = [x.strip() for x in args.labels.split(",") if x.strip()]

    outputs = []
    for text in df[col].fillna("").astype(str).tolist():
        outputs.append(classify(client, args.model, text, labels, args.temperature))
        if args.sleep:
            time.sleep(args.sleep)

    result = df.copy()
    parsed = pd.DataFrame(outputs)
    result = pd.concat([result.reset_index(drop=True), parsed.reset_index(drop=True)], axis=1)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(json.dumps({"rows": len(result), "output": str(output_path), "labels": labels}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
