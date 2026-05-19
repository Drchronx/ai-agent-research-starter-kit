# 第09讲 Agent 提示词库

## 1. 文本数据盘点

```text
请读取 data/raw/ 下的文本数据，生成 textmining/text_data_inventory.xlsx 的内容草稿。

请检查文件名、文件类型、编码、行数、文档 ID、文本列、时间列、来源列、分组列、重复文本、空文本、过短文本、异常长文本、个人信息、敏感信息、版权或平台协议风险。不要修改原始数据。
```

## 2. 清洗计划

```text
请基于 text_data_inventory.xlsx 生成 textmining/text_cleaning_plan.md。

写清去噪、分句、分词、停用词、自定义词典、去重、异常文本、脱敏、输出路径和日志记录规则。强调不得覆盖原始数据。
```

## 3. 文本变量定义

```text
请基于我的研究问题，生成 textmining/text_variable_definition.md。

每个变量包含变量名、理论构念、构念定义、文本证据、正例、反例、边界例、推荐技术路线、最终分析单位和不能支持的解释。
```

## 4. 技术路线选择

```text
请生成 textmining/route_selection.md。

对每个目标变量判断是否适合词典法、TF-IDF、情感分析、主题模型、监督分类、LLM 标注、embedding 相似度或深度学习。说明理由、输入、输出、风险和人工核验方式。
```

## 5. Codebook

```text
请基于 text_variable_definition.md 生成 textmining/annotation_codebook.md。

每个标签必须包含定义、标注单位、正例、反例、边界例、冲突规则、不确定规则和禁止文本外推断规则。
```

## 6. 抽样计划

```text
请生成 textmining/annotation_sampling_plan.md。

说明抽样数量、随机种子、分层变量、样本覆盖、过短文本处理和人工标注分工。
```

## 7. LLM 标注提示词

```text
请基于 annotation_codebook.md 生成 textmining/llm_labeling_prompt.md。

要求 LLM 只输出 JSON，不解释标签外内容。遇到证据不足输出 uncertain。禁止根据文本外常识推断。每条结果包含 doc_id、label、confidence、evidence_span、reason、needs_human_review。
```

## 8. 可靠性报告

```text
请读取 annotation_sample.xlsx，生成 textmining/reliability_report.md。

报告人工-人工一致率、Kappa 或 Alpha、LLM-人工一致率、每类标签错误、边界例、系统性偏差、codebook 修改建议和是否可批量标注。
```

## 9. 特征字典

```text
请生成 textmining/feature_dictionary.xlsx 的内容草稿。

每个特征包含 feature_name、construct、method、input_file、parameters、unit、range、interpretation、limitations、aggregation_rule、audit_status。
```

## 10. 最终变量构造报告

```text
请生成 textmining/variable_construction_report.md。

包括文本来源、清洗流程、构念定义、技术路线、标注/模型流程、可靠性结果、最终变量、合并方式、有效性证据、稳健性方案和解释边界。
```

## 11. 审稿人式审计

```text
请以严格审稿人视角审计本工作区，生成 qc/text_variable_audit.md。

检查文本来源、隐私、版权、清洗可复现性、构念定义、codebook、LLM 越界推断、标注一致性、训练测试泄漏、变量有效性和论文解释边界。输出 pass/revise/fail。
```
