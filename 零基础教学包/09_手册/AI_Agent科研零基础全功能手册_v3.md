# AI Agent 科研零基础全功能手册 v3

版本：v3.0  
适用对象：完全不懂 AI Agent，但希望最终掌握完整科研 Agent 工作流的人  
核心定位：这不是简化包，而是“零基础教学路径 + 完整 131 个科研 Skills 库 + 本地按需复制脚本 + 练习项目”的组合包。  

---

## 0. 你先记住三句话

第一，AI Agent 不是聊天机器人。它能读文件、运行脚本、整理目录、调用 Skills、生成文档和执行科研流程。

第二，Skill 不是一个普通提示词。它是一个放在本地的 `SKILL.md` 文件夹，里面写清楚某类任务应该怎么做、用什么脚本、遵守什么规则。

第三，零基础教学包不是为了少功能，而是为了让你按顺序学会完整功能。你先用最小组合跑通动作，再按任务复制完整 131 个科研 Skills 中需要的模块。

---

## 1. 这个零基础包现在有什么

目录：

```text
零基础教学包
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

核心文件：

| 文件或目录 | 作用 |
|---|---|
| `00_先读我/README_先读我.md` | 新手入口，告诉你先读什么、先运行什么 |
| `00_先读我/学习路线图.md` | 从零基础到全功能的学习顺序 |
| `02_环境与部署/PowerShell零基础.md` | 教你打开命令行、进入目录、运行脚本 |
| `02_环境与部署/完整Skills安装说明.md` | 教你按需使用全部 131 个 Skills |
| `02_环境与部署/AMiner_MCP接入说明.md` | 教你接入 AMiner MCP |
| `02_环境与部署/AI4Scholar接入说明.md` | 教你接入 AI4Scholar MCP 或 OpenClaw 插件 |
| `04_五个完整练习案例` | 新手上手的 14 个练习案例 |
| `07_示例科研项目模板` | 以后迁移到真实课题的项目骨架 |
| `08_脚本/check_environment.ps1` | 检查环境 |
| `08_脚本/check_full_skills_library.ps1` | 检查完整 Skills 库 |
| `本地Skills功能分类库/00_工具脚本/check_local_skills_library.ps1` | 检查本地 131 个 Skills |
| `本地Skills功能分类库/00_工具脚本/copy_skill_to_workspace.ps1` | 按需复制 Skills 到项目工作区 |
| `08_脚本/check_academic_platforms.ps1` | 检查 AMiner/AI4Scholar 相关环境 |
| `10_完整功能Skills库` | 全功能 Skills 库 |

---

## 2. 新手怎么开始

### 2.1 打开 PowerShell

在 Windows 开始菜单搜索 `PowerShell`，打开后输入：

```powershell
cd "<本项目路径>\零基础教学包"
```

如果路径正确，你后续命令都在这个目录里运行。

### 2.2 检查环境

```powershell
powershell -ExecutionPolicy Bypass -File .\08_脚本\check_environment.ps1
```

你要关注三件事：

| 检查项 | 看什么 |
|---|---|
| Python | 是否能显示版本号 |
| Skill directories | 是否能看到 `.codex\skills` 等目录 |
| Local full skills library | 是否显示 131 skills |

### 2.3 检查完整 Skills 库

```powershell
powershell -ExecutionPolicy Bypass -File .\08_脚本\check_full_skills_library.ps1
```

正常结果应该包含：

```text
All full-library skill folders contain SKILL.md. Total=131
```

### 2.4 先复制最小 Skills

新手先复制最小组合是为了先会操作，不是因为包里没有完整功能。

```powershell
cd "<本项目路径>\本地Skills功能分类库"
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -SkillName pdf,docx,xlsx,markitdown -Workspace "D:\你的项目路径"
```

### 2.5 按需复制全部 Skills

当前推荐不要把全部 Skills 安装进 Codex 根目录，而是从本地分类库按需复制到项目工作区。

```powershell
cd "<本项目路径>\本地Skills功能分类库"
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -SkillName ai4scholar-research -Workspace "D:\你的项目路径"
```

如果只想预览会复制哪些 Skills：

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -Category 文献 -Workspace "D:\你的项目路径" -DryRun
```

如果已有旧版本，且你明确要覆盖：

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -SkillName pdf -Workspace "D:\你的项目路径" -ForceCopy
```

---

## 3. Skills 到底怎么部署

### 3.1 部署原理

一个 Skill 通常是这样的文件夹：

```text
skill-name
  SKILL.md
  scripts
  templates
  references
```

Agent 会读取 `SKILL.md`，判断什么时候触发这个 Skill，再按里面的流程做事。

### 3.2 推荐部署位置

| 工具 | 目标目录 |
|---|---|
| 本地分类库 | `<本项目路径>\本地Skills功能分类库` |
| 项目工作区默认复制位置 | `D:\你的项目路径\skills` |
| 项目自定义 Skills 目录 | 通过 `-DestinationRoot` 指定 |

### 3.3 复制脚本的作用

复制脚本会把：

```text
<本项目路径>\本地Skills功能分类库\各类Skills\skill-name
```

复制到：

```text
D:\你的项目路径\skills\skill-name
```

复制之后，项目工作区里就保留了本次任务需要的 Skills。

### 3.4 某些 Skills 还需要依赖

有些 Skills 自带脚本，可能需要 Python 包、Node 包、数据库、浏览器、API key 或第三方账号。新手不要自己猜，应该这样问 Agent：

```text
请读取 [项目路径]\skills\[skill-name]\SKILL.md。
告诉我这个 Skill 需要哪些依赖、是否需要 API key、如何安装、如何验证。
先不要执行安装，只给出步骤。
```

### 3.5 AMiner 和 AI4Scholar 的特殊性

AMiner 和 AI4Scholar 属于外部学术平台接入，不只是本地 Skill 文件。它们需要平台 Token 或 API Key，并且通常通过 MCP 或 OpenClaw 插件调用。

| 平台 | 更适合做什么 | 接入文件 |
|---|---|---|
| AMiner | 学者、机构、专利、专家发现、学术知识图谱 | `02_环境与部署/AMiner_MCP接入说明.md` |
| AI4Scholar | 真实文献检索、PDF 阅读、引用、自动加引用、科研绘图、Scholar Mode 项目工作流 | `02_环境与部署/AI4Scholar接入说明.md` |

这次已经把 AI4Scholar 飞书教程拆成 10 个专项 Skills。新手不用只复制一个总入口：做文献检索复制 `ai4scholar-paper-search`，做全文阅读复制 `ai4scholar-pdf-fulltext-reading`，做自动加引用复制 `ai4scholar-auto-citation-bibtex`，做科研图复制 `ai4scholar-sci-draw`，需要部署时复制 `ai4scholar-mcp-openclaw-setup`。

安全底线：

- 不要把 AMiner Token 或 AI4Scholar API Key 写进手册、论文或聊天记录。
- 配置里用环境变量或本机私有配置保存。
- 输出真实文献时仍要核验 DOI、作者、期刊和年份。

---

## 4. 完整 131 个 Skills 总览

### 4.1 核心文档处理 Skills

| Skill | 能做什么 | 新手常用场景 |
|---|---|---|
| `markitdown` | 把 PDF、DOCX、PPTX、XLSX、图片、音频、HTML、CSV、JSON 等转成 Markdown | 把课程资料和论文转成 Agent 容易阅读的文本 |
| `pdf` | 读取、抽取、合并、拆分、旋转、OCR、加密、表单处理 PDF | 读论文、抽表格、处理扫描版 PDF |
| `docx` | 创建、读取、编辑 Word 文档，处理目录、标题、页码、批注和修订 | 生成手册、论文草稿、报告和审稿意见 |
| `xlsx` | 读取、清洗、编辑、格式化 Excel/CSV/TSV，生成公式和图表 | 文献矩阵、数据清洗、统计表 |
| `pptx` | 创建、读取、编辑 PPT，处理模板、布局、备注和合并拆分 | 答辩 PPT、组会汇报、课程报告 |

### 4.2 文献检索、综述和引用 Skills

| Skill | 能做什么 | 新手常用场景 |
|---|---|---|
| `academic-research-hub` | 学术搜索、下载资料、抽取引用，覆盖多种学术数据库 | 找论文、整理参考文献 |
| `academic-research-openalex` | 用 OpenAlex 免费 API 搜索论文、作者、DOI、引用链和开放全文 | 不想配置 key 时做真实文献检索 |
| `aminer-mcp-research` | 使用 AMiner MCP 查询学者、机构、论文、专利和学术知识图谱 | 专家发现、学者画像、机构比较 |
| `ai4scholar-research` | 使用 AI4Scholar MCP 或 OpenClaw 插件做真实文献检索、PDF 阅读、引用和科研绘图 | 引用真实文献、自动加引用、读全文 |
| `ai4scholar-paper-search` | 调用 AI4Scholar 的 Semantic Scholar、PubMed、Google Scholar、arXiv、bioRxiv、medRxiv 搜索 | 多数据库真实文献检索 |
| `ai4scholar-paper-detail-batch` | 按 DOI、PMID、arXiv ID、Semantic Scholar ID 或标题核验单篇/批量文献元数据 | 清理参考文献、核验文献真伪 |
| `ai4scholar-citation-network` | 查 backward references、forward citations、PubMed related papers 和引用缺口 | 从种子文献扩展文献树 |
| `ai4scholar-author-intelligence` | 查作者、作者详情、作者论文、论文作者列表和专家画像 | 找学者、实验室、潜在审稿人 |
| `ai4scholar-paper-recommendation` | 基于一篇或多篇种子论文推荐相关论文 | 做阅读清单和领域扩展 |
| `ai4scholar-pdf-fulltext-reading` | 下载或读取 Semantic Scholar、arXiv、bioRxiv、medRxiv、DOI 全文 | 提取 Method、Data、Results |
| `ai4scholar-auto-citation-bibtex` | 用 `auto_cite` 给学术文本添加真实引用，返回参考文献和 BibTeX，并做句子级核验 | 给 Introduction/Related Work 加引用 |
| `literature-review` | 多数据库系统综述、研究综合、引用格式输出 | 写综述、做系统检索 |
| `literature-reviewer-skill` | 对论文做结构化综述和评价 | 快速拆解多篇论文 |
| `citation-management` | 核验 DOI、作者、期刊、年份，生成 BibTeX | 防止引用造假或格式错误 |
| `research-lookup` | 查询当前研究信息，辅助找论文和科学事实核验 | 需要实时或较新的研究信息时 |
| `research-superpower` | 系统化文献搜索、筛选、信息抽取和引用追踪 | 从选题到文献树 |
| `pdf-paper-summary` | 从 PDF 论文抽取标题、作者、单位、期刊、问题、方法和结论 | 批量读论文 |
| `paper-innovation-extractor` | 批量提取论文创新点和贡献 | 找 novelty、写贡献段 |
| `arxiv-watcher` | 搜索和总结 arXiv 最新论文 | 跟踪 AI、算法、HCI 等前沿 |
| `ssci-literature-review` | 按 SSCI 论文结构剖析摘要、引言、方法、结果和讨论 | 学 SSCI 写法和文献对话 |

### 4.3 CNKI 选题与中文文献 Skills

| Skill | 能做什么 | 新手常用场景 |
|---|---|---|
| `cnki-exp-search-automation` | 用浏览器自动化做 CNKI 高级搜索并获取结果信息 | 新手先看搜索结果和摘要 |
| `cnki-crawler-literature` | 抓取 CNKI 期刊论文元数据并保存到数据库 | 批量中文文献采集 |
| `cnki-crawler-topic` | 面向选题的 CNKI 元数据抓取 | 做中文选题扫描 |
| `cnki-rank` | CNKI 排名、热度或榜单类分析 | 找中文热点方向 |
| `cnki-trend` | 抓取关键词分组数据，生成年度趋势、学科、期刊、作者、机构分析 | 判断中文研究趋势 |
| `cnki-research-assistant` | 整合热榜、趋势、文献调研、期刊匹配和研究空白分析 | 做 C 刊/CSSCI 选题辅助 |

### 4.4 数据采集、整合与实证 Skills

| Skill | 能做什么 | 新手常用场景 |
|---|---|---|
| `empirical-analysis-skill-python` | 数据清洗、特征工程、Table 1、回归、DID、IV、DML、机器学习、稳健性、机制和异质性 | 管理学、经济学、心理行为数据的实证分析 |
| `multi-source-data-integration-extraction` | 合并 Excel/CSV，规范列名，从 PDF/HTML/TXT/Markdown 抽表格，支持 OCR | 多来源数据整理、年报表格抽取 |
| `research-data-auto-analysis-plotting` | 自动生成统计表、相关图、分组比较图和回归诊断图 | 快速 EDA 和论文图表 |
| `data-visualization-analysis` | CSV/Excel 统计描述、相关性分析、分布图、热力图 | 数据探索 |
| `data-viz-analyzer` | 生成交互式 HTML 数据分析报告 | 给导师或团队看数据概览 |
| `decision-tree-modeling` | 决策树分类、超参数优化、可视化树和建模报告 | 入门机器学习分类 |
| `tushare-finance` | 获取 A 股、港股、美股、基金、期货、债券和宏观数据 | 金融和管理科学数据 |

### 4.5 文本挖掘与 NLP Skills

| Skill | 能做什么 | 新手常用场景 |
|---|---|---|
| `text-analysis-basic` | PDF 文本抽取、中文分词、词频、词云、TF-IDF、Word2Vec、句向量、相似度 | 文本挖掘入门 |
| `topic-modeling` | LDA、动态主题模型、BERTopic、主题关键词和文档主题分布 | 研究热点和主题演化 |
| `sentiment-analysis` | 词典情感、机器学习情感分类、LLM 情感标注 | 评论、访谈、社媒文本情感 |
| `deep-learning-nlp` | 课程中的 DNN、RNN、GRU、CNN/LeNet 示例训练、评估和预测 | 深度学习入门实验 |
| `big-data-labeling-variable-construction` | LDA、sklearn、Transformer、LLM 标注和变量构造 | 把大规模文本转成可分析变量 |

### 4.6 论文写作、审稿和投稿 Skills

| Skill | 能做什么 | 新手常用场景 |
|---|---|---|
| `scientific-writing` | 按 IMRAD 写科学论文，支持引用、图表、报告规范 | 写引言、方法、结果、讨论 |
| `empirical-paper-writer` | 按实证论文结构生成框架和正文 | 金融、经济、管理类实证论文 |
| `paper-writing-assistant-typesetting` | 整合文献元数据、生成论文大纲、规范引用键、输出 LaTeX/Word/PDF 草稿 | 从文献到初稿 |
| `peer-review` | 方法、统计、设计、可重复性、伦理、图表完整性审稿 | 投稿前自查或审别人论文 |
| `scholar-evaluation` | 系统评价学术工作质量并给出评分和改进建议 | 判断论文是否够强 |
| `scientific-critical-thinking` | 评估研究严谨性、偏差、混杂、证据质量和因果解释 | 防止理论和方法站不住 |
| `hypothesis-generation` | 从观察生成可检验假设、预测、机制和实验设计 | 写假设和研究模型 |
| `research-proposal` | 写研究计划、项目申请和研究设计 | 开题、课题申请 |
| `research-grants` | 写 NSF、NIH、DOE、DARPA 等竞争性项目申请 | 英文基金申请训练 |
| `venue-templates` | 获取 Nature、Science、PLOS、IEEE、ACM、NeurIPS 等模板和投稿格式 | 投稿格式准备 |
| `doc-coauthoring` | 协作写文档、技术规范、提案和结构化内容 | 和 Agent 共同写长文档 |
| `academic-paper-composer` | 从详细大纲系统写完整学术论文 | 大纲已经定好后写正文 |
| `academic-paper-strategist` | 规划论文、找 gap、判断原创性、生成优化大纲 | 论文动笔前做战略设计 |

### 4.7 自动化、MCP、浏览器和 Agent Skills

| Skill | 能做什么 | 新手常用场景 |
|---|---|---|
| `skill-creator` | 创建、修改、评估和优化 Skills | 把你自己的科研流程封装成 Skill |
| `find-skills` | 查找、安装和发现可用 Skills | 不知道该用哪个 Skill 时 |
| `skillhub-preference` | 优先用 skillhub 查找、安装和更新 Skills | 扩展能力 |
| `mcp-builder` | 创建 MCP 服务器，让 Agent 调用外部 API 或服务 | 接入数据库、知识库、科研工具 |
| `ai4scholar-mcp-openclaw-setup` | 部署 AI4Scholar MCP 或 OpenClaw 插件，配置 API Key、重启 Gateway、处理 Windows 安装问题 | 第一次接入 AI4Scholar |
| `ai4scholar-scholar-mode-projects` | 使用 OpenClaw 插件的 Scholar Mode、`/library`、`/projects`、`/reading-list` | 管理论文项目和阅读清单 |
| `agent-browser` | 浏览器自动化、点击、填表、截图、网页数据抽取和 Web 测试 | 采集公开网页信息或检查网页 |
| `web-browsing` | 浏览网站、读取 URL、联网搜索和网页总结 | 获取当前信息 |
| `webapp-testing` | 用 Playwright 测试本地 Web app、截图、看日志 | 检查自己做的网页工具 |
| `self-improving-agent` | 记录错误、修正和经验，改进后续行为 | 建立长期科研 Agent 习惯 |
| `parallel-web` | Web 搜索、网页抽取和深度研究，带引用综合 | 多来源网络调研 |
| `tavily-search` | Tavily API 搜索，作为网页搜索替代方案 | 需要搜索链接和摘要 |
| `claude-api` | Claude API、Anthropic SDK 和 Agent SDK 开发 | 做 Claude 相关应用 |

### 4.8 图表、PPT、海报与可视化 Skills

| Skill | 能做什么 | 新手常用场景 |
|---|---|---|
| `scientific-schematics` | 生成神经网络、流程图、机制图和科学示意图 | 理论模型图、实验流程图 |
| `ai4scholar-sci-draw` | 使用 AI4Scholar `sci_draw` 做科研图、图片编辑、风格转换、多图组合、图像评审和 SVG 风格输出 | EEG/BCI 流程图、机制图、图形摘要 |
| `scientific-slides` | 生成科研汇报、会议、答辩 slides | 组会、会议、答辩 |
| `paper-slide-deck` | 从论文生成专业 slide deck 图片 | 读完论文后做汇报 |
| `latex-posters` | 用 LaTeX 制作学术 poster | 会议海报 |
| `pptx-posters` | 制作 PPTX 风格 poster | 需要可编辑海报时 |
| `paper-2-web` | 把论文转成网页、视频摘要和 poster | 论文传播和展示 |
| `generate-image` | 生成或编辑通用图片、插图、视觉资产 | 非技术图像素材 |
| `infographics` | 生成信息图，支持研究数据和网页资料整合 | 把复杂结果做成图解 |

### 4.9 情景实验与行为研究 Skills

这 4 个 Skill 是为管理学、营销、信息系统、应用心理学和消费者心理学中的情景实验专门新增的。目标不是给你一个普通问卷模板，而是把 UTD24、FT50、AJG/ABS4 等顶刊语境下常见的“理论机制 + 干净操纵 + 预实验 + 主实验 + 机制/边界分析 + 透明汇报”流程做成可执行模块。

| Skill | 能做什么 | 新手常用场景 |
|---|---|---|
| `scenario-experiment-benchmark-mining` | 从真实顶刊论文中抽取情景实验范式，建立论文-实验矩阵 | 学 JCR、JCP、JM、JAP、ISR、JPSP 等期刊的设计套路 |
| `scenario-experiment-design` | 设计情景/ vignette 实验：条件、刺激、操纵检验、真实感检验、混淆检验、预实验和主实验 | 把研究问题转成可随机分配的实验 |
| `scenario-experiment-analysis` | 分析情景实验数据：排除、随机化、操纵检验、信度、主效应、交互、中介、调节和稳健性 | 从 CSV 到结果表 |
| `scenario-experiment-reporting` | 写 Method、Results、表格、图、附录和透明性说明 | 把结果写成顶刊可审查的表达 |

情景实验模块最适合这些问题：

- AI agent、算法、自动化、解释性、拟人化、信任、采纳、责任归因。
- 消费者判断、购买意愿、品牌关系、服务失败、道德判断。
- 组织管理、领导、员工决策、绩效评价、公平感和心理安全。
- 信息系统、人机交互、平台治理、推荐系统和数字服务。

使用底线：

- 不编造“顶刊范文”。所有论文标题、DOI、期刊、年份都要真实核验。
- 不把问卷相关研究包装成实验。必须有随机分配或明确操纵。
- 不把操纵检验当作假设检验。
- 不把一次在线情景实验过度解释为真实现场行为。

### 4.10 期刊论文排版与投稿格式 Skills

这 10 个 Skill 负责把稿件从“内容完成”推进到“可投稿格式”。核心原则是只做结构、句法、格式和合规审计，不改动原始学术数据。

| Skill | 能做什么 | 新手常用场景 |
|---|---|---|
| `journal-title-page-metadata` | 扉页、作者、机构、通讯作者和基金声明格式化 | 投稿前整理 title page |
| `journal-abstract-keywords` | 摘要字数、结构式摘要、关键词格式和排序 | 对齐 APA 或期刊要求 |
| `journal-heading-hierarchy` | 标题层级、编号、加粗/斜体/居中等格式转换 | 把论文结构改成目标期刊样式 |
| `journal-intext-citation-style` | 正文引用格式转换和引用-参考文献匹配审计 | 数字制转作者-年份制 |
| `journal-reference-list-format` | 参考文献标点、大小写、排序、DOI 和缺失项审计 | APA 7 或期刊参考文献 |
| `journal-table-figure-caption` | 图表编号、标题、注释和正文 callout 审计 | 表格标题和 Figure caption |
| `journal-statistics-units-style` | 统计符号、p 值、CI、效应量、单位格式 | Results 最容易出错的细节 |
| `journal-layout-spacing` | 页边距、行距、缩进、块引用、页面元素 | Word/PDF 最终格式 |
| `journal-footnote-endnote` | 脚注/尾注转换和编号链接审计 | 期刊要求 endnotes 时 |
| `journal-blind-review-anonymizer` | 双盲匿名化、自引、致谢、文件元数据审计 | 投稿前生成 blinded manuscript |

### 4.11 EEG / ERP 神经科学实验 Skills

这 6 个 Skill 面向认知神经科学、神经营销、脑机接口和 HCI 脑电研究。

| Skill | 能做什么 | 新手常用场景 |
|---|---|---|
| `eeg-experiment-planning` | EEG/ERP 实验设计、事件码、试次数、采样率和预注册计划 | 实验开始前 |
| `eeg-preprocessing-pipeline` | 滤波、重参考、坏道、ICA、伪迹剔除、QC 报告 | 原始脑电清洗 |
| `erp-segmentation-analysis` | 分段、基线校正、ERP 成分窗口、ROI、电极和统计 | P300、N2、LPP 等 |
| `eeg-frequency-connectivity` | 频域、时频、ERSP、功率、相位、连接分析 | alpha/theta 或功能连接 |
| `eeg-ml-classification` | EEG 特征、CSP、深度学习分类、交叉验证和泄漏审计 | BCI 或神经营销分类 |
| `eeg-results-writing-figures` | EEG 方法、结果、波形图、头皮图、时频图和审稿风险 | 写脑电论文 |

### 4.12 量表开发与心理测量 Skills

这 5 个 Skill 解决问卷和情景实验最容易被审稿人追问的测量问题。

| Skill | 能做什么 | 新手常用场景 |
|---|---|---|
| `scale-selection-adaptation` | 量表选择、来源核验、翻译回译、文化改编和条目表 | 设计问卷前 |
| `scale-reliability-validity` | alpha、omega、CR、AVE、HTMT、区分效度和条目审计 | 收完数据后 |
| `efa-cfa-measurement-model` | EFA、CFA、载荷、拟合指标、替代模型 | 验证量表结构 |
| `common-method-bias-invariance` | 共同方法偏差、程序控制、CFA common factor、测量不变性 | 自陈问卷和跨组比较 |
| `questionnaire-reporting-template` | Measures、CFA、信效度、附录条目和审稿回复 | 写方法和结果 |

### 4.13 高级统计机制与因果推断 Skills

这 6 个 Skill 用来处理机制、边界、多层数据和准实验因果推断，重点是防止把相关关系写成因果关系。

| Skill | 能做什么 | 新手常用场景 |
|---|---|---|
| `process-mediation-moderation` | 中介、调节、调节中介、simple slopes、Johnson-Neyman | PROCESS 风格机制检验 |
| `sem-cfa-path-latent` | SEM、CFA、path analysis、潜变量中介和模型比较 | 多构念理论模型 |
| `multilevel-longitudinal-modeling` | 多层模型、混合效应、日记法、纵向模型、跨层交互 | 嵌套或重复测量数据 |
| `causal-inference-design-audit` | DAG、混杂、识别假设、bad controls、因果表述边界 | 写因果声明前 |
| `did-psm-iv-rdd-dml-event-study` | DID、event study、PSM、IV、RDD、DML 和稳健性 | 管理/IS 准实验 |
| `statistical-results-tables` | 回归表、机制表、稳健性表、效应量和结果解释 | 论文 Results 表格 |

### 4.14 BCI 脑电智能建模 Skills

这 10 个 Skill 独立于普通 EEG/ERP 模块，专门处理脑机接口、脑电分类、深度学习、跨被试泛化和在线解码。核心风险是数据泄漏、评价拆分错误、跨被试泛化失败和深度模型解释过度。

| Skill | 能做什么 | 新手常用场景 |
|---|---|---|
| `bci-data-structure` | 规范 subject/session/run/trial/window、标签、元数据和 split 单位 | 建模前整理数据 |
| `eeg-feature-engineering-bci` | band power、PSD、ERP、CSP、FBCSP、Riemannian、连接特征 | 从 EEG 到特征矩阵 |
| `eeg-ml-classical-bci` | LDA、SVM、RF、XGBoost、CSP+LDA、Riemannian 分类器 | 传统 BCI 基线 |
| `eeg-deep-learning-bci` | EEGNet、DeepConvNet、ShallowConvNet、CNN-LSTM、TCN、Transformer | 脑电深度学习 |
| `eeg-cross-subject-transfer-bci` | leave-one-subject-out、domain adaptation、迁移学习、few-shot calibration | 跨被试泛化 |
| `eeg-model-evaluation-leakage` | 数据泄漏审计、nested CV、permutation test、subject-wise metrics | 判断准确率是否可信 |
| `bci-online-decoding` | 滑窗预测、实时延迟、反馈、阈值、pseudo-online/online 区分 | 在线 BCI |
| `eeg-model-interpretability-bci` | saliency、spatial pattern、频段重要性、SHAP、解释边界 | 深度模型解释 |
| `bci-benchmark-datasets` | BCI Competition、MOABB、PhysioNet、OpenNeuro 等公开数据集选择 | 找公开数据 |
| `bci-results-reporting` | accuracy、balanced accuracy、AUC、F1、混淆矩阵、subject-wise table、ITR | 写 BCI 结果 |

使用底线：

- 不能用 trial-level random split 冒充 cross-subject decoding。
- 不能把同一个 trial 的滑窗同时放进训练集和测试集。
- 不能在全数据上做标准化、CSP、PCA、特征选择后再交叉验证。
- 不能只报告最佳 seed 或最佳 fold。
- 离线、伪在线和真实在线结果必须分开写。

### 4.15 科研项目管理与版本控制 Skills

这 7 个 Skill 是整个部署包的总控层。它不替代文献、实验、数据分析或写作模块，而是让每个课题长期有状态、有日志、有版本、有数据血缘和投稿记录。

| Skill | 能做什么 | 新手常用场景 |
|---|---|---|
| `project-initializer` | 创建标准科研项目骨架、AGENTS.md、dashboard、日志和追踪表 | 新开一个课题 |
| `project-dashboard` | 维护 project_status.md，汇总当前进度、阻塞点和下一步 | 每次开始工作 |
| `research-log` | 记录每次科研工作、决策、输出文件、可靠结论和待核验项 | 每次任务结束 |
| `data-lineage-tracker` | 记录 raw 到 processed 到 analysis 到 output 的数据血缘 | 数据清洗和分析后 |
| `manuscript-version-manager` | 管理论文 v1/v2/v3，记录每版改了什么 | 写作和修改论文 |
| `submission-revision-tracker` | 管理投稿期刊、状态、审稿意见、返修任务和 response letter | 投稿和返修 |
| `weekly-research-planner` | 生成每周计划、复盘、导师问题和优先级 | 每周科研管理 |

使用底线：

- 不覆盖 raw 数据。
- 不把未完成任务标成完成。
- 不把未核验结论写成事实。
- 每次重要分析、删样本、改模型、改论文版本都要留下日志。

### 4.16 Zotero / Obsidian 长期知识库 Skills

这 5 个 Skill 用来防止资料越积越乱。Zotero 负责保存真实文献和附件，Obsidian 负责保存你自己的理解、论文卡片、理论机制、变量方法矩阵、研究问题图谱和可复用启发。

| Skill | 能做什么 | 新手常用场景 |
|---|---|---|
| `zotero-library-sync` | 同步和审计 Zotero 文献库，导出文献索引、BibTeX、缺失 DOI/PDF/标签问题 | 把散乱文献先归档 |
| `obsidian-paper-card` | 把单篇论文转成 Obsidian 论文卡片，含 YAML、理论、变量、方法、结果和可复用点 | 每读一篇论文后沉淀 |
| `theory-variable-method-matrix` | 建立理论-变量-方法矩阵，连接理论机制、构念、测量、样本、模型和结论 | 写综述、假设和方法前 |
| `research-question-knowledge-graph` | 建立研究问题知识图谱，输出节点、关系、Obsidian 链接和 Mermaid 图 | 找研究空白和文献树 |
| `paper-reusable-insight-bank` | 提取每篇论文可复用启发：理论机制、量表、刺激材料、模型、图表、审稿风险 | 长期积累选题和写作素材 |

推荐配合：

- 用 Zotero 管理 PDF、元数据和 BibTeX。
- 用 Obsidian 管理论文卡片、理论卡片、变量卡片和项目卡片。
- 每篇论文至少沉淀一个 Obsidian 论文卡片和 1-3 条可复用启发。
- 每个真实课题维护一个理论-变量-方法矩阵和一个研究问题知识图谱。

---

## 5. 新手最常用的 21 个完整科研工作流

### 工作流 1：读一篇 PDF 论文

需要 Skills：

```text
pdf
markitdown
pdf-paper-summary
paper-innovation-extractor
citation-management
```

输入：

```text
literature/pdfs/某篇论文.pdf
```

提示词：

```text
请读取 literature/pdfs 里的 PDF 论文。
先判断应该使用哪些 Skills。
输出结构化论文卡片：研究问题、理论机制、数据、方法、核心发现、创新点、局限、可借鉴之处。
引用信息必须核验 DOI、作者、期刊和年份，不确定就标注“需人工核验”。
结果写入 output/paper_cards。
```

人工核验：

- DOI 是否真实。
- 方法描述是否和原文一致。
- 贡献是否被夸大。
- 相关关系是否被误写为因果关系。

### 工作流 2：建立文献矩阵

需要 Skills：

```text
academic-research-openalex
aminer-mcp-research
ai4scholar-research
literature-review
citation-management
xlsx
```

输出列建议：

| 列名 | 说明 |
|---|---|
| `paper_id` | 自定义编号 |
| `title` | 标题 |
| `authors` | 作者 |
| `year` | 年份 |
| `journal` | 期刊 |
| `doi` | DOI |
| `theory` | 理论 |
| `constructs` | 核心变量 |
| `method` | 方法 |
| `data` | 数据 |
| `finding` | 主要发现 |
| `gap` | 可延伸空白 |

提示词：

```text
请围绕“AI Agent 与科研创造力”建立文献矩阵。
优先检索近五年高质量英文文献，同时保留经典文献。
不要编造引用。每条文献必须给出 DOI 或可核验链接。
输出 Excel 文件和 Markdown 总结。
```

### 工作流 3：写系统综述

需要 Skills：

```text
academic-research-openalex
literature-review
research-superpower
citation-management
scientific-writing
```

流程：

1. 定义检索式。
2. 检索英文和中文数据库。
3. 去重。
4. 标题和摘要筛选。
5. 全文筛选。
6. 建立证据表。
7. 按主题写综述。
8. 核验引用。

提示词：

```text
请围绕[主题]设计系统综述流程。
先输出检索式、数据库、纳入排除标准和筛选表字段。
不要直接写结论。先让我确认检索策略。
```

### 工作流 4：做 CNKI 中文选题扫描

需要 Skills：

```text
cnki-exp-search-automation
cnki-crawler-topic
cnki-rank
cnki-trend
cnki-research-assistant
```

提示词：

```text
请围绕“生成式人工智能 知识工作”做 CNKI 中文选题扫描。
输出年度趋势、期刊分布、关键词聚类、作者机构分布、可能的 C 刊选题空白。
不要把热度直接等同于选题价值，要说明理论缺口和方法缺口。
```

注意：

- CNKI 相关操作可能遇到登录、验证码或访问限制。
- 不要让 Agent 绕过网站限制。
- 可先做公开结果页分析，再决定是否深度抓取。

### 工作流 5：整合多来源数据

需要 Skills：

```text
multi-source-data-integration-extraction
xlsx
pdf
markitdown
```

适合：

- 多个 Excel 合并。
- 年报表格抽取。
- 政策文件表格抽取。
- PDF 表格转 CSV。

提示词：

```text
请检查 data/raw 目录下的 Excel、CSV 和 PDF。
先列出每个文件的字段、行数、可能的主键和质量问题。
再提出合并方案，不要直接覆盖原始文件。
合并结果写入 data/processed。
```

### 工作流 6：做完整实证分析

需要 Skills：

```text
empirical-analysis-skill-python
research-data-auto-analysis-plotting
data-visualization-analysis
xlsx
scientific-critical-thinking
```

标准步骤：

1. 读取数据字典。
2. 检查缺失、异常值、重复值。
3. 构造变量。
4. 生成描述统计和相关矩阵。
5. 建立基准模型。
6. 做稳健性检验。
7. 做机制分析。
8. 做异质性分析。
9. 输出表格和图。
10. 写结果解释。

提示词：

```text
请对 data/processed/main.csv 做完整实证分析。
先读取变量说明，再判断适合 OLS、面板、DID、IV、DML 还是机器学习。
不要把相关性写成因果。
所有表格写入 output/tables，所有图写入 output/figures，解释写入 output/report.md。
```

### 工作流 7：做文本挖掘

需要 Skills：

```text
text-analysis-basic
topic-modeling
sentiment-analysis
big-data-labeling-variable-construction
xlsx
```

标准步骤：

1. 检查文本列。
2. 清洗空值、重复、异常字符。
3. 中文分词。
4. 停用词处理。
5. 词频和 TF-IDF。
6. 主题模型。
7. 情感分析。
8. 把文本指标回写成变量。

提示词：

```text
请对 data/raw/texts.csv 的 text 列做文本挖掘。
先检查样本量、语言、空值和重复文本。
输出词频、TF-IDF、主题模型可行性、情感分数和可用于实证模型的变量。
如果样本量不适合主题模型，请直接说明。
```

### 工作流 8：写论文引言

需要 Skills：

```text
scientific-writing
ssci-literature-review
hypothesis-generation
scientific-critical-thinking
citation-management
```

提示词：

```text
请基于我的文献矩阵和研究设计，写 SSCI 风格 Introduction。
要求：问题意识清楚，理论机制具体，贡献不过度夸大。
不要堆砌文献，不要编造引用。
先给出段落功能结构，再写正文。
```

合格引言必须回答：

- 研究对象为什么重要。
- 现有文献到底缺什么。
- 你的研究为什么能补这个缺口。
- 理论机制是什么。
- 方法为什么能识别这个问题。
- 贡献边界在哪里。

### 工作流 9：审稿式自查

需要 Skills：

```text
peer-review
scholar-evaluation
scientific-critical-thinking
venue-templates
```

提示词：

```text
请以匿名审稿人的标准检查 manuscript/draft.docx。
优先找致命问题：贡献不足、理论错位、方法不匹配、识别不成立、引用不可核验、结果解释过度。
按严重程度排序，每条给出修改建议。
不要只做语言润色。
```

### 工作流 10：生成 PPT 或答辩材料

需要 Skills：

```text
pptx
scientific-slides
paper-slide-deck
scientific-schematics
```

提示词：

```text
请基于 manuscript/draft.md 生成 15 页组会汇报 PPT 大纲。
每页包括标题、核心信息、图表建议和讲稿提示。
优先突出研究问题、理论机制、方法、结果和贡献边界。
```

### 工作流 11：做浏览器自动化或网页采集

需要 Skills：

```text
agent-browser
web-browsing
parallel-web
tavily-search
webapp-testing
```

提示词：

```text
请打开[网址]，先截图并读取页面结构。
只采集公开可见信息，不登录、不绕过验证、不提交表单。
先告诉我可以合法采集哪些字段，再等我确认。
```

### 工作流 12：创建自己的 Skill

需要 Skills：

```text
skill-creator
find-skills
self-improving-agent
mcp-builder
```

适合封装的任务：

- 你每周都要做的文献检索流程。
- 固定格式的论文拆解表。
- 固定格式的数据清洗和回归流程。
- 你自己的 EEG、ERP、文本挖掘、CNKI 选题流程。

提示词：

```text
请帮我把下面这个重复科研流程封装成 Skill。
先问我输入、输出、依赖、禁止事项和质量标准。
然后创建 SKILL.md 和必要脚本。
不要覆盖已有 Skills。
```

### 工作流 13：接入 AMiner 和 AI4Scholar 做真实学术平台检索

需要 Skills：

```text
aminer-mcp-research
ai4scholar-research
ai4scholar-paper-search
ai4scholar-paper-detail-batch
ai4scholar-citation-network
ai4scholar-author-intelligence
ai4scholar-paper-recommendation
ai4scholar-pdf-fulltext-reading
ai4scholar-auto-citation-bibtex
academic-research-openalex
citation-management
literature-review
scientific-writing
```

适合：

- 查某位学者的真实身份、机构、方向、论文和专利。
- 找某个研究方向的专家和团队。
- 用 AI4Scholar 搜索真实论文并读取开放获取全文。
- 用 `auto_cite` 给学术文本添加真实引用。
- 用 AI4Scholar 的引用网络、作者工具和推荐工具扩展文献树。
- 用 AI4Scholar 的论文详情/批量详情工具核验 DOI、PMID、arXiv ID 和文献元数据。
- 把 AMiner、AI4Scholar、OpenAlex、CNKI 的结果交叉核验。

提示词：

```text
请使用 AMiner 和 AI4Scholar 帮我围绕“AI Agent 与科研创造力”做真实学术平台检索。
AMiner 负责专家、机构、代表作和知识图谱线索。
AI4Scholar 负责真实论文检索、论文详情、引用网络、作者信息、论文推荐、PDF 或摘要信息。
再用 OpenAlex 或 citation-management 交叉核验关键文献。
输出：检索式、学者/机构线索、核心论文、可核验证据、待人工核验项和下一步阅读清单。
不要暴露 API Key 或 Token。
```

注意：

- AMiner 更强在学者、机构、专利和知识图谱。
- AI4Scholar 更强在真实论文检索、论文详情、PDF 阅读、引用网络、作者工具、论文推荐、自动加引用和科研绘图。
- 自动加引用不能替代人工判断，每条引用都要看是否真正支持对应句子。

### 工作流 14：做顶刊风格情景实验

需要 Skills：

```text
scenario-experiment-benchmark-mining
scenario-experiment-design
scenario-experiment-analysis
scenario-experiment-reporting
citation-management
scientific-critical-thinking
```

适合：

- 从 JCR、JCP、JM、JAP、ISR、MISQ、OBHDP、JPSP、Psychological Science 等期刊中学习情景实验范式。
- 为 AI agent、算法决策、消费者心理、组织行为、信息系统采纳等主题设计实验。
- 生成刺激材料、操纵检验、真实感检验、混淆检验、预实验和主实验方案。
- 分析实验数据并写 Method、Results、表格、图和附录。

标准流程：

1. 用 `scenario-experiment-benchmark-mining` 找真实论文并建立范式矩阵。
2. 用 `scenario-experiment-design` 把研究问题转成因果模型和刺激材料。
3. 先做 pretest，检查操纵强度、真实感和混淆变量。
4. 主实验前写清排除规则、样本量、随机分配、主要 DV 和分析模型。
5. 用 `scenario-experiment-analysis` 跑操纵检验、信度、主效应、交互、中介、调节和稳健性。
6. 用 `scenario-experiment-reporting` 写成顶刊可审查的结果汇报。

提示词：

```text
请帮我围绕“AI agent 解释性如何影响用户信任和采纳意愿”构建一个顶刊风格情景实验包。
第一步：用 scenario-experiment-benchmark-mining 检索并核验 JCR/JCP/JM/JAP/ISR/MISQ 中相近主题的真实情景实验论文，输出范式矩阵。
第二步：用 scenario-experiment-design 设计 2 x 2 或中介/调节实验，给出刺激材料、操纵检验、真实感检验、混淆检验、预实验和主实验方案。
第三步：给出 scenario-experiment-analysis 的数据列名、模型公式、效应量和稳健性分析计划。
第四步：用 scenario-experiment-reporting 给出 Method/Results 模板、表格和附录清单。
不要编造引用；无法核验的论文只放入待核验列表。
```

最低输出标准：

- 一张真实论文范式矩阵。
- 一套可直接放进问卷平台的情景刺激文本。
- 一套操纵检验、真实感检验、混淆检验和主要测量条目。
- 一份预实验和主实验执行计划。
- 一份 CSV 数据列名模板和分析模型清单。
- 一份 Method/Results 写作模板。

### 工作流 15：把论文改成目标期刊格式

需要 Skills：

```text
journal-title-page-metadata
journal-abstract-keywords
journal-heading-hierarchy
journal-intext-citation-style
journal-reference-list-format
journal-table-figure-caption
journal-statistics-units-style
journal-layout-spacing
journal-footnote-endnote
journal-blind-review-anonymizer
```

提示词：

```text
请把我的稿件按[目标期刊/APA第7版]做格式转换。
只做排版、引用、参考文献、图表标题、统计格式、布局和盲审匿名化审计。
绝对不要改动任何数值、统计结果、作者姓名拼写、机构名称和原始数据。
输出：格式修改清单、需要人工确认的问题、盲审风险和最终投稿前 checklist。
```

### 工作流 16：完成 EEG/ERP 神经科学实验流程

需要 Skills：

```text
eeg-experiment-planning
eeg-preprocessing-pipeline
erp-segmentation-analysis
eeg-frequency-connectivity
eeg-ml-classification
eeg-results-writing-figures
```

提示词：

```text
请围绕[研究问题]设计 EEG/ERP 研究流程。
先给实验范式、事件码、试次数、采样率、预处理、ERP/频域/连接/机器学习分析计划。
再给预处理 QC 表、结果图表计划和 Methods/Results 写作模板。
不要覆盖 raw EEG 数据，不要把探索性时间窗写成验证性结果。
```

### 工作流 17：完成量表开发与心理测量

需要 Skills：

```text
scale-selection-adaptation
scale-reliability-validity
efa-cfa-measurement-model
common-method-bias-invariance
questionnaire-reporting-template
```

提示词：

```text
请围绕我的研究变量建立测量方案。
先核验真实量表来源，再给翻译回译、预测试、信度、效度、EFA/CFA、共同方法偏差和测量不变性计划。
输出：构念-条目表、数据列名、分析步骤、报告模板和审稿风险。
不要编造量表来源，不要为了提高 alpha 随意删题。
```

### 工作流 18：做高级统计、机制和因果推断审计

需要 Skills：

```text
process-mediation-moderation
sem-cfa-path-latent
multilevel-longitudinal-modeling
causal-inference-design-audit
did-psm-iv-rdd-dml-event-study
statistical-results-tables
```

提示词：

```text
请检查我的研究设计和数据能否支持因果、机制或边界条件结论。
根据变量、时间顺序、处理组、对照组、层级结构和识别假设，判断应该用中介调节、SEM、多层模型、DID、PSM、IV、RDD、DML 还是只做相关分析。
输出：可支持的结论、不能说的结论、模型公式、稳健性、结果表结构和 Results 写法。
不要用稳健性替代识别策略，不要把相关关系写成因果关系。
```

### 工作流 19：做 BCI 脑电智能建模

需要 Skills：

```text
bci-data-structure
eeg-feature-engineering-bci
eeg-ml-classical-bci
eeg-deep-learning-bci
eeg-cross-subject-transfer-bci
eeg-model-evaluation-leakage
bci-online-decoding
eeg-model-interpretability-bci
bci-benchmark-datasets
bci-results-reporting
```

提示词：

```text
请围绕[BCI任务，例如运动想象/情绪识别/P300/SSVEP/工作负荷识别]构建脑电智能建模流程。
先用 bci-data-structure 规范 subject、session、trial、window、label 和 split 单位。
再用 eeg-feature-engineering-bci 设计特征，用 eeg-ml-classical-bci 建传统基线，用 eeg-deep-learning-bci 设计深度模型。
必须用 eeg-model-evaluation-leakage 审计数据泄漏，明确是 within-subject、cross-session 还是 cross-subject。
如果涉及跨被试泛化，用 eeg-cross-subject-transfer-bci；如果涉及在线系统，用 bci-online-decoding。
最后用 bci-results-reporting 输出 subject-wise table、balanced accuracy、AUC/F1、混淆矩阵、置信区间和论文 Results 模板。
不要把 trial-level random split 写成跨被试泛化，不要在全数据上做标准化或特征选择后再交叉验证。
```

### 工作流 20：管理长期科研项目和论文版本

需要 Skills：

```text
project-initializer
project-dashboard
research-log
data-lineage-tracker
manuscript-version-manager
submission-revision-tracker
weekly-research-planner
```

提示词：

```text
请为我的课题“AI agent 解释性与用户信任”建立长期科研项目管理结构。
先用 project-initializer 创建标准目录、AGENTS.md、project_status.md、research_log.md、data_lineage.csv、manuscript_versions.md 和 submission_tracker.csv。
之后每次开始工作时，用 project-dashboard 读取当前状态并给出下一步 3 个优先任务。
每次任务结束后，用 research-log 记录做了什么、生成了哪些文件、哪些结论可靠、哪些还需要核验。
如果处理数据，用 data-lineage-tracker 记录 raw -> processed -> output。
如果修改论文，用 manuscript-version-manager 记录版本变化。
如果投稿或返修，用 submission-revision-tracker 管理期刊、审稿意见和 response letter 任务表。
不要覆盖 raw 数据，不要把未完成任务标成完成。
```

### 工作流 21：建立 Zotero / Obsidian 长期知识库

需要 Skills：

```text
zotero-library-sync
obsidian-paper-card
theory-variable-method-matrix
research-question-knowledge-graph
paper-reusable-insight-bank
citation-management
```

适合：

- Zotero 文献库已经有很多论文，但标签、PDF、DOI 和集合很乱。
- 想把每篇论文沉淀成 Obsidian 卡片，而不是读完就忘。
- 想长期积累理论、变量、方法、量表、实验设计和可复用启发。
- 想把研究问题、文献、理论、变量和方法连成知识图谱。

提示词：

```text
请帮我建立 Zotero / Obsidian 长期科研知识库。
第一步：用 zotero-library-sync 审计 Zotero 文献库，输出缺失 DOI、缺失 PDF、重复文献、未分类文献和推荐标签体系。
第二步：用 obsidian-paper-card 为核心论文生成 Obsidian 论文卡片模板，包含 YAML、研究问题、理论机制、变量、方法、数据、结果、局限和可复用点。
第三步：用 theory-variable-method-matrix 建立理论-变量-方法矩阵，区分理论构念、测量变量、方法设计和分析模型。
第四步：用 research-question-knowledge-graph 建立研究问题知识图谱，输出节点、关系和 Mermaid 图。
第五步：用 paper-reusable-insight-bank 提取每篇论文的可复用启发，并标注来源、可迁移方式和风险。
所有引用必须保留 Zotero key、DOI 或待核验状态，不要编造文献。
```

最低输出标准：

- 一个 Zotero 文献库审计表。
- 一套 Obsidian 论文卡片模板。
- 一个理论-变量-方法矩阵。
- 一个研究问题知识图谱。
- 一个论文启发库。

---

## 6. 完整功能学习顺序

### 第 1 周：基础和文档

目标：

- 会进目录。
- 会运行脚本。
- 会按需复制 Skills。
- 会读 PDF、Word、Excel。

必学 Skills：

```text
markitdown
pdf
docx
xlsx
pptx
pdf-paper-summary
```

练习：

1. 把一篇 PDF 论文转成 Markdown。
2. 生成一张论文卡片。
3. 建一个 Excel 文献矩阵。
4. 把结果写入 Word。

### 第 2 周：文献、综述和选题

目标：

- 会找真实文献。
- 会核验引用。
- 会建立文献树。
- 会做中文选题扫描。

必学 Skills：

```text
academic-research-openalex
literature-review
citation-management
research-superpower
ssci-literature-review
cnki-research-assistant
cnki-trend
```

练习：

1. 围绕一个主题找 30 篇文献。
2. 建立文献矩阵。
3. 生成研究 gap 表。
4. 用 CNKI 看中文趋势。
5. 用 AMiner 查专家和机构。
6. 用 AI4Scholar 检索真实论文并核验引用。

### 第 3 周：数据、实证和文本挖掘

目标：

- 会整理数据。
- 会做描述统计和图。
- 会选择基本模型。
- 会把文本变成变量。

必学 Skills：

```text
multi-source-data-integration-extraction
empirical-analysis-skill-python
research-data-auto-analysis-plotting
text-analysis-basic
topic-modeling
sentiment-analysis
big-data-labeling-variable-construction
```

练习：

1. 合并多个 CSV。
2. 输出 Table 1。
3. 跑一个基准回归。
4. 对文本做 TF-IDF 和情感分析。

### 第 4 周：情景实验与行为研究

目标：

- 会从真实顶刊论文中抽取实验范式。
- 会把研究问题转成情景实验因果模型。
- 会写刺激材料、操纵检验、真实感检验和混淆检验。
- 会做主效应、交互、中介、调节和结果汇报。

必学 Skills：

```text
scenario-experiment-benchmark-mining
scenario-experiment-design
scenario-experiment-analysis
scenario-experiment-reporting
scientific-critical-thinking
citation-management
```

练习：

1. 围绕一个 AI agent 或消费者心理主题找 8-12 篇真实情景实验论文。
2. 建立顶刊范式矩阵。
3. 设计一个 2 x 2 或中介/调节情景实验。
4. 写预实验和主实验方案。
5. 用模拟数据跑一遍分析并写 Method/Results。

### 第 5 周：量表、心理测量和高级统计

目标：

- 会选择真实可核验量表。
- 会做信度、效度、EFA/CFA、共同方法偏差和测量不变性。
- 会判断中介、调节、SEM、多层模型和因果推断是否适用。

必学 Skills：

```text
scale-selection-adaptation
scale-reliability-validity
efa-cfa-measurement-model
common-method-bias-invariance
process-mediation-moderation
causal-inference-design-audit
statistical-results-tables
```

练习：

1. 为一个情景实验选择 3 个真实量表。
2. 建立构念-条目-codebook。
3. 用模拟数据写信效度和 CFA 报告模板。
4. 判断一个机制模型能否支持因果语言。

### 第 6 周：EEG/ERP 和神经科学实验

目标：

- 会规划 EEG/ERP 实验范式和事件码。
- 会写预处理、ERP、频域、连接和机器学习分析计划。
- 会写脑电论文的 Methods、Results 和图表清单。

必学 Skills：

```text
eeg-experiment-planning
eeg-preprocessing-pipeline
erp-segmentation-analysis
eeg-frequency-connectivity
eeg-ml-classification
eeg-results-writing-figures
```

练习：

1. 为一个神经营销或 HCI 主题设计 ERP 实验。
2. 写事件码和 trial 结构。
3. 设计预处理 QC 表。
4. 写 ERP 波形图、头皮图和时频图计划。

### 第 7 周：BCI 脑电智能建模

目标：

- 会整理 BCI 数据结构和标签。
- 会做传统机器学习和深度学习建模计划。
- 会做跨被试泛化和防泄漏评估。
- 会区分离线、伪在线和在线 BCI。

必学 Skills：

```text
bci-data-structure
eeg-feature-engineering-bci
eeg-ml-classical-bci
eeg-deep-learning-bci
eeg-model-evaluation-leakage
bci-results-reporting
```

练习：

1. 建立 subject-session-trial-window 元数据表。
2. 设计 CSP/FBCSP 或 band power 特征。
3. 比较 LDA/SVM 和 EEGNet/DeepConvNet 的建模路线。
4. 写一份防泄漏审计和 subject-wise 结果表模板。

### 第 8 周：论文排版、投稿格式和盲审

目标：

- 会按目标期刊格式检查稿件。
- 会处理引用、参考文献、图表、统计格式、脚注尾注。
- 会生成双盲投稿版本。

必学 Skills：

```text
journal-title-page-metadata
journal-abstract-keywords
journal-intext-citation-style
journal-reference-list-format
journal-table-figure-caption
journal-statistics-units-style
journal-blind-review-anonymizer
```

练习：

1. 把一篇论文草稿按 APA 第 7 版做格式审计。
2. 检查正文引用和参考文献是否一一对应。
3. 检查 p 值、CI、效应量和单位格式。
4. 生成盲审匿名化 checklist。

### 第 9 周：写作、审稿、展示和自动化

目标：

- 会写论文段落。
- 会审稿式自查。
- 会生成 PPT 和机制图。
- 会设计自己的 Skill。

必学 Skills：

```text
scientific-writing
peer-review
scholar-evaluation
scientific-critical-thinking
venue-templates
scientific-schematics
scientific-slides
skill-creator
mcp-builder
agent-browser
```

练习：

1. 写一版 Introduction。
2. 对草稿做审稿式自查。
3. 生成理论机制图说明。
4. 生成 PPT 大纲。
5. 把一个重复流程封装成 Skill 草案。

### 第 10 周：科研项目管理与版本控制

目标：

- 会为每个真实课题建立稳定项目结构。
- 会维护 project_status、research_log、data_lineage 和 manuscript_versions。
- 会管理投稿、返修和每周科研计划。

必学 Skills：

```text
project-initializer
project-dashboard
research-log
data-lineage-tracker
manuscript-version-manager
submission-revision-tracker
weekly-research-planner
```

练习：

1. 为一个真实课题创建项目骨架。
2. 写第一版 project_status.md。
3. 记录一次 research_log。
4. 建立 data_lineage.csv。
5. 建立 manuscript_versions.md 和 submission_tracker.csv。

### 第 11 周：Zotero / Obsidian 长期知识库

目标：

- 会把 Zotero 作为真实文献和 PDF 的主库。
- 会把 Obsidian 作为论文卡片、理论机制、变量方法和研究问题图谱的知识库。
- 会把每篇论文的可复用启发沉淀成长期资产。

必学 Skills：

```text
zotero-library-sync
obsidian-paper-card
theory-variable-method-matrix
research-question-knowledge-graph
paper-reusable-insight-bank
```

练习：

1. 审计一次 Zotero 文献库。
2. 为 5 篇核心论文生成 Obsidian 论文卡片。
3. 建一个理论-变量-方法矩阵。
4. 生成一个研究问题知识图谱。
5. 从 5 篇论文中提取可复用启发库。

---

## 7. 新手提示词模板

### 7.1 让 Agent 先判断用哪些 Skills

```text
请先阅读当前项目的 AGENTS.md。
本次任务是：[写你的任务]。
请先判断应该使用哪些 Skills，并说明每个 Skill 的作用。
先给计划，不要立刻修改文件。
```

### 7.2 让 Agent 不乱改文件

```text
请只读取 input、data/raw、literature/pdfs。
不要覆盖 raw 数据。
所有新结果写入 output/[任务名]。
如果需要修改已有文件，先说明修改路径和原因。
```

### 7.3 要求真实引用

```text
所有引用必须真实可核验。
优先给 DOI、期刊、年份和作者。
无法核验的文献不要写进正文，只能放入“待核验”列表。
禁止编造引用。
```

### 7.4 要求理论机制

```text
请不要只贴理论标签。
每个理论必须解释变量之间为什么存在关系。
请写清楚：前因、心理或行为机制、边界条件、可观察预测。
```

### 7.5 要求实证严谨

```text
请先判断研究设计能否支持因果解释。
如果只能支持相关关系，请明确写成相关关系。
稳健性、机制和异质性不能替代识别策略。
```

### 7.6 要求情景实验符合顶刊标准

```text
请先用 scenario-experiment-benchmark-mining 核验真实顶刊论文范式，再设计情景实验。
输出必须包括：因果模型、实验条件、刺激材料、操纵检验、真实感检验、混淆检验、预实验、主实验、分析模型、效应量和结果汇报模板。
不要把普通问卷相关研究包装成实验，不要编造论文或引用。
```

---

## 8. 常见错误和处理

| 错误 | 原因 | 处理 |
|---|---|---|
| 运行脚本提示禁止执行 | PowerShell 执行策略限制 | 使用 `powershell -ExecutionPolicy Bypass -File ...` |
| 找不到 Skills | 没复制到项目工作区 | 用 `copy_skill_to_workspace.ps1` 复制需要的 Skill |
| 某个 Skill 不触发 | 描述不匹配或任务说得太模糊 | 在提示词里明确写 Skill 名 |
| 文献引用看起来像假的 | Agent 可能凭记忆生成 | 要求 DOI/链接核验，使用 `citation-management` |
| PDF 读不出来 | 扫描版或加密 | 使用 `pdf` 的 OCR 或先检查权限 |
| CNKI 抓取失败 | 登录、验证码、访问限制 | 不绕过限制，改为公开页面分析或人工导出 |
| 回归结果解释过度 | 把相关误写成因果 | 使用 `scientific-critical-thinking` 自查 |
| 情景实验被质疑 | 操纵不干净、没有预实验、混淆变量没排除 | 用 `scenario-experiment-design` 重写刺激并加入操纵/真实感/混淆检验 |
| 中介分析被质疑 | 只报告路径显著，没有间接效应和置信区间 | 用 `scenario-experiment-analysis` 输出 bootstrap indirect effect 和 CI |
| 主题模型结果很散 | 样本太少或文本太短 | 先做词频和 TF-IDF，不强行解释主题 |
| PPT 太像堆文字 | 没有按页设计信息密度 | 先生成每页一句话结论和图表建议 |
| 自定义 Skill 不好用 | 触发条件、输入输出和边界没写清 | 用 `skill-creator` 重新优化 `description` 和流程 |

---

## 9. 质量底线

无论使用多少 Skills，都要守住这些底线：

1. 不编造文献。
2. 不覆盖原始数据。
3. 不把模拟数据当真实结论。
4. 不把相关关系写成因果关系。
5. 不让理论只停留在名词标签。
6. 不把 API key、账号密码、cookie 写入文档。
7. 不绕过网站访问限制。
8. 每个输出都要能追溯输入来源。
9. 重要结论必须人工复核。
10. Agent 可以加速科研流程，但不能替代你的学术判断。

---

## 10. 你现在该怎么用

如果你完全新手，按这个顺序：

```text
读 README
读本手册
运行 check_environment
运行 check_full_skills_library
按需复制最小 Skills
完成 14 个练习案例，包括 AMiner/AI4Scholar、情景实验、论文排版、EEG/ERP、BCI 脑电智能建模、量表和高级统计/因果推断、科研项目管理、Zotero/Obsidian 长期知识库案例
按需复制需要的 Skills
迁移到真实课题
```

如果你已经会用 Agent，直接：

```powershell
cd "<本项目路径>\零基础教学包"
powershell -ExecutionPolicy Bypass -File .\08_脚本\check_full_skills_library.ps1
cd "<本项目路径>\本地Skills功能分类库"
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -Category 文献 -Workspace "D:\你的项目路径"
```

然后每次任务都按这个格式发给 Agent：

```text
请进入 [项目路径]，先阅读 AGENTS.md。
本次任务是 [具体任务]。
请判断需要哪些 Skills。
先给计划和输出文件路径，不要立刻修改文件。
引用必须真实可核验，raw 数据不能覆盖。
```

---

## 11. 结论

这个零基础包现在应该按“完整科研 Agent 训练包”理解。它保留了新手学习路径，但没有牺牲完整功能。

你最终要掌握的是一套科研工作流：

```text
提出问题
检索文献
核验引用
建立文献矩阵
设计研究
处理数据
运行实证或文本挖掘
写作和审稿
生成图表和汇报
沉淀成自己的 Skills
```

学会之后，你应该能独立完成文献综述、中文选题、数据分析、文本挖掘、论文写作、审稿检查、PPT 和 poster、浏览器自动化、MCP 与自定义 Skill 的基本使用。






