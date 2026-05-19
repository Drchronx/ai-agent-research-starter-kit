import argparse
import csv
import json
import os
from contextlib import contextmanager
from pathlib import Path


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
    col = text_column or ("tokens" if "tokens" in df.columns else ("text" if "text" in df.columns else None))
    if not col or col not in df.columns:
        raise SystemExit(f"Specify --text-column. Available columns: {list(df.columns)}")
    return df[col].fillna("").astype(str).tolist()


def tokenize_texts(texts, tokenized):
    if tokenized:
        return [text.split() for text in texts]
    try:
        import jieba
    except ImportError as exc:
        raise SystemExit("Missing dependency: install jieba or pass --tokenized.") from exc
    return [list(jieba.lcut(text)) for text in texts]


@contextmanager
def pushd(path):
    old = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old)


def run_tfidf(texts, output_dir, max_features, tokenized):
    try:
        import pandas as pd
        from gensim import corpora, models
    except ImportError as exc:
        raise SystemExit("Missing dependency: install pandas and gensim.") from exc

    tokens = tokenize_texts(texts, tokenized)
    dictionary = corpora.Dictionary(tokens)
    if max_features and max_features > 0:
        dictionary.filter_extremes(no_below=1, no_above=1.0, keep_n=max_features)
        dictionary.compactify()
    corpus = [dictionary.doc2bow(doc) for doc in tokens]
    tfidf_model = models.TfidfModel(corpus, dictionary=dictionary)
    tfidf_corpus = list(tfidf_model[corpus])
    features = [dictionary[i] for i in range(len(dictionary))]
    rows = []
    for doc in tfidf_corpus:
        row = [0.0] * len(dictionary)
        for term_id, weight in doc:
            row[term_id] = float(weight)
        rows.append(row)
    pd.DataFrame(rows, columns=features).to_csv(output_dir / "tfidf_matrix.csv", index=False, encoding="utf-8-sig")
    with pushd(output_dir):
        dictionary.save("tfidf_dictionary.gensim")
        tfidf_model.save("tfidf_model.gensim")
    (output_dir / "tfidf_features.json").write_text(json.dumps(features, ensure_ascii=False, indent=2), encoding="utf-8")
    return {
        "matrix": str(output_dir / "tfidf_matrix.csv"),
        "features": str(output_dir / "tfidf_features.json"),
        "dictionary": str(output_dir / "tfidf_dictionary.gensim"),
        "model": str(output_dir / "tfidf_model.gensim"),
    }


def run_word2vec(texts, output_dir, vector_size, window, min_count, workers, epochs, tokenized):
    try:
        from gensim.models import Word2Vec
    except ImportError as exc:
        raise SystemExit("Missing dependency: install gensim.") from exc
    tokens = tokenize_texts(texts, tokenized)
    model = Word2Vec(sentences=tokens, vector_size=vector_size, window=window, min_count=min_count, workers=workers, sg=1, epochs=epochs)
    model_path = output_dir / "word2vec.model"
    vectors_path = output_dir / "word_vectors.csv"
    with pushd(output_dir):
        model.save("word2vec.model")
    with vectors_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["word"] + [f"dim_{i}" for i in range(vector_size)])
        for word in model.wv.index_to_key:
            writer.writerow([word] + list(map(float, model.wv[word])))
    return {"model": str(model_path), "vectors": str(vectors_path)}


def run_embedding(texts, output_dir, model_name):
    try:
        import numpy as np
        import pandas as pd
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise SystemExit("Missing dependency: install sentence-transformers, numpy, and pandas.") from exc
    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts, show_progress_bar=True, normalize_embeddings=True)
    np.save(output_dir / "embeddings.npy", embeddings)
    pd.DataFrame(embeddings).to_csv(output_dir / "embeddings.csv", index=False, encoding="utf-8-sig")
    return {"npy": str(output_dir / "embeddings.npy"), "csv": str(output_dir / "embeddings.csv"), "model_name": model_name}


def main():
    parser = argparse.ArgumentParser(description="Vectorize text with gensim TF-IDF, Word2Vec, or sentence embeddings.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--method", choices=["tfidf", "word2vec", "embedding"], required=True)
    parser.add_argument("--text-column")
    parser.add_argument("--tokenized", action="store_true")
    parser.add_argument("--max-features", type=int, default=5000)
    parser.add_argument("--vector-size", type=int, default=100)
    parser.add_argument("--window", type=int, default=5)
    parser.add_argument("--min-count", type=int, default=2)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--embedding-model", default="paraphrase-multilingual-MiniLM-L12-v2")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    texts = load_texts(args.input, args.text_column)
    if args.method == "tfidf":
        result = run_tfidf(texts, output_dir, args.max_features, args.tokenized)
    elif args.method == "word2vec":
        result = run_word2vec(texts, output_dir, args.vector_size, args.window, args.min_count, args.workers, args.epochs, args.tokenized)
    else:
        result = run_embedding(texts, output_dir, args.embedding_model)
    result.update({"documents": len(texts), "method": args.method, "output_dir": str(output_dir)})
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
