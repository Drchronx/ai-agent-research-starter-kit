---
name: theory-variable-method-matrix
description: "Build and maintain a theory-variable-method matrix from papers, Zotero metadata, Obsidian paper cards, and research notes. Use for mapping theories to constructs, variables, measurements, experimental designs, EEG/ERP/BCI methods, text-mining methods, causal designs, and manuscript evidence tables."
---

# Theory Variable Method Matrix

Use this skill to convert scattered paper notes into a structured research matrix that shows which theories, variables, methods, measures, datasets, and findings are reusable.

## Core Rules

- Do not use theory as a label only. Record the mechanism that links theory to variables.
- Keep measured variables separate from theoretical constructs.
- Record method details precisely enough to reproduce or adapt.
- Every row must point back to a real paper or a Zotero key.
- Mark unsupported or weakly interpreted entries.

## Matrix Columns

Use these minimum columns:

```text
paper_id
zotero_key
citation
field
research_question
theory
mechanism
construct
variable_role
variable_name
definition
measurement
method_design
sample_data
analysis_model
key_result
effect_direction
limitations
reuse_for_my_project
verification_status
note_link
```

## Variable Roles

Use stable role labels:

```text
iv
dv
mediator
moderator
control
manipulation_check
realism_check
confound_check
eeg_feature
erp_component
behavioral_measure
text_variable
outcome
mechanism
boundary_condition
```

## Workflow

1. Select a project or research question.
2. Collect paper cards or Zotero items.
3. For each paper, extract:
   - theory,
   - mechanism,
   - constructs,
   - measured variables,
   - method,
   - analysis model,
   - key result,
   - reusable idea.
4. Normalize variable names.
5. Split mixed entries into multiple rows if a paper has multiple mechanisms or experiments.
6. Export CSV and Markdown tables.
7. Use the matrix to identify gaps:
   - theory without measurement,
   - variable without validated scale,
   - method without precedent,
   - causal claim without design support.

## Output Template

```text
Project:
Papers included:
Matrix file:

Top reusable theories:
| Theory | Mechanism | Papers | Reuse |

Variable map:
| Construct | Measure | Role | Papers | Notes |

Method map:
| Method | Design details | Papers | Reuse |

Gaps and risks:
```

## Beginner Prompt

```text
Use theory-variable-method-matrix to build a matrix for my project.
Input papers are from Zotero/Obsidian.
Extract theory, mechanism, variables, measures, method, sample, model, key results, and how each paper can be reused.
Do not treat theories as decorative labels.
```

## When To Combine

- Use `obsidian-paper-card` first when paper notes are missing.
- Use `scale-selection-adaptation` for measurement source checks.
- Use `scenario-experiment-design` when the matrix suggests a possible experimental design.
- Use `causal-inference-design-audit` when causal language appears.
