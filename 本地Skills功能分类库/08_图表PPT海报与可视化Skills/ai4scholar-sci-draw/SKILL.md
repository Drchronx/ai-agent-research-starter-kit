---
name: ai4scholar-sci-draw
description: "Use AI4Scholar sci_draw for scientific figure generation and editing: text-to-image, Chinese scientific diagrams, image editing, style transfer, multi-image composition, iterative refinement, figure review, and SVG vector output. Trigger for AI4Scholar scientific drawing, sci_draw, paper figures, mechanism diagrams, graphical abstracts, neuroscience/BCI schematics, or publication-style figure polishing."
---

# AI4Scholar Sci Draw

Use this skill for scientific figure generation or figure refinement through AI4Scholar `sci_draw`.

## Core Rules

- Do not invent experimental results, data values, brain maps, statistical annotations, or electrode effects.
- For data figures, use the user's real data and deterministic plotting tools first; use `sci_draw` for schematics, conceptual figures, mechanism diagrams, or style refinement.
- Keep figure text short and publication-readable.
- Preserve scientific meaning during style transfer or editing.

## Tool From The Source Guide

| Tool | Use |
|---|---|
| `sci_draw` | AI scientific drawing: Chinese prompts, text-to-image, image editing, style transfer, multi-image composition, iterative optimization, figure review, SVG vector output |

## Good Use Cases

- Graphical abstract for a manuscript.
- EEG/ERP experiment procedure diagram.
- BCI pipeline figure: acquisition, preprocessing, feature extraction, classifier, feedback.
- Management or psychology scenario-experiment flow.
- Text-mining or machine-learning architecture schematic.
- Polishing an existing conceptual figure into journal style.
- Converting a rough sketch into SVG-like vector style.

## Figure Workflow

1. Identify figure type:
   - mechanism,
   - workflow,
   - architecture,
   - experimental procedure,
   - graphical abstract,
   - review framework,
   - visual polishing.
2. Extract required scientific content:
   - constructs,
   - variables,
   - sample/stimuli,
   - pipeline steps,
   - model components,
   - labels.
3. Draft a compact prompt.
4. Generate or edit using `sci_draw`.
5. Review:
   - scientific accuracy,
   - label correctness,
   - readability,
   - color accessibility,
   - consistency with target journal.
6. Iterate with specific correction prompts.

## Prompt Template

```text
Use AI4Scholar sci_draw to generate a publication-style scientific figure.
Figure type: [mechanism diagram / workflow / BCI pipeline / EEG experiment procedure / graphical abstract]
Research topic:
Required elements:
Forbidden elements:
Language: [Chinese / English]
Style: [minimal journal style / neuroscience style / management theory model / machine-learning architecture]
Output requirement: [PNG / SVG / editable vector preferred]
```

## Figure Review Checklist

| Check | Requirement |
|---|---|
| Scientific accuracy | No unsupported claims or fake numeric effects |
| Structure | Readers can follow the causal/process logic |
| Labels | Correct terminology, no typo, no overcrowding |
| Accessibility | High contrast; avoid color-only encoding |
| Journal fit | Not decorative; suitable for manuscript, slide, or poster |

## Common Corrections

```text
Keep the original structure unchanged, translate labels into English, and reduce decorative elements.
```

```text
Make EEG preprocessing, feature extraction, classifier, and feedback a horizontal workflow. Do not add nonexistent data results.
```

```text
Convert the figure into a theory-mechanism model suitable for an SSCI management paper. Preserve variable names and arrow directions.
```
