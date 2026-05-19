import argparse
import ast
import json
import math
import os
import re
from contextlib import contextmanager
from pathlib import Path


def load_texts(path, text_column=None):
    suffix = Path(path).suffix.lower()
    if suffix == ".txt":
        return [line.strip() for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()], None
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
    col = text_column or infer_text_column(df.columns)
    if not col or col not in df.columns:
        raise SystemExit(f"Specify --text-column. Available columns: {list(df.columns)}")
    return df[col].fillna("").astype(str).tolist(), col


def infer_text_column(columns):
    priority = [
        "tokens",
        "text",
        "content",
        "abstract",
        "summary",
        "review",
        "comment",
        "\u6b63\u6587",
        "\u5185\u5bb9",
        "\u6458\u8981",
        "\u6587\u672c",
        "\u8bc4\u8bba",
    ]
    lower_map = {str(col).lower(): col for col in columns}
    for name in priority:
        if name in columns:
            return name
        if name.lower() in lower_map:
            return lower_map[name.lower()]
    return None


def read_stopwords(path):
    if not path:
        return set()
    return {line.strip() for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()}


def auto_stopwords_path():
    candidates = [
        Path("stopwords/hit_stopwords.txt"),
        Path("stopwords/cn_stopwords.txt"),
        Path("stopwords/baidu_stopwords.txt"),
        Path("stopwords/scu_stopwords.txt"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    stopword_dir = Path("stopwords")
    if stopword_dir.exists():
        txt_files = sorted(stopword_dir.glob("*.txt"))
        if txt_files:
            return txt_files[0]
    return None


def parse_tokenized_text(text):
    stripped = str(text).strip()
    if not stripped:
        return []
    if stripped.startswith("[") and stripped.endswith("]"):
        try:
            value = ast.literal_eval(stripped)
            if isinstance(value, list):
                return [str(item).strip() for item in value if str(item).strip()]
        except (SyntaxError, ValueError):
            pass
    return [item.strip() for item in re.split(r"\s+", stripped) if item.strip()]


def opencc_converter(config):
    if not config or config.lower() == "none":
        return None
    try:
        from opencc import OpenCC
    except ImportError as exc:
        raise SystemExit("Missing dependency: install opencc or pass --opencc none.") from exc
    return OpenCC(config)


def normalize_text(text, converter, args):
    if not isinstance(text, str):
        return ""
    if converter is not None:
        text = converter.convert(text)
    if args.lowercase_english:
        text = text.lower()
    if args.clean_text:
        text = re.sub(r"[^\u4e00-\u9fa5a-zA-Z]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def tokenize(texts, stopwords, tokenized, args):
    if tokenized:
        return [
            [
                w
                for w in parse_tokenized_text(text)
                if w not in stopwords and len(w.strip()) >= args.min_token_length
            ]
            for text in texts
        ]
    try:
        import jieba
    except ImportError as exc:
        raise SystemExit("Missing dependency: install jieba or pass --tokenized.") from exc
    converter = opencc_converter(args.opencc)
    output = []
    for text in texts:
        cleaned = normalize_text(text, converter, args)
        output.append(
            [
                w.strip()
                for w in jieba.lcut(cleaned)
                if w.strip()
                and w.strip() not in stopwords
                and len(w.strip()) >= args.min_token_length
            ]
        )
    return output


@contextmanager
def pushd(path):
    old = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old)


def parse_model_value(value):
    if value is None:
        return None
    lowered = str(value).lower()
    if lowered in {"auto", "symmetric", "asymmetric"}:
        return lowered
    try:
        return float(value)
    except ValueError as exc:
        raise SystemExit(f"Invalid alpha/eta value: {value}") from exc


def resolve_alpha(alpha, num_topics):
    lowered = str(alpha).lower()
    if lowered in {"scaled", "50/k", "50/num_topics"}:
        return 50 / num_topics
    return parse_model_value(alpha)


def resolve_topic_values(args, doc_count, vocab_size):
    topic_min = max(1, args.topic_min)
    if args.topic_max is None:
        auto_max = min(20, max(topic_min, doc_count, vocab_size))
        if doc_count >= 2:
            auto_max = min(auto_max, max(topic_min, doc_count))
        topic_max = auto_max
    else:
        topic_max = max(topic_min, args.topic_max)
    return list(range(topic_min, topic_max + 1, max(1, args.topic_step)))


def prepare_corpus(tokenized, args):
    from gensim import corpora, models

    dictionary = corpora.Dictionary(tokenized)
    if args.no_below > 1 or args.no_above < 1.0 or args.keep_n:
        dictionary.filter_extremes(no_below=args.no_below, no_above=args.no_above, keep_n=args.keep_n)
    dictionary.compactify()
    if len(dictionary) == 0:
        raise SystemExit("Dictionary is empty after filtering. Lower --no-below or raise --no-above.")
    bow_corpus = [dictionary.doc2bow(doc) for doc in tokenized]
    tfidf_model = models.TfidfModel(bow_corpus, dictionary=dictionary)
    tfidf_corpus = list(tfidf_model[bow_corpus])
    train_corpus = tfidf_corpus if args.corpus_weighting == "tfidf" else bow_corpus
    return dictionary, bow_corpus, tfidf_model, tfidf_corpus, train_corpus


def train_lda(num_topics, train_corpus, dictionary, args):
    from gensim.models import LdaModel

    return LdaModel(
        corpus=train_corpus,
        id2word=dictionary,
        num_topics=num_topics,
        passes=args.passes,
        iterations=args.iterations,
        alpha=resolve_alpha(args.alpha, num_topics),
        eta=parse_model_value(args.eta),
        random_state=args.random_state,
    )


def compute_metrics(model, train_corpus, bow_corpus, tokenized, dictionary):
    from gensim.models import CoherenceModel

    metrics = {}
    try:
        log_perplexity = float(model.log_perplexity(train_corpus))
        metrics["log_perplexity"] = log_perplexity
        metrics["perplexity"] = float(math.pow(2, -log_perplexity))
    except Exception as exc:
        metrics["perplexity_error"] = str(exc)
    try:
        cv = CoherenceModel(model=model, texts=tokenized, dictionary=dictionary, coherence="c_v")
        metrics["coherence_c_v"] = float(cv.get_coherence())
    except Exception as exc:
        metrics["coherence_c_v_error"] = str(exc)
    try:
        umass = CoherenceModel(model=model, corpus=bow_corpus, dictionary=dictionary, coherence="u_mass")
        metrics["coherence_u_mass"] = float(umass.get_coherence())
    except Exception as exc:
        metrics["coherence_u_mass_error"] = str(exc)
    return metrics


def topic_words_rows(model, num_topics, topn):
    rows = []
    for topic_id in range(num_topics):
        for rank, (word, weight) in enumerate(model.show_topic(topic_id, topn=topn), start=1):
            rows.append({"topic_id": topic_id, "rank": rank, "word": word, "weight": float(weight)})
    return rows


def save_topic_words(model, num_topics, topn, output_path):
    import pandas as pd

    rows = topic_words_rows(model, num_topics, topn)
    pd.DataFrame(rows).to_csv(output_path, index=False, encoding="utf-8-sig")


def plot_selection_metrics(metrics_df, output_dir, topic_min, topic_max):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError as exc:
        (output_dir / "plot_error.txt").write_text(f"Missing matplotlib: {exc}", encoding="utf-8")
        return []

    outputs = []
    x = metrics_df["num_topics"].tolist()
    log_perplexity = metrics_df["log_perplexity"].tolist()
    coherence = metrics_df["coherence_c_v"].tolist()

    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.set_xlabel("Number of Topics")
    ax1.set_ylabel("Gensim log_perplexity (higher is better)")
    ax1.plot(x, log_perplexity, linestyle="--", marker="o", color="red")
    ax1.grid(True, alpha=0.3)
    ax2 = ax1.twinx()
    ax2.set_ylabel("Coherence C_V")
    ax2.plot(x, coherence, marker="o", color="blue")
    plt.title("LDA Model Performance: Log Perplexity and Coherence")
    fig.tight_layout()
    combined = output_dir / f"lda_metrics_combined_{topic_min}_{topic_max}.png"
    plt.savefig(combined, dpi=300, bbox_inches="tight")
    plt.close(fig)
    outputs.append(str(combined))

    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(1, 2, 1)
    ax.plot(x, log_perplexity, linestyle="--", marker="o", color="red")
    ax.set_title("LDA Log Perplexity")
    ax.set_xlabel("Number of Topics")
    ax.set_ylabel("Gensim log_perplexity (higher is better)")
    ax.grid(True, alpha=0.3)
    ax = fig.add_subplot(1, 2, 2)
    ax.plot(x, coherence, marker="o", color="blue")
    ax.set_title("Topic Coherence C_V")
    ax.set_xlabel("Number of Topics")
    ax.set_ylabel("Coherence C_V")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    separate = output_dir / f"lda_metrics_separate_{topic_min}_{topic_max}.png"
    plt.savefig(separate, dpi=300, bbox_inches="tight")
    plt.close(fig)
    outputs.append(str(separate))

    return outputs


def save_pyldavis(model, train_corpus, dictionary, output_path):
    try:
        import pyLDAvis
        import pyLDAvis.gensim_models as gensimvis
        vis = gensimvis.prepare(model, train_corpus, dictionary)
        pyLDAvis.save_html(vis, str(output_path))
        return {"pyldavis_html": str(output_path)}
    except Exception as exc:
        error_path = output_path.with_name("pyldavis_error.txt")
        error_path.write_text(str(exc), encoding="utf-8")
        return {"pyldavis_error": str(error_path)}


def write_selection_report(summary, metrics_df, selection_dir):
    lines = [
        "# LDA Topic Count Selection Report",
        "",
        "This report is diagnostic only. Do not treat the recommendation as the final decision without user review.",
        "",
        "## Machine Recommendation",
        "",
        f"- Recommended by coherence C_V: {summary['recommended_num_topics']}",
        f"- Highest course-style log_perplexity: {summary['best_log_perplexity_num_topics']}",
        f"- Lowest converted perplexity: {summary['best_perplexity_num_topics']}",
        f"- Rule: {summary['recommendation_rule']}",
        f"- Note: {summary['perplexity_note']}",
        "",
        "## What the User Should Review",
        "",
        "- Review the metrics CSV and the two metric plots.",
        "- Compare candidate topic word tables for interpretability.",
        "- Open candidate pyLDAvis HTML files if they were generated.",
        "- Choose the final topic count based on domain meaning, not only the numeric recommendation.",
        "",
        "## Generated Files",
        "",
        f"- Metrics CSV: `{summary['metrics_csv']}`",
        f"- Candidate topic words: `{summary['candidate_topics_dir']}`",
        f"- Candidate visualizations: `{summary['candidate_visualizations_dir']}`",
    ]
    for plot in summary["plots"]:
        lines.append(f"- Plot: `{plot}`")

    lines.extend(["", "## Metrics Preview", ""])
    preview_cols = [col for col in ["num_topics", "log_perplexity", "perplexity", "coherence_c_v", "coherence_u_mass"] if col in metrics_df.columns]
    lines.append("| " + " | ".join(preview_cols) + " |")
    lines.append("| " + " | ".join(["---"] * len(preview_cols)) + " |")
    for _, row in metrics_df[preview_cols].iterrows():
        values = []
        for col in preview_cols:
            value = row[col]
            if isinstance(value, float):
                values.append(f"{value:.6g}")
            else:
                values.append(str(value))
        lines.append("| " + " | ".join(values) + " |")
    lines.append("")
    lines.append("## Next Command After User Chooses")
    lines.append("")
    lines.append("Run final training with the selected K:")
    lines.append("")
    lines.append("```bash")
    lines.append('python scripts/lda_model.py --input "..." --text-column "..." --output-dir "..." --num-topics K')
    lines.append("```")
    report_path = selection_dir / "topic_selection_report.md"
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return str(report_path)


def select_topics(topic_values, train_corpus, bow_corpus, tokenized, dictionary, output_dir, args):
    import pandas as pd

    selection_dir = output_dir / "topic_selection"
    topics_dir = selection_dir / "candidate_topics"
    models_dir = selection_dir / "candidate_models"
    vis_dir = selection_dir / "candidate_visualizations"
    topics_dir.mkdir(parents=True, exist_ok=True)
    vis_dir.mkdir(parents=True, exist_ok=True)
    if args.save_selection_models:
        models_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    candidate_models = {}
    for num_topics in topic_values:
        model = train_lda(num_topics, train_corpus, dictionary, args)
        candidate_models[num_topics] = model
        metrics = compute_metrics(model, train_corpus, bow_corpus, tokenized, dictionary)
        row = {"num_topics": num_topics, **metrics}
        rows.append(row)
        save_topic_words(model, num_topics, args.topn, topics_dir / f"topics_k_{num_topics}.csv")
        if args.save_selection_models:
            model_dir = models_dir / f"k_{num_topics}"
            model_dir.mkdir(parents=True, exist_ok=True)
            with pushd(model_dir):
                model.save("lda_model.gensim")
        print(json.dumps(row, ensure_ascii=False))

    metrics_df = pd.DataFrame(rows)
    metrics_df.to_csv(selection_dir / "lda_topic_selection_metrics.csv", index=False, encoding="utf-8-sig")
    topic_min = min(topic_values)
    topic_max = max(topic_values)
    plots = plot_selection_metrics(metrics_df, selection_dir, topic_min, topic_max)

    valid_cv = metrics_df.dropna(subset=["coherence_c_v"]) if "coherence_c_v" in metrics_df.columns else metrics_df.iloc[0:0]
    if not valid_cv.empty:
        best_cv_row = valid_cv.sort_values(["coherence_c_v", "num_topics"], ascending=[False, True]).iloc[0]
        recommended = int(best_cv_row["num_topics"])
    else:
        recommended = int(metrics_df.iloc[0]["num_topics"])

    valid_log_perp = metrics_df.dropna(subset=["log_perplexity"]) if "log_perplexity" in metrics_df.columns else metrics_df.iloc[0:0]
    best_log_perplexity_topics = None
    if not valid_log_perp.empty:
        best_log_perplexity_topics = int(valid_log_perp.sort_values(["log_perplexity", "num_topics"], ascending=[False, True]).iloc[0]["num_topics"])

    valid_perp = metrics_df.dropna(subset=["perplexity"]) if "perplexity" in metrics_df.columns else metrics_df.iloc[0:0]
    best_perplexity_topics = None
    if not valid_perp.empty:
        best_perplexity_topics = int(valid_perp.sort_values(["perplexity", "num_topics"], ascending=[True, True]).iloc[0]["num_topics"])

    visual_topics = []
    if args.candidate_vis_top_n > 0:
        if not valid_cv.empty:
            visual_topics.extend(
                int(row["num_topics"])
                for _, row in valid_cv.sort_values(["coherence_c_v", "num_topics"], ascending=[False, True]).head(args.candidate_vis_top_n).iterrows()
            )
        if best_log_perplexity_topics is not None:
            visual_topics.append(best_log_perplexity_topics)
    skipped_visual_topics = [
        {"num_topics": int(num_topics), "reason": "pyLDAvis is not meaningful for a one-topic model"}
        for num_topics in sorted(set(visual_topics))
        if int(num_topics) < 2
    ]
    visual_topics = sorted({int(num_topics) for num_topics in visual_topics if int(num_topics) >= 2})

    candidate_visualizations = []
    for num_topics in visual_topics:
        result = save_pyldavis(candidate_models[num_topics], train_corpus, dictionary, vis_dir / f"lda_k_{num_topics}.html")
        candidate_visualizations.append({"num_topics": num_topics, **result})

    summary = {
        "recommended_num_topics": recommended,
        "recommendation_rule": "diagnostic suggestion only: max coherence_c_v; tie-breaker smaller num_topics; user must choose final K",
        "best_log_perplexity_num_topics": best_log_perplexity_topics,
        "best_perplexity_num_topics": best_perplexity_topics,
        "perplexity_note": "Metric plots use gensim log_perplexity to match the course notebook. Higher log_perplexity is better; lower converted perplexity = 2 ** (-log_perplexity) is better. Use both only as diagnostics and let the user choose final K.",
        "topic_values": topic_values,
        "metrics_csv": str(selection_dir / "lda_topic_selection_metrics.csv"),
        "plots": plots,
        "candidate_topics_dir": str(topics_dir),
        "candidate_visualizations_dir": str(vis_dir),
        "candidate_visualizations": candidate_visualizations,
        "skipped_candidate_visualizations": skipped_visual_topics,
        "candidate_models_dir": str(models_dir) if args.save_selection_models else None,
        "model_parameters": {
            "corpus_weighting": args.corpus_weighting,
            "alpha": "50/num_topics" if str(args.alpha).lower() in {"scaled", "50/k", "50/num_topics"} else args.alpha,
            "eta": args.eta,
            "passes": args.passes,
            "iterations": args.iterations,
            "random_state": args.random_state,
        },
    }
    summary["report_md"] = write_selection_report(summary, metrics_df, selection_dir)
    (selection_dir / "topic_selection_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def save_preprocessed(texts, tokenized, output_dir):
    import pandas as pd

    rows = [
        {"doc_id": i, "text": text, "tokens": " ".join(tokens), "token_count": len(tokens)}
        for i, (text, tokens) in enumerate(zip(texts, tokenized))
    ]
    pd.DataFrame(rows).to_csv(output_dir / "preprocessed_tokens.csv", index=False, encoding="utf-8-sig")


def save_preprocessing_config(args, output_dir, original_count, valid_count, stopwords_path, stopwords_count, used_text_column):
    config = {
        "original_documents": original_count,
        "valid_documents_after_preprocessing": valid_count,
        "text_column": used_text_column,
        "stopwords_path": str(stopwords_path) if stopwords_path else None,
        "stopwords_count": stopwords_count,
        "tokenized_input": bool(args.tokenized),
        "clean_text": bool(args.clean_text),
        "opencc": args.opencc,
        "lowercase_english": bool(args.lowercase_english),
        "min_token_length": args.min_token_length,
        "dictionary_filter": {
            "no_below": args.no_below,
            "no_above": args.no_above,
            "keep_n": args.keep_n,
        },
        "corpus_weighting": args.corpus_weighting,
        "lda_parameters": {
            "alpha": "50/num_topics" if str(args.alpha).lower() in {"scaled", "50/k", "50/num_topics"} else args.alpha,
            "eta": args.eta,
            "passes": args.passes,
            "iterations": args.iterations,
            "random_state": args.random_state,
        },
    }
    (output_dir / "preprocessing_config.json").write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")


def save_final_outputs(model, num_topics, texts, train_corpus, bow_corpus, tokenized, dictionary, output_dir, args, selection_summary):
    import pandas as pd
    from gensim.corpora import MmCorpus

    with pushd(output_dir):
        model.save("lda_model.gensim")
        dictionary.save("dictionary.gensim")
        MmCorpus.serialize("bow_corpus.mm", bow_corpus)
        MmCorpus.serialize("training_corpus.mm", train_corpus)

    save_topic_words(model, num_topics, args.topn, output_dir / "topics.csv")

    doc_rows = []
    dominant_rows = []
    for doc_id, doc in enumerate(train_corpus):
        topic_probs = model.get_document_topics(doc, minimum_probability=0)
        best_topic, best_prob = max(topic_probs, key=lambda item: item[1])
        dominant_rows.append({"doc_id": doc_id, "dominant_topic": int(best_topic), "dominant_probability": float(best_prob), "text": texts[doc_id]})
        for topic_id, prob in topic_probs:
            doc_rows.append({"doc_id": doc_id, "topic_id": int(topic_id), "probability": float(prob)})
    pd.DataFrame(doc_rows).to_csv(output_dir / "document_topics.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(dominant_rows).to_csv(output_dir / "dominant_topics.csv", index=False, encoding="utf-8-sig")

    topic_lines = ["# LDA Topic Summary", ""]
    for topic_id in range(num_topics):
        words = [word for word, _ in model.show_topic(topic_id, topn=min(args.topn, 10))]
        topic_lines.append(f"- Topic {topic_id}: {' / '.join(words)}")
    (output_dir / "topic_summary.md").write_text("\n".join(topic_lines) + "\n", encoding="utf-8")

    metrics = {
        "documents": len(texts),
        "vocab_size": len(dictionary),
        "num_topics": num_topics,
        "corpus_weighting": args.corpus_weighting,
        "alpha": "50/num_topics" if str(args.alpha).lower() in {"scaled", "50/k", "50/num_topics"} else args.alpha,
        "eta": args.eta,
        **compute_metrics(model, train_corpus, bow_corpus, tokenized, dictionary),
        "selection_summary": selection_summary,
    }
    if args.vis_html:
        metrics.update(save_pyldavis(model, train_corpus, dictionary, output_dir / "lda_visualization.html"))
    (output_dir / "metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
    return metrics


def main():
    parser = argparse.ArgumentParser(description="Run human-in-the-loop gensim LDA diagnostics or final training.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--text-column")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--num-topics", type=int, help="Final topic count chosen by the user. If omitted, run diagnostics only.")
    parser.add_argument("--select-topics", action="store_true", help="Run topic-count validation even when --num-topics is provided.")
    parser.add_argument("--topic-min", type=int, default=1)
    parser.add_argument("--topic-max", type=int)
    parser.add_argument("--topic-step", type=int, default=1)
    parser.add_argument("--corpus-weighting", choices=["tfidf", "bow"], default="tfidf")
    parser.add_argument("--stopwords")
    parser.add_argument("--auto-stopwords", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--tokenized", action="store_true")
    parser.add_argument("--clean-text", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--opencc", default="t2s", help="OpenCC config for Chinese normalization, e.g. t2s. Use 'none' to disable.")
    parser.add_argument("--lowercase-english", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--min-token-length", type=int, default=2)
    parser.add_argument("--no-below", type=int, default=1)
    parser.add_argument("--no-above", type=float, default=1.0)
    parser.add_argument("--keep-n", type=int)
    parser.add_argument("--passes", type=int, default=10)
    parser.add_argument("--iterations", type=int, default=50)
    parser.add_argument("--topn", type=int, default=20)
    parser.add_argument("--alpha", default="scaled", help="Document-topic prior: scaled means 50/num_topics. Also accepts symmetric/asymmetric/auto/float.")
    parser.add_argument("--eta", default="0.01", help="Topic-word prior: default 0.01. Also accepts auto/symmetric/float.")
    parser.add_argument("--random-state", type=int, default=100)
    parser.add_argument("--vis-html", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--save-selection-models", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--candidate-vis-top-n", type=int, default=3, help="Generate pyLDAvis HTML for top-N coherence candidates plus the best perplexity candidate. Use 0 to disable.")
    args = parser.parse_args()

    try:
        from gensim import corpora  # noqa: F401
        from gensim import models  # noqa: F401
    except ImportError as exc:
        raise SystemExit("Missing dependency: install gensim.") from exc

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    texts, used_text_column = load_texts(args.input, args.text_column)
    original_count = len(texts)
    stopwords_path = Path(args.stopwords) if args.stopwords else (auto_stopwords_path() if args.auto_stopwords else None)
    stopwords = read_stopwords(stopwords_path) if stopwords_path else set()
    raw_tokenized = tokenize(texts, stopwords, args.tokenized, args)
    valid_pairs = [(text, tokens) for text, tokens in zip(texts, raw_tokenized) if tokens]
    texts = [text for text, _ in valid_pairs]
    tokenized = [tokens for _, tokens in valid_pairs]
    if not tokenized:
        raise SystemExit("No valid tokenized documents after preprocessing. Check text column, stopwords, or --min-token-length.")
    save_preprocessed(texts, tokenized, out)
    save_preprocessing_config(args, out, original_count, len(tokenized), stopwords_path, len(stopwords), used_text_column)
    dictionary, bow_corpus, tfidf_model, tfidf_corpus, train_corpus = prepare_corpus(tokenized, args)
    with pushd(out):
        tfidf_model.save("tfidf_model.gensim")

    run_selection = args.select_topics or args.num_topics is None
    selection_summary = None
    if run_selection:
        topic_values = resolve_topic_values(args, len(texts), len(dictionary))
        selection_summary = select_topics(topic_values, train_corpus, bow_corpus, tokenized, dictionary, out, args)

    if args.num_topics is None:
        result = {
            "output_dir": str(out),
            "stage": "topic_selection_only",
            "final_model_trained": False,
            "user_action_required": "Review topic_selection_report.md, metrics, plots, topic words, and candidate visualizations; then rerun with --num-topics K.",
            "selection_summary": selection_summary,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    final_model = train_lda(args.num_topics, train_corpus, dictionary, args)
    metrics = save_final_outputs(final_model, args.num_topics, texts, train_corpus, bow_corpus, tokenized, dictionary, out, args, selection_summary)
    print(json.dumps({"output_dir": str(out), **metrics}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
