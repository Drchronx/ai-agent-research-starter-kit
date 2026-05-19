# Scenario Experiment Extraction Schema

Use this schema for a benchmark matrix. Keep unknown fields explicit.

## Required Columns

| Column | Meaning |
|---|---|
| `paper_id` | Short ID, e.g. `AuthorYear_Journal` |
| `verified` | `yes`, `partial`, or `no` |
| `title` | Exact title |
| `authors` | First author et al. or full authors if needed |
| `year` | Publication year |
| `journal` | Journal title |
| `doi_or_url` | DOI or stable URL |
| `ranking_claim_checked` | Whether UTD/FT50/AJG claim was checked for target year |
| `topic` | Substantive topic |
| `theory` | Theory actually used to explain mechanism |
| `study_number` | Study 1, Study 2A, etc. |
| `design` | Between-subjects, 2 x 2, within, mixed, choice, etc. |
| `iv_manipulation` | What changed across conditions |
| `scenario_context` | Setting, actor, task, stakes |
| `dv` | Dependent variable |
| `mediator` | Mediator if tested |
| `moderator` | Moderator if tested |
| `sample` | Platform/population |
| `n_final` | Final sample size |
| `cell_sizes` | Condition-level sample sizes |
| `exclusions` | Exclusion rules |
| `pretest_or_pilot` | Manipulation/stimulus validation before main study |
| `manipulation_check` | Item or test used |
| `realism_check` | Whether scenario realism was checked |
| `confound_check` | Alternative constructs checked |
| `analysis` | Main model and mechanism model |
| `effect_reporting` | p-values, SE/CI, effect sizes |
| `materials_available` | Appendix, OSF, journal supplement, unavailable |
| `transferable_pattern` | What to adapt for user's study |
| `risk_or_limitation` | What not to overclaim |

## Synthesis Template

After filling the matrix, write:

```text
1. Dominant design pattern:
2. Strongest manipulation pattern:
3. Common validity checks:
4. Common analysis models:
5. Common reporting conventions:
6. Patterns suitable for the user's topic:
7. Patterns to avoid:
8. Minimum study package recommended:
```

## Evidence Language

Use:

- "The paper reports..." for directly verified information.
- "The design implies..." for inference from methods/results.
- "Not reported in the accessible text" when the source is unavailable.
- "Needs verification in appendix/full text" when only abstract or metadata is available.

