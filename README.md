# AI Agent Research Starter Kit

面向科研训练、论文写作和学术工作流自动化的 AI Agent 教学与部署资料包。

本项目把 AI Agent 在科研中的常用能力整理成可教学、可复制、可部署的资料体系：从零基础入门、Agent 环境配置、Skills 使用，到真实文献检索、知识库建设、实验设计、统计分析、文本挖掘、EEG/ERP、BCI 脑电建模、论文写作、审稿自查和期刊排版。适合用于研究生课程、课题组内部培训、个人科研工作流搭建和 AI Agent 能力包二次开发。

本仓库是公开发布清洁版，已排除原始第三方课程资料、压缩包、安装包、大文件、真实本地配置文件和明显个人路径。

## 适合谁

- 刚开始学习 AI Agent 的研究生、本科生和科研助理。
- 想把 AI Agent 用到文献综述、论文写作、数据分析和项目管理中的科研人员。
- 需要给学生开设 AI Agent 科研方法课程的教师或课题组负责人。
- 想按功能区复用 Skills、提示词和教学案例的 Agent 使用者。

## 能做什么

- AI Agent 入门部署：OpenClaw、Claude Code、Codex、Hermes 等 Agent 的科研应用场景比较。
- 文献与引用：真实文献检索、BibTeX 生成、引用核验、AMiner、AI4Scholar、Zotero 与 Obsidian 知识库。
- 选题与综述：CNKI 中文选题、C刊迁移、文献综述、理论建构、研究问题生成。
- 实证研究：情景实验、问卷与量表、信效度、CFA/EFA、机制检验、高级统计和因果推断。
- 数据与文本：数据采集、清洗、可视化、文本挖掘、LLM 标注、变量构造。
- 神经科学与 BCI：EEG/ERP 预处理、结果报告、脑电机器学习和深度学习建模。
- 写作与发表：论文结构写作、审稿自查、rebuttal、期刊格式转换、APA 第 7 版排版、盲审匿名化。
- 课程教学：每讲大纲、课件、课堂任务、课后作业和零基础实操教程。

## 目录结构

- `教学资料/`：按讲次组织的课程大纲、实操教程、课件、课堂任务和作业。
- `零基础教学包/`：面向新手的完整学习路径、案例、提示词模板、Skills 库和排错说明。
- `综合学术部署包/`：面向科研工作流的综合部署手册与功能区 Skills。
- `本地Skills功能分类库/`：按功能分类整理的本地 Skills，可按需复制到 Agent 工作区。
- `SECURITY_CHECK_REPORT.md`：本次公开发布前的安全检查与脱敏记录。
- `release_build_stats.json`：清洁版生成过程的机器可读统计。

## 推荐学习路径

1. 先读 `零基础教学包/00_先读我/README_先读我.md`，了解整体学习顺序。
2. 再看 `教学资料/课程总大纲.md`，按讲次学习每个科研任务。
3. 学到某个功能时，到 `本地Skills功能分类库/` 或 `零基础教学包/10_完整功能Skills库/` 找对应 Skill。
4. 把需要的 Skill 文件夹复制到你的 Agent 工作区或 Agent 的 skills 目录。
5. 使用案例材料完成一轮完整任务，再替换成自己的论文、数据或研究问题。

## Skills 怎么用

每个 Skill 通常是一个包含 `SKILL.md` 的文件夹。使用时建议遵循下面的方式：

1. 根据任务选择功能区，例如文献综述、统计分析、EEG、BCI、论文排版。
2. 复制对应 Skill 文件夹到你的 Agent 工作区或全局 skills 目录。
3. 在对话中明确告诉 Agent：使用哪个 Skill、输入文件在哪里、输出文件放到哪里。
4. 对所有涉及真实文献、统计结果、实验结论和投稿格式的输出做人工复核。

## 配置与安全

涉及 API、数据库、MCP、飞书、Zotero、AMiner、AI4Scholar 等连接时，请只提交示例配置：

- 可以提交：`.env.example`、`config.example.json`
- 不要提交：`.env`、`config.json`、API Key、账号密码、Cookie、Token、私有数据库地址

本清洁版已经做过一次发布前安全检查，但如果你后续添加真实数据、学生作业、会议纪要、文献 PDF、问卷原始数据或 EEG 原始数据，请重新做脱敏检查。

## 推荐仓库名

建议使用英文小写加连字符，方便 GitHub 搜索、引用和命令行使用。

首选：

```text
ai-agent-research-starter-kit
```

备选：

```text
research-agent-skills-kit
academic-agent-deployment-kit
ai-agent-research-course
ai-for-research-skills
```

如果这个仓库主要用于教学，推荐 `ai-agent-research-course`；如果主要用于给别人复用 Skills 和部署包，推荐 `ai-agent-research-starter-kit`。

## 许可证

本项目采用双许可证：

- 代码和脚本：`MIT License`，见 `LICENSE`
- 教学资料、手册、课件、提示词和 Skills 文档：`CC BY-NC-SA 4.0`，见 `LICENSE-DOCS.md`

这意味着：脚本可以较宽松地复用；文档和教学材料可以学习、引用、改编和非商业教学使用，但不能直接拿去商业售卖，改编后也应采用相同许可证。

## GitHub 上传

```powershell
cd "<你的GitHub发布清洁版目录>"
git init
git add .
git commit -m "Initial public clean release"
git branch -M main
git remote add origin <你的GitHub仓库地址>
git push -u origin main
```

公开上传前建议再运行一次本地密钥扫描，并确认你对发布内容拥有分享或教学使用权限。
