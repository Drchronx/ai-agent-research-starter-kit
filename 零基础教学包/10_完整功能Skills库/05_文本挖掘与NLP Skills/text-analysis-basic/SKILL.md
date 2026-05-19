---
name: text-analysis-basic
description: Basic Chinese NLP and text analysis workflows for PDF text/table extraction, jieba tokenization, word and sentence frequency, word clouds, TF-IDF, Word2Vec, sentence embeddings, and text similarity. Use when a user asks Codex to extract text from PDFs, segment Chinese text, count terms or sentences, create word clouds, vectorize text, train Word2Vec, encode embeddings, or compute text similarity from files or short inputs.
---

# Text Analysis Basic

## Operating Rule

Use this skill as a command-line workflow, not as a code-writing prompt.

1. Decide whether the user's request is covered by the capabilities below.
2. If it is not covered, state that the skill cannot solve it and identify the missing capability.
3. If it is covered, write a short plan before running commands. The plan must list:
   - Which capability will be used.
   - Which reference file will be followed.
   - Which script will be called.
   - Required inputs, parameters, and output paths.
4. Ask only for missing data paths or parameters that cannot be inferred safely.
5. Execute the relevant script with command-line arguments. Do not write one-off Python code for the operation.

Use absolute paths when passing files to scripts.

## Capability Map

- PDF text extraction or PDF table extraction: read `references/pdf-extraction.md`, then call `scripts/pdf_extract.py`.
- jieba segmentation or custom dictionary segmentation: read `references/jieba-tokenization.md`, then call `scripts/jieba_tokenize.py`.
- Word frequency or sentence frequency: read `references/frequency.md`, then call `scripts/frequencies.py`.
- Word cloud image generation: read `references/wordcloud.md`, then call `scripts/wordcloud_generate.py`.
- TF-IDF matrix or keyword features: read `references/tfidf.md`, then call `scripts/vectorize.py --method tfidf`.
- Word2Vec training or word vectors: read `references/word2vec.md`, then call `scripts/vectorize.py --method word2vec`.
- Sentence embedding: read `references/embedding.md`, then call `scripts/vectorize.py --method embedding`.
- Text similarity: read `references/similarity.md`, then call `scripts/similarity.py`.

## Input Expectations

Supported inputs are:

- `.txt`: one document or one document per line.
- `.csv`: requires `--text-column` unless the file has a clear `text` column.
- `.xlsx`: requires `--text-column`.
- `.pdf`: only for `pdf_extract.py`.

If the user provides a CSV/XLSX path without a text column, inspect the header and ask the user to choose the column when ambiguous.

## Course Context

This skill follows the current course notebooks for text preprocessing, vectorization, and similarity:

- PDF extraction, OCR context, and jieba segmentation.
- Word/sentence frequency, word clouds, TF-IDF, Word2Vec, and embeddings.
- Cosine, Jaccard, TF-IDF, Word2Vec, and sentence embedding similarity.

The scripts are the source of truth for repeatable execution.
