# 案例 14：Zotero 与 Obsidian 长期知识库

这个案例用于把散乱文献变成长期可复用的科研知识库。

## 目标

完成后你应该能：

- 用 Zotero 保存真实文献、PDF、DOI、BibTeX 和集合标签。
- 用 Obsidian 保存论文卡片、理论卡片、变量卡片、方法卡片和项目卡片。
- 建立理论-变量-方法矩阵。
- 建立研究问题知识图谱。
- 从每篇论文中沉淀可复用启发，而不是只做一次性摘要。

## 前置条件

- 已经有 Zotero 文献库，或者至少有一批论文 PDF/DOI/题录。
- 如果要调用 Zotero API，需要本机安全保存：
  - `ZOTERO_LIBRARY_ID`
  - `ZOTERO_LIBRARY_TYPE`
  - `ZOTERO_API_KEY`
- 不要把 Zotero API key 写进论文、手册或聊天记录。

## 练习 1：审计 Zotero 文献库

提示词：

```text
请使用 zotero-library-sync 审计我的 Zotero 文献库。
不要显示 API key。
输出缺失 DOI、缺失 PDF、重复文献、未分类文献、未打标签文献和推荐集合结构。
先不要写回 Zotero，只生成审计表。
```

## 练习 2：生成 Obsidian 论文卡片

提示词：

```text
请使用 obsidian-paper-card 为 5 篇核心论文生成 Obsidian 论文卡片。
每张卡片包含 YAML、Citation、One-Sentence Takeaway、Research Question、Theory And Mechanism、Variables、Method、Data、Key Results、Limitations、Reusable Ideas 和 Related Notes。
请区分论文原文内容、我的解释和待核验内容。
```

## 练习 3：建立理论-变量-方法矩阵

提示词：

```text
请使用 theory-variable-method-matrix 围绕我的课题建立理论-变量-方法矩阵。
列出 paper_id、zotero_key、theory、mechanism、construct、variable_role、measurement、method_design、sample_data、analysis_model、key_result、reuse_for_my_project 和 verification_status。
不要把理论当标签，必须写清机制。
```

## 练习 4：建立研究问题知识图谱

提示词：

```text
请使用 research-question-knowledge-graph 为我的研究问题建立知识图谱。
节点包括 paper、theory、mechanism、construct、variable、method、measure、research_question、hypothesis、finding、project。
关系必须有类型，例如 supports、uses_theory、tests_mechanism、measures、uses_method、informs_hypothesis。
输出节点表、关系表、Mermaid 图和需要进一步检索核验的 gap。
```

## 练习 5：沉淀论文可复用启发

提示词：

```text
请使用 paper-reusable-insight-bank 从这些论文中提取可复用启发。
每篇论文最多提取 3-7 条，类型包括 theory_mechanism、measurement_source、scenario_design、eeg_erp_pipeline、bci_modeling_pattern、text_mining_variable、causal_identification、figure_design、reviewer_risk 和 future_study。
请区分论文实际结论、我的可能迁移想法和风险。
```

## 输出要求

把结果写入：

```text
output/knowledge_base
```

建议文件：

```text
zotero_audit.csv
obsidian_paper_cards/
theory_variable_method_matrix.csv
research_question_graph.md
reusable_insight_bank.csv
```

不要覆盖 Zotero 原始元数据，不要把未核验文献写成已核验。
