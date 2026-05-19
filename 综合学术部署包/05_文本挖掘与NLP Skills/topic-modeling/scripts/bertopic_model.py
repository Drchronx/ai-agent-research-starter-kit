import argparse
import json
from pathlib import Path


def load_texts(path, text_column=None):
    suffix = Path(path).suffix.lower()
    if suffix == ".txt":
        return [line.strip() for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
    try:
        import pandas as pd
    except ImportError as exc:
        raise SystemExit("Missing dependency: install pandas.") from exc
    if suffix == ".csv":
        df = pd.read_csv(path)
    elif suffix in {".xlsx", ".xls"}:
        df = pd.read_excel(path)
    else:
        raise SystemExit(f"Unsupported input: {path}")
    col = text_column or ("text" if "text" in df.columns else None)
    if not col or col not in df.columns:
        raise SystemExit(f"Specify --text-column. Available columns: {list(df.columns)}")
    return df[col].fillna("").astype(str).tolist()


def parse_nr_topics(value):
    if value is None or value.lower() == "none":
        return None
    if value.lower() == "auto":
        return "auto"
    return int(value)


def main():
    parser = argparse.ArgumentParser(description="Train BERTopic on Chinese text.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--text-column")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--embedding-model", default="paraphrase-multilingual-MiniLM-L12-v2")
    parser.add_argument("--min-topic-size", type=int, default=10)
    parser.add_argument("--nr-topics")
    parser.add_argument("--ngram-min", type=int, default=1)
    parser.add_argument("--ngram-max", type=int, default=2)
    parser.add_argument("--min-df", type=int, default=2)
    parser.add_argument("--calculate-probabilities", action="store_true")
    parser.add_argument("--vis-html", action="store_true")
    args = parser.parse_args()

    try:
        import jieba
        import pandas as pd
        from bertopic import BERTopic
        from sklearn.feature_extraction.text import CountVectorizer
    except ImportError as exc:
        raise SystemExit("Missing dependency: install bertopic, jieba, pandas, and scikit-learn.") from exc

    texts = load_texts(args.input, args.text_column)
    vectorizer_model = CountVectorizer(tokenizer=jieba.lcut, token_pattern=None, min_df=args.min_df, ngram_range=(args.ngram_min, args.ngram_max))
    topic_model = BERTopic(
        embedding_model=args.embedding_model,
        vectorizer_model=vectorizer_model,
        min_topic_size=args.min_topic_size,
        nr_topics=parse_nr_topics(args.nr_topics) if args.nr_topics else None,
        calculate_probabilities=args.calculate_probabilities,
    )
    topics, probabilities = topic_model.fit_transform(texts)

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    topic_model.save(str(out / "bertopic_model"))
    topic_model.get_topic_info().to_csv(out / "topics.csv", index=False, encoding="utf-8-sig")

    doc_rows = []
    for doc_id, topic_id in enumerate(topics):
        row = {"doc_id": doc_id, "topic_id": int(topic_id), "text": texts[doc_id]}
        if probabilities is not None:
            try:
                row["probability"] = float(max(probabilities[doc_id]))
            except Exception:
                pass
        doc_rows.append(row)
    pd.DataFrame(doc_rows).to_csv(out / "document_topics.csv", index=False, encoding="utf-8-sig")

    if args.vis_html:
        try:
            topic_model.visualize_topics().write_html(str(out / "bertopic_topics.html"))
            topic_model.visualize_barchart().write_html(str(out / "bertopic_barchart.html"))
        except Exception as exc:
            (out / "vis_error.txt").write_text(str(exc), encoding="utf-8")

    result = {"output_dir": str(out), "documents": len(texts), "topic_count": int(topic_model.get_topic_info().shape[0])}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
