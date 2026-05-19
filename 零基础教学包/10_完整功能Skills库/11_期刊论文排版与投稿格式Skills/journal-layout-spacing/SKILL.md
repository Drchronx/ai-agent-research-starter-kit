---
name: journal-layout-spacing
description: "Audit manuscript layout and spacing constraints for journal submission. Use for margins, line spacing, paragraph indentation, block quotes, page breaks, title page layout, double spacing, section spacing, DOCX rendering instructions, and final submission layout checks."
---

# Journal Layout And Spacing

Use this skill to translate journal layout rules into document-level formatting instructions.

## Inputs

- Manuscript text or DOCX structure.
- Target journal layout requirements.
- Output format: DOCX, LaTeX, Markdown, or submission portal text.

## Workflow

1. Extract layout requirements: margins, line spacing, font, page numbers, indentation, block quotes, tables, figures, and appendices.
2. Check current document layout if a rendered file is available.
3. Produce deterministic formatting instructions or apply them through a document-processing workflow when requested.
4. Flag layout rules that require the final DOCX/PDF renderer to verify visually.

## Hard Constraints

- Do not change prose content.
- Do not alter data, references, or citations.
- Keep structural instructions separate from scholarly edits.

## Output

```text
Layout settings:
Spacing and indentation rules:
Document-level instructions:
Renderer verification checklist:
Manual review items:
```

