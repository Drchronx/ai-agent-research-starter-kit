# Search Backend Contract

The literature reviewer skill delegates retrieval to backend skills. Retrieval backends return normalized paper metadata; the reviewer skill does not own database-specific automation.

## Backend Selection Matrix

| Need | Backend | Skill Path | Data Source | Notes |
| --- | --- | --- | --- | --- |
| Chinese CNKI papers | `cnki-crawler` | `../cnki-crawler` | CNKI 知网 | 中文文献首选 |
| English scholarly papers | `academic-research` | `../academic-research` | OpenAlex | 2.5 亿 + 论文，免费无 key |
| English supplementary | `academic-research-hub` | `../academic-research-hub` | Google Scholar | 补充会议论文和预印本 |
| Future databases | dedicated skill | `../<new-skill>` | TBD | 添加新行，不改工作流 |

## Backend Configuration

### 1. CNKI Backend (`cnki-crawler`)

**Location:** `/root/.openclaw/skills/cnki-crawler`

**Prerequisites:**
```bash
cd /root/.openclaw/skills/cnki-crawler
python -m pip install -r requirements.txt
cp .env.example .env
# Edit .env: set CNKI_DB_DSN, CNKI_PROXY_HTTP, CNKI_PROXY_HTTPS
```

**Command:**
```bash
python scripts/main.py "SU='主题词'" \
  --start-year 2020 \
  --end-year 2025 \
  --limit-pages 10
```

**Query Syntax:**
- 必须阅读 `../cnki-crawler/reference/专业检索语法.md`
- 年份通过 `--start-year/--end-year` 参数传递，**不要**嵌入专业检索表达式
- 常用字段：`SU=主题`, `TI=题名`, `AB=摘要`, `KY=关键词`, `AU=作者`

**Output Mapping:**
```python
{
  "source_db": "cnki",
  "backend": "cnki-crawler",
  "backend_query": "SU='主题词'",
  "title": paper.title,
  "authors": paper.authors,  # List[str]
  "journal": paper.journal,
  "year": paper.year,
  "abstract": paper.abstract,
  "keywords": paper.keywords,
  "doi": paper.doi,
  "source_url": paper.url,
  "language": "zh"
}
```

**Failure Behavior:**
- 超时：5 分钟，重试 3 次，间隔 5 秒
- 失败后：记录警告，继续其他后端，如论文不足则询问用户

---

### 2. OpenAlex Backend (`academic-research`)

**Location:** `/root/.openclaw/skills/academic-research`

**Prerequisites:**
```bash
cd /root/.openclaw/skills/academic-research
# No API key required, uses OpenAlex free API
```

**Command:**
```bash
python3 scripts/scholar-search.py search "transformer architectures" \
  --limit 50 \
  --json > openalex_results.json
```

**Advanced Options:**
```bash
# Sort by citations
python3 scripts/scholar-search.py search "deep learning" --sort citations --limit 50

# Filter by year
python3 scripts/scholar-search.py search "AI ethics" --from-year 2020 --to-year 2024

# Search by author
python3 scripts/scholar-search.py author "Yann LeCun" --limit 20

# Get citation chain
python3 scripts/scholar-search.py citations "10.1038/s41586-021-03819-2" --direction both
```

**Output Mapping:**
```python
{
  "source_db": "openalex",
  "backend": "academic-research",
  "backend_query": "transformer architectures",
  "title": paper.title,
  "authors": [a.display_name for a in paper.authorships[:5]],
  "journal": paper.primary_location.source.display_name if paper.primary_location else "",
  "year": paper.publication_year,
  "abstract": paper.abstract,
  "doi": paper.doi,
  "source_url": paper.open_access.url if paper.open_access else paper.url,
  "cited_count": paper.cited_by_count,
  "language": "en"
}
```

**Failure Behavior:**
- 超时：5 分钟，重试 3 次，间隔 5 秒
- 速率限制：单次不超过 100 条，检索间添加延迟
- 失败后：记录警告，继续 Google Scholar 或 CNKI

---

### 3. Google Scholar Backend (`academic-research-hub`)

**Location:** `/root/.openclaw/skills/academic-research-hub`

**Prerequisites:**
```bash
cd /root/.openclaw/skills/academic-research-hub
pip install lxml requests
```

**Command:**
```bash
python scripts/research.py "machine learning" \
  --max-results 50 \
  --format json \
  --output scholar_results.json
```

**Advanced Options:**
```bash
# Filter by year range
python scripts/research.py "deep learning" \
  --start-year 2020 --end-year 2024 \
  --format json --output results.json

# Sort by date (most recent first)
python scripts/research.py "large language models" \
  --sort-by date --format json --output results.json

# Generate BibTeX
python scripts/research.py "neural networks" \
  --format bibtex --output references.bib
```

**Output Mapping:**
```python
{
  "source_db": "google_scholar",
  "backend": "academic-research-hub",
  "backend_query": "machine learning",
  "title": paper.title,
  "authors": paper.authors,  # List[str]
  "year": paper.year,
  "journal": paper.venue or "",
  "abstract": paper.snippet or "",
  "source_url": paper.url,
  "cited_count": paper.citations,
  "language": "en"
}
```

**Failure Behavior:**
- 超时：5 分钟，重试 3 次，间隔 10 秒
- 速率限制：每小时不超过 50 次检索，"Unusual traffic detected" 时等待 10-15 分钟
- 失败后：记录警告，如 OpenAlex 已完成可继续撰写，建议用户稍后补做

---

## Unified Retrieval Flow

```
Phase 2: Backend Retrieval
│
├── Step 2.1: CNKI Retrieval (Chinese papers)
│   ├── Generate CNKI query from Chinese keywords
│   ├── Run cnki-crawler with year filters
│   └── Save to papers_raw.json (source_db: "cnki")
│
├── Step 2.2: OpenAlex Retrieval (English papers - primary)
│   ├── Generate English query
│   ├── Run academic-research with JSON output
│   └── Append to papers_raw.json (source_db: "openalex")
│
├── Step 2.3: Google Scholar Retrieval (English papers - supplementary)
│   ├── Run academic-research-hub if needed
│   └── Append to papers_raw.json (source_db: "google_scholar")
│
└── Step 2.4: Merge Results
    ├── Combine all backend outputs
    ├── Record backend status in session_log.md
    └── Proceed to Phase 3 (Deduplication)
```

## Normalized Paper Schema

All backends must return papers in this format:

```json
{
  "id": "C1",  // Assigned during deduplication: C1, C2... (Chinese) or E1, E2... (English)
  "source_db": "cnki|openalex|google_scholar",
  "backend": "cnki-crawler|academic-research|academic-research-hub",
  "backend_query": "original query string",
  "title": "Paper Title",
  "authors": ["Author 1", "Author 2"],
  "organizations": ["Affiliation 1"],
  "journal": "Journal/Conference Name",
  "year": 2024,
  "publish_date": "2024-01-01",
  "volume": "",
  "issue": "",
  "pages": "",
  "doi": "10.xxxx/xxxxx",
  "abstract": "Abstract text...",
  "keywords": ["keyword1", "keyword2"],
  "funds": [],
  "cited_count": 150,
  "download_count": "",
  "source_url": "https://...",
  "language": "zh|en"
}
```

## Routing Rules

1. **Year Filters:** Never embed year filters in CNKI professional search expressions. Use `--start-year/--end-year` parameters.

2. **Raw Storage:** Keep all backend results in `papers_raw.json` before normalization and deduplication.

3. **Auditability:** Preserve both `backend` and `backend_query` fields for traceability.

4. **Failure Handling:**
   - Record warnings in `session_log.md`
   - Continue with successful backends if enough papers remain (≥20)
   - If insufficient papers, ask user: retry failed backend or adjust query?

5. **Adding New Backends:**
   - Add a row to the Backend Selection Matrix table
   - Document: trigger name, required inputs, command/API call, output mapping, failure behavior
   - Do not modify the core 8-phase workflow

## Session Logging

Record retrieval status in `sessions/{YYYYMMDD}_{topic}/session_log.md`:

```markdown
## Phase 2: Backend Retrieval Status

| Backend | Query | Status | Papers Found | Warnings |
|---------|-------|--------|--------------|----------|
| cnki-crawler | SU='耐心资本' | ✅ Success | 45 | None |
| academic-research | "patient capital" | ✅ Success | 38 | None |
| academic-research-hub | "patient capital" | ⚠️ Partial | 12 | Rate limit detected |

**Total Raw Papers:** 95
**Proceed to Phase 3:** Yes
```
