# BibTeX 生成与复核模板

用途：让 AI 生成真实文献 BibTeX 后，逐条核验元数据和句子支持关系，避免假引用、错引用和弱引用。

## 1. 任务信息

| 字段 | 内容 |
|---|---|
| target_style | APA 7 / IEEE / Vancouver / Nature / Journal-specific |
| source_tool | AI4Scholar auto_cite / Crossref / DOI / Zotero / Publisher |
| topic |  |
| generated_date |  |
| auditor |  |

## 2. BibTeX 原文

```bibtex

```

## 3. 元数据核验表

| citation_key | title_match | authors_match | year_match | venue_match | DOI_match | URL_accessible | required_fields_missing | status |
|---|---|---|---|---|---|---|---|---|
|  | yes/no/uncertain | yes/no/uncertain | yes/no/uncertain | yes/no/uncertain | yes/no/uncertain | yes/no |  | verified / needs_fix / reject |

## 4. 句子级支持核验

| claim_sentence | inserted_citation | what_the_paper_actually_supports | support_strength | action |
|---|---|---|---|---|
|  |  |  | strong / partial / weak / reject | keep / replace / remove / manual_read |

## 5. 常见问题

- [ ] 引用支持的是相近主题，但不是当前句子的具体主张。
- [ ] 方法论文被用来支持理论主张。
- [ ] 综述论文被当成一手实证证据。
- [ ] 预印本被当成已发表论文。
- [ ] DOI 属于另一篇同名或相似题名论文。
- [ ] BibTeX 缺少 `journal`、`volume`、`number`、`pages` 或 `doi`。
- [ ] 作者姓名顺序或大小写错误。
- [ ] 期刊缩写不符合目标格式。

## 6. 最终可用 BibTeX

```bibtex

```

## 7. 不可用或需替换引用

| citation | reason | replacement_strategy |
|---|---|---|
|  |  |  |
