# 最小 Skills 按需复制说明

完整功能库里有 116 个 Skills。零基础用户不需要一开始全部复制到项目里，更不要一次性装进 Codex 根目录。

推荐做法：从本地分类库按需复制。

## 进入本地分类库

```powershell
cd "<本项目路径>\本地Skills功能分类库"
```

## 先检查本地库

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\check_local_skills_library.ps1
```

## 新手最小组合

建议先复制这些：

```text
pdf
docx
xlsx
markitdown
citation-management
academic-research-openalex
text-analysis-basic
scientific-writing
```

如果你要做管理学、营销、心理学或信息系统中的情景实验，再加这 4 个：

```text
scenario-experiment-benchmark-mining
scenario-experiment-design
scenario-experiment-analysis
scenario-experiment-reporting
```

如果你要做投稿前排版，再加这 3 个起步：

```text
journal-reference-list-format
journal-statistics-units-style
journal-blind-review-anonymizer
```

如果你要做 EEG/ERP，再加这 3 个起步：

```text
eeg-experiment-planning
eeg-preprocessing-pipeline
erp-segmentation-analysis
```

如果你要做 BCI 脑电智能建模，再加这 4 个起步：

```text
bci-data-structure
eeg-feature-engineering-bci
eeg-model-evaluation-leakage
bci-results-reporting
```

如果你要管理一个长期论文项目，再加这 4 个起步：

```text
project-initializer
project-dashboard
research-log
data-lineage-tracker
```

## 复制示例

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -SkillName pdf,docx,xlsx,markitdown -Workspace "D:\你的项目路径"
```

复制情景实验模块：

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -Category 情景 -Workspace "D:\你的项目路径"
```

默认复制到：

```text
D:\你的项目路径\skills
```

## 只预览不复制

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -SkillName pdf -Workspace "D:\你的项目路径" -DryRun
```
