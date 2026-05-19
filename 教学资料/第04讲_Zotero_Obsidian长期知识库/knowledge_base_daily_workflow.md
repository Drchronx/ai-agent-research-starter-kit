# 每日知识库维护流程

用途：让学生每天用 20-40 分钟维护 Zotero / Obsidian 长期知识库，防止资料再次变乱。

## 每日流程

### 1. 收文献

- 从 AI4Scholar、AMiner、OpenAlex、PubMed、CNKI 或期刊网页收集新文献。
- 先进入 Zotero `00_inbox`。
- 不确定是否重要的文献不要立刻删除，先标 `status:to_read`。

### 2. 补元数据

检查：

- [ ] 题名。
- [ ] 作者。
- [ ] 年份。
- [ ] 期刊/会议。
- [ ] DOI/PMID/arXiv。
- [ ] URL。
- [ ] PDF 附件。

### 3. 打标签

至少打 3 类标签：

```text
field:...
method:...
status:...
```

重要论文再加：

```text
role:classic
role:must_read
role:method_source
role:measure_source
role:theory_source
```

### 4. 生成 Obsidian 卡片

每篇核心论文生成一张笔记：

```text
obsidian_vault/01_Papers/@FirstAuthorYear_ShortTitle.md
```

卡片必须写：

- 一句话贡献。
- 研究问题。
- 理论机制。
- 变量。
- 方法。
- 主要结果。
- 局限。
- 对我研究的启发。
- 人工核验项。

### 5. 更新矩阵

把论文卡片中的理论、变量、方法、样本、结果写入：

```text
matrices/theory_variable_method_matrix.xlsx
```

### 6. 更新知识图谱

新论文如果引入新理论、新变量或新方法，更新：

```text
graphs/research_question_graph.md
```

### 7. 沉淀可复用启发

把真正可复用的内容写入：

```text
reusable_insights/paper_reusable_insight_bank.md
```

启发必须具体：

- 可复用理论机制。
- 可复用变量测量。
- 可复用实验设计。
- 可复用 EEG/ERP/BCI 分析方式。
- 可复用文本挖掘变量。
- 可复用审稿回应或局限写法。

### 8. 记录日志

更新：

```text
research_log.md
```

记录今天新增、已读、已核验、待处理。

## 每周维护

- 清理 Zotero `00_inbox`。
- 去重。
- 修正缺 DOI 文献。
- 检查 PDF 附件缺失。
- 合并重复标签。
- 更新文献阅读矩阵。
- 输出每周文献摘要。

## 禁止事项

- 不把 Obsidian 当 Zotero 替代品。
- 不把 Zotero 当读书笔记库。
- 不在 Obsidian 卡片中混淆论文原意和自己的推断。
- 不让 Agent 批量修改 Zotero 元数据，除非先 dry run 并人工确认。
- 不把 API Key 写入 vault。
