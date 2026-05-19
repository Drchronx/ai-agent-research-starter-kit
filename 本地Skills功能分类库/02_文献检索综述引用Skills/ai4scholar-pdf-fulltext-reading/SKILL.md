---
name: ai4scholar-pdf-fulltext-reading
description: "Use AI4Scholar to download open-access PDFs or read full text from Semantic Scholar, arXiv, bioRxiv, medRxiv, and DOI-based sources when access permits. Trigger for reading papers, extracting methods/results, PDF download, full-text summaries, or DOI full-text retrieval."
---

# AI4Scholar PDF And Full-Text Reading

Use this skill when the user wants to read or summarize paper full text, download PDFs, inspect methods/results, or extract evidence from an article.

## Core Rules

- Prefer legal open-access routes first.
- DOI download for paywalled papers works only when the running environment has institutional access.
- If extraction is poor, say so and do not infer missing methods or results.
- Do not summarize a full paper from title/abstract alone unless explicitly labeled as abstract-only.

## Tools From The Source Guide

| Tool | Use |
|---|---|
| `download_semantic` | Get Semantic Scholar open-access PDF link |
| `read_semantic_paper` | Download and extract Semantic Scholar full text |
| `download_arxiv` | Get arXiv PDF link |
| `read_arxiv_paper` | Download and extract arXiv full text |
| `download_biorxiv` | Get bioRxiv PDF link |
| `read_biorxiv_paper` | Download and extract bioRxiv full text |
| `download_medrxiv` | Get medRxiv PDF link |
| `read_medrxiv_paper` | Download and extract medRxiv full text |
| `download_by_doi` | Download PDF by DOI when access permits |
| `read_by_doi` | Download and extract full text by DOI when access permits |

## Reading Workflow

1. Verify the paper identifier.
2. Try open-access source in this order:
   - arXiv/bioRxiv/medRxiv if the identifier is a preprint ID,
   - Semantic Scholar open-access PDF,
   - DOI access when permitted.
3. Extract and segment:
   - Abstract,
   - Introduction,
   - Theory/background,
   - Method,
   - Data/sample,
   - Measures/stimuli,
   - Analysis,
   - Results,
   - Discussion/limitations.
4. For empirical papers, record exact design, sample, variables, model, and key statistics.
5. Mark any unreadable sections.

## Evidence Extraction Template

```text
Paper:
Identifier:
Access route:
Extraction quality: good / partial / poor

Research question:
Theory/mechanism:
Data/sample:
Method/design:
Variables/measures:
Key results:
Limitations:
Reusable ideas for my project:
Sections that need manual PDF reading:
```

## Beginner Prompt

```text
Use AI4Scholar to try to read the full text of this paper: [DOI/arXiv/PMID/title].
Extract research question, mechanism, sample, experiment/data design, variables, model, key results, and limitations.
If only the abstract is available or PDF extraction fails, say so clearly and do not guess.
```

## Fallbacks

- Use the local `pdf` or `markitdown` skill for downloaded PDFs.
- Use publisher HTML when PDF extraction is bad.
- For scanned PDFs, tell the user OCR is required.
