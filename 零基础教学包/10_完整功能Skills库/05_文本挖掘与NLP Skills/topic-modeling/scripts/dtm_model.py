import argparse
import json
import os
import re
from contextlib import contextmanager
from pathlib import Path


def load_dataframe(path):
    try:
        import pandas as pd
    except ImportError as exc:
        raise SystemExit("Missing dependency: install pandas.") from exc
    suffix = Path(path).suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    raise SystemExit("DTM requires CSV or XLSX input with a time column.")


def read_stopwords(path):
    if not path:
        return set()
    return {line.strip() for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()}


def tokenize(texts, stopwords, tokenized):
    if tokenized:
        return [[w for w in str(text).split() if w and w not in stopwords] for text in texts]
    try:
        import jieba
    except ImportError as exc:
        raise SystemExit("Missing dependency: install jieba or pass --tokenized.") from exc
    output = []
    for text in texts:
        cleaned = re.sub(r"\s+", " ", str(text))
        output.append([w.strip() for w in jieba.lcut(cleaned) if w.strip() and w.strip() not in stopwords])
    return output


@contextmanager
def pushd(path):
    old = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old)


def main():
    parser = argparse.ArgumentParser(description="Train a gensim dynamic topic model with LdaSeqModel.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--text-column", required=True)
    parser.add_argument("--time-column", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--num-topics", type=int, required=True)
    parser.add_argument("--stopwords")
    parser.add_argument("--tokenized", action="store_true")
    parser.add_argument("--no-below", type=int, default=2)
    parser.add_argument("--no-above", type=float, default=0.8)
    parser.add_argument("--keep-n", type=int, default=50000)
    parser.add_argument("--passes", type=int, default=5)
    parser.add_argument("--topn", type=int, default=20)
    parser.add_argument("--random-state", type=int, default=42)
    args = parser.parse_args()

    try:
        import pandas as pd
        from gensim import corpora
        from gensim.models import LdaSeqModel
    except ImportError as exc:
        raise SystemExit("Missing dependency: install pandas and gensim.") from exc

    df = load_dataframe(args.input)
    if args.text_column not in df.columns or args.time_column not in df.columns:
        raise SystemExit(f"Columns not found. Available columns: {list(df.columns)}")
    data = df[[args.text_column, args.time_column]].dropna().copy()
    data[args.time_column] = data[args.time_column].astype(str)
    data = data.sort_values(args.time_column).reset_index(drop=True)
    time_values = data[args.time_column].drop_duplicates().tolist()
    time_slices = [int((data[args.time_column] == t).sum()) for t in time_values]

    tokenized = tokenize(data[args.text_column].astype(str).tolist(), read_stopwords(args.stopwords), args.tokenized)
    dictionary = corpora.Dictionary(tokenized)
    dictionary.filter_extremes(no_below=args.no_below, no_above=args.no_above, keep_n=args.keep_n)
    corpus = [dictionary.doc2bow(doc) for doc in tokenized]
    model = LdaSeqModel(
        corpus=corpus,
        time_slice=time_slices,
        id2word=dictionary,
        num_topics=args.num_topics,
        passes=args.passes,
        random_state=args.random_state,
    )

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    with pushd(out):
        model.save("dtm_model.gensim")
        dictionary.save("dictionary.gensim")
    (out / "time_slices.json").write_text(json.dumps({"time_values": time_values, "time_slices": time_slices}, ensure_ascii=False, indent=2), encoding="utf-8")

    topic_rows = []
    for time_index, time_value in enumerate(time_values):
        for topic_id in range(args.num_topics):
            terms = model.print_topic(topic=topic_id, time=time_index, top_terms=args.topn)
            for rank, item in enumerate(terms, start=1):
                word, weight = item if isinstance(item, tuple) else (str(item), None)
                topic_rows.append({"time": time_value, "topic_id": topic_id, "rank": rank, "word": word, "weight": weight})
    pd.DataFrame(topic_rows).to_csv(out / "topics_by_time.csv", index=False, encoding="utf-8-sig")

    doc_rows = []
    for doc_id in range(len(corpus)):
        probs = model.doc_topics(doc_id)
        for topic_id, prob in enumerate(probs):
            doc_rows.append({"doc_id": doc_id, "time": data.loc[doc_id, args.time_column], "topic_id": topic_id, "probability": float(prob)})
    pd.DataFrame(doc_rows).to_csv(out / "document_topics.csv", index=False, encoding="utf-8-sig")

    result = {"output_dir": str(out), "documents": len(data), "vocab_size": len(dictionary), "num_topics": args.num_topics, "time_slices": dict(zip(time_values, time_slices))}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
