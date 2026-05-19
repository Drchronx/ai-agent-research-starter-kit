---
name: ai4scholar-paper-detail-batch
description: "Use AI4Scholar to retrieve and verify detailed metadata for one paper or many papers by DOI, PMID, arXiv ID, Semantic Scholar ID, or title. Trigger for paper detail lookup, batch paper metadata, DOI verification, PMID verification, BibTeX preparation, reference cleanup, or checking whether a cited paper is real."
---

# AI4Scholar Paper Detail And Batch Verification

Use this skill when a paper has already been identified and the task is to verify its metadata, abstract, identifiers, authors, venue, year, open-access status, or batch details.

## Core Rules

- Do not invent missing DOI, issue, volume, pages, PMID, or arXiv ID.
- Preserve author names and title spelling exactly as returned by verified sources.
- If AI4Scholar and another source disagree, report the conflict instead of silently choosing one.
- For final manuscripts, cross-check important references with `citation-management`, publisher pages, PubMed, Crossref, OpenAlex, or Zotero where available.

## Tools From The Source Guide

Use the exact schemas exposed by AI4Scholar. Common detail tools include:

| Tool | Use |
|---|---|
| `get_semantic_paper_detail` | Get paper detail by DOI, arXiv ID, PMID, Semantic Scholar ID, or URL if supported |
| `get_pubmed_paper_detail` | Get PubMed detail for biomedical, neuroscience, psychology, and clinical papers |
| `get_semantic_paper_batch` | Batch detail lookup, up to 500 papers if supported |
| `get_pubmed_paper_batch` | Batch PubMed details |
| `search_semantic_paper_match` | Exact title match before detail lookup |

## Single Paper Workflow

1. Identify the strongest input key in this order: DOI, PMID, arXiv ID, Semantic Scholar ID, exact title.
2. Call the relevant detail tool.
3. Extract:
   - title,
   - authors,
   - year,
   - venue,
   - abstract,
   - DOI/PMID/arXiv/S2 ID,
   - citation count if available,
   - open-access URL or PDF URL if available.
4. Compare against any metadata provided by the user.
5. Flag mismatches.

## Batch Workflow

1. Normalize the input list into a table with one row per paper.
2. Deduplicate before lookup by DOI and title.
3. Run batch lookup where supported; otherwise process in small batches.
4. Mark each row:
   - `verified`,
   - `metadata_conflict`,
   - `not_found`,
   - `needs_manual_check`.
5. Export a clean reference matrix.

## Output Template

```text
Input identifiers:
Lookup tools used:

Verified metadata:
| Title | Authors | Year | Venue | DOI/PMID/arXiv/S2 | OA/PDF | Status |

Conflicts:
| Paper | User metadata | AI4Scholar metadata | Action |

Unresolved:
| Input | Reason | Manual check path |
```

## Beginner Prompt

```text
Use AI4Scholar to verify whether the following references are real.
Prefer DOI, PMID, or arXiv ID lookup; for items without IDs, use exact-title matching.
Return standardized metadata, conflicts, and items that require manual verification.
```

## Failure Handling

- If a title match returns multiple papers, compare authors and year before selecting.
- If the paper is not found in PubMed, try Semantic Scholar; PubMed does not cover all fields.
- If a preprint and published article both exist, report both and ask which version should be cited.
