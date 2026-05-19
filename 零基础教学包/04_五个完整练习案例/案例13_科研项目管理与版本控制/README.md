# 案例 13：科研项目管理与版本控制

目标：让新手学会把一个长期博士课题变成可持续管理的项目，而不是每次都从零解释背景。

## 需要 Skills

```text
project-initializer
project-dashboard
research-log
data-lineage-tracker
manuscript-version-manager
submission-revision-tracker
weekly-research-planner
```

## 复制模块

```powershell
cd "<本项目路径>\本地Skills功能分类库"
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -Category 项目 -Workspace "D:\你的项目路径"
```

## 第 1 步：创建项目骨架

```powershell
python "<本项目路径>\本地Skills功能分类库\16_科研项目管理与版本控制Skills\project-initializer\scripts\create_project_skeleton.py" `
  --root "D:\你的项目路径\AI_agent_trust_project" `
  --title "AI agent explainability and user trust" `
  --methods "scenario experiment, EEG, BCI, SEM"
```

## 第 2 步：每次开始工作

提示词：

```text
请进入 D:\你的项目路径\AI_agent_trust_project。
先阅读 AGENTS.md 和 00_project_dashboard/project_status.md。
不要修改文件，先告诉我当前项目状态、最近完成的工作、阻塞点和下一步 3 个优先任务。
```

## 第 3 步：每次结束工作

提示词：

```text
请使用 research-log 更新 08_logs/research_log.md。
记录本次任务：做了什么、使用了哪些输入文件、生成了哪些输出文件、做了哪些决策、哪些结论可靠、哪些需要人工核验、下一步是什么。
同时更新 00_project_dashboard/project_status.md。
```

## 第 4 步：数据处理后

提示词：

```text
请使用 data-lineage-tracker 检查 04_data/raw、04_data/processed 和 05_analysis/output。
生成或更新 04_data/codebook/data_lineage.csv，记录每个 processed 文件来自哪个 raw 文件、经过哪个脚本或步骤、输出到哪里。
不要修改 raw 数据。
```

## 第 5 步：论文改版后

提示词：

```text
请使用 manuscript-version-manager，为 06_manuscript/drafts/main_v2.docx 生成版本记录。
说明本版相对上一版修改了哪些章节、表格、图、分析和引用，哪些问题仍未解决。
```

## 第 6 步：投稿或返修时

提示词：

```text
请使用 submission-revision-tracker 建立投稿追踪表。
目标期刊包括 Journal of Consumer Research、Journal of Applied Psychology、Information Systems Research。
记录期刊匹配度、格式要求、状态、提交日期、审稿结果、返修截止日期和下一步行动。
```

## 完成标准

- 有标准项目目录。
- 有 AGENTS.md。
- 有 project_status.md。
- 有 research_log.md。
- 有 data_lineage.csv。
- 有 manuscript_versions.md。
- 有 submission_tracker.csv。
- 你知道每次开始和结束工作时该让 Agent 做什么。

