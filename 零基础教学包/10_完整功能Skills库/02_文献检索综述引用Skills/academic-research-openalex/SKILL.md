---
name: academic-research
version: 1.0.0
description: Search academic papers and conduct literature reviews using OpenAlex API (free, no key needed). Use when the user needs to find scholarly papers by topic/author/DOI, explore citation chains, get structured paper metadata (title, authors, abstract, citations, DOI, open access URL), fetch full text of open access papers, or conduct automated literature reviews with theme identification and synthesis. Triggers on requests involving academic search, paper lookup, citation analysis, literature review, research synthesis, or scholarly reference gathering.
---

# Academic Research

Search 250M+ academic works via OpenAlex. No API key required.

Built by [Topanga](https://topanga.ludwitt.com) — AI Research Consultant

## Quick Start

### Search papers by topic
```bash
python3 scripts/scholar-search.py search "transformer architectures" --limit 10
```

### Search by author
```bash
python3 scripts/scholar-search.py author "Yann LeCun" --limit 5
```

### Look up by DOI
```bash
python3 scripts/scholar-search.py doi "10.1038/s41586-021-03819-2"
```

### Get citation chain (papers that cite a work)
```bash
python3 scripts/scholar-search.py citations "10.1038/s41586-021-03819-2" --direction both
```

### Deep read (fetch abstract + full text when available)
```bash
python3 scripts/scholar-search.py deep "10.1038/s41586-021-03819-2"
```

### JSON output for programmatic use
```bash
python3 scripts/scholar-search.py search "CRISPR" --json
```

## Literature Review Workflow

Automated multi-step literature review:

```bash
python3 scripts/literature-review.py "algorithmic literacy in education" --papers 30 --output review.md
```

This will:
1. Search for papers across multiple query variations
2. Deduplicate and rank by relevance + citations
3. Identify thematic clusters
4. Generate a structured synthesis in markdown

Options:
- `--papers N` — Target number of papers (default: 20)
- `--output FILE` — Write review to file (default: stdout)
- `--years 2020-2025` — Restrict publication year range
- `--json` — Output structured JSON instead of markdown

## Output Format

All search commands return structured data per paper:
- **Title** and publication year
- **Authors** (up to 5)
- **Abstract** (when available)
- **Citation count**
- **DOI**
- **Open access URL** (when available)
- **Source journal/venue**

## Tips

- OpenAlex sorts by relevance by default; use `--sort citations` for most-cited
- Combine `search` + `deep` for quick triage: search first, deep-read promising hits
- The literature review script caches results in `/tmp/litreview_cache/` to avoid re-fetching
- For full-text PDFs, pipe DOIs to your PDF extraction tool

---

## ⏱️ 超时处理与重试机制（v1.0.1 新增）

**超时配置：**
- 单次检索超时时间：**5 分钟**
- 最大重试次数：**3 次**
- 重试间隔：**5 秒**

**重试策略：**
```
第 1 次失败 → 等待 5 秒 → 重试（减少 limit 参数）
第 2 次失败 → 等待 5 秒 → 重试（简化查询词）
第 3 次失败 → 记录失败原因 → 向主人汇报
```

**OpenAlex API 限制：**
- 免费 API 无 key，但有速率限制
- 建议单次检索不超过 100 条结果
- 多次检索之间添加延迟

**失败后处理：**
1. 记录失败原因（API 超时 / 解析失败 / 网络错误）
2. 向主人汇报："OpenAlex 检索失败，原因：XXX，已重试 3 次"
3. 如 CNKI 和 Google Scholar 已完成，可继续撰写综述
4. 在文档中标注缺失的数据源
