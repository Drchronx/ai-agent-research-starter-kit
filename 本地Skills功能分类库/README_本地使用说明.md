# 本地 Skills 功能分类库

这个文件夹是本地离线 Skills 库，不会自动安装到 Codex 根目录。

位置：

```text
<本项目路径>\本地Skills功能分类库
```

## 功能分类

| 文件夹 | 功能 |
|---|---|
| `01_核心文档处理Skills` | PDF、Word、Excel、PPT、Markdown、OCR、表格抽取 |
| `02_文献检索综述引用Skills` | OpenAlex、AMiner、AI4Scholar 论文搜索/详情核验/引用网络/作者画像/全文阅读/自动加引用、综述、引用核验、arXiv |
| `03_CNKI选题与中文文献Skills` | CNKI 检索、趋势、热榜、中文选题 |
| `04_数据采集整合与实证Skills` | 数据整合、描述统计、回归、DID、IV、DML、机器学习 |
| `05_文本挖掘与NLP Skills` | 中文分词、TF-IDF、主题模型、情感分析、LLM 标注 |
| `06_论文写作审稿投稿Skills` | 论文写作、审稿、自评、投稿模板、研究计划 |
| `07_自动化MCP浏览器与Agent Skills` | Skill 创建、MCP、AI4Scholar MCP/OpenClaw 部署、浏览器自动化、网页检索 |
| `08_图表PPT海报与可视化Skills` | 科学图、AI4Scholar sci_draw、PPT、poster、论文网页、信息图 |
| `09_建议自定义Skills模板` | 后续自定义 Skills 的建议模板 |
| `10_情景实验与行为研究Skills` | 顶刊情景实验范式挖掘、实验设计、数据分析和结果汇报 |
| `11_期刊论文排版与投稿格式Skills` | APA/期刊格式、引用、参考文献、图表、统计格式、盲审匿名化 |
| `12_EEG_ERP神经科学实验Skills` | EEG/ERP 实验设计、预处理、ERP、频域、连接、脑电机器学习和结果写作 |
| `13_量表开发与心理测量Skills` | 量表选择、翻译改编、信效度、EFA/CFA、共同方法偏差、测量不变性 |
| `14_高级统计机制与因果推断Skills` | 中介调节、SEM、多层模型、DID/PSM/IV/RDD/DML、因果边界审计 |
| `15_BCI脑电智能建模Skills` | BCI 数据结构、脑电特征工程、机器学习、深度学习、跨被试迁移、在线解码和防泄漏评估 |
| `16_科研项目管理与版本控制Skills` | 科研项目骨架、状态仪表盘、研究日志、数据血缘、论文版本、投稿返修和每周计划 |
| `17_Zotero_Obsidian长期知识库Skills` | Zotero 文献库同步、Obsidian 论文卡片、理论-变量-方法矩阵、研究问题知识图谱和论文启发沉淀 |

## 检查本地库

```powershell
cd "<本项目路径>\本地Skills功能分类库"
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\check_local_skills_library.ps1
```

正常应看到 131 个 Skills。

## 复制单个 Skill 到工作区

默认复制到 `目标工作区\skills`：

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -SkillName ai4scholar-research -Workspace "D:\你的项目路径"
```

结果：

```text
D:\你的项目路径\skills\ai4scholar-research
```

## 复制整个功能分类到工作区

例如复制文献检索类：

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -Category 文献 -Workspace "D:\你的项目路径"
```

例如复制 AI4Scholar 常用文献子模块：

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -SkillName ai4scholar-paper-search,ai4scholar-paper-detail-batch,ai4scholar-citation-network,ai4scholar-pdf-fulltext-reading,ai4scholar-auto-citation-bibtex -Workspace "D:\你的项目路径"
```

例如复制情景实验类：

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -Category 情景 -Workspace "D:\你的项目路径"
```

例如复制论文排版类：

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -Category 排版 -Workspace "D:\你的项目路径"
```

例如复制 EEG/ERP 类：

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -Category EEG -Workspace "D:\你的项目路径"
```

例如复制 BCI 脑电智能建模类：

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -Category BCI -Workspace "D:\你的项目路径"
```

例如复制科研项目管理类：

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -Category 项目 -Workspace "D:\你的项目路径"
```

例如复制 Zotero / Obsidian 长期知识库模块：

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -Category Zotero -Workspace "D:\你的项目路径"
```

## 只预览，不复制

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -SkillName aminer-mcp-research -Workspace "D:\你的项目路径" -DryRun
```

## 复制到指定目录

如果你的 Agent 要求 Skills 放在某个固定目录，可以指定 `-DestinationRoot`：

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -SkillName pdf -DestinationRoot "D:\你的项目路径\.codex\skills"
```

## 注意

- 这个库是本地可复制库，不会自动安装到 `C:\Users\<用户名>\.codex\skills`。
- 如果目标目录已有同名 Skill，默认跳过。
- 确认要覆盖时加 `-ForceCopy`。
- AMiner 和 AI4Scholar 仍需要单独配置 Token 或 API Key。


