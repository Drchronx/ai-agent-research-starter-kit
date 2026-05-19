---
name: obsidian-paper-card
description: "Create Obsidian paper cards from Zotero items, PDFs, annotations, abstracts, or literature notes. Use for Markdown note templates, YAML frontmatter, backlinks, tags, literature summaries, theory-method-result extraction, and turning each paper into a reusable permanent note."
---

# Obsidian Paper Card

Use this skill to convert a paper into a structured Obsidian Markdown note that is useful for long-term research, not just a one-time summary.

## Core Rules

- One paper gets one canonical note.
- Put verified bibliographic metadata in YAML frontmatter.
- Separate what the paper says from the user's interpretation.
- Mark unverified claims and weak extraction quality.
- Prefer stable note names based on first author, year, and short title.

## File Naming

Recommended note name:

```text
@FirstAuthorYear_ShortTitle.md
```

Example:

```text
@Smith2024_AITrust.md
```

## YAML Frontmatter

```yaml
---
zotero_key:
title:
authors:
year:
venue:
doi:
pmid:
arxiv:
url:
item_type:
fields: []
methods: []
theories: []
variables: []
tags: []
status: to_read
created:
updated:
---
```

## Paper Card Template

```markdown
# @FirstAuthorYear Short Title

## Citation

## One-Sentence Takeaway

## Research Question

## Theory And Mechanism

## Variables

| Role | Variable | Definition | Measurement | Source |
|---|---|---|---|---|

## Method

## Data Or Sample

## Key Results

## Strengths

## Limitations

## Reusable Ideas

## How This Helps My Project

## Direct Quotes To Verify

## Links

- Zotero:
- PDF:
- Related notes:
```

## Extraction Workflow

1. Read Zotero metadata, abstract, annotations, and PDF text if available.
2. Fill metadata first.
3. Extract the paper's own contribution.
4. Extract theory, variables, method, data, and results.
5. Add links:
   - theory notes,
   - variable notes,
   - method notes,
   - research question notes,
   - project notes.
6. Mark status:
   - `to_read`,
   - `skimmed`,
   - `read`,
   - `verified`,
   - `needs_check`.

## Link Conventions

Use Obsidian wikilinks:

```text
[[Theory_Name]]
[[Variable_Name]]
[[Method_Name]]
[[RQ_AI_Trust_BCI]]
[[Project_Manuscript_1]]
```

## Beginner Prompt

```text
Use obsidian-paper-card to turn this paper into an Obsidian note.
Create YAML frontmatter, extract theory, variables, methods, data, key results, limitations, reusable ideas, and links to related notes.
Separate verified paper content from my interpretation.
```

## Quality Check

- A useful card should answer: why keep this paper?
- If the note contains only an abstract summary, it is not finished.
- If variables or mechanisms are unclear, explicitly mark them as unclear.
