---
name: sentiment-analysis
description: Chinese sentiment analysis workflows using dictionary scoring, traditional machine learning classifiers, and LLM API calls. Use when a user asks Codex to label sentiment, calculate dictionary sentiment scores, train a TF-IDF sentiment classifier, predict sentiment from a saved classifier, or call a large language model for sentiment classification on text files or short inputs.
---

# Sentiment Analysis

## Operating Rule

Use this skill as a fixed command-line workflow. Do not write ad-hoc sentiment analysis code.

1. Decide whether the task is covered by dictionary, machine-learning, or LLM sentiment analysis.
2. If unsupported, say the skill cannot solve it and name the missing method or input.
3. If supported, write a plan before running commands. Include the chosen method, reference file, script, required inputs, required columns, and output path.
4. Ask for missing lexicon paths, label columns, model paths, or API key environment details when required.
5. Execute the script by command line and report the produced files and key metrics.

## Capability Map

- Dictionary method: read `references/dictionary-method.md`, then call `scripts/dictionary_sentiment.py`.
- Machine learning method: read `references/machine-learning-method.md`, then call `scripts/ml_sentiment.py`.
- LLM method: read `references/llm-method.md`, then call `scripts/llm_sentiment.py`.

## Input Expectations

- `.txt`: one text per line.
- `.csv` or `.xlsx`: requires `--text-column`; training also requires `--label-column`.
- Dictionary method requires either positive/negative word lists or a scored lexicon.
- Machine learning training requires labeled examples.
- LLM method requires an OpenAI-compatible API key in an environment variable.

## Course Context

This skill follows the current sentiment analysis course notebooks:

- Dictionary method and SnowNLP-style sentiment workflow.
- TF-IDF plus Logistic Regression, SVM, Naive Bayes, and Random Forest.

The scripts are the source of truth for repeatable execution.
