# AI Agent 科研零基础全功能手册 v2

> 旧版提示：请优先阅读 `AI_Agent科研零基础全功能手册_v3.md` 或 Word 版。v3 已改为 72 个 Skills 的本地按需复制模式，并新增情景实验模块；不再建议把 Skills 安装到 Codex 根目录。

版本：v2.0  
适用对象：完全不懂 AI Agent，但希望最终掌握完整科研 Agent 功能的人  
核心原则：先按零基础路径上手，再逐步打开全部功能。这个包不是简化版，已经内置完整科研 Skills 库。

---

## 1. 这个零基础包现在包含什么

现在的 `零基础教学包` 同时包含两层内容：

| 层级 | 作用 |
|---|---|
| 零基础教学层 | 教你从 PowerShell、项目路径、第一次对话开始 |
| 完整功能层 | 内置 66 个科研 Skills，覆盖综合部署包所有核心功能 |

核心目录：

```text
零基础教学包/
  00_先读我
  01_认识AI_Agent
  02_环境与部署
  03_第一次运行
  04_五个完整练习案例
  05_提示词模板
  06_常见错误与排错
  07_示例科研项目模板
  08_脚本
  09_手册
  10_完整功能Skills库
```

你现在不需要在“零基础”和“完整功能”之间二选一。正确方法是：

1. 先用零基础案例学会基本操作。
2. 再安装或调用完整功能 Skills。
3. 最后迁移到自己的真实课题。

---

## 2. 一句话理解：你要学的不是 AI，而是科研工作流

AI Agent 的价值不是“替你思考”，而是把科研中的重复性任务工具化。

你最终要学会这条流程：

```text
读项目规则
  -> 调用合适 Skill
  -> 读取论文/数据/文本
  -> 生成结构化输出
  -> 核验引用和结果
  -> 写入指定目录
  -> 人工判断理论和方法是否成立
```

---

## 3. 新手先做哪一步

### 第一步：打开 PowerShell

```powershell
cd "<本项目路径>\零基础教学包"
```

### 第二步：检查环境

```powershell
powershell -ExecutionPolicy Bypass -File .\08_脚本\check_environment.ps1
```

### 第三步：检查完整 Skills 库

```powershell
powershell -ExecutionPolicy Bypass -File .\08_脚本\check_full_skills_library.ps1
```

你应该看到 8 大类 Skills，并显示全部都有 `SKILL.md`。

### 第四步：选择安装方式

如果你是第一次学，先装最小版：

```powershell
powershell -ExecutionPolicy Bypass -File .\08_脚本\install_minimal_skills.ps1 -Target codex
```

如果你明确要所有功能，一次装全：

```powershell
powershell -ExecutionPolicy Bypass -File .\08_脚本\install_all_skills.ps1 -Target codex
```

只预览，不复制：

```powershell
powershell -ExecutionPolicy Bypass -File .\08_脚本\install_all_skills.ps1 -Target codex -DryRun
```

---

## 4. 全部功能地图

`10_完整功能Skills库` 中包含以下完整功能：

| 功能模块 | 包含能力 | 代表 Skills |
|---|---|---|
| 文档处理 | PDF、Word、Excel、PPT、Markdown | `markitdown`、`pdf`、`docx`、`xlsx`、`pptx` |
| 文献检索综述引用 | 检索、筛选、综述、引用核验 | `academic-research-openalex`、`literature-review`、`citation-management`、`research-superpower` |
| CNKI 与中文文献 | 知网检索、热榜、趋势、选题报告 | `cnki-crawler`、`cnki-rank`、`cnki-trend`、`cnki-research-assistant` |
| 数据与实证 | 数据清洗、描述统计、回归、DID、IV、DML、机器学习 | `empirical-analysis-skill-python` |
| 文本挖掘 NLP | 分词、词频、TF-IDF、主题模型、情感分析、LLM 标注 | `text-analysis-basic`、`topic-modeling`、`sentiment-analysis` |
| 写作审稿投稿 | Introduction、Results、Discussion、审稿、投稿模板 | `scientific-writing`、`peer-review`、`venue-templates` |
| 自动化与工具 | Skill 开发、MCP、浏览器自动化、Web 检索 | `skill-creator`、`mcp-builder`、`agent-browser` |
| 可视化展示 | 科学图、PPT、poster、网页 | `scientific-schematics`、`scientific-slides`、`paper-slide-deck` |

---

## 5. 新手学习路线：从最小功能到全功能

### 阶段 1：基础操作

目标：

- 会进入目录。
- 会运行脚本。
- 会让 Agent 先读项目规则。

必须读：

```text
00_先读我
01_认识AI_Agent
02_环境与部署
03_第一次运行
```

### 阶段 2：五个基础案例

目标：

- 跑通科研 Agent 的核心动作。

按顺序做：

1. 读一篇论文。
2. 建立文献矩阵。
3. 分析 Excel/CSV 数据。
4. 文本挖掘入门。
5. 论文写作与审稿。

### 阶段 3：打开完整文献功能

要学：

- 系统综述。
- 引文网络。
- SSCI 论文拆解。
- BibTeX 核验。
- CNKI 选题。

使用目录：

```text
10_完整功能Skills库/02_文献检索综述引用Skills
10_完整功能Skills库/03_CNKI选题与中文文献Skills
```

### 阶段 4：打开完整实证与文本功能

要学：

- 数据清洗。
- 描述统计。
- OLS、面板、DID、IV、DML。
- 机器学习。
- 中文 NLP。
- 主题模型。
- 情感分析。

使用目录：

```text
10_完整功能Skills库/04_数据采集整合与实证Skills
10_完整功能Skills库/05_文本挖掘与NLP Skills
```

### 阶段 5：打开写作、审稿、展示和自动化

要学：

- SSCI 写作。
- 审稿式自查。
- 投稿模板。
- PPT / poster。
- MCP。
- 浏览器自动化。
- 自定义 Skill。

使用目录：

```text
10_完整功能Skills库/06_论文写作审稿投稿Skills
10_完整功能Skills库/07_自动化MCP浏览器与Agent Skills
10_完整功能Skills库/08_图表PPT海报与可视化Skills
```

---

## 6. 全功能安装后怎么用

全功能安装只是把 Skills 放到 Agent 能看到的位置。真正使用时，你仍然要告诉 Agent 任务目标。

标准提示词结构：

```text
请进入 [项目路径]。
先阅读 AGENTS.md。
本次任务是 [任务目标]。
请判断应该使用哪些 Skills。
先给出计划，不要立刻修改文件。
输出必须写入 [输出目录]。
不要编造引用，不要覆盖 raw 数据。
```

示例：

```text
请进入 <本项目路径>\零基础教学包\07_示例科研项目模板。
先阅读 AGENTS.md。
本次任务是对 data/raw/sample_empirical_data.csv 做完整实证分析。
请判断应该使用哪些 Skills。
先给出计划，不要立刻修改文件。
输出必须写入 output/empirical。
不要覆盖 raw 数据。
```

---

## 7. 全功能模块教学

### 7.1 文档处理模块

适合任务：

- PDF 转 Markdown。
- Word 草稿读取。
- Excel 数据读取。
- PPT 生成。

代表提示词：

```text
请读取 literature/pdfs 中的 PDF，转换为 Markdown，并输出结构化摘要。不要修改原始 PDF。
```

### 7.2 文献综述与引用模块

适合任务：

- 选题文献检索。
- 建立文献矩阵。
- 写文献综述。
- 核验 DOI。
- 生成 BibTeX。

代表提示词：

```text
请围绕“AI agent 与科研创造力”做中英文文献检索，输出检索式、核心文献、近五年趋势、研究方法分布和潜在 GAP。引用必须可核验。
```

### 7.3 CNKI 中文选题模块

适合任务：

- 中文热点扫描。
- CSSCI 期刊匹配。
- CNKI 趋势分析。

代表提示词：

```text
请使用 CNKI 相关 Skills 分析“生成式人工智能 知识工作”的中文研究热度、年度趋势、期刊分布和潜在选题缺口。
```

### 7.4 实证分析模块

适合任务：

- 数据清洗。
- Table 1。
- 相关矩阵。
- 回归。
- DID。
- IV。
- DML。
- 机器学习。
- 稳健性。

代表提示词：

```text
请使用 empirical-analysis-skill-python 对 data/processed/main.csv 做完整实证分析，包括清洗、变量构造、描述统计、基准回归、机制、异质性和稳健性。
```

### 7.5 文本挖掘模块

适合任务：

- 中文分词。
- 词频。
- TF-IDF。
- Word2Vec。
- Embedding。
- LDA / BERTopic。
- 情感分析。
- LLM 标注。

代表提示词：

```text
请对 data/raw/sample_texts.csv 的 text 列做文本挖掘分析，包括清洗、分词、词频、TF-IDF、情感分析，并说明样本是否适合主题模型。
```

### 7.6 写作与审稿模块

适合任务：

- Introduction。
- Method。
- Results。
- Discussion。
- 投稿格式。
- 审稿意见。
- 研究计划。

代表提示词：

```text
请基于文献矩阵和研究设计写 SSCI 风格 Introduction。要求问题意识清楚，理论机制具体，不要堆砌文献，不要编造引用。
```

### 7.7 自动化与 MCP 模块

适合任务：

- 自动浏览网页。
- 表单填写。
- 数据下载。
- 创建 MCP。
- 创建新 Skill。

代表提示词：

```text
请使用 agent-browser 打开目标网页，先截图和读取页面结构，不要登录或提交表单，先告诉我可以采集哪些公开信息。
```

### 7.8 图表展示模块

适合任务：

- 理论模型图。
- EEG 实验流程图。
- 文本挖掘流程图。
- 答辩 PPT。
- 学术 poster。

代表提示词：

```text
请根据我的研究框架生成一张适合论文的理论机制图，包含 AI agent 使用、认知负荷、知识整合和科研创造力。
```

---

## 8. 新手什么时候用最小安装，什么时候用全部安装

| 情况 | 推荐 |
|---|---|
| 第一次接触 AI Agent | 最小安装 |
| 只想完成五个练习 | 最小安装 |
| 已经知道要长期使用 | 全部安装 |
| 要做文献、实证、文本、写作全流程 | 全部安装 |
| 电脑空间紧张或不想混乱 | 先最小安装 |
| 准备建设个人科研 Agent 系统 | 全部安装 |

注意：安装全部 Skills 不等于你要一次学完全部功能。你只是在工具箱里放齐工具。

---

## 9. 完整功能学习顺序

建议 4 周学完：

### 第 1 周：基础与文献

- PowerShell。
- Skills 安装。
- PDF 阅读。
- 文献矩阵。
- 引用核验。

### 第 2 周：选题与综述

- OpenAlex。
- CNKI。
- SSCI 文献拆解。
- 综述写作。

### 第 3 周：实证与文本

- 数据清洗。
- 描述统计。
- 回归。
- DML 入门。
- 文本分词、TF-IDF、主题模型。

### 第 4 周：写作、审稿和自动化

- Introduction。
- Results。
- Discussion。
- Peer review。
- PPT / 图示。
- 自定义 Skill。

---

## 10. 最重要的规则

无论安装多少功能，都必须遵守：

1. 不覆盖 raw 数据。
2. 不编造引用。
3. 不把相关写成因果。
4. 不把模拟数据当真实结论。
5. 不把 API key 写进文档。
6. 不让 Agent 替你做理论判断。
7. 每个输出都要能追踪来源。

---

## 11. 你现在应该怎么开始

如果你是完全新手，现在按这个顺序做：

1. 打开 `00_先读我/README_先读我.md`。
2. 打开本手册。
3. 运行环境检查。
4. 运行 `check_full_skills_library.ps1`。
5. 先安装最小 Skills。
6. 做五个练习案例。
7. 再运行 `install_all_skills.ps1` 安装全部功能。
8. 开始迁移到自己的真实课题。

如果你已经确定要全功能：

```powershell
cd "<本项目路径>\零基础教学包"
powershell -ExecutionPolicy Bypass -File .\08_脚本\install_all_skills.ps1 -Target codex
```

---

## 12. 结论

这个零基础教学包现在不是简化版，而是“零基础教学 + 全功能 Skills 库”的组合包。

它的正确用法是：

```text
用零基础材料学会怎么操作
用完整功能库覆盖所有科研场景
用练习案例建立手感
用项目模板迁移到真实研究
```

学会以后，你应该能独立完成：

- 文献检索。
- 文献综述。
- 引用核验。
- CNKI 选题。
- PDF/Word/Excel/PPT 处理。
- 数据清洗和实证分析。
- 机器学习和因果推断。
- 文本挖掘和情感分析。
- 论文写作、审稿和投稿准备。
- 科学图表、PPT 和 poster。
- 浏览器自动化、MCP 和自定义 Skill。
