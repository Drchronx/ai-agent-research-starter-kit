---
name: journal-reference-list-format
description: "Format and audit academic reference lists for journal submission. Use for APA 7 references, journal-specific bibliography style, DOI audit, punctuation, title case or sentence case, journal name italics, volume issue pages, alphabetical or numeric sorting, and incomplete reference flagging without fabricating metadata."
---

# Journal Reference List Format

Use this skill to clean, sort, and format reference lists while preserving bibliographic integrity.

For a complete manuscript-formatting workflow, read `references/formatting-pipeline.md`. Use `scripts/create_formatting_audit_template.py` to create a full formatting audit sheet.

## Inputs

- Raw reference list, BibTeX, RIS, Zotero export, or manuscript references.
- Target journal style.
- Optional DOI or metadata lookup results.

## Workflow

1. Parse each reference into authors, year, title, source, volume, issue, pages, DOI, and URL.
2. Apply target style punctuation, capitalization, italics markers, and DOI format.
3. Sort according to target rule: alphabetical, citation order, or numbered order.
4. Check for duplicates, missing required fields, and metadata inconsistencies.
5. Return formatted references plus an audit list.

## Hard Constraints

- Do not invent DOI, issue, page range, publisher, or article title.
- Do not delete incomplete references.
- Mark unverified or incomplete references for author review.
- Use real metadata verification tools when available.

## Output

```text
Formatted reference list:
Reference audit table:
Incomplete references:
Duplicate or conflicting references:
Verification recommendations:
```
