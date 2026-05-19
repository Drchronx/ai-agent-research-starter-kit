---
name: paper-reusable-insight-bank
description: "Extract and maintain reusable insights from each paper for long-term research ideation. Use for turning papers into idea cards, reusable theory mechanisms, variable definitions, stimuli, measures, datasets, analysis strategies, limitations, reviewer-risk notes, and future-study opportunities."
---

# Paper Reusable Insight Bank

Use this skill to preserve what each paper can contribute to future research projects. It is not a generic summary; it is an idea and reuse extraction workflow.

## Core Rules

- Separate paper content, user interpretation, and future idea.
- Every insight must point back to a paper note or Zotero key.
- Do not convert limitations into research gaps without checking later literature.
- Do not reuse stimuli, scales, or figures without checking copyright and citation requirements.

## Insight Types

```text
theory_mechanism
construct_definition
measurement_source
experimental_stimulus
scenario_design
eeg_erp_pipeline
bci_modeling_pattern
text_mining_variable
causal_identification
statistical_reporting
figure_design
reviewer_risk
future_study
writing_move
```

## Insight Card Template

```markdown
# Insight: Short Name

## Source
- Paper:
- Zotero key:
- Obsidian note:
- DOI/ID:

## Type

## What The Paper Actually Shows

## Reusable Pattern

## How I Can Use It

## Needed Adaptation

## Risks

## Linked Project Or Research Question

## Verification Status
```

## Workflow

1. Start from one paper card or a batch of papers.
2. Extract no more than 3-7 high-value reusable insights per paper.
3. Classify each insight by type.
4. Record:
   - source paper,
   - exact reusable pattern,
   - possible adaptation,
   - risk or boundary,
   - linked project or question.
5. Store as:
   - Obsidian insight note,
   - `insight_bank.csv`,
   - project-specific idea list.
6. Review duplicates monthly and merge overlapping insights.

## Batch Output Table

```text
| Insight | Type | Source | Reusable pattern | Project use | Risk | Status |
|---|---|---|---|---|---|---|
```

## Beginner Prompt

```text
Use paper-reusable-insight-bank to extract reusable insights from these papers.
For each paper, output theory mechanisms, variables, methods, stimuli/measures, analysis strategies, figure ideas, limitations, reviewer risks, and future-study opportunities.
Separate what the paper actually says from my possible new idea.
```

## Monthly Review

At the end of each month:

1. Sort insights by project.
2. Merge duplicates.
3. Promote strong insights to research questions.
4. Demote weak or unsupported ideas to `needs_check`.
5. Link final insights back to Zotero and Obsidian paper cards.
