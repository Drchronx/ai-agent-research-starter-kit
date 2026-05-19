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
    if suffix == ".txt":
        return pd.DataFrame({"text": [line.strip() for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]})
    raise SystemExit(f"Unsupported input: {path}")


def build_classifier(method):
    try:
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.linear_model import LogisticRegression
        from sklearn.naive_bayes import MultinomialNB
        from sklearn.svm import LinearSVC
    except ImportError as exc:
        raise SystemExit("Missing dependency: install scikit-learn.") from exc

    if method == "tfidf-logreg":
        clf = LogisticRegression(max_iter=1000)
    elif method == "tfidf-svm":
        clf = LinearSVC()
    elif method == "tfidf-nb":
        clf = MultinomialNB()
    elif method == "tfidf-rf":
        clf = RandomForestClassifier(n_estimators=300, random_state=42, n_jobs=-1)
    else:
        raise SystemExit(f"Unsupported method: {method}")
    return clf


def segment_texts(texts):
    try:
        import jieba
    except ImportError as exc:
        raise SystemExit("Missing dependency: install jieba.") from exc
    return [" ".join(t.strip() for t in jieba.lcut(str(text)) if t.strip()) for text in texts]


def build_gensim_tfidf(segmented_texts, max_features):
    try:
        from gensim import corpora, models
    except ImportError as exc:
        raise SystemExit("Missing dependency: install gensim.") from exc
    tokenized = [text.split() for text in segmented_texts]
    dictionary = corpora.Dictionary(tokenized)
    if max_features and max_features > 0:
        dictionary.filter_extremes(no_below=1, no_above=1.0, keep_n=max_features)
        dictionary.compactify()
    corpus = [dictionary.doc2bow(tokens) for tokens in tokenized]
    tfidf_model = models.TfidfModel(corpus, dictionary=dictionary)
    return dictionary, tfidf_model, corpus


def corpus_to_csr(tfidf_corpus, num_terms):
    try:
        from scipy.sparse import csr_matrix
    except ImportError as exc:
        raise SystemExit("Missing dependency: install scipy.") from exc
    data = []
    rows = []
    cols = []
    for row_id, doc in enumerate(tfidf_corpus):
        for col_id, weight in doc:
            rows.append(row_id)
            cols.append(col_id)
            data.append(float(weight))
    return csr_matrix((data, (rows, cols)), shape=(len(tfidf_corpus), num_terms))


def transform_with_gensim_tfidf(segmented_texts, dictionary, tfidf_model):
    tokenized = [text.split() for text in segmented_texts]
    corpus = [dictionary.doc2bow(tokens) for tokens in tokenized]
    return corpus_to_csr(list(tfidf_model[corpus]), len(dictionary))


def train(args):
    try:
        import pandas as pd
        import joblib
        from sklearn.metrics import accuracy_score, classification_report
        from sklearn.model_selection import train_test_split
    except ImportError as exc:
        raise SystemExit("Missing dependency: install joblib, pandas, and scikit-learn.") from exc

    df = load_table(args.input)
    if args.text_column not in df.columns or args.label_column not in df.columns:
        raise SystemExit(f"Columns not found. Available columns: {list(df.columns)}")
    data = df[[args.text_column, args.label_column]].dropna()
    x_train, x_test, y_train, y_test = train_test_split(
        data[args.text_column].astype(str),
        data[args.label_column],
        test_size=args.test_size,
        random_state=args.random_state,
        stratify=data[args.label_column] if data[args.label_column].nunique() > 1 else None,
    )
    classifier = build_classifier(args.method)
    x_train_seg = segment_texts(x_train)
    x_test_seg = segment_texts(x_test)
    dictionary, tfidf_model, train_corpus = build_gensim_tfidf(x_train_seg, args.max_features)
    train_matrix = corpus_to_csr(list(tfidf_model[train_corpus]), len(dictionary))
    test_matrix = transform_with_gensim_tfidf(x_test_seg, dictionary, tfidf_model)
    classifier.fit(train_matrix, y_train)
    pred = classifier.predict(test_matrix)
    metrics = {
        "accuracy": float(accuracy_score(y_test, pred)),
        "classification_report": classification_report(y_test, pred, output_dict=True, zero_division=0),
        "method": args.method,
        "train_rows": int(len(x_train)),
        "test_rows": int(len(x_test)),
    }
    model_path = Path(args.model_output)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"dictionary": dictionary, "tfidf_model": tfidf_model, "classifier": classifier, "method": args.method}, model_path)
    metrics_path = Path(args.metrics_output) if args.metrics_output else model_path.with_suffix(".metrics.json")
    metrics_path.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"model": str(model_path), "metrics": str(metrics_path), "accuracy": metrics["accuracy"]}, ensure_ascii=False, indent=2))


def predict(args):
    try:
        import joblib
        import pandas as pd
    except ImportError as exc:
        raise SystemExit("Missing dependency: install joblib and pandas.") from exc

    df = load_table(args.input)
    col = args.text_column or ("text" if "text" in df.columns else None)
    if not col or col not in df.columns:
        raise SystemExit(f"Specify --text-column. Available columns: {list(df.columns)}")
    bundle = joblib.load(args.model)
    matrix = transform_with_gensim_tfidf(
        segment_texts(df[col].fillna("").astype(str)),
        bundle["dictionary"],
        bundle["tfidf_model"],
    )
    classifier = bundle["classifier"]
    pred = classifier.predict(matrix)
    out = df.copy()
    out["sentiment_label"] = pred
    if hasattr(classifier, "predict_proba"):
        proba = classifier.predict_proba(matrix)
        out["sentiment_confidence"] = proba.max(axis=1)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(json.dumps({"rows": len(out), "output": str(output_path)}, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Train or apply traditional ML sentiment classifiers.")
    sub = parser.add_subparsers(dest="command", required=True)

    train_p = sub.add_parser("train")
    train_p.add_argument("--input", required=True)
    train_p.add_argument("--text-column", required=True)
    train_p.add_argument("--label-column", required=True)
    train_p.add_argument("--method", choices=["tfidf-logreg", "tfidf-svm", "tfidf-nb", "tfidf-rf"], default="tfidf-logreg")
    train_p.add_argument("--model-output", required=True)
    train_p.add_argument("--metrics-output")
    train_p.add_argument("--max-features", type=int, default=8000)
    train_p.add_argument("--test-size", type=float, default=0.2)
    train_p.add_argument("--random-state", type=int, default=42)
    train_p.set_defaults(func=train)

    pred_p = sub.add_parser("predict")
    pred_p.add_argument("--model", required=True)
    pred_p.add_argument("--input", required=True)
    pred_p.add_argument("--text-column")
    pred_p.add_argument("--output", required=True)
    pred_p.set_defaults(func=predict)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
