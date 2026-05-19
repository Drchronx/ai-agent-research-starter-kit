import argparse
import json
from pathlib import Path


def read_stopwords(path):
    if not path:
        return set()
    return {line.strip() for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()}


def load_texts(path, text_column=None):
    suffix = Path(path).suffix.lower()
    if suffix == ".txt":
        return Path(path).read_text(encoding="utf-8")
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
    col = text_column or ("tokens" if "tokens" in df.columns else ("text" if "text" in df.columns else None))
    if not col or col not in df.columns:
        raise SystemExit(f"Specify --text-column. Available columns: {list(df.columns)}")
    return "\n".join(df[col].fillna("").astype(str).tolist())


def find_font(font):
    if font:
        return font
    for candidate in [Path.cwd() / "simhei.ttf", Path(__file__).resolve().parents[3] / "simhei.ttf"]:
        if candidate.exists():
            return str(candidate)
    raise SystemExit("Chinese word clouds require --font-path, or simhei.ttf in the course root.")


def main():
    parser = argparse.ArgumentParser(description="Generate a word cloud image.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--text-column", help="Text/token column for CSV/XLSX input.")
    parser.add_argument("--font-path")
    parser.add_argument("--stopwords")
    parser.add_argument("--width", type=int, default=1200)
    parser.add_argument("--height", type=int, default=800)
    parser.add_argument("--background-color", default="white")
    parser.add_argument("--max-words", type=int, default=300)
    parser.add_argument("--tokenized", action="store_true", help="Input text is already tokenized by spaces.")
    args = parser.parse_args()

    try:
        import jieba
        from wordcloud import WordCloud
    except ImportError as exc:
        raise SystemExit("Missing dependency: install jieba and wordcloud.") from exc

    raw = load_texts(args.input, args.text_column)
    stopwords = read_stopwords(args.stopwords)
    words = raw.split() if args.tokenized else jieba.lcut(raw)
    text = " ".join(w.strip() for w in words if w.strip() and w.strip() not in stopwords)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    wc = WordCloud(
        font_path=find_font(args.font_path),
        width=args.width,
        height=args.height,
        background_color=args.background_color,
        max_words=args.max_words,
    )
    wc.generate(text)
    wc.to_file(str(output_path))
    print(json.dumps({"output": str(output_path), "max_words": args.max_words}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
