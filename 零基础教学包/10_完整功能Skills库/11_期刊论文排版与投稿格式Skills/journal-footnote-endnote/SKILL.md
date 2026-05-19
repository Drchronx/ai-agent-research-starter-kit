---
name: journal-footnote-endnote
description: "Convert and audit manuscript footnotes and endnotes for journal submission. Use for footnote-to-endnote conversion, endnote-to-footnote conversion, note numbering, note marker placement, supplementary notes, APA notes, and preserving note text links."
---

# Journal Footnote And Endnote

Use this skill to convert and standardize supplementary notes.

## Inputs

- Manuscript with footnotes, endnotes, or inline note markers.
- Target journal note policy.

## Workflow

1. Detect all note markers and note bodies.
2. Verify numbering order and marker-body matching.
3. Convert footnotes to endnotes or endnotes to footnotes according to target rules.
4. Standardize note placement, numbering, and punctuation.
5. Flag broken, duplicated, or orphaned notes.

## Hard Constraints

- Preserve note text exactly unless the user asks for editorial revision.
- Do not remove notes.
- Do not change non-note citations.
- Keep note links or markers traceable.

## Output

```text
Converted note structure:
Note numbering audit:
Broken or ambiguous notes:
Style rules applied:
```

