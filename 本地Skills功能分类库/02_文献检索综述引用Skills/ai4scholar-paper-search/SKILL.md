---
name: ai4scholar-paper-search
description: "Use AI4Scholar to search real scholarly papers across Semantic Scholar, PubMed, Google Scholar, arXiv, bioRxiv, and medRxiv. Trigger for AI4Scholar paper search, latest literature, top journal literature discovery, cross-database search, paper search prompts, or when the user needs traceable real references rather than invented citations."
---

# AI4Scholar Paper Search

Use this skill to search real scholarly literature through AI4Scholar MCP or the OpenClaw AI4Scholar plugin.

Source guide: `https://lifu-coze.feishu.cn/wiki/WOaewK33Ei2g1nkt44kcRXiBnze`  
AI4Scholar MCP endpoint: `https://mcp.ai4scholar.net/sse`

## Non-Negotiable Rules

- Never fabricate references.
- Never expose an API key. Use `${AI4SCHOLAR_API_KEY}` or "your AI4Scholar API key".
- Prefer verified identifiers: DOI, PMID, arXiv ID, Semantic Scholar ID, publisher URL.
- Mark unverifiable or weakly matched results as needing manual verification.
- For management, psychology, neuroscience, BCI, HCI, and text-mining topics, search both classic and recent papers when possible.

## Tools From The Source Guide

Use the exact schemas exposed by the MCP server or plugin. Common search tools described by the source guide include:

| Tool | Source | Best use |
|---|---|---|
| `search_semantic` | Semantic Scholar | Broad semantic literature search with year filters |
| `search_pubmed` | PubMed | Biomedical, psychology-adjacent, neuroscience, clinical, health topics |
| `search_google_scholar` | Google Scholar proxy | Broad cross-disciplinary discovery |
| `search_arxiv` | arXiv | AI, ML, CS, BCI algorithms, HCI preprints |
| `search_biorxiv` | bioRxiv | Biology and neuroscience preprints |
| `search_medrxiv` | medRxiv | Medical and clinical preprints |
| `search_semantic_snippets` | Semantic Scholar | Search text snippets inside paper full text |
| `search_semantic_bulk` | Semantic Scholar | Large search, up to 1000 results if supported |
| `search_semantic_paper_match` | Semantic Scholar | Exact title matching |

## Search Workflow

1. Convert the user question into 2-4 precise English queries. Add Chinese queries only when Chinese literature is relevant.
2. Choose databases:
   - Management, psychology, HCI, IS: Semantic Scholar + Google Scholar.
   - Neuroscience, EEG, ERP, BCI: PubMed + Semantic Scholar + arXiv when algorithms are involved.
   - AI/ML/text mining: arXiv + Semantic Scholar + Google Scholar.
3. Run at least two sources when available.
4. Deduplicate by DOI, title, year, and first author.
5. Prioritize:
   - recent five-year papers,
   - top journals or major conferences,
   - highly cited classics,
   - papers that match the user's method and variables.
6. Output a literature matrix before writing narrative synthesis.

## Screening Criteria

Score each candidate paper from 0-2 on:

| Criterion | 0 | 1 | 2 |
|---|---|---|---|
| Topic fit | unrelated | adjacent | directly relevant |
| Method fit | wrong method | partially similar | same or transferable method |
| Evidence quality | unclear | usable | strong design/data |
| Venue quality | unknown | field-normal | top or authoritative |
| Citation traceability | no identifier | partial metadata | DOI/PMID/arXiv/publisher URL |

Keep papers scoring at least 7/10 unless the user requests broad exploration.

## Output Template

```text
Research question:
AI4Scholar mode: MCP / OpenClaw plugin / unknown
Databases searched:
Query strings:
Filters:

Top papers:
| # | Title | Authors | Year | Venue | DOI/ID | Source | Why it matters | Verification |

Excluded or weak papers:
| Title | Reason |

Next search move:
```

## Beginner Prompt

```text
Use AI4Scholar to search real English-language papers on "[topic]".
Prioritize the most recent five years, while keeping necessary classic papers.
Use at least Semantic Scholar plus one of PubMed, Google Scholar, or arXiv.
Return title, authors, year, venue, DOI/PMID/arXiv ID, abstract, source, and manual-verification status.
```

## Quality Checks

- If results are empty, broaden the query and try another database.
- If the same paper appears across sources, merge the metadata instead of duplicating it.
- If a result has no DOI or stable identifier, do not cite it as verified.
- If the user asks for "top journal" evidence, explain the venue screen used.
