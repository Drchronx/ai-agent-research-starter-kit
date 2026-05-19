# 理论-变量-方法矩阵模板

用途：把 Zotero/Obsidian 中的论文卡片变成可用于综述、选题、假设和方法设计的结构化矩阵。

## 最小字段

| 字段 | 说明 |
|---|---|
| paper_id | 文献编号 |
| zotero_key | Zotero 条目 key |
| citation_key | Better BibTeX citekey |
| citation | 简短引用 |
| field | 管理学 / 心理学 / 神经科学 / BCI / HCI / 文本挖掘 |
| research_question | 研究问题 |
| theory | 理论 |
| mechanism | 理论解释机制 |
| construct | 理论构念 |
| variable_role | iv / dv / mediator / moderator / control / eeg_feature / text_variable |
| variable_name | 变量名 |
| definition | 定义 |
| measurement | 测量方式、量表、特征构造 |
| method_design | 实验、问卷、EEG、文本挖掘、因果推断等 |
| sample_data | 样本、数据来源、时间范围 |
| analysis_model | PROCESS / SEM / regression / ML / DL / ERP / DML 等 |
| key_result | 核心结果 |
| effect_direction | 正向 / 负向 / 不显著 / 混合 |
| limitations | 局限 |
| reuse_for_my_project | 可复用方式 |
| verification_status | unverified / partial / verified |
| note_link | Obsidian note link |

## 变量角色标签

```text
iv
dv
mediator
moderator
control
manipulation_check
realism_check
confound_check
eeg_feature
erp_component
behavioral_measure
text_variable
outcome
mechanism
boundary_condition
```

## 使用规则

- 一篇论文可以有多行。
- 一个机制或一个实验对应一组行。
- 理论不能只写名称，必须写机制。
- 变量要区分理论构念和实际测量。
- 每一行都必须能回到 Zotero 条目或 Obsidian note。
- 不确定的信息写 `needs_check`，不要猜。
