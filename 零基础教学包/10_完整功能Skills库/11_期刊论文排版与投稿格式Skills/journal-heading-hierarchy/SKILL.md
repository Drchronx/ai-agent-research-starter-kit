---
name: journal-heading-hierarchy
description: "Standardize manuscript heading hierarchy for academic journals. Use for APA 7 heading levels, numbered headings, H1 H2 H3 mapping, bold italic centered headings, section structure audit, manuscript outline consistency, and journal-specific heading conversion without changing heading wording."
---

# Journal Heading Hierarchy

Use this skill to map existing headings to target journal heading levels.

## Inputs

- Manuscript text or outline.
- Current heading levels if available.
- Target journal heading guide.

## Workflow

1. Detect all headings and their implied hierarchy.
2. Check for skipped levels, duplicate headings, and inconsistent numbering.
3. Map current headings to target levels.
4. Apply formatting instructions such as bold, italic, centered, title case, sentence case, or numbering.
5. Return an audit table and formatted heading structure.

## Hard Constraints

- Do not rewrite heading wording.
- Do not change section order unless the user asks for structural editing.
- Preserve hierarchy logic and flag ambiguous heading levels.

## Output

```text
Heading map:
Standardized heading structure:
Ambiguous headings:
Style rules applied:
```

