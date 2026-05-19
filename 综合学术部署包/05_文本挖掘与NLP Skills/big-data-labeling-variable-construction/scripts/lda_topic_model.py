import argparse
import json
from pathlib import Path

import pandas as pd
import pyLDAvis.gensim_models
from gensim.corpora import Dictionary
from gensim.models import LdaModel, TfidfModel
from gensim.models.coherencemodel import CoherenceModel

from topic_modeling_utils import (
    build_preprocessed_frame,
    configure_matplotlib,
    ensure_dir,
    integer_range,
    load_stopwords,
    load_table,
    plot_metric_lines,
    save_preprocessed_outputs,
    save_token_frequency,
    topic_diversity,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run LDA topic modeling with automatic topic-count evaluation.")
    parser.add_argument("input_path", help="CSV or Excel file containing text data.")
    parser.add_argument("--text-col", default="text", help="Text column name.")
    parser.add_argument("--id-col", default="doc_id", help="Document id column.")
    parser.add_argument("--topic-range", default="2-10", help="Candidate topic counts, e.g. 2-10 or 3,5,7.")
    parser.add_argument("--passes", type=int, default=20, help="Number of full corpus passes.")
    parser.add_argument("--iterations", type=int, default=200, help="Maximum iterations per pass.")
    parser.add_argument("--no-tfidf", action="store_true", help="Use bag-of-words instead of TF-IDF weighted corpus.")
    parser.add_argument("--stopwords-path", help="Optional UTF-8 stopwords file.")
    parser.add_argument("--output-dir", default="reports/lda-topic-model", help="Output directory.")
    return parser.parse_args()


def build_corpus(tokens: list[list[str]], use_tfidf: bool) -> tuple[Dictionary, list[list[tuple[int, float]]]]:
    dictionary = Dictionary(tokens)
    dictionary.filter_extremes(no_below=1, no_above=0.9, keep_n=5000)
    bow_corpus = [dictionary.doc2bow(doc) for doc in tokens]
    if use_tfidf:
        tfidf_model = TfidfModel(bow_corpus)
        return dictionary, [tfidf_model[doc] for doc in bow_corpus]
    return dictionary, bow_corpus


def fit_lda_model(
    corpus: list[list[tuple[int, float]]],
    dictionary: Dictionary,
    num_topics: int,
    passes: int,
    iterations: int,
) -> LdaModel:
    return LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics=num_topics,
        passes=passes,
        iterations=iterations,
        alpha="auto",
        eta="auto",
        random_state=42,
        minimum_probability=0.0,
    )


def evaluate_candidate_models(
    topic_counts: list[int],
    corpus: list[list[tuple[int, float]]],
    dictionary: Dictionary,
    tokens: list[list[str]],
    passes: int,
    iterations: int,
) -> tuple[pd.DataFrame, dict[int, LdaModel]]:
    rows: list[dict[str, float | int]] = []
    models: dict[int, LdaModel] = {}
    for topic_count in topic_counts:
        model = fit_lda_model(corpus, dictionary, topic_count, passes, iterations)
        models[topic_count] = model
        coherence_cv = CoherenceModel(model=model, texts=tokens, dictionary=dictionary, coherence="c_v").get_coherence()
        coherence_umass = CoherenceModel(model=model, corpus=corpus, dictionary=dictionary, coherence="u_mass").get_coherence()
        rows.append(
            {
                "num_topics": topic_count,
                "coherence_cv": round(float(coherence_cv), 6),
                "coherence_umass": round(float(coherence_umass), 6),
                "log_perplexity": round(float(model.log_perplexity(corpus)), 6),
                "topic_diversity": topic_diversity(
                    [[word for word, _ in model.show_topic(topic_id, topn=10)] for topic_id in range(topic_count)]
                ),
            }
        )
        print(
            f"topics={topic_count} coherence_cv={coherence_cv:.4f} "
            f"coherence_umass={coherence_umass:.4f} perplexity={model.log_perplexity(corpus):.4f}"
        )
    evaluation_df = pd.DataFrame(rows).sort_values("num_topics").reset_index(drop=True)
    return evaluation_df, models


def select_best_topic_count(evaluation_df: pd.DataFrame) -> int:
    ranked = evaluation_df.sort_values(
        ["coherence_cv", "topic_diversity", "log_perplexity", "num_topics"],
        ascending=[False, False, False, True],
    )
    return int(ranked.iloc[0]["num_topics"])


def export_topic_words(model: LdaModel, output_dir: Path) -> Path:
    rows = []
    for topic_id in range(model.num_topics):
        for rank, (word, weight) in enumerate(model.show_topic(topic_id, topn=15), start=1):
            rows.append(
                {
                    "topic_id": topic_id,
                    "rank": rank,
                    "word": word,
                    "weight": round(float(weight), 6),
                }
            )
    path = output_dir / "topic_words.csv"
    pd.DataFrame(rows).to_csv(path, index=False, encoding="utf-8-sig")
    return path


def export_document_topics(
    df: pd.DataFrame,
    model: LdaModel,
    corpus: list[list[tuple[int, float]]],
    id_col: str,
    text_col: str,
    output_dir: Path,
) -> Path:
    records = []
    for (_, row), topic_distribution in zip(df.iterrows(), model.get_document_topics(corpus, minimum_probability=0.0)):
        sorted_topics = sorted(topic_distribution, key=lambda item: item[1], reverse=True)
        dominant_topic, dominant_prob = sorted_topics[0]
        record = {
            id_col: row[id_col],
            text_col: row[text_col],
            "dominant_topic": dominant_topic,
            "dominant_topic_probability": round(float(dominant_prob), 6),
        }
        for topic_id, probability in topic_distribution:
            record[f"topic_{topic_id}_probability"] = round(float(probability), 6)
        records.append(record)
    path = output_dir / "document_topics.csv"
    pd.DataFrame(records).to_csv(path, index=False, encoding="utf-8-sig")
    return path


def export_topic_summary(model: LdaModel, output_dir: Path) -> Path:
    rows = []
    for topic_id in range(model.num_topics):
        words = [word for word, _ in model.show_topic(topic_id, topn=10)]
        rows.append({"topic_id": topic_id, "top_words": " ".join(words)})
    path = output_dir / "topic_summary.csv"
    pd.DataFrame(rows).to_csv(path, index=False, encoding="utf-8-sig")
    return path


def export_pyldavis(model: LdaModel, corpus: list[list[tuple[int, float]]], dictionary: Dictionary, output_dir: Path) -> Path:
    prepared = pyLDAvis.gensim_models.prepare(model, corpus, dictionary)
    path = output_dir / "lda_visualization.html"
    pyLDAvis.save_html(prepared, str(path))
    return path


def export_best_summary(best_topics: int, evaluation_df: pd.DataFrame, output_dir: Path) -> Path:
    best_row = evaluation_df.loc[evaluation_df["num_topics"] == best_topics].iloc[0].to_dict()
    summary = {
        "best_num_topics": best_topics,
        "selection_rule": "highest coherence_cv, then higher topic_diversity, then better log_perplexity",
        "best_metrics": best_row,
    }
    path = output_dir / "best_model_summary.json"
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def main() -> None:
    args = parse_args()
    output_dir = ensure_dir(Path(args.output_dir))
    configure_matplotlib()

    stopwords = load_stopwords(args.stopwords_path)
    raw_df = load_table(Path(args.input_path))
    processed_df = build_preprocessed_frame(raw_df, args.text_col, args.id_col, stopwords)
    processed_path, token_path = save_preprocessed_outputs(processed_df, output_dir)
    frequency_path = save_token_frequency(processed_df["tokens"].tolist(), output_dir)

    dictionary, corpus = build_corpus(processed_df["tokens"].tolist(), use_tfidf=not args.no_tfidf)
    evaluation_df, models = evaluate_candidate_models(
        integer_range(args.topic_range),
        corpus,
        dictionary,
        processed_df["tokens"].tolist(),
        args.passes,
        args.iterations,
    )
    evaluation_path = output_dir / "topic_count_evaluation.csv"
    evaluation_df.to_csv(evaluation_path, index=False, encoding="utf-8-sig")
    plot_path = plot_metric_lines(
        evaluation_df,
        x_col="num_topics",
        output_path=output_dir / "topic_count_evaluation.png",
        title="LDA Topic Count Evaluation",
        primary_cols=["coherence_cv", "topic_diversity"],
        secondary_cols=["log_perplexity"],
    )

    best_topics = select_best_topic_count(evaluation_df)
    best_model = models[best_topics]
    model_dir = ensure_dir(output_dir / "model")
    model_path = model_dir / "lda_model.gensim"
    best_model.save(str(model_path))
    topic_words_path = export_topic_words(best_model, output_dir)
    topic_summary_path = export_topic_summary(best_model, output_dir)
    document_topics_path = export_document_topics(processed_df, best_model, corpus, args.id_col, args.text_col, output_dir)
    pyldavis_path = export_pyldavis(best_model, corpus, dictionary, output_dir)
    summary_path = export_best_summary(best_topics, evaluation_df, output_dir)

    print(f"Preprocessed documents: {processed_path}")
    print(f"Token lists: {token_path}")
    print(f"Token frequency: {frequency_path}")
    print(f"Evaluation table: {evaluation_path}")
    print(f"Evaluation plot: {plot_path}")
    print(f"Best num_topics: {best_topics}")
    print(f"Model: {model_path}")
    print(f"Topic words: {topic_words_path}")
    print(f"Topic summary: {topic_summary_path}")
    print(f"Document topics: {document_topics_path}")
    print(f"pyLDAvis: {pyldavis_path}")
    print(f"Summary JSON: {summary_path}")


if __name__ == "__main__":
    main()
