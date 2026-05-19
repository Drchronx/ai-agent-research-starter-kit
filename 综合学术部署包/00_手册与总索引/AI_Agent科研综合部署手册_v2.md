# AI Agent 科研综合部署手册 v2

适用路径：`<本项目路径>\综合学术部署包`  
版本日期：2026-05-12  
定位：把课程资料中的 Claude Code、OpenClaw、Skills、Subagent、MCP、Python 实证分析、文本挖掘、文献综述与论文写作方法，整理为一个可复制部署的个人科研 Agent 系统。

---

## 1. 这不是资料归档，而是科研操作系统部署包

这个包的目标不是“把课程文件换个地方放”，而是把你后续科研中会反复用到的能力整理成可部署模块。核心思想有三条：

1. **科研任务工程化**：每个任务都有输入、步骤、输出、日志和可复现命令。
2. **重复能力 Skill 化**：文献检索、数据清洗、文本变量构造、论文写作、审稿检查都应该变成可反复调用的技能。
3. **AI Agent 工具化**：Agent 不只是回答问题，还要能读文件、跑脚本、连数据库、调用浏览器、生成表格和维护知识库。

你后续应该把这个包当成三种东西使用：

- 安装包：把 Skills 复制到 Codex / Claude Code / OpenClaw。
- 教学手册：查每类功能怎么用、怎么部署、怎么触发。
- 科研 SOP 模板：把你的博士论文、SSCI、C 刊、实验项目都放到统一流程里。

---

## 2. 部署包目录说明

| 目录 | 包含能力 | 什么时候用 |
|---|---|---|
| `01_核心文档处理Skills` | PDF、DOCX、PPTX、XLSX、Markdown 转换 | 任何项目第一批部署 |
| `02_文献检索综述引用Skills` | 文献检索、系统综述、SSCI 阅读、引用核验 | 选题、综述、投稿前补文献 |
| `03_CNKI选题与中文文献Skills` | CNKI 检索、热榜、趋势、CSSCI 期刊匹配 | C 刊、中文课题、国内热点分析 |
| `04_数据采集整合与实证Skills` | 数据采集、表格提取、实证分析、机器学习 | 量化研究、管理学实证、因果推断 |
| `05_文本挖掘与NLP Skills` | 中文分词、TF-IDF、主题模型、情感分析、LLM 标注 | 年报、政策、评论、访谈、开放文本 |
| `06_论文写作审稿投稿Skills` | 科学写作、论文策略、同行评审、投稿模板 | 开题、写作、返修、投稿 |
| `07_自动化MCP浏览器与Agent Skills` | Skill 开发、MCP、浏览器自动化、Web 检索 | 自动化采集、工具接入、网页任务 |
| `08_图表PPT海报与可视化Skills` | 科学图、PPT、poster、paper-to-web | 汇报、答辩、会议、论文图 |
| `09_建议自定义Skills模板` | EEG/ERP、SSCI 写作、文本变量、因果稳健性模板 | 个人研究方向定制 |
| `scripts` | 安装、检查、依赖脚本 | 部署和维护 |

---

## 3. 一键部署方法

### 3.1 安装到 Codex

Codex 技能目录一般是：

```powershell
C:\Users\<用户名>\.codex\skills
```

运行：

```powershell
cd "<本项目路径>\综合学术部署包"
powershell -ExecutionPolicy Bypass -File .\scripts\install_skills.ps1 -Target codex
```

只预览不复制：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_skills.ps1 -Target codex -DryRun
```

覆盖已有同名 Skill：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_skills.ps1 -Target codex -ForceCopy
```

### 3.2 安装到 Claude Code

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_skills.ps1 -Target claude
```

目标目录：

```powershell
C:\Users\<用户名>\.claude\skills
```

### 3.3 安装到 OpenClaw

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_skills.ps1 -Target openclaw
```

目标目录：

```powershell
C:\Users\<用户名>\.openclaw\skills
```

### 3.4 检查包完整性

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\check_package.ps1
```

这个脚本会检查每个 Skill 文件夹是否包含 `SKILL.md`。

### 3.5 查看依赖

先只列出所有 `requirements.txt`：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\list_or_install_requirements.ps1
```

确认后再安装：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\list_or_install_requirements.ps1 -Install
```

建议不要一上来全量安装依赖。更稳妥的方式是：你要用哪个功能，就进入对应 Skill 文件夹安装它自己的依赖。

---

## 4. 学习路线：从能用到好用

### 第 1 天：文档处理与引用核验

部署：

- `markitdown`
- `pdf`
- `docx`
- `xlsx`
- `citation-management`

练习任务：

```text
请读取 literature/pdfs 里的 5 篇论文，分别生成结构化摘要，并核验参考文献信息。
```

验收标准：

- 能把 PDF 转成 Markdown。
- 能提取标题、作者、期刊、年份、DOI。
- 能生成或修正 BibTeX。
- 能指出无法核验的引用。

### 第 2-3 天：文献综述系统

部署：

- `academic-research-hub`
- `academic-research-openalex`
- `literature-review`
- `research-superpower`
- `ssci-literature-review`

练习任务：

```text
请围绕“AI agent 使用对科研创造力的影响”做文献检索，输出检索式、核心文献、研究方法分布、理论机制和潜在 GAP。
```

验收标准：

- 有检索式。
- 有筛选标准。
- 有文献矩阵。
- 有真实引用。
- 综述不是逐篇罗列，而是分类比较。

### 第 4-5 天：数据与实证分析

部署：

- `empirical-analysis-skill-python`
- `research-data-auto-analysis-plotting`
- `multi-source-data-integration-extraction`
- `data-viz-analyzer`

练习任务：

```text
请对 data/raw/sample.xlsx 进行数据质量检查、清洗、描述统计、相关矩阵和基准回归，并把所有输出写入 output/empirical。
```

验收标准：

- 原始数据没有被覆盖。
- 输出 Table 1。
- 输出相关矩阵和图。
- 输出模型结果。
- 有清洗日志和 artifact manifest。

### 第 6-7 天：文本挖掘

部署：

- `text-analysis-basic`
- `topic-modeling`
- `sentiment-analysis`
- `big-data-labeling-variable-construction`

练习任务：

```text
请对 comments.xlsx 的 text 列做分词、词频、TF-IDF、主题模型和情感分析，输出文本变量数据集。
```

验收标准：

- 有清洗前后样例。
- 有分词和停用词说明。
- 有主题词和文档主题概率。
- 有情感得分或情感标签。
- 有人工抽样核验建议。

### 第 2 周：论文写作与审稿

部署：

- `scientific-writing`
- `empirical-paper-writer`
- `peer-review`
- `scholar-evaluation`
- `scientific-critical-thinking`
- `venue-templates`

练习任务：

```text
请基于 literature/matrix.xlsx 和 output/empirical 的结果，写 Introduction、Results 和 Discussion，并以 SSCI 审稿人视角指出主要缺陷。
```

验收标准：

- Introduction 有问题意识。
- 理论机制不是贴标签。
- Results 不夸大结果。
- Discussion 有机制解释、文献对话和局限。
- 审稿报告能指出拒稿级问题。

---

## 5. 功能模块详解一：核心文档处理

### 5.1 解决什么问题

科研资料最常见的问题是：PDF、Word、PPT、Excel、图片和网页内容散落在不同格式里。核心文档 Skills 的作用是把这些资料转换成 Agent 能处理的结构化文本、表格和报告。

### 5.2 包含 Skills

| Skill | 用途 |
|---|---|
| `markitdown` | PDF、DOCX、PPTX、XLSX、HTML 等转 Markdown |
| `pdf` | PDF 提取、拆分、合并、表单处理 |
| `docx` | Word 创建、编辑、提取、格式保留 |
| `xlsx` | Excel/CSV 读写、公式、表格、分析 |
| `pptx` | PPT 创建和编辑 |
| `document-skills` | 文档处理综合工具包 |

### 5.3 典型任务

```text
把这个文件夹里的 PDF 论文全部转成 Markdown，并保留原文件名和来源路径。
```

```text
读取这个 Word 草稿，提取章节结构、表格和参考文献，输出修改建议。
```

```text
把 Excel 数据整理成描述统计表，并导出 Word 表格。
```

### 5.4 输出规范

```text
output/document/
  converted_md/
  extracted_tables/
  document_summary.md
  conversion_log.csv
```

---

## 6. 功能模块详解二：文献检索、综述与引用

### 6.1 解决什么问题

文献工作不是“找几篇论文”，而是一个完整流程：

```text
确定问题 -> 设计检索式 -> 多库检索 -> 去重 -> 筛选 -> 全文阅读 -> 文献矩阵 -> 综述写作 -> 引用核验
```

### 6.2 包含 Skills

| Skill | 最适合的场景 |
|---|---|
| `academic-research-openalex` | 免费 OpenAlex 检索、DOI、引用信息 |
| `academic-research-hub` | 多数据库学术检索 |
| `literature-review` | 系统综述、scoping review、主题综合 |
| `literature-reviewer-skill` | 文献综述自动化工作流 |
| `citation-management` | DOI、PMID、BibTeX、引用核验 |
| `research-superpower` | 大规模文献搜索、筛选、引用网络 |
| `pdf-paper-summary` | PDF 论文结构化总结 |
| `paper-innovation-extractor` | 批量提取论文创新点 |
| `ssci-literature-review` | SSCI 论文拆解和批判性阅读 |
| `arxiv-watcher` | arXiv 新论文追踪 |
| `research-lookup` | 当前研究信息检索与核验 |

### 6.3 教学流程：如何做一篇合格综述

第一步，定义研究问题：

```text
我不是要综述“AI agent”，而是要综述“AI agent 如何影响科研人员的问题发现、知识整合和创造性产出”。
```

第二步，拆关键词：

```text
AI agent / autonomous agent / LLM agent / research assistant
research productivity / scientific creativity / knowledge work
human-AI collaboration / augmented intelligence
```

第三步，设计检索式：

```text
("AI agent" OR "LLM agent" OR "autonomous agent")
AND ("research productivity" OR "scientific creativity" OR "knowledge work")
AND ("human-AI collaboration" OR "augmented intelligence")
```

第四步，筛选标准：

- 纳入：同行评审论文、近五年文献、与科研任务或知识工作相关。
- 排除：纯技术 benchmark、无人的组织行为研究、非学术来源。

第五步，建立文献矩阵：

| 字段 | 说明 |
|---|---|
| `research_question` | 论文问了什么问题 |
| `theory` | 使用什么理论 |
| `mechanism` | 解释机制是什么 |
| `method` | 实验、问卷、二手数据、文本挖掘还是模型 |
| `sample` | 样本和情境 |
| `findings` | 主要发现 |
| `limitation` | 局限 |
| `gap_for_my_study` | 对你的选题有什么启发 |

第六步，写综述段落：

不要写：

```text
A 研究了……B 研究了……C 发现了……
```

要写：

```text
现有研究主要从三条路径解释 AI 工具对知识工作的影响：效率增强、认知外包与协同创造。效率增强路径强调任务执行速度，但较少解释复杂问题发现；认知外包路径关注认知负荷下降，但忽视过度依赖导致的探索收缩；协同创造路径开始讨论人机互补，但尚未清楚区分“生成更多想法”和“生成更有理论价值的问题”。
```

### 6.4 高质量综述的检查清单

- 是否有清楚的综述问题？
- 是否说明检索范围和检索式？
- 是否覆盖经典文献和近五年文献？
- 是否比较不同理论路径？
- 是否指出方法差异导致的结论差异？
- 是否有真正的研究缺口，而不是“研究较少”？
- 是否把缺口自然导向你的研究问题？
- 引用是否全部可核验？

---

## 7. 功能模块详解三：CNKI 选题与中文文献

### 7.1 包含 Skills

| Skill | 用途 |
|---|---|
| `cnki-exp-search-automation` | CNKI 高级搜索自动化 |
| `cnki-crawler-literature` | 中文文献元数据采集 |
| `cnki-crawler-topic` | 选题助手中的 CNKI 爬取 |
| `cnki-rank` | 下载热榜、热词榜 |
| `cnki-trend` | 关键词年度趋势、学科、期刊、机构分布 |
| `cnki-research-assistant` | 热榜、趋势、文献、期刊、研究空白综合分析 |

### 7.2 什么时候用 CNKI 模块

- 准备 C 刊论文。
- 需要判断中文领域是否已有大量研究。
- 需要找 CSSCI 期刊匹配。
- 需要观察国内研究热词和趋势。
- 需要将 SSCI 选题本土化。

### 7.3 教学流程：从关键词到中文选题报告

第一步，给出关键词：

```text
数字化转型 员工创造力
AI工具 科研效率
生成式人工智能 知识工作
```

第二步，跑趋势：

```text
python scripts/analyzer.py "生成式人工智能 知识工作" --check-trend
```

第三步，跑期刊匹配：

```text
python scripts/analyzer.py "生成式人工智能 知识工作" --match-journals --top 10
```

第四步，跑完整报告：

```text
python scripts/auto_analyzer.py "生成式人工智能 知识工作"
```

第五步，人工判断：

- 热度高不等于好选题。
- 热度低不等于没价值。
- 真正关键是：你能否提出清楚机制、合适数据和可检验设计。

### 7.4 注意事项

- CNKI 类工具可能受登录、验证码、网络、代理和平台策略影响。
- 不建议高频、大规模、无节制抓取。
- 输出结果必须人工核验，尤其是题名、作者、期刊和下载/引用量。

---

## 8. 功能模块详解四：数据采集、整合与实证分析

### 8.1 包含 Skills

| Skill | 用途 |
|---|---|
| `empirical-analysis-skill-python` | 清洗、变量构造、描述统计、回归、面板、DID、IV、DML、稳健性 |
| `multi-source-data-integration-extraction` | 合并 Excel/CSV，提取 PDF/HTML/TXT 表格，OCR |
| `research-data-auto-analysis-plotting` | 自动描述统计、缺失、相关图、分组图、回归诊断 |
| `data-visualization-analysis` | 数据探索和图表 |
| `data-viz-analyzer` | 交互式数据可视化报告 |
| `decision-tree-modeling` | 决策树分类、调参、可视化 |
| `tushare-finance` | A 股、财务、宏观、金融数据 |

### 8.2 标准实证项目目录

```text
project/
  data/
    raw/
    processed/
  scripts/
  output/
    empirical/
      tables/
      figures/
      logs/
  manuscript/
```

### 8.3 数据清洗教学流程

第一步：原始数据不可覆盖。

```text
data/raw/original.xlsx
```

第二步：生成数据质量报告。

检查：

- 行列数量。
- 变量类型。
- 缺失率。
- 重复值。
- 异常值。
- 极端值。
- 分类变量水平。

第三步：变量构造。

常见操作：

- log。
- winsorize。
- z-score。
- dummy。
- lag/lead。
- 交互项。
- 文本变量合并。

第四步：描述统计。

输出：

- Table 1。
- 相关矩阵。
- 缺失值表。
- 分组比较。

第五步：模型诊断。

检查：

- VIF。
- 异方差。
- 自相关。
- 残差分布。
- 固定效应设置。
- 聚类标准误。

第六步：主模型与稳健性。

输出：

```text
table2_main
table3_mechanism
table4_heterogeneity
table5_robustness
fig3_coefplot
artifact_manifest
```

### 8.4 模型选择教学

| 研究问题 | 常用模型 | 注意事项 |
|---|---|---|
| X 是否影响 Y | OLS / Logit | 不要直接声称因果 |
| 企业面板数据 | 固定效应 / 随机效应 | 解释固定效应吸收了什么 |
| 政策冲击 | DID / event study | 必须检查平行趋势 |
| 内生性 | IV / 2SLS | 工具变量相关性与外生性要解释 |
| 高维控制下因果效应 | DML | 明确处理变量和识别假设 |
| 异质性因果效应 | CATE / causal forest | 不要把探索性异质性过度理论化 |
| 预测任务 | Lasso / RF / GBDT / XGBoost | 分清预测准确率与理论解释 |

### 8.5 触发词模板

```text
请使用 empirical-analysis-skill-python 对 data/processed/main.csv 做完整分析：
1. 检查数据质量；
2. 构造变量；
3. 输出 Table 1 和相关矩阵；
4. 跑基准回归；
5. 做稳健性、机制和异质性；
6. 所有输出写入 output/empirical；
7. 最后生成结果解释报告。
```

---

## 9. 功能模块详解五：文本挖掘与 NLP

### 9.1 包含 Skills

| Skill | 用途 |
|---|---|
| `text-analysis-basic` | PDF 抽取、分词、词频、词云、TF-IDF、Word2Vec、Embedding、相似度 |
| `topic-modeling` | LDA、DTM、BERTopic |
| `sentiment-analysis` | 词典法、机器学习、LLM 情感分析 |
| `deep-learning-nlp` | DNN、CNN、RNN/GRU 课程案例 |
| `big-data-labeling-variable-construction` | LDA、sklearn、transformer、LLM 标注路由 |

### 9.2 文本挖掘完整流程

```text
文本采集
  -> OCR / PDF 提取
  -> 清洗
  -> 分词
  -> 停用词
  -> 词典扩展
  -> 向量化
  -> 变量构造
  -> 人工核验
  -> 实证建模
```

### 9.3 年报文本变量构造教学

变量一：AI 关注度。

```text
AI 词典词频 / 年报总词数
```

变量二：前瞻性信息。

```text
前瞻性词汇所在句子数量 / 总句子数量
```

变量三：文本特质性。

```text
企业文本向量与行业平均文本向量的距离
```

变量四：情绪倾向。

```text
正向词得分 - 负向词得分
```

变量五：语义相似度。

```text
企业战略文本与政策文本的 sentence embedding cosine similarity
```

### 9.4 主题模型教学

不要直接给 LDA 设一个 K 就跑最终模型。正确流程：

1. 清洗文本。
2. 运行多个 K 的困惑度和一致性。
3. 查看候选主题词。
4. 人工判断主题是否可解释。
5. 再训练最终模型。
6. 输出文档-主题概率。
7. 将主题概率作为实证变量或描述趋势。

触发词：

```text
请对 data/text/policy.csv 的 content 列做 LDA 主题模型。先运行 K=3 到 K=12 的一致性诊断，输出候选主题词和图，不要直接训练最终模型，等我确认 K。
```

### 9.5 情感分析教学

三种路线：

| 方法 | 优点 | 缺点 |
|---|---|---|
| 词典法 | 可解释、适合论文说明 | 对语境和反讽弱 |
| 机器学习 | 有标签时稳定 | 需要标注数据 |
| LLM 标注 | 语义理解强 | 成本高、需一致性核验 |

论文中推荐至少做：

- 人工抽样核验。
- 多方法稳健性。
- 标签一致性报告。

---

## 10. 功能模块详解六：论文写作、审稿与投稿

### 10.1 包含 Skills

| Skill | 用途 |
|---|---|
| `scientific-writing` | IMRAD、Abstract、Introduction、Methods、Results、Discussion |
| `empirical-paper-writer` | 实证论文结构和正文 |
| `paper-writing-assistant-typesetting` | 文献元数据、outline、LaTeX、Word、PDF 草稿 |
| `peer-review` | 同行评审式审查 |
| `scientific-critical-thinking` | 方法、统计、因果、证据强度批判 |
| `scholar-evaluation` | 学术质量系统评分 |
| `hypothesis-generation` | 机制、假设、预测、实验设计 |
| `research-proposal` | 博士/课题研究计划 |
| `venue-templates` | 投稿模板、会议/期刊格式 |
| `doc-coauthoring` | 长文档协同写作 |
| `academic-paper-composer` | 论文大纲到正文 |
| `academic-paper-strategist` | 论文策略、缺口、结构规划 |

### 10.2 Introduction 教学模板

一篇好的 Introduction 通常有 6 个动作：

1. **问题重要性**：为什么这个问题值得研究。
2. **已有研究进展**：别人已经解释了什么。
3. **核心不足**：还有什么没有解释清楚。
4. **理论机制**：你为什么认为变量之间存在这种关系。
5. **研究设计**：你如何检验这个机制。
6. **贡献声明**：理论、方法、数据或情境贡献。

错误写法：

```text
随着人工智能的发展，AI agent 越来越重要，因此研究它具有重要意义。
```

更好的写法：

```text
AI agent 正在从被动工具转向主动协作者，这改变了科研人员获取、筛选和重组知识的方式。然而，现有研究主要把 AI 工具视为效率提升装置，较少解释它如何影响研究者的问题发现和理论连接过程。因此，仅用“生产率”框架可能低估了 AI agent 对科研创造力的机制性影响。
```

### 10.3 Methods 教学模板

Methods 不能只写“我们做了回归”。应包括：

- 数据来源。
- 样本筛选。
- 变量测量。
- 模型设定。
- 标准误。
- 固定效应。
- 稳健性检验。
- 软件版本。

### 10.4 Results 教学模板

Results 的原则：

- 先描述，再模型。
- 先主效应，再机制、调节、异质性。
- 不要在 Results 里过度理论化。
- 所有数字来自表格。
- 显著性不等于重要性，要报告效应大小。

### 10.5 Discussion 教学模板

Discussion 必须回答：

- 结果说明了什么？
- 为什么会出现这个结果？
- 与已有研究一致还是冲突？
- 冲突的原因可能是什么？
- 理论贡献是什么？
- 方法局限是什么？
- 下一步研究怎么做？

### 10.6 审稿前自查

用 `peer-review` 检查：

- 理论机制是否空泛。
- 假设是否从理论推导出来。
- 变量和理论是否对应。
- 方法是否能回答研究问题。
- 稳健性是否足够。
- 是否过度声称因果。
- 引用是否真实。
- 贡献是否夸大。

触发词：

```text
请以 SSCI 管理学审稿人视角审查 manuscript/draft.docx，优先指出可能导致拒稿的理论、方法、结果解释和引用问题，并给出可执行修改方案。
```

---

## 11. 功能模块详解七：自动化、MCP、浏览器与 Agent 系统

### 11.1 包含 Skills

| Skill | 用途 |
|---|---|
| `skill-creator` | 创建和迭代新 Skill |
| `find-skills` | 查找和安装 Skill |
| `mcp-builder` | 构建 MCP 工具服务器 |
| `agent-browser` | 浏览器自动化 |
| `web-browsing` | 网页浏览和总结 |
| `webapp-testing` | Playwright 本地网页测试 |
| `self-improving-agent` | 记录错误、纠正和经验 |
| `parallel-web` | Web 搜索和深度研究 |
| `tavily-search` | Tavily 搜索 |
| `claude-api` | Claude API / Agent SDK |

### 11.2 MCP 适合接什么

对你最有价值的 MCP：

- Zotero MCP：读文献库、导出 BibTeX。
- OpenAlex/Semantic Scholar MCP：查文献、引文网络。
- 本地文件索引 MCP：查论文、笔记、数据。
- EEG 数据处理 MCP：调用 MNE 预处理脚本。
- 飞书 MCP：日程、任务、知识库、文档协作。

### 11.3 浏览器自动化教学

基本流程：

```powershell
agent-browser open https://example.com
agent-browser snapshot -i
agent-browser click @e1
agent-browser fill @e2 "关键词"
agent-browser wait --load networkidle
agent-browser screenshot page.png
```

使用原则：

- 先 snapshot，再操作。
- 页面变化后重新 snapshot。
- 登录态文件不要提交到 Git。
- 涉及机构账号和数据库时遵守协议。

### 11.4 Skill 创建教学

当一个任务满足以下条件，就应该创建 Skill：

- 你会重复做。
- 步骤相对稳定。
- 输入输出格式清楚。
- 可以用脚本提高可靠性。
- 对学术严谨性有固定要求。

Skill 最小模板：

```text
skill-name/
  SKILL.md
```

推荐模板：

```text
skill-name/
  SKILL.md
  scripts/
  references/
  assets/
```

`SKILL.md` 应写：

- 何时触发。
- 能做什么。
- 不能做什么。
- 输入要求。
- 输出格式。
- 执行步骤。
- 需要读哪些 reference。
- 需要运行哪些 script。

---

## 12. 功能模块详解八：图表、PPT、Poster 与 Paper-to-Web

### 12.1 包含 Skills

| Skill | 用途 |
|---|---|
| `scientific-schematics` | 科学示意图、流程图、机制图 |
| `scientific-slides` | 学术汇报 PPT |
| `paper-slide-deck` | 从论文生成 slide deck |
| `latex-posters` | LaTeX 学术海报 |
| `pptx-posters` | PPTX 海报 |
| `paper-2-web` | 论文转网页、视频、poster |
| `generate-image` | 通用图像生成 |
| `infographics` | 信息图 |

### 12.2 对你最有用的图

- AI Agent 科研工作流图。
- 文献筛选 PRISMA 流程图。
- 理论机制模型图。
- EEG/ERP 实验流程图。
- 文本挖掘变量构造流程图。
- DML 因果识别流程图。
- 论文研究设计总览图。

### 12.3 触发词模板

```text
请根据我的研究模型生成一张适合 SSCI 论文的理论机制图，包含 AI agent 使用、认知负荷、探索行为、知识整合和科研创造力。
```

```text
请把 manuscript/draft.docx 生成 15 页答辩 PPT，结构包括研究背景、理论框架、方法、结果、贡献和局限。
```

---

## 13. 面向你研究方向的自定义 Skills 路线

### 13.1 为什么必须自定义

现有课程对文献、写作、文本挖掘、实证分析支持较强，但对 EEG/ERP、认知神经科学实验、人机交互实验流程的支持还不够。因此你应该把自己的方法偏好沉淀成专用 Skills。

### 13.2 第一优先级：EEG/ERP

建议 Skill：

```text
eeg-preprocessing
erp-analysis
time-frequency-analysis
eeg-ml-pipeline
neuro-method-writer
```

输出必须包括：

- 预处理报告。
- 坏道列表。
- ICA 成分图。
- Epoch 剔除日志。
- ERP 波形图。
- 地形图。
- 成分时间窗统计。
- Methods 英文段落。

### 13.3 第二优先级：管理学 SSCI 写作

建议 Skill：

```text
ssci-introduction-writer
theory-mechanism-checker
hypothesis-logic-builder
discussion-contribution-writer
```

强制规则：

- 理论必须解释机制。
- 变量必须对应理论构念。
- 不接受“研究较少”作为唯一缺口。
- 不允许贡献夸大。

### 13.4 第三优先级：文本变量构造

建议 Skill：

```text
annual-report-text-variable
policy-text-alignment
llm-labeling-audit
dictionary-expansion
```

输出必须包括：

- 词典。
- 清洗规则。
- 样本核验。
- 变量计算公式。
- 稳健性替代口径。

---

## 14. 项目级 AGENTS.md 模板

建议每个论文项目根目录放一个：

```markdown
# 项目协作规则

## 研究主题
本项目研究 [主题]。

## 学科定位
管理学、心理学、神经科学与计算机科学交叉。

## 方法偏好
优先使用实验设计、EEG/ERP、文本挖掘、机器学习、因果推断。

## 文献规则
必须引用真实文献。不能编造 DOI、作者、期刊或年份。无法核验时必须说明。

## 理论规则
理论必须解释机制，不能贴标签式套用。

## 数据规则
raw 数据不可覆盖。所有清洗结果写入 data/processed 或 output。

## 输出规则
分析必须输出命令、日志、表格、图和解释报告。
```

---

## 15. 常见任务触发词大全

### 文献检索

```text
请围绕 [主题] 做中英文文献检索，输出检索式、核心文献、近五年趋势、经典文献和研究缺口。引用必须可核验。
```

### 文献矩阵

```text
请读取 literature/pdfs 中的论文，建立文献矩阵，字段包括研究问题、理论、变量、样本、方法、主要发现、局限和与我研究的关联。
```

### 选题分析

```text
请用 CNKI 选题分析助手分析 [关键词] 的中文研究热度、年度趋势、CSSCI 期刊匹配和潜在研究缺口。
```

### 实证分析

```text
请对 data/processed/main.csv 做完整实证分析：清洗、描述统计、相关矩阵、基准回归、机制、异质性、稳健性，并输出所有表格和图。
```

### 文本挖掘

```text
请对 [文件] 的 [文本列] 做分词、TF-IDF、主题模型、情感分析，并构造可用于回归的文本变量。
```

### 写作

```text
请基于文献矩阵和研究设计写 SSCI 风格 Introduction，要求问题意识清楚、理论机制明确、避免文献堆砌。
```

### 审稿

```text
请以严苛审稿人视角审查我的论文，优先指出理论错位、方法不匹配、因果表述过度、引用不实和贡献夸大问题。
```

---

## 16. 维护建议

每个月做一次：

1. 检查哪些 Skills 真正用过。
2. 删除或归档不用的 Skills。
3. 把常用提示词升级成项目模板。
4. 把重复任务升级成 Skill。
5. 把失败经验写入 `self-improving-agent` 或项目日志。
6. 更新文献检索式和关键词。

---

## 17. 最小可行科研 Agent 系统

如果只保留最关键的能力，建议是：

```text
markitdown
pdf
docx
xlsx
citation-management
academic-research-openalex
literature-review
empirical-analysis-skill-python
text-analysis-basic
topic-modeling
sentiment-analysis
scientific-writing
peer-review
skill-creator
```

这个组合已经可以覆盖：

- 文献检索。
- PDF 阅读。
- 引用核验。
- 数据清洗。
- 实证分析。
- 文本挖掘。
- 论文写作。
- 审稿检查。
- 自定义扩展。

---

## 18. 最后提醒

AI Agent 能显著提高科研效率，但不能替代三件事：

1. 研究问题判断。
2. 理论机制判断。
3. 方法识别假设判断。

这三件事必须由你负责。Agent 的价值在于把重复性、格式化、可脚本化、可检索、可核验的任务压缩到最低成本，让你把时间用在真正的博士训练上：提出好问题、设计好研究、解释好机制。

