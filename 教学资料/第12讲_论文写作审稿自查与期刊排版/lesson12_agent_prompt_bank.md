# 第12讲 Agent Prompt Bank

## Prompt 1：生成证据包

```text
请读取 input/ 下的研究问题、假设、文献、方法计划、结果表和图表计划，生成 manuscript/evidence_pack.md。每条证据包含 claim、evidence source、result/table/figure、citation needed、support strength、risk、manuscript section。禁止编造不存在的数据、引用或结果。
```

## Prompt 2：生成论文故事线

```text
请基于 evidence_pack.md，生成 manuscript/manuscript_storyline.md。结构包括 problem、context、theoretical tension、gap、mechanism、hypotheses、method fit、main findings、contribution、limitations。不要写空泛贡献。
```

## Prompt 3：生成 Reverse Outline

```text
请生成 manuscript/reverse_outline.md。按章节列出 paragraph purpose、topic sentence、evidence、citation、link to next paragraph、risk。每段只服务一个核心功能。
```

## Prompt 4：写 Methods

```text
请基于 input/方法计划.md、input/数据说明.md 和 evidence_pack.md，写 manuscript/methods.md。要求可复现，包含样本、程序、变量、测量、统计方法、伦理和排除规则。禁止编造未提供的信息，不确定处标待人工核验。
```

## Prompt 5：写 Results

```text
请基于 input/结果表.xlsx 和 input/统计输出.md，写 manuscript/results.md。所有数值必须来自输入表，不得改动。报告主结果、机制/调节、稳健性、非显著结果、效应量和置信区间。不要把相关结果写成因果证明。
```

## Prompt 6：写 Introduction

```text
请基于 manuscript_storyline.md、reverse_outline.md 和 references/reference_audit.xlsx，写 manuscript/introduction.md。按问题、文献张力、gap、研究方案、贡献推进。引用必须真实且支持句子，不确定引用标待人工核验。
```

## Prompt 7：引用核验

```text
请使用 citation-management。读取 manuscript/ 草稿和 references/references.bib，生成 references/reference_audit.xlsx。检查正文引用、参考文献条目、缺失 DOI/volume/issue/pages、引用支持句子和人工核验项。不得编造缺失字段。
```

## Prompt 8：审稿自查

```text
请使用 peer-review 和 scientific-critical-thinking，生成 qc/reviewer_risk_audit.md。按 severity 排序列出 contribution、theory、method、statistics、causality、citation、figure/table、reproducibility、ethics 风险，并给出具体修改方案。
```

## Prompt 9：期刊排版流水线

```text
请生成 formatting/formatting_pipeline.md。目标格式：[APA 7 / 目标期刊]。依次处理 title page、abstract keywords、heading hierarchy、in-text citations、reference list、captions、statistics units、layout spacing、footnote/endnote、blind review。每步输出输入、规则、输出和人工核验项。
```

## Prompt 10：盲审匿名化

```text
请使用 journal-blind-review-anonymizer，生成 formatting/blind_review_checklist.md。检查作者姓名、单位、致谢、基金、自引、数据仓库、文件属性、补充材料和图表身份线索。输出 author version 与 blind version 差异清单。
```

## Prompt 11：Cover Letter

```text
请基于 manuscript_storyline.md 和 reviewer_risk_audit.md，生成 output/cover_letter.md。内容包括投稿期刊、论文标题、研究问题、核心贡献、方法和数据、为什么适合该期刊、原创性声明、利益冲突和通讯作者信息占位符。不要夸大贡献。
```
