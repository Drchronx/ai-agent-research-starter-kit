# Zotero / Obsidian 长期知识库工作区模板

用途：让学生把 Zotero 文献库、PDF、Obsidian 笔记、论文卡片、理论-变量-方法矩阵和研究问题图谱连接成可长期维护的科研知识库。

## 1. 本地文件夹结构

```text
第04讲_知识库工作区/
├─ AGENTS.md
├─ research_log.md
├─ configs/
│  ├─ zotero.env.example
│  └─ obsidian_paths.example.md
├─ zotero_exports/
│  ├─ zotero_items.csv
│  ├─ zotero_items.json
│  ├─ references.bib
│  ├─ metadata_audit.xlsx
│  └─ obsidian_paper_index.md
├─ obsidian_vault/
│  ├─ 00_Inbox/
│  ├─ 01_Papers/
│  ├─ 02_Theories/
│  ├─ 03_Variables/
│  ├─ 04_Methods/
│  ├─ 05_Projects/
│  ├─ 06_Matrices/
│  ├─ 07_Graphs/
│  ├─ 08_Templates/
│  └─ 99_Archive/
├─ matrices/
│  ├─ theory_variable_method_matrix.xlsx
│  └─ theory_variable_method_matrix.md
├─ graphs/
│  ├─ research_question_graph.md
│  └─ research_question_edges.xlsx
├─ reusable_insights/
│  └─ paper_reusable_insight_bank.md
├─ qc/
│  └─ knowledge_base_audit.md
└─ output/
```

## 2. Zotero 推荐分类

```text
00_inbox
01_to_read
02_reading
03_core_theory
04_methods
05_measures
06_datasets
07_reviews_meta
08_manuscript_citations
09_daily_literature
99_archive
```

## 3. Zotero 推荐标签

```text
field:management
field:psychology
field:neuroscience
field:bci
method:eeg
method:erp
method:scenario_experiment
method:text_mining
method:machine_learning
method:causal_inference
role:classic
role:must_read
role:method_source
role:measure_source
role:theory_source
status:to_read
status:read
status:verified
status:needs_check
```

## 4. 环境变量示例

文件：

```text
configs/zotero.env.example
```

内容：

```text
ZOTERO_LIBRARY_ID=your_user_or_group_id
ZOTERO_LIBRARY_TYPE=user
ZOTERO_API_KEY=your_private_key
OBSIDIAN_VAULT_PATH=D:\AI科研训练营\第04讲_知识库工作区\obsidian_vault
```

注意：真实 API Key 不要提交作业、飞书、Git 或聊天记录。
