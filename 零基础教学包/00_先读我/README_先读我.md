# 零基础教学包：先读我

这个文件夹不是简化版。它现在的定位是：

```text
零基础学习路径 + 完整 131 个科研 Skills 库 + 本地按需复制脚本 + 可练习的科研项目模板
```

如果你完全不懂 AI Agent，也可以从这里开始；如果你已经会用 Agent，也可以直接从本地分类库按任务复制需要的 Skills。

## 先按这个顺序做

1. 读 `09_手册/AI_Agent科研零基础全功能手册_v3.md` 或 Word 版。
2. 打开 `02_环境与部署/PowerShell零基础.md`，学会进入文件夹和运行命令。
3. 运行 `08_脚本/check_environment.ps1` 检查 Python、PowerShell 和 Skills 目录。
4. 运行 `08_脚本/check_full_skills_library.ps1` 检查内置完整 Skills 库。
5. 新手先用旁边的 `本地Skills功能分类库`，按需复制 Skill 到自己的项目工作区。
6. 不再建议把全部 131 个 Skills 一次安装到 Codex 根目录。
7. 按 `04_五个完整练习案例` 下的 14 个案例练习，尤其是 AMiner/AI4Scholar、情景实验、论文排版、EEG/ERP、BCI 脑电智能建模、量表心理测量、高级统计/因果推断、科研项目管理和 Zotero/Obsidian 长期知识库案例，再迁移到自己的真实课题。

## 这个包现在包含哪些完整功能

- 文档处理：PDF、Word、Excel、PPT、Markdown、OCR、表格抽取。
- 文献科研：OpenAlex、系统综述、论文拆解、引用核验、BibTeX、arXiv 跟踪。
- 学术平台：AMiner MCP、AI4Scholar MCP/OpenClaw 插件、真实文献检索、论文详情核验、引用网络、学者画像、论文推荐、全文阅读、自动加引用、科研绘图。
- 中文文献与选题：CNKI 检索、趋势、热榜、期刊和选题分析。
- 数据与实证：数据整合、描述统计、回归、DID、IV、DML、机器学习、图表。
- 文本挖掘：中文分词、词频、TF-IDF、Word2Vec、主题模型、情感分析、LLM 标注。
- 情景实验：学习 UTD24/FT50/AJG 顶刊情景实验范式，完成刺激材料、操纵检验、预实验、主实验、数据分析和结果汇报。
- 论文排版：APA 第 7 版和期刊格式转换、引用/参考文献、图表标题、统计格式、脚注尾注、盲审匿名化。
- EEG/ERP：脑电实验设计、预处理、ERP、频域/时频、功能连接、脑电机器学习和结果写作。
- BCI 脑电智能建模：数据结构、特征工程、传统机器学习、深度学习、跨被试迁移、在线解码、防泄漏评估和结果汇报。
- 科研项目管理：项目骨架、状态仪表盘、研究日志、数据血缘、论文版本、投稿返修和每周计划。
- 长期知识库：Zotero 文献库同步、Obsidian 论文卡片、理论-变量-方法矩阵、研究问题知识图谱和每篇论文的可复用启发沉淀。
- 量表心理测量：量表选择、翻译回译、信效度、EFA/CFA、共同方法偏差、测量不变性。
- 高级统计与因果推断：PROCESS 风格中介调节、SEM、多层模型、DID、PSM、IV、RDD、DML、event study。
- 写作审稿：论文段落、实证论文、审稿、自评、投稿模板、基金和研究计划。
- 自动化：Skill 创建、MCP、浏览器自动化、网页检索、Web app 测试。
- 展示输出：科学图、PPT、答辩 slides、poster、论文网页、信息图。

完整 Skills 在：

```text
<本项目路径>\本地Skills功能分类库
```

## 推荐使用方式：按需复制到工作区

进入本地 Skills 分类库：

```powershell
cd "<本项目路径>\本地Skills功能分类库"
```

检查完整库：

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\check_local_skills_library.ps1
```

复制单个 Skill 到你的项目工作区：

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -SkillName ai4scholar-research -Workspace "D:\你的项目路径"
```

复制某一类 Skills 到你的项目工作区：

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -Category 文献 -Workspace "D:\你的项目路径"
```

复制情景实验完整模块：

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -Category 情景 -Workspace "D:\你的项目路径"
```

复制论文排版模块：

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -Category 排版 -Workspace "D:\你的项目路径"
```

复制 EEG/ERP 模块：

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -Category EEG -Workspace "D:\你的项目路径"
```

复制 BCI 脑电智能建模模块：

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -Category BCI -Workspace "D:\你的项目路径"
```

复制科研项目管理模块：

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -Category 项目 -Workspace "D:\你的项目路径"
```

复制 Zotero / Obsidian 长期知识库模块：

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -Category Zotero -Workspace "D:\你的项目路径"
```

只预览不复制：

```powershell
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -SkillName aminer-mcp-research -Workspace "D:\你的项目路径" -DryRun
```

## 重要提醒

- 本包不删除、不移动你的原始资料。
- 所有练习数据都是模拟数据，只能用于学习，不能直接用于论文。
- 涉及真实文献时，必须核验 DOI、作者、期刊和年份。
- 涉及 CNKI、网页、API、数据库和浏览器自动化时，要遵守网站规则和数据使用边界。
- 不要把 API key、账号密码、浏览器 cookie 写进文档或提示词。



