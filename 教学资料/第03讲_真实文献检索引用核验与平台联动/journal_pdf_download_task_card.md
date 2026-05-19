# 目标期刊 PDF 自动下载任务卡

用途：按目标期刊、关键词、时间范围自动检索文献，并把合法可获取的 PDF 下载到本地。

## 1. 任务目标

```text
从指定目标期刊中检索与我的研究主题相关的论文，下载开放获取或已有权限的 PDF 到本地，并生成下载日志和未获取清单。
```

## 2. 输入

| 字段 | 示例 |
|---|---|
| topic | AI agents in literature review automation |
| target_journals | Journal of Consumer Research; Journal of Applied Psychology; Information Systems Research |
| time_range | 2021-2026 |
| keywords | AI agent; scholarly search; literature review automation; human-AI collaboration |
| access_policy | open-access first; DOI access only if institutional access permits |
| local_pdf_dir | literature/pdfs/ |

## 3. 可用 Skills

- `ai4scholar-paper-search`
- `ai4scholar-paper-detail-batch`
- `ai4scholar-pdf-fulltext-reading`
- `citation-management`
- `pdf`
- `markitdown`

## 4. Agent 执行步骤

1. 构造检索式：

```text
("AI agent" OR "autonomous agent" OR "LLM agent") AND ("literature review" OR "scholarly search")
```

2. 限定期刊和年份。
3. 用 AI4Scholar 或其他真实数据库检索。
4. 对候选论文做 DOI/URL/年份/期刊核验。
5. 优先尝试开放获取 PDF：

```text
arXiv / bioRxiv / medRxiv / Semantic Scholar OA / publisher OA
```

6. DOI 下载只在合法权限允许时执行。
7. 保存 PDF 到：

```text
literature/pdfs/{year}_{first_author}_{short_title}.pdf
```

8. 生成：

```text
literature/pdf_download_log.xlsx
literature/pdf_download_failures.md
literature/verified_references.bib
```

## 5. 禁止事项

- 不绕过版权或付费墙。
- 不使用盗版网站。
- 不把无法下载的论文写成已下载。
- 不从标题或摘要推断全文方法和结果。
- 不把机构权限下载的 PDF 公开分享。

## 6. 下载日志字段

| 字段 | 说明 |
|---|---|
| paper_id | 论文编号 |
| title | 标题 |
| authors | 作者 |
| year | 年份 |
| venue | 期刊/会议 |
| DOI | DOI |
| access_route | arXiv / Semantic Scholar OA / DOI / publisher OA / unavailable |
| pdf_status | downloaded / failed / no_access / unreadable |
| local_path | 本地保存路径 |
| extraction_quality | good / partial / poor |
| manual_check | 需人工核验项 |

## 7. 核验清单

- [ ] DOI 与题名一致。
- [ ] 期刊与年份一致。
- [ ] PDF 文件是否完整。
- [ ] PDF 是否为目标论文而非补充材料。
- [ ] 本地文件名是否可追踪。
- [ ] 是否记录失败原因。
- [ ] 是否遵守版权和机构权限要求。
