---
name: topic-modeling
description: Topic modeling workflows for Chinese corpora using LDA, Dynamic Topic Model/DTM, and BERTopic. Use when a user asks Codex to discover topics, train LDA models, compute topic keywords, model topic evolution over time, train DTM, run BERTopic, export document-topic assignments, or create topic visualization outputs from text files or tabular corpora.
---

# Topic Modeling

## Operating Rule

Use this skill as a fixed command-line workflow. Do not write ad-hoc topic modeling code.

1. Decide whether the request is LDA, DTM, or BERTopic.
2. If unsupported, state that this skill cannot solve it and identify the missing capability.
3. If supported, write a plan before running commands. Include the model type, reference file, script, input data path, required columns, key parameters, and output directory.
4. For LDA topic-count selection, run diagnostics first when the user has not explicitly chosen a final topic count. Show the diagnostic report, metrics, plots, candidate topic words, and candidate visualizations to the user, then stop and ask the user to choose the final topic count. Do not train the final LDA model until the user confirms K.
5. Ask for missing text column, time column, topic count, model path, or output directory.
6. Execute the relevant script with command-line arguments and report generated files.

## Capability Map

- LDA topic modeling, automatic topic-count selection, perplexity/coherence diagnostics, and pyLDAvis output: read `references/lda.md`, then call `scripts/lda_model.py`.
- Dynamic Topic Model over time: read `references/dtm.md`, then call `scripts/dtm_model.py`.
- BERTopic semantic topic modeling: read `references/bertopic.md`, then call `scripts/bertopic_model.py`.

## Input Expectations

- `.txt`: one document per line.
- `.csv` or `.xlsx`: requires `--text-column`.
- DTM additionally requires `--time-column`.
- Chinese text is tokenized with jieba unless the user passes `--tokenized`.

## Course Context

This skill follows the topic modeling course notebook, including LDA, DTM/LdaSeqModel, BERTopic, topic words, document-topic outputs, and visualization-oriented artifacts.

The scripts are the source of truth for repeatable execution.
