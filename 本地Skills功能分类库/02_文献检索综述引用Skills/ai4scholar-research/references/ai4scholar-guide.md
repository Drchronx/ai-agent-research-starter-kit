# AI4Scholar Beginner Guide

Source document supplied by the user:

```text
https://lifu-coze.feishu.cn/wiki/WOaewK33Ei2g1nkt44kcRXiBnze
```

Fetched title: `OpenClaw 教程：安装、配置与使用Ai4Scholar`  
Fetched date: 2026-05-16  

## What AI4Scholar Adds

AI4Scholar is useful when a task needs real literature search, citation support, PDF reading, automatic citation insertion, or scientific figure generation.

The source document describes two access modes:

| Mode | Use |
|---|---|
| MCP | Lightweight setup through `https://mcp.ai4scholar.net/sse` |
| OpenClaw plugin | Full setup with Scholar Mode, slash commands, and broader tool access |

## Get API Key

1. Open `https://ai4scholar.net`.
2. Register or log in.
3. Create an API key.
4. Store it safely.

Never paste the API key into a shared document or prompt history. Use `AI4SCHOLAR_API_KEY` as a placeholder in teaching material.

## MCP Setup

Add:

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

Restart the gateway or AI client.

## OpenClaw Plugin Setup

Install:

```bash
openclaw plugins install ai4scholar
```

Configure:

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

## Tool Families

The source document describes AI4Scholar capabilities across these families:

- Search: Semantic Scholar, PubMed, Google Scholar, arXiv, bioRxiv, medRxiv.
- Paper detail: single and batch details by common identifiers.
- Citation and references: citing papers, reference lists, related papers.
- Authors: author search, detail, papers, and batch lookup.
- Recommendations: based on one or more papers.
- PDF/full text: open-access PDF links, arXiv reading, DOI-based download when access permits.
- `auto_cite`: add real citations to academic text and return references/BibTeX.
- `sci_draw`: scientific drawing and figure generation.
- Slash commands in plugin mode: `/library`, `/projects`, `/reading-list`.

## Focused Skills Added To This Package

The package now splits the AI4Scholar source guide into task-specific Skills so users can copy only the function they need:

| Skill | Category | Use |
|---|---|---|
| `ai4scholar-paper-search` | Literature | Search real papers across Semantic Scholar, PubMed, Google Scholar, arXiv, bioRxiv, medRxiv |
| `ai4scholar-paper-detail-batch` | Literature | Verify one or many papers by DOI, PMID, arXiv ID, Semantic Scholar ID, or title |
| `ai4scholar-citation-network` | Literature | Trace citing papers, references, PubMed related papers, and citation gaps |
| `ai4scholar-author-intelligence` | Literature | Search scholars, retrieve author papers, compare experts, and reduce author ambiguity |
| `ai4scholar-paper-recommendation` | Literature | Recommend related papers from one or more seed papers |
| `ai4scholar-pdf-fulltext-reading` | Literature | Download/read OA PDFs and DOI-based full text when access permits |
| `ai4scholar-auto-citation-bibtex` | Literature | Use `auto_cite` for real citations, references, and BibTeX with audit |
| `ai4scholar-mcp-openclaw-setup` | Automation/MCP | Deploy AI4Scholar via MCP or OpenClaw plugin and troubleshoot Windows install failures |
| `ai4scholar-scholar-mode-projects` | Automation/MCP | Use Scholar Mode plus `/library`, `/projects`, and `/reading-list` |
| `ai4scholar-sci-draw` | Visualization | Use `sci_draw` for scientific diagrams, style transfer, figure review, and SVG-style outputs |

## Exact Tool Names From The Source Guide

Common AI4Scholar tools described by the source guide:

```text
search_semantic
search_pubmed
search_google_scholar
search_arxiv
search_biorxiv
search_medrxiv
search_semantic_snippets
search_semantic_bulk
search_semantic_paper_match
get_semantic_paper_detail
get_pubmed_paper_detail
get_semantic_paper_batch
get_pubmed_paper_batch
get_semantic_citations
get_semantic_references
get_pubmed_citations
get_pubmed_related
search_semantic_authors
get_semantic_author_detail
get_semantic_author_papers
get_semantic_author_batch
get_semantic_paper_authors
get_semantic_recommendations
get_semantic_recommendations_for_paper
download_semantic
read_semantic_paper
download_arxiv
read_arxiv_paper
download_biorxiv
download_medrxiv
read_biorxiv_paper
read_medrxiv_paper
download_by_doi
read_by_doi
auto_cite
sci_draw
```

## Beginner Workflows

### Search papers

```text
请用 AI4Scholar 搜索“AI Agent 与科研创造力”的近五年英文文献。输出 title、authors、year、venue、DOI、abstract、source，并说明哪些结果需要人工核验。
```

### Verify a DOI

```text
请用 AI4Scholar 查询 DOI: [DOI] 的论文详情，并用 citation-management 再核验作者、期刊、年份和 DOI。
```

### Read full text

```text
请用 AI4Scholar 尝试读取 arXiv:[ID] 的全文，并总结 Method、Data、Results。若全文提取失败，请说明失败原因，不要猜测。
```

### Add citations

```text
请用 AI4Scholar 的 auto_cite 给下面这段 Introduction 加 APA 引用。返回标注文本、参考文献列表和待人工核验项。
```

## Common Failure Handling

| Problem | Action |
|---|---|
| API key invalid | Recreate or reconfigure key |
| Search result empty | Broaden query and try another source |
| DOI download fails | Check institutional access; prefer open-access sources |
| PDF extraction poor | Use `pdf` or manual reading fallback |
| Windows plugin install fails | Use MCP mode or manual npm package method |
| Citation seems weak | Remove or mark as needing manual verification |

## Quality Standard

AI4Scholar can reduce fabricated citation risk, but it does not remove human responsibility. Final academic writing must still check whether each citation actually supports the sentence it is attached to.
