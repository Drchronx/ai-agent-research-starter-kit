# 案例 3：分析 Excel/CSV 数据

## 目标

你将学会让 Agent 对一个表格数据做最基础的科研分析。

## 练习数据

已提供模拟数据：

```text
07_示例科研项目模板/data/raw/sample_empirical_data.csv
```

注意：这是模拟数据，只能练习，不能用于论文。

## 提示词

```text
请读取 data/raw/sample_empirical_data.csv，完成一个零基础实证分析练习。

要求：
1. 不要修改 raw 原始数据；
2. 检查变量、缺失值、描述统计；
3. 输出清洗后的数据到 data/processed/sample_empirical_data_clean.csv；
4. 生成描述统计表、相关矩阵和至少 2 张图；
5. 以 creativity_score 为因变量，ai_agent_use、cognitive_load、experience_years 为自变量做一个基础回归；
6. 输出结果到 output/empirical；
7. 用通俗语言解释每个输出文件是干什么的。
```

## 输出物

```text
data/processed/sample_empirical_data_clean.csv
output/empirical/summary_statistics.csv
output/empirical/correlation_matrix.csv
output/empirical/regression_results.md
output/empirical/figures/
```

## 学习重点

- raw 数据不动。
- processed 数据才用于分析。
- 回归结果不等于因果结论。
- 模拟数据的显著性没有真实意义。

