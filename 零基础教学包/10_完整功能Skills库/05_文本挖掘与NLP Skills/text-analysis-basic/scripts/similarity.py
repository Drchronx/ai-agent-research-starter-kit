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


def pairwise_output(matrix, output_path):
    import pandas as pd
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(matrix).to_csv(output_path, index=False, encoding="utf-8-sig")


def score_two(method, text_a, text_b, embedding_model):
    if method == "jaccard":
        import jieba
        a = set(jieba.lcut(text_a))
        b = set(jieba.lcut(text_b))
        return len(a & b) / len(a | b) if (a | b) else 0.0
    if method == "tfidf":
        import jieba
        from gensim import corpora, models, matutils
        tokens = [list(jieba.lcut(text_a)), list(jieba.lcut(text_b))]
        dictionary = corpora.Dictionary(tokens)
        corpus = [dictionary.doc2bow(doc) for doc in tokens]
        tfidf_model = models.TfidfModel(corpus, dictionary=dictionary)
        tfidf_corpus = list(tfidf_model[corpus])
        return float(matutils.cossim(tfidf_corpus[0], tfidf_corpus[1]))
    from sklearn.metrics.pairwise import cosine_similarity
    if method == "bow":
        from sklearn.feature_extraction.text import CountVectorizer
        import jieba
        vectorizer = CountVectorizer(tokenizer=jieba.lcut, token_pattern=None)
        matrix = vectorizer.fit_transform([text_a, text_b])
        return float(cosine_similarity(matrix[0], matrix[1])[0, 0])
    if method == "embedding":
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(embedding_model)
        emb = model.encode([text_a, text_b], normalize_embeddings=True)
        return float(cosine_similarity([emb[0]], [emb[1]])[0, 0])
    raise SystemExit("Direct two-text scoring supports bow, tfidf, jaccard, and embedding.")


def pairwise(method, texts, embedding_model):
    if method == "tfidf":
        import numpy as np
        import jieba
        from gensim import corpora, models, matutils
        tokens = [list(jieba.lcut(text)) for text in texts]
        dictionary = corpora.Dictionary(tokens)
        corpus = [dictionary.doc2bow(doc) for doc in tokens]
        tfidf_model = models.TfidfModel(corpus, dictionary=dictionary)
        tfidf_corpus = list(tfidf_model[corpus])
        matrix = np.zeros((len(texts), len(texts)))
        for i, left in enumerate(tfidf_corpus):
            for j, right in enumerate(tfidf_corpus):
                matrix[i, j] = matutils.cossim(left, right)
        return matrix
    if method == "bow":
        from sklearn.metrics.pairwise import cosine_similarity
        from sklearn.feature_extraction.text import CountVectorizer
        import jieba
        matrix = CountVectorizer(tokenizer=jieba.lcut, token_pattern=None).fit_transform(texts)
        return cosine_similarity(matrix)
    if method == "jaccard":
        import numpy as np
        import jieba
        sets = [set(jieba.lcut(t)) for t in texts]
        matrix = np.zeros((len(sets), len(sets)))
        for i, a in enumerate(sets):
            for j, b in enumerate(sets):
                matrix[i, j] = len(a & b) / len(a | b) if (a | b) else 0.0
        return matrix
    if method == "embedding":
        from sklearn.metrics.pairwise import cosine_similarity
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(embedding_model)
        emb = model.encode(texts, normalize_embeddings=True, show_progress_bar=True)
        return cosine_similarity(emb)
    raise SystemExit("Pairwise mode supports bow, tfidf, jaccard, and embedding.")


def main():
    parser = argparse.ArgumentParser(description="Compute text similarity.")
    parser.add_argument("--method", choices=["bow", "tfidf", "jaccard", "embedding"], required=True)
    parser.add_argument("--text-a")
    parser.add_argument("--text-b")
    parser.add_argument("--input")
    parser.add_argument("--text-column")
    parser.add_argument("--output")
    parser.add_argument("--embedding-model", default="paraphrase-multilingual-MiniLM-L12-v2")
    args = parser.parse_args()

    if args.text_a is not None and args.text_b is not None:
        score = score_two(args.method, args.text_a, args.text_b, args.embedding_model)
        print(json.dumps({"method": args.method, "similarity": score}, ensure_ascii=False, indent=2))
        return

    if not args.input or not args.output:
        raise SystemExit("Use --text-a/--text-b for direct scoring, or --input/--output for pairwise matrix.")
    texts = load_texts(args.input, args.text_column)
    matrix = pairwise(args.method, texts, args.embedding_model)
    pairwise_output(matrix, Path(args.output))
    print(json.dumps({"method": args.method, "documents": len(texts), "output": args.output}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
