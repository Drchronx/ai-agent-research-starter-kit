import argparse
import json
from pathlib import Path


def read_stopwords(path):
    if not path:
        return set()
    return {line.strip() for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()}


def cut_text(text, mode):
    import jieba
    if mode == "full":
        return list(jieba.cut(text, cut_all=True))
    if mode == "search":
        return list(jieba.cut_for_search(text))
    return list(jieba.cut(text, cut_all=False))


def load_dataframe(path):
    try:
        import pandas as pd
    except ImportError as exc:
        raise SystemExit("Missing dependency: install pandas for CSV/XLSX input.") from exc
    suffix = Path(path).suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    raise SystemExit(f"Unsupported table input: {path}")


def main():
    parser = argparse.ArgumentParser(description="Segment Chinese text with jieba.")
    parser.add_argument("--input", required=True, help="Input .txt/.csv/.xlsx file.")
    parser.add_argument("--output", required=True, help="Output .txt/.csv/.jsonl file.")
    parser.add_argument("--text-column", help="Text column for CSV/XLSX input.")
    parser.add_argument("--mode", choices=["precise", "full", "search"], default="precise")
    parser.add_argument("--user-dict", help="jieba custom dictionary path.")
    parser.add_argument("--stopwords", help="Stopword file path.")
    parser.add_argument("--separator", default=" ", help="Token separator.")
    args = parser.parse_args()

    try:
        import jieba
    except ImportError as exc:
        raise SystemExit("Missing dependency: install jieba.") from exc

    if args.user_dict:
        jieba.load_userdict(args.user_dict)
    stopwords = read_stopwords(args.stopwords)
    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    suffix = input_path.suffix.lower()

    def tokenize(value):
        tokens = [t.strip() for t in cut_text(str(value), args.mode)]
        return [t for t in tokens if t and t not in stopwords]

    if suffix == ".txt":
        lines = input_path.read_text(encoding="utf-8").splitlines()
        tokenized = [args.separator.join(tokenize(line)) for line in lines if line.strip()]
        output_path.write_text("\n".join(tokenized) + "\n", encoding="utf-8")
        print(json.dumps({"rows": len(tokenized), "output": str(output_path)}, ensure_ascii=False, indent=2))
        return

    df = load_dataframe(input_path)
    text_col = args.text_column or ("text" if "text" in df.columns else None)
    if not text_col or text_col not in df.columns:
        raise SystemExit(f"Specify --text-column. Available columns: {list(df.columns)}")
    df["tokens"] = df[text_col].fillna("").map(lambda x: args.separator.join(tokenize(x)))
    if output_path.suffix.lower() == ".jsonl":
        records = df.to_dict(orient="records")
        output_path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n", encoding="utf-8")
    else:
        df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(json.dumps({"rows": len(df), "output": str(output_path), "token_column": "tokens"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
