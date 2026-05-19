# 案例 2：建立文献矩阵

## 目标

你将学会把多篇论文整理成一个表格，用于文献综述和选题。

## 准备材料

至少准备 3 篇真实论文 PDF，放入：

```text
07_示例科研项目模板/literature/pdfs/
```

## 提示词

```text
请读取 literature/pdfs 中的论文，建立文献矩阵，输出到 literature/matrix/literature_matrix.xlsx 和 literature/matrix/literature_matrix.md。

字段包括：
- paper_id
- title
- authors
- year
- journal
- doi
- research_question
- theory_or_concepts
- independent_variable
- dependent_variable
- mediator
- moderator
- sample
- method
- main_findings
- limitations
- relevance_to_my_study
- possible_gap
- confidence_note

要求：
1. 不要编造文献元数据；
2. 找不到的信息写“未报告”；
3. possible_gap 不能只写“研究较少”，必须说明具体缺口；
4. 最后总结这批文献可以分成哪几类。
```

## 输出物

```text
literature/matrix/literature_matrix.xlsx
literature/matrix/literature_matrix.md
```

## 你要学会的判断

文献矩阵不是越多越好，而是要能支持三件事：

1. 看出研究流派。
2. 看出方法差异。
3. 看出你的研究问题从哪里来。

