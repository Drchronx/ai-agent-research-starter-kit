# AI Agent 科研零基础入门手册

> 旧版提示：请优先阅读 `AI_Agent科研零基础全功能手册_v3.md` 或 Word 版。v3 已改为 72 个 Skills 的本地按需复制模式，并新增情景实验模块；不再建议把 Skills 安装到 Codex 根目录。

版本：v1.0  
适用对象：完全没有 AI Agent、Skills、命令行经验的科研学习者  
目标：照着本手册做，能完成从安装 Skills 到完成 5 个科研练习案例的全过程。

---

## 第 1 章 你现在有什么

你现在有两个相关文件夹：

```text
<本项目路径>\综合学术部署包
<本项目路径>\零基础教学包
```

两者区别：

| 文件夹 | 作用 |
|---|---|
| 综合学术部署包 | 放完整 Skills 和高级部署手册 |
| 零基础教学包 | 教完全新手一步步上手 |

如果你完全不懂，先不要直接看综合包。先看零基础教学包。

---

## 第 2 章 AI Agent 是什么

普通聊天 AI 像一个“会回答问题的人”。  
AI Agent 像一个“会使用工具做事的人”。

在科研中，Agent 可以：

- 读取 PDF、Word、Excel。
- 整理论文。
- 建立文献矩阵。
- 检查引用。
- 分析 CSV/Excel 数据。
- 运行 Python 脚本。
- 做文本挖掘。
- 写论文段落。
- 以审稿人视角检查论文。

但 Agent 不能替代你：

- 判断研究问题是否重要。
- 判断理论机制是否成立。
- 判断研究设计是否能支持因果结论。

你可以把 Agent 理解为“科研助理”，不是“导师”，更不是“作者本人”。

---

## 第 3 章 Skill 是什么

Skill 是一个封装好的专项能力。

例如：

| Skill | 能做什么 |
|---|---|
| `citation-management` | 核验引用、生成 BibTeX |
| `literature-review` | 做文献综述 |
| `empirical-analysis-skill-python` | 做实证分析 |
| `text-analysis-basic` | 做中文文本挖掘 |
| `peer-review` | 审稿式检查论文 |

Skill 通常长这样：

```text
skill-name/
  SKILL.md
  scripts/
  references/
  assets/
```

你只需要记住：

- `SKILL.md` 是说明书。
- `scripts` 是能执行的脚本。
- `references` 是方法说明。
- `assets` 是模板或示例。

---

## 第 4 章 第一次打开 PowerShell

PowerShell 是 Windows 的命令行工具。

打开方式：

1. 按 Windows 键。
2. 输入 `PowerShell`。
3. 点击打开。

进入本教学包：

```powershell
cd "<本项目路径>\零基础教学包"
```

查看文件：

```powershell
dir
```

如果能看到 `00_先读我`、`01_认识AI_Agent` 等文件夹，说明成功。

---

## 第 5 章 检查环境

在 PowerShell 中运行：

```powershell
powershell -ExecutionPolicy Bypass -File .\08_脚本\check_environment.ps1
```

你会看到：

- 当前目录。
- Python 是否可用。
- PowerShell 版本。
- Codex / Claude / OpenClaw 的 Skills 目录是否存在。
- 是否能找到综合学术部署包。

如果有 `MISS`，不一定是错误。比如你没装 OpenClaw，`.openclaw\skills` 不存在是正常的。

---

## 第 6 章 安装最小可用 Skills

先预览：

```powershell
powershell -ExecutionPolicy Bypass -File .\08_脚本\install_minimal_skills.ps1 -Target codex -DryRun
```

正式安装：

```powershell
powershell -ExecutionPolicy Bypass -File .\08_脚本\install_minimal_skills.ps1 -Target codex
```

这会从综合学术部署包复制最小 Skills 到：

```text
C:\Users\<用户名>\.codex\skills
```

最小 Skills 包括：

- 文档处理：`markitdown`、`pdf`、`docx`、`xlsx`
- 文献和引用：`citation-management`、`academic-research-openalex`、`literature-review`
- 实证分析：`empirical-analysis-skill-python`
- 文本挖掘：`text-analysis-basic`、`topic-modeling`、`sentiment-analysis`
- 写作审稿：`scientific-writing`、`peer-review`
- 扩展工具：`skill-creator`、`agent-browser`、`mcp-builder`

---

## 第 7 章 第一次和 Agent 说话

第一次不要让 Agent 直接大干一场。先让它理解项目。

复制这个提示词：

```text
请进入 <本项目路径>\零基础教学包\07_示例科研项目模板。
先阅读 AGENTS.md 和 README.md。
不要修改任何文件，先告诉我：
1. 这个项目的目录结构；
2. 里面有哪些练习数据；
3. 我应该先做哪个练习；
4. 哪些文件不能修改。
```

如果 Agent 能正确回答，说明它已经理解项目。

---

## 第 8 章 案例 1：读一篇论文

目标：让 Agent 读取一篇 PDF 论文并生成结构化笔记。

步骤：

1. 找一篇真实 PDF 论文。
2. 放入：

```text
零基础教学包\07_示例科研项目模板\literature\pdfs
```

3. 对 Agent 说：

```text
请读取 literature/pdfs 中的一篇 PDF 论文，输出结构化论文笔记到 literature/notes。

笔记必须包括：
1. 标题、作者、年份、期刊、DOI；
2. 研究问题；
3. 理论或核心概念；
4. 样本和数据；
5. 方法；
6. 主要发现；
7. 局限；
8. 对我的研究有什么启发；
9. 哪些信息无法从 PDF 中确认。

不要编造引用。无法确认的地方写“未确认”。
```

成功输出：

```text
literature/notes/论文笔记_xxx.md
```

你要检查：

- DOI 是否真实。
- 作者年份是否和 PDF 一致。
- 局限是否具体。
- 是否出现“未确认”而不是乱编。

---

## 第 9 章 案例 2：建立文献矩阵

目标：把多篇论文整理成表格。

准备：

- 至少 3 篇真实 PDF。
- 放入 `literature/pdfs`。

提示词：

```text
请读取 literature/pdfs 中的论文，建立文献矩阵，输出到 literature/matrix/literature_matrix.xlsx 和 literature/matrix/literature_matrix.md。

字段包括：
- paper_id
- title
- authors
- year
- journal
- doi
- research_question
- theory_or_concepts
- independent_variable
- dependent_variable
- mediator
- moderator
- sample
- method
- main_findings
- limitations
- relevance_to_my_study
- possible_gap
- confidence_note

要求：
1. 不要编造文献元数据；
2. 找不到的信息写“未报告”；
3. possible_gap 不能只写“研究较少”，必须说明具体缺口；
4. 最后总结这批文献可以分成哪几类。
```

成功输出：

```text
literature/matrix/literature_matrix.xlsx
literature/matrix/literature_matrix.md
```

你要学会：

- 文献矩阵不是“摘要合集”。
- 它是后续写综述、找 GAP、设计研究的基础。

---

## 第 10 章 案例 3：分析 Excel/CSV 数据

目标：让 Agent 完成一次基础实证分析。

练习数据：

```text
data/raw/sample_empirical_data.csv
```

提示词：

```text
请读取 data/raw/sample_empirical_data.csv，完成一个零基础实证分析练习。

要求：
1. 不要修改 raw 原始数据；
2. 检查变量、缺失值、描述统计；
3. 输出清洗后的数据到 data/processed/sample_empirical_data_clean.csv；
4. 生成描述统计表、相关矩阵和至少 2 张图；
5. 以 creativity_score 为因变量，ai_agent_use、cognitive_load、experience_years 为自变量做一个基础回归；
6. 输出结果到 output/empirical；
7. 用通俗语言解释每个输出文件是干什么的。
```

成功输出可能包括：

```text
data/processed/sample_empirical_data_clean.csv
output/empirical/summary_statistics.csv
output/empirical/correlation_matrix.csv
output/empirical/regression_results.md
```

注意：

- 这是模拟数据，不能当真实研究结论。
- 回归结果不等于因果。
- 如果样本只有 15 行，任何显著性都不可靠。

---

## 第 11 章 案例 4：文本挖掘入门

目标：对中文文本做最基础的文本分析。

练习数据：

```text
data/raw/sample_texts.csv
```

提示词：

```text
请读取 data/raw/sample_texts.csv，对 text 列做文本挖掘入门分析。

要求：
1. 清洗文本；
2. 中文分词；
3. 输出词频表；
4. 输出 TF-IDF 关键词；
5. 尝试做情感倾向分析；
6. 如果主题模型样本太少，请明确说明不适合做正式 LDA；
7. 输出结果到 output/nlp；
8. 用零基础能听懂的话解释每一步。
```

成功输出：

```text
output/nlp/tokenized_texts.csv
output/nlp/word_frequency.csv
output/nlp/tfidf_keywords.csv
output/nlp/sentiment_scores.csv
output/nlp/nlp_report.md
```

注意：

- 文本样本太少时，不适合正式主题模型。
- 情感分析必须核验。
- 分词词典和停用词会改变结果。

---

## 第 12 章 案例 5：论文写作与审稿

目标：让 Agent 写一个论文 Introduction 片段，并审查它。

材料：

```text
manuscript/mini_outline.md
```

第一步，写作：

```text
请读取 manuscript/mini_outline.md，写一个 SSCI 风格 Introduction 草稿。

要求：
1. 先写中文逻辑版，再写英文投稿版；
2. 必须包含研究背景、研究缺口、理论机制、研究设计和贡献；
3. 不要编造引用；
4. 如果需要文献支持，请列出需要补充检索的文献类型，而不是虚构文献。
```

第二步，审稿：

```text
请以严苛 SSCI 审稿人视角审查刚才的 Introduction 草稿。

重点检查：
1. 研究问题是否清楚；
2. 理论机制是否具体；
3. 缺口是否真实；
4. 贡献是否夸大；
5. 哪些地方需要真实文献支持；
6. 给出逐条修改建议。
```

成功输出：

```text
manuscript/introduction_draft.md
manuscript/introduction_review.md
```

注意：

- AI 写作只是草稿。
- 真正的理论判断必须由你完成。
- 没有真实文献的地方必须补检索。

---

## 第 13 章 常见提示词写法

### 13.1 先让 Agent 看项目

```text
请先阅读项目中的 AGENTS.md 和 README.md。不要修改文件，先总结项目结构和建议下一步。
```

### 13.2 限制不要乱动

```text
不要删除文件，不要覆盖 raw 数据，不要修改原始 PDF。所有输出写入 output 文件夹。
```

### 13.3 要求列出输出文件

```text
任务结束后，请列出生成了哪些文件、每个文件的用途、哪些结果需要人工核验。
```

### 13.4 要求不要编造引用

```text
不要编造任何引用。无法核验的文献请标注“未核验”，不要写成确定事实。
```

### 13.5 要求先计划

```text
先不要执行。请先给出你的操作计划、需要读取的文件、会生成的文件和潜在风险。
```

---

## 第 14 章 常见错误

### 14.1 文件找不到

通常是路径写错。路径中有中文或空格时，一定加引号。

### 14.2 脚本不能运行

使用：

```powershell
powershell -ExecutionPolicy Bypass -File .\脚本名.ps1
```

### 14.3 Python 缺包

看到 `ModuleNotFoundError` 时，安装对应包：

```powershell
python -m pip install 包名
```

### 14.4 Agent 编造文献

马上要求核验：

```text
请逐条核验刚才所有引用，无法核验的全部删除或标注“未核验”。
```

### 14.5 分析结果过度解释

纠正：

```text
请区分相关关系和因果关系。不要把模拟数据或普通回归结果写成因果结论。
```

---

## 第 15 章 学会之后怎么用到自己的论文

复制：

```text
07_示例科研项目模板
```

改名为你的课题，例如：

```text
博士论文_AIagent科研创造力
```

然后：

1. 把真实论文放入 `literature/pdfs`。
2. 把真实数据放入 `data/raw`。
3. 修改 `AGENTS.md`。
4. 从案例 1 到案例 5 依次迁移。

---

## 第 16 章 最小掌握清单

如果你能独立做到下面这些，就算真正入门：

- 会打开 PowerShell。
- 会进入教学包目录。
- 会运行环境检查脚本。
- 会安装最小 Skills。
- 会让 Agent 先读项目规则。
- 会让 Agent 读论文并输出笔记。
- 会建立文献矩阵。
- 会分析一个 CSV。
- 会做一个简单文本分析。
- 会让 Agent 写草稿并审稿。
- 会要求 Agent 不编造引用。
- 会保护 raw 数据不被覆盖。

---

## 结语

AI Agent 的重点不是“让 AI 替你做研究”，而是把重复、机械、格式化、可复现的部分交给工具。你要保留的是研究者最核心的判断：问题是否重要、机制是否成立、方法是否匹配、结论是否克制。
