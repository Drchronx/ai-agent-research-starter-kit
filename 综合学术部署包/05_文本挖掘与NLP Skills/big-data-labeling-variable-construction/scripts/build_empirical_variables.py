import argparse
import json
import re
from pathlib import Path

import jieba
import pandas as pd
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer


POSITIVE_WORDS = {"增长", "提升", "改善", "创新", "突破", "稳健", "领先", "优化"}
NEGATIVE_WORDS = {"风险", "压力", "下降", "波动", "受限", "减弱", "亏损", "不确定"}
CATEGORY_LEXICONS = {
    "innovation": {"创新", "研发", "专利", "技术", "数字化"},
    "risk": {"风险", "压力", "不确定", "债务", "波动"},
    "policy": {"政策", "补贴", "监管", "政府", "扶持"},
    "governance": {"治理", "董事会", "内控", "审计", "股东"},
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Label text data, run topic extraction, and build empirical variables.")
    parser.add_argument("input_path", help="CSV or Excel file containing text documents.")
    parser.add_argument("--text-col", default="text", help="Text column name.")
    parser.add_argument("--id-col", default="doc_id", help="Document id column.")
    parser.add_argument("--topics", type=int, default=3, help="Number of NMF topics.")
    parser.add_argument("--output-dir", default="reports/empirical-variables", help="Output directory.")
    return parser.parse_args()


def load_data(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    raise ValueError(f"Unsupported file type: {path.suffix}")


def tokenize(text: str) -> list[str]:
    words = [word.strip() for word in jieba.lcut(str(text)) if word.strip()]
    return [word for word in words if re.search(r"[\u4e00-\u9fffA-Za-z0-9]", word)]


def sentiment_metrics(tokens: list[str]) -> dict[str, float]:
    pos = sum(1 for token in tokens if token in POSITIVE_WORDS)
    neg = sum(1 for token in tokens if token in NEGATIVE_WORDS)
    total = max(len(tokens), 1)
    return {"positive_count": pos, "negative_count": neg, "sentiment_score": round((pos - neg) / total, 6)}


def category_metrics(tokens: list[str]) -> dict[str, int]:
    token_set = set(tokens)
    return {f"{name}_label": int(bool(token_set.intersection(words))) for name, words in CATEGORY_LEXICONS.items()}


def build_topic_outputs(df: pd.DataFrame, text_col: str, topic_count: int, output_dir: Path) -> tuple[pd.DataFrame, Path]:
    vectorizer = TfidfVectorizer(tokenizer=tokenize, token_pattern=None, lowercase=False, min_df=1, max_df=0.95)
    matrix = vectorizer.fit_transform(df[text_col].astype(str))
    model = NMF(n_components=min(topic_count, max(1, matrix.shape[0])), random_state=42, init="nndsvda", max_iter=400)
    doc_topics = model.fit_transform(matrix)
    feature_names = vectorizer.get_feature_names_out()

    topic_keywords: dict[str, list[str]] = {}
    for topic_index, topic in enumerate(model.components_):
        top_indices = topic.argsort()[::-1][:8]
        topic_keywords[f"topic_{topic_index + 1}"] = [feature_names[i] for i in top_indices]

    keywords_path = output_dir / "topic_keywords.json"
    keywords_path.write_text(json.dumps(topic_keywords, ensure_ascii=False, indent=2), encoding="utf-8")
    topic_columns = [f"topic_{i + 1}_weight" for i in range(doc_topics.shape[1])]
    topic_df = pd.DataFrame(doc_topics, columns=topic_columns)
    return topic_df, keywords_path


def build_summary(df: pd.DataFrame, output_dir: Path) -> Path:
    summary_lines = [
        "# Empirical Variable Construction Summary",
        "",
        f"- Documents processed: {len(df)}",
        f"- Mean sentiment score: {df['sentiment_score'].mean():.4f}",
        f"- Innovation label share: {df['innovation_label'].mean():.2%}",
        f"- Risk label share: {df['risk_label'].mean():.2%}",
        f"- Policy label share: {df['policy_label'].mean():.2%}",
        f"- Governance label share: {df['governance_label'].mean():.2%}",
    ]
    summary_path = output_dir / "summary.md"
    summary_path.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")
    return summary_path


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = load_data(Path(args.input_path)).copy()
    if args.text_col not in df.columns or args.id_col not in df.columns:
        raise ValueError(f"Input must contain '{args.id_col}' and '{args.text_col}' columns.")

    df["tokens"] = df[args.text_col].astype(str).apply(tokenize)
    sentiment_df = df["tokens"].apply(sentiment_metrics).apply(pd.Series)
    category_df = df["tokens"].apply(category_metrics).apply(pd.Series)
    topic_df, keywords_path = build_topic_outputs(df, args.text_col, args.topics, output_dir)

    result = pd.concat([df[[args.id_col, args.text_col]], sentiment_df, category_df, topic_df], axis=1)
    result["token_count"] = df["tokens"].apply(len)
    enriched_path = output_dir / "enriched_documents.csv"
    result.to_csv(enriched_path, index=False, encoding="utf-8-sig")

    summary_path = build_summary(result, output_dir)

    print(f"Enriched dataset: {enriched_path}")
    print(f"Topic keywords: {keywords_path}")
    print(f"Summary: {summary_path}")


if __name__ == "__main__":
    main()
