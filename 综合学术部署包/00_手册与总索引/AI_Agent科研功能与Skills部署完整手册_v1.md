# AI Agent 科研功能与 Skills 部署完整手册

版本：v1.0  
整理时间：2026-05-12  
资料来源：`<本项目路径>` 下的 Claude Code、OpenClaw、Python 大语言模型与智能体前沿实证特训营、OpenClaw SSCI 特训营、工程化科研课程资料。  
适用对象：管理学、心理学、神经科学、计算机科学交叉方向博士生，尤其适合文献综述、选题设计、EEG/ERP 研究、文本挖掘、机器学习、因果推断、实证论文写作与复现。

---

## 0. 这份手册怎么用

这份手册不是课程资料的简单目录，而是把现有课程内容重组为一个可部署、可执行、可扩展的个人科研 Agent 系统。建议按以下顺序阅读：

1. 先读第 1-3 章，理解 Claude Code / OpenClaw / Skills / MCP / Subagent 之间的关系。
2. 再读第 4 章，完成 Skills 的基础部署。
3. 根据当前任务查第 5-16 章：文献、选题、数据、实证、文本、写作、审稿、展示。
4. 最后读第 17-20 章，把这些功能整合成你的博士科研 SOP。

最重要的原则：不要把 Agent 当作“问答工具”，而要把它配置成“科研操作系统”。它应该能读你的文件、调用脚本、维护知识库、检索真实文献、生成可追踪输出，并在长期项目中持续复用。

---

## 1. 课程精髓总览

### 1.1 从 Vibe Research 到工程化科研

课程的核心观点可以概括为：AI Agent 不只是帮你写几段文字，而是把科研过程从“临时对话”升级为“工程化工作流”。

传统使用大模型的问题：

- 每次重新解释背景，浪费上下文。
- 文献、数据、代码、图表分散，难以复现。
- 大模型容易生成看似合理但不可核验的文献和方法。
- 复杂任务依赖多轮提示词，结果不稳定。

工程化科研的改造方向：

- 用项目文件固定研究背景、偏好、约束与输出格式。
- 用 Skills 封装重复任务。
- 用脚本和命令行保证数据处理、建模和输出可复现。
- 用知识库沉淀文献、概念、变量、理论与方法。
- 用 Subagent 并行处理大规模文献和复杂任务。
- 用 MCP、浏览器自动化、API 让 Agent 能调用外部工具。

### 1.2 Claude Code 与 OpenClaw 的定位

| 工具 | 核心定位 | 最适合做什么 | 不适合做什么 |
|---|---|---|---|
| Claude Code / Codex 类编码 Agent | 本地项目级科研操作系统 | 读写文件、跑代码、整理文献、处理数据、复现论文、生成报告、开发 Skills | 长期在线值守、群聊机器人、跨平台通知 |
| OpenClaw | 持续运行的自动化学术助手 | 飞书/群聊接入、定时任务、自动回复、长期知识库、自动化调度 | 精细代码修改、复杂本地工程管理 |
| 普通网页版大模型 | 轻量问答与初稿生成 | 快速解释概念、生成思路、润色短文本 | 大规模文件处理、可复现分析、本地自动化 |

实用建议：

- 写论文、跑代码、整理本地资料：优先 Claude Code / Codex。
- 做自动提醒、飞书群助手、定时文献监控：优先 OpenClaw。
- 只做临时头脑风暴：网页版模型即可。

### 1.3 Skills 的本质

Skills 不是普通提示词。它们是“结构化经验封装”：

- `SKILL.md`：说明何时触发、如何执行、读哪些参考、调用哪些脚本。
- `scripts/`：稳定执行的脚本，适合数据清洗、建模、批处理。
- `references/`：大段方法说明、字段说明、写作模板，不必每次全部加载。
- `assets/`：模板、字体、示例文件、表格样式。

课程中的关键判断是：当一个任务需要反复做、步骤稳定、输出格式稳定时，就应该从提示词升级为 Skill。

适合 Skill 化的科研任务：

- 文献检索与筛选。
- PDF 论文结构化阅读。
- 文献综述分类与写作。
- 数据清洗、描述统计、建模与稳健性检验。
- 文本挖掘变量构造。
- EEG/ERP 预处理与统计报告。
- 论文 Introduction / Method / Results / Discussion 写作。
- 投稿期刊匹配、审稿回复、引用核验。

不适合 Skill 化的任务：

- 一次性的闲聊。
- 尚未稳定的方法探索。
- 需要你进行理论判断和研究贡献判断的最终决策。

---

## 2. 推荐的个人科研 Agent 架构

### 2.1 五类 Agent

建议你把个人科研系统拆成五个角色，而不是让一个 Agent 做所有事：

| Agent | 职责 | 典型 Skills |
|---|---|---|
| 文献 Agent | 检索、筛选、阅读、文献矩阵、引用核验 | `academic-research`、`literature-review`、`citation-management`、`pdf-paper-summary`、`ssci-literature-review` |
| 方法 Agent | 实验设计、统计方案、因果推断、机器学习、EEG/ERP 方法审查 | `empirical-analysis-skill-python`、`statistical-analysis`、`scientific-critical-thinking`、自定义 EEG Skill |
| 数据 Agent | 数据采集、清洗、表格提取、可视化、建模产物管理 | `multi-source-data-integration-extraction`、`research-data-auto-analysis-plotting`、`xlsx`、`text-analysis-basic` |
| 写作 Agent | 大纲、章节写作、论文语言、投稿材料 | `scientific-writing`、`empirical-paper-writer`、`paper-writing-assistant-typesetting`、`venue-templates` |
| 审稿 Agent | 方法漏洞、理论错位、引用不实、贡献夸大、格式缺陷 | `peer-review`、`scholar-evaluation`、`scientific-critical-thinking` |

### 2.2 文件层面的基础设施

每个重要科研项目建议采用如下目录结构：

```text
project-name/
  AGENTS.md 或 CLAUDE.md
  README.md
  data/
    raw/
    interim/
    processed/
  literature/
    pdfs/
    notes/
    matrix/
    references.bib
  scripts/
  output/
    empirical/
    nlp/
    figures/
    tables/
    reports/
  manuscript/
    outline.md
    draft.docx
    response-to-reviewers.md
  logs/
    decisions.md
    experiment-log.md
```

其中：

- `raw/` 只存原始数据，不修改。
- `processed/` 存可分析数据。
- `output/` 存所有可复现产物。
- `logs/` 记录关键决策、失败尝试、模型参数和版本。
- `AGENTS.md` / `CLAUDE.md` 固定项目规则。

### 2.3 项目级 AGENTS.md / CLAUDE.md 应写什么

建议写入以下内容：

```markdown
# 项目规则

## 研究主题
本项目关注：[主题]。

## 学科定位
管理学、心理学、神经科学、计算机科学交叉。

## 方法偏好
优先考虑实验设计、EEG/ERP、机器学习、文本挖掘、因果推断。

## 文献标准
禁止编造引用。涉及文献时必须核验 DOI、期刊、作者、年份。

## 数据规则
raw 数据不可覆盖。所有清洗输出写入 data/processed 或 output。

## 写作规则
避免空话，理论必须解释机制，不接受贴标签式理论套用。

## 输出规则
所有分析必须输出表格、图、日志和可复现命令。
```

---

## 3. Skills 部署总原则

### 3.1 Skills 的标准结构

一个 Skill 的最小结构：

```text
skill-name/
  SKILL.md
```

复杂 Skill 的推荐结构：

```text
skill-name/
  SKILL.md
  scripts/
    run_task.py
    requirements.txt
  references/
    method-guide.md
    output-format.md
  assets/
    template.docx
    sample.csv
```

部署时最重要的是保证 `SKILL.md` 在技能目录根部。

### 3.2 Windows 下常见部署路径

根据工具不同，Skills 可能放在不同位置。你当前电脑已有 Codex 技能目录：

```text
C:\Users\<用户名>\.codex\skills
```

Claude Code 常见路径：

```text
C:\Users\<用户名>\.claude\skills
```

OpenClaw 常见路径：

```text
C:\Users\<用户名>\.openclaw\skills
```

课程资料中也出现了 Linux / 服务器路径：

```text
/root/.openclaw/skills
```

项目级技能也可以放在：

```text
project-name/.claude/skills
project-name/.codex/skills
```

建议：

- 全局长期复用 Skill 放到用户级目录。
- 某个课题专用 Skill 放到项目级目录。
- 课程原始 Skill 不要直接改，先复制一份到你的技能目录再修改。

### 3.3 从本地课程资料部署 Skill

通用步骤：

1. 找到 Skill 文件夹，确认里面有 `SKILL.md`。
2. 复制整个文件夹到技能目录。
3. 检查 `scripts/requirements.txt`，安装依赖。
4. 检查是否需要 API key、数据库、浏览器、字体或外部软件。
5. 用最小测试任务验证。
6. 把使用说明写入项目 `AGENTS.md`。

PowerShell 示例：

```powershell
$src = "<本项目路径>\Python大语言模型与智能体前沿实证特训营\专题五：文本分析NLP与Skill构建\skills\topic-modeling"
$dst = "C:\Users\<用户名>\.codex\skills\topic-modeling"
Copy-Item -Recurse -Force -LiteralPath $src -Destination $dst
```

安装依赖：

```powershell
cd "C:\Users\<用户名>\.codex\skills\topic-modeling"
python -m pip install -r scripts\requirements.txt
```

如果没有 `requirements.txt`，先读取 `SKILL.md` 和 `scripts/` 中的 import，再按需安装。

### 3.4 从 GitHub 或 Skill 平台部署

课程强调：不要盲装 Skill。标准流程是：

1. 获取 Skill 源码。
2. 审查 `SKILL.md`。
3. 审查 `scripts/` 是否有危险操作。
4. 检查是否读取隐私文件、上传数据、删除文件、执行远程代码。
5. 评估权限范围。
6. 安装到技能目录。
7. 先用测试数据跑，不直接用真实论文和真实数据。

安全红线：

- 不安装来源不明、脚本不可读的 Skill。
- 不把 API key 写进 `SKILL.md`。
- 不把浏览器 cookie、数据库密码、Zotero key 明文写进项目文档。
- 涉及 CNKI、数据库、机构账号时要遵守使用协议。

### 3.5 API key 的正确配置方式

不要把 key 写进手册或代码。推荐使用环境变量。

PowerShell 临时设置：

```powershell
$env:OPENAI_API_KEY="你的key"
$env:SEMANTIC_SCHOLAR_API_KEY="你的key"
```

永久设置：

```powershell
setx OPENAI_API_KEY "你的key"
setx SEMANTIC_SCHOLAR_API_KEY "你的key"
```

项目配置文件中只写变量名：

```text
本项目使用 OPENAI_API_KEY 环境变量，不在项目中保存明文 key。
```

---

## 4. 优先部署清单

### 4.1 第一批：必须优先部署

| 功能 | 推荐 Skill | 本地资料位置 | 部署优先级 |
|---|---|---|---|
| 文档转换 | `markitdown`、`pdf`、`docx`、`xlsx` | `cc课程资料\skills` | 最高 |
| 引用核验 | `citation-management` | `cc课程资料\skills\citation-management` | 最高 |
| 文献综述 | `literature-review`、`ssci-literature-review` | `cc课程资料\skills`、`openclawssci特训营` | 最高 |
| 学术检索 | `academic-research`、`research-lookup`、`research-superpower` | `cc课程资料\skills`、Python 课程 Skill 包 | 最高 |
| 实证分析 | `empirical-analysis-skill-python` | `专题四：机器学习与Skill构建` | 最高 |
| 文本挖掘 | `text-analysis-basic`、`topic-modeling`、`sentiment-analysis` | `专题五：文本分析NLP与Skill构建\skills` | 最高 |
| Skill 开发 | `skill-creator` | `cc课程资料\skills\skill-creator` | 很高 |
| 审稿与批判 | `peer-review`、`scientific-critical-thinking`、`scholar-evaluation` | `cc课程资料\skills` | 很高 |

### 4.2 第二批：项目成熟后部署

| 功能 | 推荐 Skill | 使用时机 |
|---|---|---|
| 浏览器自动化 | `agent-browser` | 需要网页采集、表单、下载、截图时 |
| MCP 开发 | `mcp-builder` | 需要接入 Zotero、数据库、文献 API、实验平台时 |
| 多来源数据整合 | `multi-source-data-integration-extraction` | 年报、政策、PDF、Excel 混合资料时 |
| 自动图表 | `research-data-auto-analysis-plotting`、`data-viz-analyzer` | 数据初探和论文图表时 |
| 论文排版包 | `paper-writing-assistant-typesetting` | 需要 Word/LaTeX/PDF 草稿时 |
| 学术展示 | `scientific-slides`、`paper-slide-deck`、`latex-posters` | 开题、答辩、会议时 |

### 4.3 暂时不建议优先部署

以下 Skill 对你当前研究方向不是核心：

- `slack-gif-creator`
- `polymarket`
- `algorithmic-art`
- `clinical-reports`
- `treatment-plans`
- 通用前端和品牌设计类 Skill

除非你有明确需求，否则它们会增加目录噪音。

---

## 5. 功能一：文献发现与选题扫描

### 5.1 目标

解决三个问题：

1. 这个主题有没有研究价值？
2. 近五年研究热点在哪里？
3. 你的切入点是否只是旧问题换说法？

### 5.2 需要的 Skills

| 子任务 | Skills |
|---|---|
| 英文文献检索 | `academic-research`、`research-lookup`、`research-superpower/searching-literature` |
| 中文文献检索 | `cnki-crawler`、`cnki-exp-search-automation` |
| 选题热度分析 | `cnki-rank`、`cnki-trend`、`cnki-research-assistant` |
| arXiv 快速追踪 | `arxiv-watcher` |
| 文献开放获取 | `finding-open-access-papers` |

### 5.3 部署重点

英文检索类：

- `academic-research` 基于 OpenAlex，通常不需要 API key。
- Semantic Scholar 可不配 key，但高频调用建议配置 key。
- `research-lookup` 若依赖外部搜索 API，需要检查是否配置环境变量。

CNKI 类：

- 通常需要 Python 依赖：`requests`、`pandas`、`beautifulsoup4`、`lxml`、`psycopg2-binary`、`openpyxl`。
- 课程中的 CNKI crawler 可能需要 PostgreSQL。
- 可能需要代理、cookie、浏览器辅助。不要绕过平台规则。

部署命令示例：

```powershell
cd "...\cnki-crawler"
python -m pip install -r requirements.txt
```

如果用数据库：

```text
host: localhost
port: 5432
dbname: cnki_db
user: cnki_user
password: 使用本地安全配置，不写入手册
```

### 5.4 推荐工作流

1. 先用 `academic-research` / OpenAlex 查英文核心文献。
2. 再用 CNKI 工具查中文研究热度、CSSCI 期刊分布和本土化议题。
3. 用 `cnki-trend` 看年度趋势、学科分布、期刊集中度和基金支持。
4. 用 `cnki-research-assistant` 生成选题可行性报告。
5. 用 `citation-management` 核验关键文献。
6. 最后人工判断：问题是否真有机制增量。

### 5.5 触发词示例

```text
请围绕“AI 代理使用对科研创造力的影响”做中英文文献发现，输出近五年核心文献、经典文献、研究方法分布和潜在研究空白。必须核验引用。
```

```text
请用 CNKI 选题分析助手分析“数字化转型与员工创造力”的研究热度、年度趋势、CSSCI 期刊匹配和可能的研究缺口。
```

### 5.6 输出物

```text
literature/search_queries.md
literature/raw_results.json
literature/screened_papers.csv
literature/topic_trend_report.md
literature/references.bib
```

---

## 6. 功能二：文献筛选、阅读与综述写作

### 6.1 目标

把“读了很多论文但没有结构”转化为：

- 文献矩阵。
- 研究流派图谱。
- 理论机制链条。
- 方法优缺点比较。
- 可写入论文的综述段落。

### 6.2 需要的 Skills

| 子任务 | Skills |
|---|---|
| 系统综述流程 | `literature-review` |
| 大规模筛选 | `research-superpower`、`evaluating-paper-relevance`、`subagent-driven-review` |
| SSCI 论文拆解 | `ssci-literature-review` |
| PDF 快速总结 | `pdf-paper-summary`、`paper-innovation-extractor` |
| 引文网络追踪 | `traversing-citations` |
| 引用核验 | `citation-management` |

### 6.3 课程精髓

文献综述不是“按作者逐篇介绍”，而是建立一种研究者视角下的秩序。课程中强调了五种分类路线：

1. 从上到下：从选题、理论、变量结构出发建立分类。
2. 从下到上：从已有论文归纳编码，形成类别。
3. 从老到新：按研究演化脉络组织。
4. 从 X 到 Y：按变量路径组织。
5. 由点到面：基于文献计量或主题模型组织。

高质量综述必须有“评”：

- 评关系：研究结论之间是互补、冲突还是替代？
- 评方法：样本、识别策略、测量方式是否限制结论？
- 评理论：理论是否解释机制，还是只贴标签？
- 评趋势：焦点是否从 A 转向 B？
- 评缺口：缺口是否真能支撑你的研究问题？

### 6.4 部署重点

`literature-review` 适合完整综述项目，建议配合：

- `citation-management`
- `research-lookup`
- `scientific-schematics`
- `pdf` / `markitdown`

如果要做大规模筛选，建议使用研究会话目录：

```text
research-sessions/YYYY-MM-DD-topic/
  SUMMARY.md
  papers-reviewed.json
  papers/
  citations/
```

### 6.5 推荐工作流

1. 建立检索式并保存。
2. 执行多数据库检索。
3. 去重。
4. 标题和摘要筛选。
5. 全文筛选。
6. 建立文献矩阵。
7. 提取理论、变量、方法、样本、结论、局限。
8. 按分类框架重组。
9. 写综述段落。
10. 用 `peer-review` 检查是否只是堆文献。

### 6.6 文献矩阵字段

建议字段：

```text
paper_id
authors
year
journal
doi
research_question
theory
independent_variable
dependent_variable
mediator
moderator
sample
method
identification_strategy
main_findings
limitations
relevance_to_my_study
possible_gap
```

### 6.7 触发词示例

```text
请读取 literature/pdfs 中的论文，建立文献矩阵。字段包括研究问题、理论、变量、样本、方法、主要发现、局限和与我研究的关联。不要编造文献，缺失信息标注“未报告”。
```

```text
请基于这些文献写一个 SSCI 风格文献综述，不要逐篇罗列。按理论机制和方法范式分类，每一类都要写出共识、分歧、原因和不足。
```

---

## 7. 功能三：引用管理与真实性核验

### 7.1 目标

避免学术写作中最危险的问题：引用不存在、DOI 错误、作者年份错误、期刊信息不完整。

### 7.2 需要的 Skills

| 子任务 | Skills |
|---|---|
| DOI 转 BibTeX | `citation-management` |
| PubMed 元数据 | `citation-management`、`searching-literature` |
| Google Scholar 辅助搜索 | `citation-management` |
| BibTeX 清洗 | `citation-management` |
| 投稿格式 | `venue-templates` |

### 7.3 部署重点

检查脚本依赖：

```powershell
cd "...\citation-management"
python -m pip install -r scripts\requirements.txt
```

如果没有 requirements，通常需要：

```text
requests
beautifulsoup4
pandas
feedparser
pybtex 或 bibtexparser
```

### 7.4 使用规则

1. 论文写作时，不允许凭记忆生成参考文献。
2. 每个关键引用至少核验标题、作者、年份、期刊、DOI。
3. 引用缺少 volume、issue、pages、doi 时，必须补全或标注缺失。
4. 中文文献也要保留来源、期刊、年份和数据库记录。

### 7.5 触发词示例

```text
请核验 manuscript/references.bib 中所有文献，检查 DOI、作者、年份、期刊、卷期页是否完整，并输出问题清单和修正后的 BibTeX。
```

---

## 8. 功能四：知识库、Obsidian 与文献管理

### 8.1 目标

把“读过的论文”变成“可复用的知识资产”。

### 8.2 推荐工具组合

| 层级 | 工具 | 适用场景 |
|---|---|---|
| 快速批量阅读 | NotebookLM / PDF 总结 Skill | 5-10 篇论文快速比较 |
| 结构化文献库 | 飞书多维表格 / Excel / CSV | 长期筛选、分组、排序 |
| 深度知识网络 | Obsidian / Markdown | 概念、理论、变量、方法长期积累 |
| 引用管理 | Zotero + BibTeX | 投稿、参考文献、PDF 管理 |

### 8.3 需要的 Skills

```text
markitdown
pdf-paper-summary
citation-management
docx
xlsx
literature-review
```

### 8.4 Obsidian 笔记模板

```markdown
# 论文标题

## 基本信息
- 作者：
- 年份：
- 期刊：
- DOI：

## 研究问题

## 理论机制

## 变量与假设

## 方法设计
- 样本：
- 数据：
- 识别策略：
- 模型：

## 主要发现

## 局限

## 可迁移到我研究中的部分

## 可疑之处或需要核验之处
```

### 8.5 概念库五分类

建议把 Obsidian 中的概念分为：

1. 理论概念。
2. 变量概念。
3. 方法概念。
4. 数据来源。
5. 机制解释。

---

## 9. 功能五：科研数据采集

### 9.1 目标

把网页、年报、政策文本、期刊页面、公开数据库中的资料转成可分析数据。

### 9.2 需要的 Skills

| 数据来源 | Skills |
|---|---|
| 网页数据 | `agent-browser`、`web-browsing`、`chinanews-scraper` |
| CNKI 文献数据 | `cnki-crawler`、`cnki-exp-search-automation` |
| 年报 PDF | `multi-source-data-integration-extraction`、`text-analysis-basic` |
| 政策文本 | `agent-browser`、`text-analysis-basic` |
| 金融数据 | `tushare-finance` |
| 学术文献 API | `academic-research`、`research-lookup` |

### 9.3 课程精髓

Python 数据采集课程强调：

- 先理解浏览器与服务器如何交互。
- 区分 GET、POST、HTML、JSON、文件下载。
- 先看网页源数据，再决定用 requests、BeautifulSoup、XPath、Selenium/浏览器自动化。
- 保存到 CSV、Excel、MySQL 或 PostgreSQL。
- 注意反爬、验证码、IP 封禁、robots 和平台规则。
- 多线程/多进程只在合规和必要时使用。

### 9.4 agent-browser 部署与使用

`agent-browser` 适合自动浏览、点击、填表、下载、截图。

核心命令：

```powershell
agent-browser open https://example.com
agent-browser snapshot -i
agent-browser click @e1
agent-browser fill @e2 "关键词"
agent-browser wait --load networkidle
agent-browser screenshot page.png
```

使用原则：

- 先 `snapshot -i` 获取元素编号。
- 页面变化后重新 snapshot。
- 登录态文件要加密或删除。
- 下载的 PDF 统一放入 `literature/pdfs` 或 `data/raw`。

### 9.5 输出规范

```text
data/raw/source_name/
  raw_pages/
  downloaded_files/
  crawl_log.md
  metadata.csv
data/interim/
  parsed_records.csv
```

---

## 10. 功能六：多来源数据整合与表格提取

### 10.1 目标

把散乱的 Excel、CSV、PDF 表格、HTML 表格、TXT/MD 表格整理为统一数据集。

### 10.2 需要的 Skill

```text
multi-source-data-integration-extraction
markitdown
pdf
xlsx
text-analysis-basic
```

### 10.3 部署

课程 Skill 包路径：

```text
Python大语言模型与智能体前沿实证特训营\专题三：AI智能体、Skill开发与科研自动化\05_Skill能力包\03_多来源数据提取_Skill
```

安装依赖：

```powershell
cd "...\03_多来源数据提取_Skill"
python -m pip install -r scripts\requirements.txt
```

常见依赖：

```text
pandas
openpyxl
lxml
beautifulsoup4
pdfplumber
PyMuPDF
paddlepaddle
paddleocr
```

### 10.4 使用命令

```powershell
python scripts\merge_extract_sources.py "D:\data\annual_reports" --output-dir "D:\output\merged_reports"
```

启用 OCR：

```powershell
python scripts\merge_extract_sources.py "D:\data\scanned_pdf" --output-dir "D:\output\ocr_tables" --ocr
```

### 10.5 输出物

```text
merged_dataset.csv
extraction_manifest.json
extracted_tables/
```

其中 `extraction_manifest.json` 很重要，它记录每张表来自哪个文件、哪一页、多少行列。论文复现和数据审计时必须保留。

---

## 11. 功能七：数据清洗、描述统计与可视化

### 11.1 目标

把原始数据转为可分析数据，并自动生成质量报告、缺失值报告、描述统计和初步图表。

### 11.2 需要的 Skills

| 子任务 | Skills |
|---|---|
| 数据质量检查 | `empirical-analysis-skill-python`、`research-data-auto-analysis-plotting` |
| 描述统计 | `empirical-analysis-skill-python`、`data-viz-analyzer` |
| 缺失值与异常值 | `empirical-analysis-skill-python` |
| 相关矩阵与热力图 | `research-data-auto-analysis-plotting` |
| Excel 清洗与合并 | `xlsx`、`multi-source-data-integration-extraction` |

### 11.3 empirical-analysis 部署

路径：

```text
Python大语言模型与智能体前沿实证特训营\专题四：机器学习与Skill构建\empirical-analysis-skill_Python
```

安装：

```powershell
cd "...\empirical-analysis-skill_Python"
python -m pip install -r requirements.txt
```

如果没有统一 requirements，可根据脚本安装：

```powershell
python -m pip install pandas numpy scipy statsmodels scikit-learn matplotlib seaborn openpyxl linearmodels econml
```

### 11.4 典型脚本链

```text
scripts/clean_data.py
scripts/transform_data.py
scripts/describe_data.py
scripts/run_diagnostics.py
scripts/run_model.py
scripts/run_robustness.py
scripts/run_further_analysis.py
scripts/table_factory.py
scripts/plot_factory.py
scripts/render_manifest.py
```

### 11.5 推荐工作流

1. `clean_data.py`：检查类型、缺失、去重、样本构造。
2. `transform_data.py`：构造 log、IHS、winsor、z-score、dummy、lag、lead。
3. `describe_data.py`：生成 Table 1、相关矩阵、趋势图。
4. `run_diagnostics.py`：正态性、异方差、自相关、VIF。
5. `run_model.py` 或其他模型脚本。
6. `run_robustness.py`：替代控制、聚类标准误、样本过滤、安慰剂。
7. `render_manifest.py`：汇总输出清单。

### 11.6 输出规范

```text
output/empirical/
  table1_summary.csv
  table1_summary.xlsx
  table2_main.csv
  table5_robustness.csv
  fig1_trend.png
  fig3_coefplot.png
  artifact_manifest.md
```

---

## 12. 功能八：实证建模、机器学习与因果推断

### 12.1 目标

支持管理学、心理学、神经营销和文本挖掘研究中的核心实证分析。

### 12.2 模型与 Skill 映射

| 研究任务 | 推荐脚本 / Skill |
|---|---|
| OLS / Logit / Probit / Poisson | `run_model.py` |
| 面板固定效应 | `run_panel.py` |
| DID / 事件研究 | `run_did.py` |
| IV / 2SLS | `run_iv.py` |
| RD | `run_rd.py` |
| PSM / IPW | `run_matching.py` |
| 合成控制 | `run_synth.py` |
| DML | `run_dml.py` |
| 因果森林 / CATE | `run_cate.py` |
| Lasso / Ridge / ElasticNet | `run_supervised_ml.py` |
| 决策树 / 随机森林 / GBDT | `run_supervised_ml.py` |
| 机制 / 异质性 / 中介 | `run_further_analysis.py` |
| 稳健性 / 敏感性 | `run_robustness.py`、`run_sensitivity.py` |

### 12.3 课程精髓

机器学习课程的关键不是“模型越复杂越好”，而是：

- 明确预测任务和解释任务的差异。
- 先定义 X 和 y。
- 固定训练集、验证集、测试集。
- 回归任务看 RMSE、MAE、R2。
- 分类任务看 accuracy、precision、recall、F1。
- 树模型要解释特征重要性。
- DML 用于在高维控制下估计因果效应，不等于随便跑一个机器学习模型。

### 12.4 DML 使用条件

DML 适合：

- 处理变量 T 明确。
- 结果变量 Y 明确。
- 有大量控制变量 W/X。
- 研究目标是估计 T 对 Y 的因果效应。
- 你愿意接受并解释识别假设。

DML 不适合：

- 没有明确处理变量。
- 只是想做预测。
- 数据严重缺乏可比性。
- 不能解释为什么满足条件独立或可忽略性。

### 12.5 触发词示例

```text
请使用 empirical-analysis-skill-python 对 data/processed/panel.csv 做完整实证分析：先清洗、描述统计、相关矩阵，再跑固定效应模型，最后做稳健性、异质性和机制检验。所有输出写入 output/empirical。
```

```text
请把“AI 工具使用”作为处理变量，把“科研创造力评分”作为结果变量，使用 DML 估计处理效应。先说明识别假设，再生成代码和结果报告。
```

---

## 13. 功能九：文本挖掘与 NLP

### 13.1 目标

把年报、政策、评论、论文摘要、访谈文本等非结构化文本转成可建模变量。

### 13.2 需要的 Skills

| 子任务 | Skills |
|---|---|
| PDF/OCR 提取 | `text-analysis-basic`、`markitdown`、`multi-source-data-integration-extraction` |
| 中文分词 | `text-analysis-basic` |
| 词频/句频/词云 | `text-analysis-basic` |
| TF-IDF / Word2Vec / Embedding | `text-analysis-basic` |
| 文本相似度 | `text-analysis-basic` |
| LDA / DTM / BERTopic | `topic-modeling` |
| 情感分析 | `sentiment-analysis` |
| 大规模文本标注 | `big-data-labeling-variable-construction` |
| 深度学习 NLP | `deep-learning-nlp` |

### 13.3 部署

路径：

```text
Python大语言模型与智能体前沿实证特训营\专题五：文本分析NLP与Skill构建\skills
```

建议部署：

```text
text-analysis-basic
topic-modeling
sentiment-analysis
deep-learning-nlp
```

安装常见依赖：

```powershell
python -m pip install pandas numpy jieba scikit-learn gensim matplotlib seaborn wordcloud sentence-transformers bertopic snownlp openpyxl
```

OCR 相关：

```powershell
python -m pip install paddlepaddle paddleocr pymupdf pdfplumber
```

### 13.4 文本分析路线

基础路线：

```text
PDF/CSV/XLSX 输入
  -> 文本抽取
  -> 清洗
  -> 分词
  -> 停用词
  -> 词频/TF-IDF/Embedding
  -> 变量构造
  -> 回归/机器学习/可视化
```

主题模型路线：

```text
清洗语料
  -> LDA 主题数诊断
  -> 选择 K
  -> 最终训练
  -> 文档-主题概率
  -> 主题词解释
  -> 随年份/行业/组别分析
```

情感分析路线：

```text
词典法：适合透明、可解释、论文中易说明
传统机器学习：适合有标签样本
LLM 标注：适合复杂语义，但必须抽样核验一致性
```

### 13.5 年报文本变量构造

课程案例包含年报文本信息含量、前瞻性信息、特质信息等变量。可迁移为：

| 变量 | 构造思路 |
|---|---|
| 信息含量 | 财务金融词典词频 / 总词数 |
| 前瞻性信息 | 前瞻性词汇在相关语句中的占比 |
| 文本特质性 | 企业文本向量与行业/市场平均向量的距离 |
| 情绪倾向 | 正负情绪词典或分类模型输出 |
| AI 关注度 | AI 词典词频或语义扩展词频 |
| 战略相似度 | SentenceTransformer 或 TF-IDF 余弦相似度 |

### 13.6 触发词示例

```text
请用 text-analysis-basic 对 data/raw/reports 中的年报 PDF 提取文本，分词，计算 AI 相关词频、TF-IDF 关键词和企业层面的文本信息含量，输出 CSV 和方法说明。
```

```text
请对 comments.xlsx 的 text 列做 BERTopic 主题建模，先运行主题数和聚类诊断，不要直接给最终主题。输出主题词、文档主题分配和可视化。
```

---

## 14. 功能十：EEG/ERP 与神经科学研究的 Skill 化建议

### 14.1 现有课程的不足

当前资料中对 EEG/ERP 的直接 Skill 较少。对你来说，这是最需要个人定制的部分。

### 14.2 建议创建的 Skills

| Skill 名称 | 功能 |
|---|---|
| `eeg-preprocessing` | 导入 EEG、滤波、重参考、坏道检测、ICA、epoch、baseline |
| `erp-analysis` | 条件平均、峰值/均值振幅、潜伏期、时间窗统计 |
| `time-frequency-analysis` | ERSP、功率谱、频段能量、时频图 |
| `eeg-connectivity` | 相干、PLI、wPLI、功能连接矩阵 |
| `eeg-ml-pipeline` | 特征提取、分类、交叉验证、模型解释 |
| `neuro-paper-method-writer` | EEG/ERP 方法部分英文写作模板 |

### 14.3 EEG Skill 的结构建议

```text
eeg-preprocessing/
  SKILL.md
  scripts/
    preprocess_mne.py
    quality_report.py
    requirements.txt
  references/
    preprocessing-standard.md
    artifact-handling.md
    reporting-template.md
  assets/
    sample_config.yaml
```

### 14.4 关键输出

```text
output/eeg/
  preprocessing_report.html
  bad_channels.csv
  rejected_epochs.csv
  ica_components.png
  erp_waveforms.png
  erp_statistics.csv
  method_text_en.md
```

### 14.5 方法严谨性要求

EEG/ERP 分析必须记录：

- 采样率。
- 滤波参数。
- 重参考方式。
- 伪迹剔除标准。
- ICA 成分判断依据。
- epoch 时间窗。
- baseline 时间窗。
- ERP 成分时间窗。
- 多重比较校正方式。
- 被试剔除标准。

---

## 15. 功能十一：论文写作

### 15.1 课程精髓

论文写作课程的核心原则：

1. 骨架优先：先结构，再段落，再句子。
2. 你是思想工具，AI 是表达工具。
3. 写 Introduction 前，先明确任务、挑战、缺口、机制、贡献。
4. Results 要忠于数据，不提前过度解释。
5. Discussion 要解释机制、比较文献、承认局限，不要空泛拔高。

### 15.2 需要的 Skills

| 写作任务 | Skills |
|---|---|
| 英文科学论文 | `scientific-writing` |
| 实证论文框架 | `empirical-paper-writer` |
| 论文排版包 | `paper-writing-assistant-typesetting` |
| 研究计划 | `research-proposal` |
| 投稿格式 | `venue-templates` |
| 协同写作 | `doc-coauthoring` |
| 文档处理 | `docx`、`pdf`、`xlsx` |

### 15.3 Introduction 工作流

```text
1. 研究背景：为什么重要
2. 现有研究：已经知道什么
3. 关键不足：尚未解释什么
4. 理论机制：为什么你的变量之间有关系
5. 研究设计：你如何检验
6. 贡献：理论、方法、情境或数据贡献
```

### 15.4 Results 工作流

```text
1. 先报告描述统计和相关矩阵
2. 再报告主效应
3. 再报告中介/调节/机制
4. 再报告稳健性
5. 最后报告补充分析
```

写 Results 时不要说：

- “这充分证明了……”
- “显著促进了理论发展……”

应该说：

- “结果与 H1 预期一致。”
- “该效应在替代模型中保持方向一致。”
- “这一发现为……机制提供了初步证据。”

### 15.5 Discussion 工作流

```text
1. 回答研究问题
2. 解释主要发现
3. 与既有研究对话
4. 说明理论贡献
5. 说明方法或实践启示
6. 承认局限
7. 提出未来研究方向
```

### 15.6 触发词示例

```text
请基于 manuscript/outline.md 和 literature/matrix.xlsx 写 SSCI 风格 Introduction。要求：问题意识清楚，理论机制明确，不要堆砌文献，不要编造引用。
```

```text
请根据 output/empirical 中的表格写 Results 部分。只解释统计结果，不夸大因果，不引入表格中不存在的数字。
```

---

## 16. 功能十二：审稿、批判性评估与投稿准备

### 16.1 目标

在投稿前主动发现问题，避免理论错位、方法不匹配、结果夸大、引用不实。

### 16.2 需要的 Skills

```text
peer-review
scholar-evaluation
scientific-critical-thinking
venue-templates
citation-management
```

### 16.3 审查维度

| 维度 | 重点问题 |
|---|---|
| 研究问题 | 是否清楚、有意义、可检验 |
| 理论机制 | 是否真正解释变量关系 |
| 文献综述 | 是否有分类、比较、批判，而不是堆砌 |
| 方法设计 | 样本、测量、模型是否匹配假设 |
| 统计分析 | 是否有诊断、稳健性、效应量 |
| 因果表述 | 是否把相关说成因果 |
| 贡献 | 是否夸大 |
| 引用 | 是否真实、完整、相关 |
| 图表 | 是否自解释、格式一致 |
| 写作 | 是否简洁、推进、避免套话 |

### 16.4 触发词示例

```text
请以 SSCI 审稿人视角审查 manuscript/draft.docx。优先指出会导致拒稿的主要问题，包括理论机制、方法识别、结果解释和引用真实性。
```

---

## 17. 功能十三：学术图表、PPT、Poster 与 Paper-to-Web

### 17.1 需要的 Skills

| 输出 | Skills |
|---|---|
| 科学示意图 | `scientific-schematics` |
| 学术 PPT | `scientific-slides`、`paper-slide-deck`、`pptx` |
| 学术海报 | `latex-posters`、`pptx-posters` |
| 论文网页 | `paper-2-web` |
| 信息图 | `infographics` |

### 17.2 使用建议

对你的研究方向，最值得做的图：

- AI Agent 科研工作流图。
- EEG/ERP 实验流程图。
- 文本挖掘变量构造流程图。
- 理论机制模型图。
- 数据处理与建模 pipeline。
- DML / 因果推断识别框架图。

### 17.3 触发词示例

```text
请根据我的论文框架生成一张理论机制图，包含 AI agent 使用、认知负荷、探索行为、科研创造力之间的路径，并适合放入 SSCI 论文。
```

---

## 18. 功能十四：MCP、Hooks、Cron 与自动化

### 18.1 MCP

MCP 的作用是让 Agent 调用外部服务。适合接入：

- Zotero。
- 文献数据库。
- 实验平台。
- 本地文件索引。
- 统计软件。
- 飞书/日历/任务。
- 自建文献 API。

使用 `mcp-builder` 时，课程强调四步：

1. 研究 API 和 MCP 规范。
2. 设计工具：名称清楚、参数明确、错误信息可执行。
3. 实现服务：Python FastMCP 或 TypeScript SDK。
4. 测试评估：用真实问题验证 Agent 是否能用工具完成任务。

### 18.2 Hooks

Hooks 适合：

- 运行前检查目录结构。
- 写入后自动格式化。
- 分析后自动生成日志。
- 阻止覆盖 raw 数据。
- 提醒补充引用核验。

### 18.3 Cron / Heartbeat

OpenClaw 的定时任务适合：

- 每周检索新文献。
- 每天汇总学术热点。
- 定期检查项目进度。
- 自动生成文献监控报告。

示例任务：

```text
每周一上午 9 点检索“AI agent + research productivity”近一周新文献，输出摘要和 DOI 核验结果。
```

---

## 19. Subagent 并行协作

### 19.1 什么时候用 Subagent

适合：

- 50 篇以上文献筛选。
- 多数据库检索。
- 一个项目中同时做理论审查、方法审查、代码复现。
- 大型论文修改。

不适合：

- 你还没明确任务标准。
- 子任务强依赖同一个判断。
- 最终理论贡献判断。

### 19.2 推荐分工

| 子代理 | 任务 |
|---|---|
| Literature Explorer | 找文献、去重、提取元数据 |
| Theory Reviewer | 检查理论机制与变量对应 |
| Method Reviewer | 检查模型、识别策略、统计假设 |
| Code Worker | 跑数据清洗和模型 |
| Writing Reviewer | 检查段落逻辑、语言和投稿格式 |

### 19.3 标准提示词

```text
你负责文献筛选。请只处理 literature/raw_results.csv 中的论文，按 inclusion/exclusion criteria 判断相关性，输出 screened_papers.csv。不要修改其他文件。
```

---

## 20. 推荐学习路线

### 第 1 阶段：三天建立基础

1. 学会项目目录结构。
2. 写好全局和项目级 `AGENTS.md` / `CLAUDE.md`。
3. 部署 `markitdown`、`pdf`、`docx`、`xlsx`。
4. 部署 `citation-management`。
5. 用 5 篇论文测试 PDF 摘要和 BibTeX 核验。

### 第 2 阶段：一周建立文献系统

1. 部署 `academic-research`、`literature-review`。
2. 部署 CNKI 相关 Skill。
3. 建立文献矩阵模板。
4. 建立 Obsidian 笔记模板。
5. 做一个小型文献综述样例。

### 第 3 阶段：两周建立数据与实证系统

1. 部署 `empirical-analysis-skill-python`。
2. 部署 `research-data-auto-analysis-plotting`。
3. 用示例数据跑完整清洗、描述统计、主模型和稳健性。
4. 固定输出目录规范。

### 第 4 阶段：两周建立文本挖掘系统

1. 部署 `text-analysis-basic`。
2. 部署 `topic-modeling`。
3. 部署 `sentiment-analysis`。
4. 用年报或评论文本构造 2-3 个变量。
5. 把变量接入实证分析。

### 第 5 阶段：长期建设个人专用 Skill

优先开发：

1. EEG/ERP 分析 Skill。
2. 管理学 SSCI Introduction 写作 Skill。
3. 文本挖掘变量构造 Skill。
4. 因果推断稳健性检验 Skill。
5. 审稿回复 Skill。

---

## 21. 常用功能-技能总表

| 功能 | 必需 Skills | 可选 Skills | 核心输出 |
|---|---|---|---|
| 选题扫描 | `academic-research`、`cnki-research-assistant` | `arxiv-watcher` | 选题报告、趋势图 |
| 文献综述 | `literature-review`、`ssci-literature-review` | `subagent-driven-review` | 文献矩阵、综述草稿 |
| 引用核验 | `citation-management` | `venue-templates` | `references.bib`、问题清单 |
| PDF 处理 | `markitdown`、`pdf` | `pdf-paper-summary` | Markdown、结构化摘要 |
| 数据采集 | `agent-browser`、`cnki-crawler` | `web-browsing` | CSV、JSON、PDF |
| 数据整合 | `multi-source-data-integration-extraction` | `xlsx` | 合并数据集、manifest |
| 实证分析 | `empirical-analysis-skill-python` | `data-viz-analyzer` | 表格、图、模型报告 |
| 机器学习 | `empirical-analysis-skill-python` | `deep-learning-nlp` | 预测指标、特征重要性 |
| 因果推断 | `empirical-analysis-skill-python` | `scientific-critical-thinking` | DID/IV/DML/稳健性 |
| 文本挖掘 | `text-analysis-basic` | `topic-modeling`、`sentiment-analysis` | 文本变量、主题、情感 |
| EEG/ERP | 自定义 EEG Skills | `statistical-analysis` | 波形、统计、方法报告 |
| 论文写作 | `scientific-writing` | `empirical-paper-writer` | 章节草稿 |
| 论文审查 | `peer-review` | `scholar-evaluation` | 审稿报告 |
| 学术展示 | `scientific-slides` | `paper-slide-deck` | PPT、Poster、图 |
| 自动化 | `mcp-builder` | OpenClaw cron/hooks | 定时报告、工具接入 |

---

## 22. 最终建议

对你来说，最应该沉淀的不是“更多课程资料”，而是一个可持续运行的个人科研系统。

最小可行版本：

```text
文献检索 + 引用核验 + 文献矩阵 + 实证分析 + 文本挖掘 + 写作审稿
```

建议你先完成这六件事：

1. 把核心 Skills 复制到统一技能目录。
2. 建一个博士论文或当前论文项目模板。
3. 用 10 篇真实文献跑通文献矩阵。
4. 用一个 CSV 数据跑通 empirical-analysis。
5. 用一批文本跑通 NLP 变量构造。
6. 用一篇草稿跑 peer-review 和 citation-management。

如果这六步跑通，AI Agent 才真正从“课程资料”变成你的科研生产力。

