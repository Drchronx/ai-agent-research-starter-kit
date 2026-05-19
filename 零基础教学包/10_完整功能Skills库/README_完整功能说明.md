# 零基础教学包内置完整功能 Skills 库

这个目录是零基础教学包里的完整 Skills 镜像，当前共有 131 个 Skills，按功能分类保存。它只是本地文件库，不会自动安装到 Codex 根目录。

优先使用旁边的统一本地库：

```text
<本项目路径>\本地Skills功能分类库
```

## 推荐使用方式

先检查完整性：

```powershell
cd "<本项目路径>\零基础教学包"
powershell -ExecutionPolicy Bypass -File .\08_脚本\check_full_skills_library.ps1
```

需要哪个 Skill，再从本地分类库复制到你的项目工作区：

```powershell
cd "<本项目路径>\本地Skills功能分类库"
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -SkillName pdf -Workspace "D:\你的项目路径"
```

复制整个情景实验模块：

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -Category 情景 -Workspace "D:\你的项目路径"
```

## 功能分类

| 目录 | 功能 |
|---|---|
| `01_核心文档处理Skills` | PDF、DOCX、PPTX、XLSX、Markdown |
| `02_文献检索综述引用Skills` | AMiner、AI4Scholar 论文搜索/详情核验/引用网络/作者画像/全文阅读/自动加引用、OpenAlex、综述、引用核验 |
| `03_CNKI选题与中文文献Skills` | CNKI、中文选题、趋势分析 |
| `04_数据采集整合与实证Skills` | 数据整合、实证分析、机器学习、因果推断 |
| `05_文本挖掘与NLP Skills` | 分词、TF-IDF、主题模型、情感分析、LLM 标注 |
| `06_论文写作审稿投稿Skills` | 写作、审稿、投稿、研究计划 |
| `07_自动化MCP浏览器与Agent Skills` | Skill 开发、MCP、AI4Scholar MCP/OpenClaw 部署、浏览器、Web |
| `08_图表PPT海报与可视化Skills` | 科学图、AI4Scholar sci_draw、PPT、poster、paper-to-web |
| `10_情景实验与行为研究Skills` | 顶刊情景实验范式挖掘、设计、分析和汇报 |
| `11_期刊论文排版与投稿格式Skills` | 期刊排版、引用、参考文献、图表、统计格式、盲审匿名化 |
| `12_EEG_ERP神经科学实验Skills` | EEG/ERP、频域、连接、脑电机器学习和结果写作 |
| `13_量表开发与心理测量Skills` | 量表选择、信效度、EFA/CFA、共同方法偏差、测量不变性 |
| `14_高级统计机制与因果推断Skills` | 中介调节、SEM、多层模型、准实验因果推断和结果表 |
| `15_BCI脑电智能建模Skills` | BCI 数据结构、脑电特征、传统机器学习、深度学习、迁移学习、在线解码和结果汇报 |
| `16_科研项目管理与版本控制Skills` | 项目初始化、状态仪表盘、研究日志、数据血缘、论文版本和投稿返修追踪 |
| `17_Zotero_Obsidian长期知识库Skills` | Zotero 文献库同步、Obsidian 论文卡片、理论-变量-方法矩阵、研究问题知识图谱和论文启发沉淀 |

## 注意

- 不建议把全部 Skills 一次性复制到 Codex 根目录。
- 如果目标项目已有同名 Skill，复制脚本默认跳过。
- AMiner、AI4Scholar 等平台仍需要单独配置 Token 或 API Key。
- 情景实验模块中的顶刊范式学习必须基于真实可核验论文，禁止编造引用。


