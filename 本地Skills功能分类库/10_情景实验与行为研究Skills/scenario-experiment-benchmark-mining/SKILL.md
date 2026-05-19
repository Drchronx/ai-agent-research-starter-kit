---
name: scenario-experiment-benchmark-mining
description: "Mine and synthesize real top-journal scenario/vignette experiment patterns for behavioral research. Use when the user asks to learn from UTD24, FT50, AJG/ABS4, JCR, JCP, JM, JMR, ISR, MISQ, JAP, OBHDP, JPSP, Psychological Science, or other top journals; extract experiment design, stimuli, manipulations, pretests, data analysis, mediation/moderation, reporting style, and reusable research templates from verified papers; build journal benchmark matrices for scenario experiment design."
---

# Scenario Experiment Benchmark Mining

Use this skill to learn scenario/vignette experiment craft from verified top-journal papers instead of relying on generic advice.

## Non-Negotiables

- Use real, verifiable papers only. Do not fabricate titles, authors, journals, DOIs, sample sizes, or results.
- Verify the target ranking list and year before claiming a journal is UTD24, FT50, AJG/ABS 4, or AJG/ABS 4*.
- Separate direct evidence from inference. If an article's appendix or data/code is unavailable, mark the field as "not reported" or "not verified".
- Prefer the user's domains: management, marketing, information systems, psychology, consumer behavior, AI agent use, HCI, neuro/behavioral decision research.

## When To Use Which Reference

- Use `references/journal-scope-map.md` to choose journals and search routes.
- Use `references/extraction-schema.md` to build the paper-by-paper benchmark matrix.
- Use `scripts/make_benchmark_matrix.py` to create a blank CSV extraction sheet.

## Workflow

### 1. Define the benchmark target

Ask or infer:

- Research topic and construct family.
- Target journal family: marketing, applied psychology, information systems, management, social/personality psychology.
- Desired study type: two-condition vignette, 2 x 2 experiment, mediated design, moderated mediation, choice experiment, multi-study package.
- Output format: benchmark matrix, design playbook, analysis playbook, or journal-style writing template.

### 2. Build a verified article pool

Search real literature through available academic tools such as AI4Scholar, AMiner, OpenAlex, Semantic Scholar, PubMed for psychology/medicine-adjacent work, publisher pages, Crossref, or the journal website.

Use query patterns such as:

```text
("scenario" OR "vignette" OR "experiment" OR "manipulation" OR "randomly assigned") AND [topic]
site:[journal domain] [topic] experiment manipulation
[journal name] [construct] scenario experiment mediation
```

For each candidate, verify at least:

- Title.
- Authors.
- Journal.
- Year.
- DOI or stable URL.
- Whether it actually contains an experiment, not only survey, archival, or qualitative evidence.

### 3. Extract experiment architecture

For every usable paper, extract:

- Theoretical problem and contribution.
- Construct-to-manipulation mapping.
- Number of studies and role of each study.
- Scenario content and manipulated elements.
- Pretest or pilot evidence.
- Manipulation, realism, attention, suspicion, and confound checks.
- Sample source, cell sizes, exclusions, and final N.
- DV, mediator, moderator, covariates, and measurement sources.
- Analysis model: ANOVA, regression, logistic model, mediation, moderation, moderated mediation, multilevel model, SEM, or robustness tests.
- Reporting style: exact p-values, standard errors/CIs, effect sizes, tables, figures, appendix materials.

### 4. Synthesize reusable patterns

Do not merely summarize papers. Convert them into reusable decisions:

- What design choice made the causal claim credible?
- What confound did the authors prevent?
- What analysis matched the hypothesis?
- What reporting move made the result easy to audit?
- What should the user copy, adapt, or avoid?

### 5. Produce output

Default output:

```text
Verified article pool:
Benchmark extraction matrix:
Cross-journal design patterns:
Recommended design for user's topic:
Recommended analysis plan:
Recommended reporting template:
Evidence gaps and items to verify:
```

## Quality Bar

A useful benchmark report should let the user design a new study, not just know which papers exist. It must translate top-journal examples into concrete choices for stimulus construction, manipulation checks, sample planning, model specification, and Results writing.
