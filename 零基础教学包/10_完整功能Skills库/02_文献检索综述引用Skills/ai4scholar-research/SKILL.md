---
name: ai4scholar-research
description: "Use AI4Scholar for real scholarly literature tasks through MCP or the OpenClaw plugin: paper search, Google Scholar/Semantic Scholar/PubMed/arXiv/bioRxiv/medRxiv queries, PDF download and reading, citation network lookup, author lookup, paper recommendations, auto_cite for real references, BibTeX, and sci_draw scientific figures. Trigger when the user mentions AI4Scholar, ai4scholar.net, mcp.ai4scholar.net, auto citation, real references, OpenClaw scholar plugin, Scholar Mode, or wants traceable citations."
---

# AI4Scholar Research

Use this skill when a task needs AI4Scholar's scholarly search, PDF reading, citation, auto-citation, or scientific drawing tools.

Primary source document: `https://lifu-coze.feishu.cn/wiki/WOaewK33Ei2g1nkt44kcRXiBnze`  
AI4Scholar MCP endpoint: `https://mcp.ai4scholar.net/sse`  
AI4Scholar website: `https://ai4scholar.net`

## Core Rule

Never fabricate references. AI4Scholar can help find real literature, but the final output must still report DOI, PMID, arXiv ID, URL, or another verification path whenever possible.

Never expose the API key. Refer to it as `AI4SCHOLAR_API_KEY` or "your AI4Scholar API key".

## Choose Access Mode

Use MCP mode when the user wants quick access or is not ready to install plugins.

Use OpenClaw plugin mode when the user wants the complete experience: more tools, Scholar Mode, project/library commands, and slash commands.

| Mode | Best for | Key tradeoff |
|---|---|---|
| MCP | Fast setup, paper search, PDF reading, citation, drawing | Fewer workflow conveniences |
| OpenClaw plugin | Full AI4Scholar toolset, Scholar Mode, slash commands | Requires OpenClaw and plugin config |

## MCP Setup

Add an MCP server entry:

```json
{
  "ai4scholar": {
    "url": "https://mcp.ai4scholar.net/sse",
    "headers": {
      "Authorization": "Bearer ${AI4SCHOLAR_API_KEY}"
    }
  }
}
```

Restart the MCP gateway or AI client after editing config.

## OpenClaw Plugin Setup

Requirements:

- OpenClaw installed.
- Node.js 18 or newer.
- AI4Scholar API key from `ai4scholar.net`.

Install:

```bash
openclaw plugins install ai4scholar
```

Configure `openclaw.json`:

```json
"ai4scholar": {
  "enabled": true,
  "config": {
    "apiKey": "${AI4SCHOLAR_API_KEY}"
  }
}
```

Restart:

```bash
openclaw gateway stop
openclaw gateway start
```

Verify:

```bash
openclaw plugins list
```

## Main Tool Families

Use the actual available tool schemas returned by the MCP server or plugin. Common AI4Scholar tool families include:

- Paper search: Semantic Scholar, PubMed, Google Scholar, arXiv, bioRxiv, medRxiv.
- Paper detail: DOI, arXiv ID, PMID, Semantic Scholar IDs, batch detail.
- Citation network: citing papers, references, related papers.
- Author lookup: author search, author detail, author papers, batch authors.
- Recommendation: paper-based recommendations.
- PDF and full-text: open-access links, arXiv reading, DOI-based download when access is available.
- Auto citation: `auto_cite` for adding references to academic text.
- Scientific drawing: `sci_draw` for research figures.

## Focused Local Skills

This skill is the hub. For narrower tasks, route to the focused local skill:

| Focused skill | Use |
|---|---|
| `ai4scholar-paper-search` | Multi-source real paper search |
| `ai4scholar-paper-detail-batch` | Single or batch metadata verification |
| `ai4scholar-citation-network` | Backward/forward citations and related papers |
| `ai4scholar-author-intelligence` | Scholar, expert, lab, and reviewer discovery |
| `ai4scholar-paper-recommendation` | Related-paper recommendations from seed papers |
| `ai4scholar-pdf-fulltext-reading` | PDF download and full-text extraction |
| `ai4scholar-auto-citation-bibtex` | `auto_cite`, reference list, and BibTeX audit |
| `ai4scholar-sci-draw` | `sci_draw` scientific figures |
| `ai4scholar-mcp-openclaw-setup` | MCP/OpenClaw deployment and troubleshooting |
| `ai4scholar-scholar-mode-projects` | Scholar Mode, `/library`, `/projects`, `/reading-list` |

## Literature Search Workflow

1. Translate the research question into 2-4 English query strings and, if relevant, 1-2 Chinese query strings.
2. Search across at least two sources when possible.
3. Export structured metadata: title, authors, year, venue, DOI/PMID/arXiv ID, abstract, citation count, URL.
4. Deduplicate by DOI, title, and year.
5. Screen results by relevance, method match, and venue quality.
6. Verify high-value papers through `citation-management` or original publisher pages.
7. Write an evidence table before writing prose.

## Auto-Citation Workflow

Use `auto_cite` only after clarifying:

- Target citation style: APA, IEEE, Vancouver, or Nature.
- Text length and topic.
- Whether citations should prioritize classic papers, recent papers, or top journals.

After tool output:

- Check every reference for DOI or stable identifier.
- Remove references that do not support the sentence they were attached to.
- Mark weak matches as "needs manual verification".
- Do not submit auto-cited text without human review.

## PDF Reading Workflow

Prefer open-access sources first:

- arXiv, bioRxiv, medRxiv.
- Semantic Scholar open-access PDF.
- DOI download only when institutional access is available.

If PDF extraction is poor:

- Report the extraction problem.
- Use `pdf` or `markitdown` as fallback.
- Do not infer methods/results from unreadable sections.

## Output Template

```text
Task:
AI4Scholar access mode:
Search sources used:
Query strings:
Screening criteria:
Top papers:
Verified identifiers:
Citation or PDF status:
Unverified references:
Recommended next steps:
```

## Reference

For detailed beginner instructions, read `references/ai4scholar-guide.md`.
