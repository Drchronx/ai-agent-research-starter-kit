# AI4Scholar 接入说明

来源文档：

```text
https://lifu-coze.feishu.cn/wiki/WOaewK33Ei2g1nkt44kcRXiBnze
```

AI4Scholar MCP 服务地址：

```text
https://mcp.ai4scholar.net/sse
```

AI4Scholar 网站：

```text
https://ai4scholar.net
```

## 适合做什么

AI4Scholar 更适合真实文献任务：

- 搜索真实论文。
- 查 DOI、PMID、arXiv ID。
- 读开放获取 PDF。
- 查引用和参考文献。
- 查作者信息。
- 做论文推荐。
- 用 `auto_cite` 给学术文本加真实引用。
- 用 `sci_draw` 做科研绘图。

## 已拆分到本包的 AI4Scholar 专项 Skills

| Skill | 放在哪个功能区 | 适合任务 |
|---|---|---|
| `ai4scholar-research` | 文献检索综述引用 | 总入口，适合不确定该用哪个 AI4Scholar 功能时 |
| `ai4scholar-paper-search` | 文献检索综述引用 | 多数据库搜真实论文 |
| `ai4scholar-paper-detail-batch` | 文献检索综述引用 | 单篇或批量核验 DOI、PMID、arXiv ID、标题和元数据 |
| `ai4scholar-citation-network` | 文献检索综述引用 | 查被引、参考文献、相关论文和文献缺口 |
| `ai4scholar-author-intelligence` | 文献检索综述引用 | 查学者、作者论文、专家画像和潜在审稿人 |
| `ai4scholar-paper-recommendation` | 文献检索综述引用 | 根据种子论文推荐后续阅读 |
| `ai4scholar-pdf-fulltext-reading` | 文献检索综述引用 | 下载/读取开放获取 PDF 或 DOI 全文 |
| `ai4scholar-auto-citation-bibtex` | 文献检索综述引用 | 用 `auto_cite` 加引用、生成参考文献和 BibTeX，并做核验 |
| `ai4scholar-mcp-openclaw-setup` | 自动化 MCP 与 Agent | 配置 MCP、OpenClaw 插件、Gateway、Windows 安装问题 |
| `ai4scholar-scholar-mode-projects` | 自动化 MCP 与 Agent | 用 Scholar Mode、`/library`、`/projects`、`/reading-list` 管理论文项目 |
| `ai4scholar-sci-draw` | 图表 PPT 海报与可视化 | 用 `sci_draw` 做科研图、图形摘要、风格转换和图像评审 |

## 两种接入方式

| 方式 | 适合谁 | 特点 |
|---|---|---|
| MCP | 新手快速接入 | 改配置即可，适合先跑通 |
| OpenClaw 插件 | 长期重度使用 | 工具更完整，有 Scholar Mode 和快捷命令 |

## MCP 方式

在 MCP 配置里加入：

```json
{
  "mcpServers": {
    "ai4scholar": {
      "url": "https://mcp.ai4scholar.net/sse",
      "headers": {
        "Authorization": "Bearer ${AI4SCHOLAR_API_KEY}"
      }
    }
  }
}
```

然后重启客户端或 Gateway。

## OpenClaw 插件方式

安装：

```bash
openclaw plugins install ai4scholar
```

配置：

```json
"ai4scholar": {
  "enabled": true,
  "config": {
    "apiKey": "${AI4SCHOLAR_API_KEY}"
  }
}
```

重启：

```bash
openclaw gateway stop
openclaw gateway start
```

验证：

```bash
openclaw plugins list
```

## 推荐提示词

### 论文搜索

```text
请使用 ai4scholar-paper-search 搜索“AI Agent 与科研创造力”的近五年英文文献。
至少使用 Semantic Scholar 和 Google Scholar/ PubMed/ arXiv 中的一个来源。
输出 title、authors、year、venue、DOI/PMID/arXiv ID、abstract、source、是否需要人工核验。
```

### 文献详情核验

```text
请使用 ai4scholar-paper-detail-batch 核验下面这些文献是否真实。
优先按 DOI/PMID/arXiv ID 查询；没有 ID 的按标题精确匹配。
输出标准元数据、冲突项和需要人工核验的条目。
```

### 引用网络扩展

```text
请使用 ai4scholar-citation-network 对下面 3 篇种子文献做引用网络扩展。
分别输出 backward references、forward citations、related papers。
最后按理论、方法、实证证据、综述/元分析分类，并标出最应该先读的 10 篇。
```

### 自动加引用

```text
请使用 ai4scholar-auto-citation-bibtex 给下面这段 Introduction 添加 APA 第 7 版引用。
返回标注后的正文、参考文献列表、BibTeX 和每条引用是否真正支撑原句的核验表。
```

### 全文阅读

```text
请使用 ai4scholar-pdf-fulltext-reading 读取 arXiv:[ID] 的全文，重点总结 Method、Data、Results。
如果全文提取失败，请说明失败原因，不要猜测。
```

### 科研绘图

```text
请使用 ai4scholar-sci-draw 生成一张论文风格 BCI 脑电智能建模流程图。
必须包含 EEG acquisition、preprocessing、feature extraction、classifier、feedback 和 evaluation。
不要加入不存在的数据结果。
```

```text
请使用 AI4Scholar 检索“AI Agent 与科研创造力”的近五年英文文献。
输出 title、authors、year、venue、DOI、abstract、source。
不要编造引用，无法核验的文献放入待核验列表。
```

```text
请使用 AI4Scholar 的 auto_cite 给下面这段 Introduction 添加 APA 引用。
返回标注文本、参考文献列表、BibTeX 和待人工核验项。
```

```text
请使用 AI4Scholar 读取 arXiv:[ID] 的全文，重点总结 Method、Data、Results。
如果全文提取失败，请说明失败原因，不要猜测。
```
