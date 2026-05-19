---
name: ai4scholar-paper-recommendation
description: "Use AI4Scholar recommendation tools to find related papers from one or more seed papers, build reading lists, expand a literature map, and discover papers adjacent to a user's theory, method, dataset, or empirical context."
---

# AI4Scholar Paper Recommendation

Use this skill when the user has seed papers and wants targeted related-paper recommendations rather than a broad keyword search.

## Core Rules

- Recommendations are candidates, not verified citations.
- Always keep the seed set visible so the recommendation logic can be audited.
- Do not let recommendations drift away from the user's research question.
- Deduplicate recommendations against papers already in the user's library.

## Tools From The Source Guide

| Tool | Use |
|---|---|
| `get_semantic_recommendations` | Recommend papers based on multiple seed papers |
| `get_semantic_recommendations_for_paper` | Recommend papers based on a single seed paper |
| `get_semantic_paper_detail` | Verify details for recommended papers |
| `get_semantic_citations` / `get_semantic_references` | Combine recommendation with citation network expansion |

## Recommendation Workflow

1. Ask for or infer the seed papers:
   - DOI,
   - Semantic Scholar ID,
   - arXiv ID,
   - exact title.
2. Classify each seed by role:
   - theory,
   - method,
   - empirical context,
   - dataset,
   - measurement,
   - modeling technique.
3. Run recommendation tools.
4. Deduplicate with current reading list.
5. Screen recommendations for:
   - topic fit,
   - method fit,
   - venue and year,
   - whether it adds something new beyond the seed papers.
6. Return a reading order.

## Use Cases

- "I have 5 papers, what should I read next?"
- "Find papers similar to this ERP/EEG experiment."
- "Find BCI deep learning papers near this architecture."
- "Find management/psychology papers using similar scenario experiments."
- "Expand a literature review without changing the research question."

## Output Template

```text
Seed papers:
Recommendation tool:

Recommended papers:
| Priority | Title | Authors | Year | Venue | DOI/ID | Why recommended | What to read for |

Not selected:
| Title | Reason |

Reading order:
```

## Beginner Prompt

```text
Use AI4Scholar to recommend follow-up readings from the following seed papers.
Do not rely only on keywords; explain the recommendation by theory, method, data, and research context.
Return priority, DOI/ID, reading purpose, and verification status.
```

## Quality Checks

- If the seed paper is too broad, ask for the user's target angle.
- If recommendations are mostly irrelevant, switch to `ai4scholar-paper-search` with narrower queries.
- If the user needs a complete literature map, combine this skill with `ai4scholar-citation-network`.
