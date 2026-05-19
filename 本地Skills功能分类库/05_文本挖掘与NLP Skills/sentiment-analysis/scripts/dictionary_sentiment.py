import argparse
import json
from pathlib import Path


def load_table(path):
    try:
        import pandas as pd
    except ImportError as exc:
        raise SystemExit("Missing dependency: install pandas.") from exc
    suffix = Path(path).suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    raise SystemExit(f"Unsupported table input: {path}")


def load_texts(path, text_column=None):
    suffix = Path(path).suffix.lower()
    if suffix == ".txt":
        return None, [line.strip() for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
    df = load_table(path)
    col = text_column or ("text" if "text" in df.columns else None)
    if not col or col not in df.columns:
        raise SystemExit(f"Specify --text-column. Available columns: {list(df.columns)}")
    return df, df[col].fillna("").astype(str).tolist()


def read_word_list(path):
    if not path:
        return set()
    p = Path(path)
    if p.suffix.lower() in {".xlsx", ".xls", ".csv"}:
        df = load_table(p)
        col = "word" if "word" in df.columns else df.columns[0]
        return {str(x).strip() for x in df[col].dropna().tolist() if str(x).strip()}
    return {line.strip() for line in p.read_text(encoding="utf-8").splitlines() if line.strip()}


def read_scored_lexicon(path, word_column, score_column):
    if not path:
        return {}
    p = Path(path)
    if p.suffix.lower() in {".xlsx", ".xls", ".csv"}:
        df = load_table(p)
        wcol = word_column or ("word" if "word" in df.columns else df.columns[0])
        scol = score_column or ("score" if "score" in df.columns else df.columns[1])
        return {str(row[wcol]).strip(): float(row[scol]) for _, row in df[[wcol, scol]].dropna().iterrows()}
    scores = {}
    for line in p.read_text(encoding="utf-8").splitlines():
        parts = line.strip().split()
        if len(parts) >= 2:
            scores[parts[0]] = float(parts[1])
    return scores


def main():
    parser = argparse.ArgumentParser(description="Dictionary-based Chinese sentiment scoring.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--text-column")
    parser.add_argument("--positive-lexicon")
    parser.add_argument("--negative-lexicon")
    parser.add_argument("--scored-lexicon")
    parser.add_argument("--word-column")
    parser.add_argument("--score-column")
    parser.add_argument("--threshold-positive", type=float, default=0.0)
    parser.add_argument("--threshold-negative", type=float, default=0.0)
    args = parser.parse_args()

    try:
        import jieba
        import pandas as pd
    except ImportError as exc:
        raise SystemExit("Missing dependency: install jieba and pandas.") from exc

    df, texts = load_texts(args.input, args.text_column)
    scored = read_scored_lexicon(args.scored_lexicon, args.word_column, args.score_column)
    positive = read_word_list(args.positive_lexicon)
    negative = read_word_list(args.negative_lexicon)
    if not scored and not positive and not negative:
        raise SystemExit("Provide --scored-lexicon or --positive-lexicon/--negative-lexicon.")

    rows = []
    for text in texts:
        tokens = [t.strip() for t in jieba.lcut(text) if t.strip()]
        score = 0.0
        matched = []
        for token in tokens:
            if token in scored:
                score += scored[token]
                matched.append(f"{token}:{scored[token]}")
            elif token in positive:
                score += 1.0
                matched.append(f"{token}:1")
            elif token in negative:
                score -= 1.0
                matched.append(f"{token}:-1")
        if score > args.threshold_positive:
            label = "positive"
        elif score < -abs(args.threshold_negative):
            label = "negative"
        else:
            label = "neutral"
        rows.append({"sentiment_score": score, "sentiment_label": label, "matched_words": ";".join(matched)})

    result_df = pd.DataFrame(rows)
    if df is not None:
        result_df = pd.concat([df.reset_index(drop=True), result_df], axis=1)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result_df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(json.dumps({"rows": len(result_df), "output": str(output_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
