---
name: journal-blind-review-anonymizer
description: "Prepare manuscripts for double-blind peer review by auditing and anonymizing identifying information. Use for removing author names, affiliations, acknowledgements, grants, IRB identifiers, self-citations, file metadata, document properties, supplementary files, and blind-review compliance checks."
---

# Journal Blind Review Anonymizer

Use this skill as the final pre-submission anonymity audit.

## Inputs

- Final manuscript.
- Title page if separate.
- Reference list.
- Supplementary materials.
- Author names, institutions, grants, project names, OSF links, and prior work to mask.
- Target journal blind-review policy.

## Workflow

1. Build an identity inventory: author names, affiliations, grants, project names, labs, datasets, preregistration links, repositories, acknowledgements, and self-citations.
2. Scan manuscript text, references, tables, figures, appendices, supplements, headers, footers, comments, tracked changes, and file metadata.
3. Replace or mask identifying content using target journal rules.
4. Keep non-author citations intact.
5. Produce a blind-review audit table.

## Hard Constraints

- Do not remove scientific content needed for review unless masking is required.
- Do not anonymize non-author citations.
- Do not lose links between masked self-citations and the final unblinded version.
- Flag uncertain self-citations instead of guessing.

## Output

```text
Blind manuscript changes:
Masked identity inventory:
Self-citation audit:
File metadata checklist:
Items requiring author confirmation:
```

