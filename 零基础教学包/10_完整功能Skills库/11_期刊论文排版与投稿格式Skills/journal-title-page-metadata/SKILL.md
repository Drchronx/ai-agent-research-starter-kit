---
name: journal-title-page-metadata
description: "Format manuscript title pages and front matter metadata for academic journal submission. Use for title page formatting, author names, affiliations, corresponding author details, funding statement placement, acknowledgements metadata, APA 7 title page, journal-specific front matter, and manuscript metadata audit."
---

# Journal Title Page Metadata

Use this skill to standardize title page and front matter metadata without changing scholarly content.

## Inputs

- Manuscript title.
- Author names exactly as provided.
- Affiliations and affiliation order.
- Corresponding author details.
- Funding, acknowledgements, conflict of interest, data availability, ethics approval, and author contribution statements if provided.
- Target journal instructions or style guide.

## Workflow

1. Extract all front matter fields.
2. Map each author to affiliations.
3. Apply target journal rules for title capitalization, author order, superscripts, correspondence, running head, word count, and notes.
4. Place required statements in the required order.
5. Mark missing required metadata for author review.

## Hard Constraints

- Preserve all names, institutions, grant numbers, emails, and IDs exactly.
- Do not invent funding, ethics, conflicts, ORCID, or acknowledgements.
- Do not reorder authors unless the user explicitly requests it.
- If the target journal rule is not provided, ask for it or produce a neutral APA 7-compatible draft with caveats.

## Output

```text
Title page block:
Metadata checklist:
Missing or ambiguous fields:
Style decisions applied:
Items requiring author confirmation:
```

