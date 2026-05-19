---
name: ai4scholar-scholar-mode-projects
description: "Use AI4Scholar OpenClaw plugin Scholar Mode and slash commands for literature projects, local paper library, project reading lists, and academic assistant context. Trigger for /library, /projects, /reading-list, Scholar Mode, AI4Scholar project workflow, downloaded-paper library, or managing papers inside OpenClaw."
---

# AI4Scholar Scholar Mode And Project Commands

Use this skill when AI4Scholar is installed as the OpenClaw plugin and the user wants project/library workflow support beyond raw MCP calls.

## Availability Rule

This skill requires the OpenClaw AI4Scholar plugin. If the user only configured MCP mode, use `ai4scholar-mcp-openclaw-setup` or the focused literature skills instead.

## Source Guide Capabilities

The source guide says plugin mode adds:

- the full AI4Scholar toolset,
- Scholar Mode academic assistant context,
- slash commands:
  - `/library`,
  - `/projects`,
  - `/reading-list`.

## Slash Commands

| Command | Use |
|---|---|
| `/library` | List papers downloaded in the current project |
| `/projects` | List literature projects |
| `/reading-list` | Show the current project's reading list |

## Project Workflow

1. Start with a research question and create or select a project.
2. Search papers with `ai4scholar-paper-search`.
3. Add high-value papers to the reading list.
4. Use `/reading-list` to inspect pending papers.
5. Use AI4Scholar full-text tools to read priority papers.
6. Use `/library` to list downloaded papers.
7. Build a literature matrix with:
   - theory,
   - method,
   - data/sample,
   - variables,
   - key findings,
   - DOI/ID,
   - reading status.

## Reading List Triage

Classify each paper:

| Status | Meaning |
|---|---|
| `must_read` | Directly supports theory, method, or benchmark |
| `skim` | Background or adjacent |
| `citation_check` | Useful only if citation support is verified |
| `exclude` | Not relevant enough |

## Beginner Prompt

```text
Use the AI4Scholar OpenClaw plugin Scholar Mode workflow.
First use /projects and /reading-list to inspect the current project status, then build a reading list around "[topic]".
Classify papers as must_read, skim, citation_check, or exclude, and return the next reading order.
```

## Output Template

```text
Plugin mode status:
Project:
Library status:
Reading list status:

Recommended reading actions:
| Paper | Status | Why | Next action |

Commands used:
```

## Safety

- Do not expose API keys from project config.
- Do not assume downloaded PDFs are legally shareable.
- If library commands are unavailable, report that plugin mode may not be active.
