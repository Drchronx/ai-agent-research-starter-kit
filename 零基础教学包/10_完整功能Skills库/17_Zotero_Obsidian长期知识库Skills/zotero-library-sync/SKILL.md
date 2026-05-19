---
name: zotero-library-sync
description: "Synchronize and audit a Zotero literature library for long-term research knowledge management. Use for Zotero Web API or local read-only access, pyzotero workflows, collection design, tag taxonomy, metadata cleanup, PDF attachment status, BibTeX export, DOI checks, and syncing Zotero items into an Obsidian-ready paper index."
---

# Zotero Library Sync

Use this skill to keep Zotero as the canonical reference library and produce clean exports for Obsidian, literature matrices, and manuscript reference checks.

## Core Rules

- Never expose Zotero API keys. Use `ZOTERO_API_KEY`, `ZOTERO_LIBRARY_ID`, and `ZOTERO_LIBRARY_TYPE`.
- Do not invent missing DOI, PMID, arXiv ID, volume, issue, or pages.
- Zotero stores references; Obsidian stores interpretation. Keep these roles separate.
- Preserve original metadata before bulk edits. Prefer a dry run for cleanup actions.
- For manuscripts, cross-check important citations with `citation-management`, AI4Scholar, AMiner, OpenAlex, PubMed, Crossref, or publisher pages.

## Credentials

Recommended environment variables:

```text
ZOTERO_LIBRARY_ID=your_user_or_group_id
ZOTERO_LIBRARY_TYPE=user
ZOTERO_API_KEY=your_private_key
```

Use group libraries with `ZOTERO_LIBRARY_TYPE=group`.

## Workflow

1. Connect through `pyzotero` or read-only local mode if no API key is available.
2. Export core fields:
   - Zotero key,
   - item type,
   - title,
   - authors,
   - year,
   - venue,
   - DOI/PMID/arXiv,
   - URL,
   - collections,
   - tags,
   - attachment status,
   - date added,
   - date modified.
3. Audit metadata:
   - missing DOI,
   - duplicate title,
   - missing year,
   - inconsistent venue names,
   - missing PDF attachment,
   - untagged items.
4. Normalize tag taxonomy.
5. Export:
   - `zotero_items.csv`,
   - `zotero_items.json`,
   - `references.bib`,
   - `obsidian_paper_index.md`.
6. Do not change Zotero metadata unless the user explicitly approves write-back.

## Recommended Collection Structure

```text
00_inbox
01_to_read
02_reading
03_core_theory
04_methods
05_measures
06_datasets
07_reviews_meta
08_manuscript_citations
99_archive
```

## Recommended Tags

Use stable tags:

```text
field:management
field:psychology
field:neuroscience
field:bci
method:eeg
method:erp
method:scenario_experiment
method:text_mining
method:causal_inference
role:classic
role:must_read
role:method_source
role:measure_source
status:to_read
status:read
status:verified
status:needs_check
```

## Output Template

```text
Zotero library:
Access mode:
Items scanned:
Collections scanned:

Metadata audit:
| Issue | Count | Example | Action |

Exported files:
| File | Purpose |

Next cleanup actions:
```

## Beginner Prompt

```text
Use zotero-library-sync to audit my Zotero library.
Do not display API keys.
Export an Obsidian-ready paper index and a metadata issue table.
Do not write changes back to Zotero until I approve them.
```

## When To Combine With Other Skills

- Use `obsidian-paper-card` after export to create paper notes.
- Use `theory-variable-method-matrix` to turn Zotero items into a research matrix.
- Use `citation-management` for final citation verification.
- Use `pyzotero` when direct Zotero API operations are needed.
