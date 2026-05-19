# 案例 8：论文排版与盲审匿名化

目标：让新手学会把论文草稿做成目标期刊格式审计版本。重点是结构和格式，不改学术内容。

## 需要 Skills

```text
journal-title-page-metadata
journal-abstract-keywords
journal-heading-hierarchy
journal-intext-citation-style
journal-reference-list-format
journal-table-figure-caption
journal-statistics-units-style
journal-layout-spacing
journal-footnote-endnote
journal-blind-review-anonymizer
```

## 复制模块

```powershell
cd "<本项目路径>\本地Skills功能分类库"
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -Category 排版 -Workspace "D:\你的项目路径"
```

## 提示词

```text
请按 APA 第 7 版对 manuscript/draft.docx 做投稿前格式审计。
请依次检查：扉页、摘要和关键词、标题层级、正文引用、参考文献、图表标题、统计格式、脚注尾注、布局和盲审匿名化。
只做格式和结构处理，不要改动任何统计数值、研究结论、作者姓名拼写和参考文献事实。
输出：格式审计表、待人工确认问题、盲审风险清单和最终投稿 checklist。
```

## 完成标准

- 有一份格式审计表。
- 有一份参考文献和正文引用匹配审计。
- 有一份统计格式审计。
- 有一份盲审匿名化 checklist。

