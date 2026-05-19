# 完整 Skills 本地分类使用说明

当前推荐方式：把 131 个 Skills 保存在当前路径的本地分类库中，需要哪个再复制到项目工作区。

本地分类库：

```text
<本项目路径>\本地Skills功能分类库
```

## 检查完整库

```powershell
cd "<本项目路径>\本地Skills功能分类库"
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\check_local_skills_library.ps1
```

正常应看到：

```text
All local skill folders contain SKILL.md. Total=131
```

## 复制单个 Skill

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -SkillName ai4scholar-research -Workspace "D:\你的项目路径"
```

AI4Scholar 已经拆成多个专项 Skills。常用复制方式：

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -SkillName ai4scholar-paper-search,ai4scholar-paper-detail-batch,ai4scholar-citation-network,ai4scholar-pdf-fulltext-reading,ai4scholar-auto-citation-bibtex -Workspace "D:\你的项目路径"
```

如果要配置 AI4Scholar MCP/OpenClaw，再复制部署 Skill：

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -SkillName ai4scholar-mcp-openclaw-setup -Workspace "D:\你的项目路径"
```

## 复制多个 Skills

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -SkillName pdf,docx,xlsx -Workspace "D:\你的项目路径"
```

## 复制一个功能分类

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -Category 文献 -Workspace "D:\你的项目路径"
```

说明：`-Category` 支持模糊匹配。例如 `文献` 会匹配所有分类名中包含“文献”的分类。

情景实验完整模块：

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -Category 情景 -Workspace "D:\你的项目路径"
```

论文排版模块：

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -Category 排版 -Workspace "D:\你的项目路径"
```

EEG/ERP 模块：

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -Category EEG -Workspace "D:\你的项目路径"
```

BCI 脑电智能建模模块：

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -Category BCI -Workspace "D:\你的项目路径"
```

科研项目管理模块：

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -Category 项目 -Workspace "D:\你的项目路径"
```

Zotero / Obsidian 长期知识库模块：

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -Category Zotero -Workspace "D:\你的项目路径"
```

## 复制到指定 Skills 目录

如果你的项目要求 Skills 放在特定目录：

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -SkillName pdf -DestinationRoot "D:\你的项目路径\.codex\skills"
```

## 覆盖已有 Skill

默认遇到同名 Skill 会跳过。确认要覆盖时：

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -SkillName pdf -Workspace "D:\你的项目路径" -ForceCopy
```


