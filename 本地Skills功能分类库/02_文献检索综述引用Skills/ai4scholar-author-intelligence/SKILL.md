---
name: ai4scholar-author-intelligence
description: "Use AI4Scholar author tools to search scholars, inspect author profiles, retrieve an author's papers, compare experts, identify potential reviewers, map labs or collaborators, and verify whether an author is the correct person."
---

# AI4Scholar Author Intelligence

Use this skill for scholar lookup, author disambiguation, expert mapping, reviewer discovery, or identifying a research community around a topic.

## Core Rules

- Author names are ambiguous. Always disambiguate by affiliation, coauthors, topic, ORCID, homepage, or paper list when available.
- Do not infer personal attributes beyond scholarly metadata.
- Do not label someone as a reviewer target without checking conflict-of-interest risks.
- For collaboration or reviewer lists, include uncertainty.

## Tools From The Source Guide

| Tool | Use |
|---|---|
| `search_semantic_authors` | Search authors by name |
| `get_semantic_author_detail` | Get author profile details such as h-index and paper count if available |
| `get_semantic_author_papers` | Get an author's papers |
| `get_semantic_author_batch` | Batch author details, up to 1000 people if supported |
| `get_semantic_paper_authors` | Get author details for a specific paper |

## Author Lookup Workflow

1. Search by full name.
2. Use affiliation, field, coauthors, and representative papers to choose the likely person.
3. Retrieve author detail and paper list.
4. Summarize:
   - main topics,
   - methods,
   - key venues,
   - recent activity,
   - recurring coauthors,
   - possible labs/institutions.
5. Mark unresolved ambiguity.

## Expert Mapping Workflow

1. Start from a topic query or seed papers.
2. Extract authors from top papers.
3. Batch fetch author details.
4. Rank by a mixed score:
   - topic fit,
   - recent publications,
   - venue quality,
   - citation impact,
   - methodological relevance,
   - conflict risk if reviewer discovery is requested.
5. Output a table, not just a list.

## Output Template

```text
Task:
Search input:
Tools used:

Author candidates:
| Name | Affiliation | Topics | Key papers | IDs/URLs | Match confidence |

Expert shortlist:
| Author | Why relevant | Recent papers | Methods | Possible conflict | Verification |
```

## Beginner Prompt

```text
Use AI4Scholar to find key scholars in "[topic]".
Return name, affiliation, representative papers, recent five-year papers, main methods, relevance to my project, and identity-disambiguation status.
```

## Common Risks

- Same name, different scholar.
- Senior scholar has high citations but no recent work in the exact topic.
- A coauthor or advisor may be unsuitable as an external reviewer due to conflict of interest.
