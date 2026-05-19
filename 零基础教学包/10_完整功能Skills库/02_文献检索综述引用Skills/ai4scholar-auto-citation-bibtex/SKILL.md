---
name: ai4scholar-auto-citation-bibtex
description: "Use AI4Scholar auto_cite to add real citations to academic text and return formatted references and BibTeX. Trigger for automatic citation insertion, APA/IEEE/Vancouver/Nature citation support, reference generation, BibTeX export, or checking whether claims have real supporting papers."
---

# AI4Scholar Auto Citation And BibTeX

Use this skill to add real citations to a user's academic text with AI4Scholar `auto_cite`, then audit whether the citations actually support the claims.

## Core Rules

- `auto_cite` reduces fabricated citation risk but does not remove human verification.
- Never accept an added citation without checking sentence-level support.
- Do not add references to unsupported claims just to make the paragraph look scholarly.
- Keep the user's original data and claims intact unless asked to rewrite.
- Output references plus verification status.

## Tool From The Source Guide

| Tool | Use |
|---|---|
| `auto_cite` | Add real citations to academic text; supports IEEE, APA, Vancouver, and Nature styles; returns cited text, references, and BibTeX if available |

## Before Calling `auto_cite`

Clarify or infer:

- Citation style: APA, IEEE, Vancouver, or Nature.
- Field: management, psychology, neuroscience, BCI, HCI, text mining, etc.
- Preference: recent five-year papers, top journals, classic foundations, or mixed.
- Whether the text is Chinese or English.
- Whether the output should preserve wording or lightly polish prose.

## Auto-Citation Workflow

1. Segment the text into claim units.
2. Identify claims that need citations:
   - theoretical mechanism,
   - empirical fact,
   - method precedent,
   - measurement source,
   - benchmark claim,
   - statistical or neuroscience convention.
3. Call `auto_cite` with the citation style and text.
4. For every inserted citation, build an audit table:
   - sentence,
   - citation,
   - support strength,
   - DOI/ID,
   - action.
5. Remove or flag weak citations.
6. Return:
   - cited text,
   - reference list,
   - BibTeX,
   - verification warnings.

## Output Template

```text
Citation style:
Tool used: auto_cite

Cited text:

References:

BibTeX:

Citation audit:
| Sentence/claim | Citation | DOI/ID | Support strength | Action |

Needs manual verification:
```

## Beginner Prompt

```text
Use AI4Scholar auto_cite to add APA 7th citations to the following Introduction paragraph.
Prioritize real top-journal and recent five-year literature, while preserving necessary classics.
Return the cited text, reference list, BibTeX, and a sentence-level citation-support audit table.
```

## Red Flags

- Citation supports a nearby topic but not the exact claim.
- Method citation is used to support a theory claim.
- Review paper is used where primary empirical evidence is needed.
- A preprint is cited as final evidence when a peer-reviewed version exists.
