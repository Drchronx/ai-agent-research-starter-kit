# 每日文献日报模板

用途：每天自动或半自动追踪指定主题、期刊、作者、机构或关键词的新文献，并同步到本地表格或飞书表格。

## 0. 日报元信息

| 字段 | 内容 |
|---|---|
| report_date |  |
| generated_by |  |
| search_window | 例如：过去 24 小时 / 过去 7 天 |
| topic |  |
| databases | AI4Scholar / AMiner / OpenAlex / PubMed / arXiv / Semantic Scholar / CNKI |
| verification_status | 未核验 / 部分核验 / 已核验 |

## 1. 今日新增论文概览

| paper_id | title | authors | year | venue | DOI/ID | source | relevance_score | verification_status |
|---|---|---|---|---|---|---|---:|---|
|  |  |  |  |  |  |  |  |  |

## 2. 今日最值得读的 3-5 篇

### Paper 1

| 字段 | 内容 |
|---|---|
| title |  |
| why_read |  |
| method |  |
| theory_or_topic |  |
| possible_use | 文献综述 / 理论建构 / 方法学习 / 数据来源 / 审稿回应 |
| verification_needed |  |

## 3. 今日学者 / 团队 / 机构动态

| target | AMiner evidence | representative papers | coauthor_network | verification_status |
|---|---|---|---|---|
|  |  |  |  |  |

## 4. 今日 PDF 下载状态

| paper_id | access_route | pdf_status | local_path | extraction_status | manual_check |
|---|---|---|---|---|---|
|  | arXiv / Semantic Scholar OA / DOI / publisher / unavailable | downloaded / failed / no OA |  |  |  |

## 5. 今日引用与 BibTeX 状态

| paper_id | citation_status | bibtex_status | DOI_verified | metadata_verified | action |
|---|---|---|---|---|---|
|  | usable / weak / reject | generated / missing / error | yes / no | yes / no |  |

## 6. 今日风险与人工核验项

- [ ] DOI 是否真实。
- [ ] 期刊/会议名称是否准确。
- [ ] 作者是否同名误配。
- [ ] AMiner 学者画像是否与机构、领域、代表作一致。
- [ ] PDF 是否为合法开放获取或有机构权限。
- [ ] BibTeX 是否字段完整。
- [ ] 引用是否真正支撑句子。

## 7. 明日追踪任务

```text

```
