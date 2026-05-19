---
name: ai4scholar-citation-network
description: "Use AI4Scholar to trace citation networks: citing papers, references, PubMed related papers, backward/forward citation search, classic paper discovery, mechanism literature expansion, and reviewer-style citation gap checks."
---

# AI4Scholar Citation Network

Use this skill to expand a literature set from seed papers through backward references, forward citations, and related-paper tools.

## Core Rules

- Citation links are evidence for discovery, not automatic proof of relevance.
- Do not claim a paper supports a theoretical statement until the relevant abstract or full text is checked.
- Keep seed papers, backward references, forward citations, and related recommendations in separate columns.
- For thesis, SSCI, SCI, and C-journal work, mix classic roots with recent forward citations.

## Tools From The Source Guide

| Tool | Use |
|---|---|
| `get_semantic_citations` | Find papers that cite a seed paper |
| `get_semantic_references` | Find papers cited by a seed paper |
| `get_pubmed_citations` | PubMed citation lookup |
| `get_pubmed_related` | PubMed related-paper recommendations |
| `get_semantic_paper_detail` | Verify high-value nodes |
| `get_semantic_recommendations_for_paper` | Expand around one seed paper |

## Citation Expansion Workflow

1. Start from 3-8 seed papers, preferably verified by DOI or PMID.
2. For each seed:
   - collect backward references,
   - collect forward citations,
   - collect related papers where available.
3. Deduplicate by DOI/title.
4. Classify each paper:
   - theory foundation,
   - method precedent,
   - empirical benchmark,
   - measure/stimulus source,
   - contrary evidence,
   - review/meta-analysis.
5. Prioritize papers that are both recent and connected to multiple seed papers.
6. Build a citation matrix and a reading order.

## Review Gap Check

Use the network to answer:

- Which classic papers must be cited?
- Which recent top-journal papers are missing?
- Which methods have direct precedents?
- Which theories are being used as labels instead of mechanisms?
- Which citations are too weak for the sentence they support?

## Output Template

```text
Seed papers:
Citation tools used:

Network summary:
| Cluster | Key papers | Role | Why it matters |

Citation matrix:
| Paper | Direction | Linked seed | DOI/ID | Role | Priority | Verification |

Must-read first:
1.
2.
3.

Potential citation gaps:
```

## Beginner Prompt

```text
Use AI4Scholar to expand the citation network for the following three seed papers.
Return backward references, forward citations, and related papers separately.
Classify the final list into theory, method, empirical evidence, and review/meta-analysis, then mark the top 10 papers to read first.
```

## Caution

If the user asks for "highly cited papers", do not rank only by citation count. Also check field fit, publication year, and whether the paper directly supports the research mechanism.
