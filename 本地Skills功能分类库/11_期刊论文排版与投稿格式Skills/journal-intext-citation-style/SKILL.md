---
name: journal-intext-citation-style
description: "Convert and audit in-text citation style for academic manuscripts. Use for APA 7 in-text citations, author-year citations, numeric citations, et al. rules, parenthetical and narrative citation formatting, citation link preservation, and checking that cited works match the reference list."
---

# Journal In-Text Citation Style

Use this skill to convert or audit in-text citations against a target style guide.

## Inputs

- Manuscript text.
- Reference list or bibliography metadata.
- Target citation style rules.

## Workflow

1. Detect all in-text citations.
2. Classify citation type: parenthetical, narrative, numeric, multiple sources, direct quotation, secondary citation.
3. Convert syntax to target style when enough metadata is available.
4. Check every in-text citation against the reference list.
5. Flag missing, uncited, ambiguous, or duplicate references.

## Hard Constraints

- Do not add or remove citations.
- Do not invent author names, years, DOIs, page numbers, or source metadata.
- If numeric-to-author-year conversion lacks metadata, mark it for manual resolution.
- Keep citation links or citation keys when working in DOCX, Markdown, LaTeX, Zotero, or BibTeX workflows.

## Output

```text
Converted manuscript citations:
Citation audit table:
Missing reference-list entries:
Uncited reference-list entries:
Manual resolution items:
```

