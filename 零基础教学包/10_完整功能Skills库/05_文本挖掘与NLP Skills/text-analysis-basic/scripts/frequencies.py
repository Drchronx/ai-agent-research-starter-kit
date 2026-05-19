import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path


def read_stopwords(path):
    if not path:
        return set()
    return {line.strip() for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()}


def load_texts(path, text_column=None):
    suffix = Path(path).suffix.lower()
    if suffix == ".txt":
        return [line.strip() for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
    try:
        import pandas as pd
    except ImportError as exc:
        raise SystemExit("Missing dependency: install pandas for CSV/XLSX input.") from exc
    if suffix == ".csv":
        df = pd.read_csv(path)
    elif suffix in {".xlsx", ".xls"}:
        df = pd.read_excel(path)
    else:
        raise SystemExit(f"Unsupported input type: {path}")
    col = text_column or ("text" if "text" in df.columns else None)
    if not col or col not in df.columns:
        raise SystemExit(f"Specify --text-column. Available columns: {list(df.columns)}")
    return df[col].fillna("").astype(str).tolist()


def split_sentences(text):
    return [s.strip() for s in re.split(r"[。！？!?；;\n]+", text) if s.strip()]


def write_counter(counter, output_path, total, top_n):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = counter.most_common(top_n if top_n > 0 else None)
    with output_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["item", "count", "frequency"])
        for item, count in rows:
            writer.writerow([item, count, count / total if total else 0])


def main():
    parser = argparse.ArgumentParser(description="Count word or sentence frequencies.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--mode", choices=["word", "sentence"], required=True)
    parser.add_argument("--text-column", help="Text column for CSV/XLSX input.")
    parser.add_argument("--tokenized", action="store_true", help="Treat text as already tokenized by spaces.")
    parser.add_argument("--stopwords")
    parser.add_argument("--top-n", type=int, default=200)
    args = parser.parse_args()

    texts = load_texts(args.input, args.text_column)
    stopwords = read_stopwords(args.stopwords)
    counter = Counter()

    if args.mode == "word":
        if not args.tokenized:
            try:
                import jieba
            except ImportError as exc:
                raise SystemExit("Missing dependency: install jieba or pass --tokenized.") from exc
        for text in texts:
            tokens = text.split() if args.tokenized else jieba.lcut(text)
            counter.update(t for t in tokens if t.strip() and t.strip() not in stopwords)
    else:
        for text in texts:
            counter.update(split_sentences(text))

    total = sum(counter.values())
    write_counter(counter, Path(args.output), total, args.top_n)
    print(json.dumps({"unique_items": len(counter), "total_count": total, "output": args.output}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
