# 案例 6：AMiner 与 AI4Scholar 真实学术平台

这个案例用于学习如何把 AMiner 和 AI4Scholar 接入科研 Agent。

## 目标

完成后你应该能：

- 知道 AMiner 更适合学者、机构、专利、知识图谱和专家发现。
- 知道 AI4Scholar 更适合真实论文检索、论文详情核验、引用网络、作者画像、论文推荐、PDF 阅读、自动加引用和科研绘图。
- 能把两个平台和已有 OpenAlex、CNKI、citation-management Skills 组合使用。

## 前置条件

- AMiner MCP Token。
- AI4Scholar API Key。
- 能访问对应 MCP 服务。
- 不把 Token 或 API Key 写进文档。

## 练习 1：AMiner 查学者

提示词：

```text
请使用 aminer-mcp-research 查询[学者姓名]在[机构]的学术信息。
输出研究方向、代表论文、合作网络、专利或应用产出。
请区分 AMiner 返回的信息、你自己的推断和需要人工核验的信息。
```

## 练习 2：AI4Scholar 搜论文

提示词：

```text
请使用 ai4scholar-research 搜索“AI Agent 与科研创造力”的近五年英文文献。
输出 title、authors、year、venue、DOI、abstract、source。
不要编造引用，无法核验的文献放入待核验列表。
```

如果你已经复制了专项 Skills，也可以这样写：

```text
请使用 ai4scholar-paper-search 搜索“AI Agent 与科研创造力”的近五年英文文献。
再用 ai4scholar-paper-detail-batch 核验前 10 篇的 DOI、作者、年份和期刊。
最后用 ai4scholar-citation-network 对最相关的 3 篇做引用网络扩展。
```

## 练习 3：交叉核验

提示词：

```text
请把 AI4Scholar 搜到的前 10 篇文献与 OpenAlex 或 citation-management 交叉核验。
输出 DOI 是否一致、作者是否一致、期刊年份是否一致，以及需要人工核验的条目。
```

## 练习 4：全文阅读和自动加引用

提示词：

```text
请使用 ai4scholar-pdf-fulltext-reading 读取最相关论文的 Method、Data 和 Results。
再使用 ai4scholar-auto-citation-bibtex 给我的 Introduction 段落添加 APA 第 7 版引用。
输出标注文本、参考文献列表、BibTeX 和每条引用的支撑强度。
```

## 输出要求

把结果写入：

```text
output/platforms
```

不要覆盖原始数据和已有文献矩阵。
