# 飞书文献日报表字段设计

用途：把每日文献检索、筛选、PDF 下载、BibTeX、学者画像和人工核验同步到飞书电子表格或多维表格。

## 一、推荐表 1：Daily Literature Report

| 字段名 | 类型 | 说明 |
|---|---|---|
| report_date | 日期 | 日报日期 |
| topic | 文本 | 追踪主题 |
| query | 文本 | 检索式 |
| source | 单选 | AI4Scholar / AMiner / OpenAlex / PubMed / arXiv / Semantic Scholar / CNKI |
| title | 文本 | 论文标题 |
| authors | 文本 | 作者 |
| year | 数字 | 年份 |
| venue | 文本 | 期刊/会议/预印本平台 |
| DOI | 文本 | DOI |
| PMID_arXiv_S2ID | 文本 | PMID / arXiv ID / Semantic Scholar ID |
| url | URL | 稳定链接 |
| abstract | 多行文本 | 摘要 |
| relevance_score | 数字 | 1-5 分 |
| method_tag | 多选 | experiment / survey / EEG / ERP / BCI / ML / DL / text mining / causal inference / review |
| theory_tag | 多选 | 使用的理论或机制标签 |
| pdf_status | 单选 | not_checked / open_access / downloaded / no_access / failed |
| pdf_local_path | 文本 | 本地 PDF 路径 |
| bibtex_status | 单选 | not_generated / generated / verified / needs_fix |
| verification_status | 单选 | unverified / partial / verified / rejected |
| manual_check_notes | 多行文本 | 人工核验备注 |
| next_action | 单选 | read / cite / download_pdf / check_author / ignore / add_to_zotero |

## 二、推荐表 2：Scholar Profiles

| 字段名 | 类型 | 说明 |
|---|---|---|
| scholar_name | 文本 | 学者姓名 |
| english_name | 文本 | 英文名或拼音 |
| affiliation | 文本 | 机构 |
| field | 文本 | 研究领域 |
| AMiner_url | URL | AMiner 页面 |
| representative_papers | 多行文本 | 代表作 |
| coauthors | 多行文本 | 合作者 |
| patents_or_outputs | 多行文本 | 专利或应用成果 |
| disambiguation_evidence | 多行文本 | 同名消歧证据 |
| verification_status | 单选 | unverified / partial / verified |
| notes | 多行文本 | 备注 |

## 三、推荐表 3：BibTeX Audit

| 字段名 | 类型 | 说明 |
|---|---|---|
| citation_key | 文本 | BibTeX key |
| title | 文本 | 题名 |
| authors | 文本 | 作者 |
| year | 数字 | 年份 |
| venue | 文本 | 期刊/会议 |
| DOI | 文本 | DOI |
| bibtex_raw | 多行文本 | 原始 BibTeX |
| required_fields_missing | 多行文本 | 缺失字段 |
| metadata_match | 单选 | yes / no / uncertain |
| support_strength | 单选 | strong / partial / weak / reject |
| audit_notes | 多行文本 | 核验说明 |

## 四、飞书写入方式

课堂建议先用本地 Excel 练习，确认字段后再写入飞书。

飞书电子表格常用方式：

```bash
# 创建表格，写入表头
lark-cli sheets +create --title "AI Agent 科研每日文献日报" --headers "report_date,topic,query,source,title,authors,year,venue,DOI,url,relevance_score,pdf_status,bibtex_status,verification_status,next_action"

# 向已有表格追加行
lark-cli sheets +append --spreadsheet-token "<spreadsheet_token>" --sheet-id "<sheet_id>" --values "<json rows>"
```

注意：

- 首次使用必须完成 `lark-cli config init` 或相应授权。
- Bot 和 user 身份能访问的资源不同。
- 不要把 API Key、AI4Scholar Token、AMiner Token 写入飞书表格。
- 批量写入前先用 1-2 行测试。
