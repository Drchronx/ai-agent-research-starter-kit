# 综合学术部署包：先读我

本部署包把 `<本项目路径>` 中最适合科研工作的 Skills 按功能重新整理为 8 类，便于复制到 Codex、Claude Code 或 OpenClaw 的技能目录。

## 目录结构

| 目录 | 内容 |
|---|---|
| `01_核心文档处理Skills` | PDF、DOCX、PPTX、XLSX、MarkItDown 等文档处理能力 |
| `02_文献检索综述引用Skills` | 学术检索、文献综述、引用核验、SSCI 文献解读 |
| `03_CNKI选题与中文文献Skills` | CNKI 检索、热榜、趋势、选题分析 |
| `04_数据采集整合与实证Skills` | 多源数据整合、实证分析、机器学习、图表 |
| `05_文本挖掘与NLP Skills` | 中文 NLP、主题模型、情感分析、LLM 标注 |
| `06_论文写作审稿投稿Skills` | 科学写作、论文审查、投稿模板、研究计划 |
| `07_自动化MCP浏览器与Agent Skills` | Skill 开发、MCP、浏览器自动化、Web 检索 |
| `08_图表PPT海报与可视化Skills` | 科学示意图、PPT、poster、paper-to-web |
| `09_建议自定义Skills模板` | 面向 EEG/ERP、SSCI 写作、文本变量构造的模板 |
| `scripts` | 安装与检查脚本 |

## 推荐部署顺序

1. 先部署 `01_核心文档处理Skills`。
2. 再部署 `02_文献检索综述引用Skills` 和 `06_论文写作审稿投稿Skills`。
3. 做实证或文本挖掘时部署 `04_数据采集整合与实证Skills`、`05_文本挖掘与NLP Skills`。
4. 需要 CNKI 选题和中文文献时部署 `03_CNKI选题与中文文献Skills`。
5. 需要自动化、网页操作、MCP 开发时部署 `07_自动化MCP浏览器与Agent Skills`。
6. 需要图表、PPT、poster 时部署 `08_图表PPT海报与可视化Skills`。

## 一键安装到 Codex

在 PowerShell 中运行：

```powershell
cd "<本项目路径>\综合学术部署包"
powershell -ExecutionPolicy Bypass -File .\scripts\install_skills.ps1 -Target codex
```

安装到 Claude Code：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_skills.ps1 -Target claude
```

安装到 OpenClaw：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_skills.ps1 -Target openclaw
```

只预览不复制：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_skills.ps1 -Target codex -DryRun
```

## 注意事项

- 安装脚本只复制包含 `SKILL.md` 的文件夹。
- 复制不会删除原文件。
- 若目标目录已有同名 Skill，默认跳过；需要覆盖时加 `-ForceCopy`。
- 部分 Skills 需要额外安装 Python 依赖，请查看每个 Skill 的 `scripts/requirements.txt`。
- CNKI、浏览器自动化、API 检索类 Skills 可能需要数据库、代理、浏览器登录态或 API key。不要把 key 写入文档或脚本。

## 核心清单

- `skills_manifest.csv`：按类别列出所有已打包 Skills。
- `skills_manifest.json`：机器可读清单。
- `AI_Agent科研功能与Skills部署完整手册_v2.md/docx`：新版详细教学手册。
