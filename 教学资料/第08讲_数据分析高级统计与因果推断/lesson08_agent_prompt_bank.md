# 第 08 讲 Agent 提示词库

每次只复制一个任务给 Agent，确认输出质量后再进入下一步。

## 0. 通用安全提示词

```text
请遵守以下规则：
1. 不修改原始数据。
2. 不编造统计结果、系数、标准误、p 值、N 或效应量。
3. 不隐藏非显著结果。
4. 不用稳健性检验替代因果识别。
5. 不把横截面相关写成因果。
6. 不控制 post-treatment mediator 或 collider。
7. 每个模型都要说明适用条件、诊断和解释边界。
8. 输出后列出需要人工核验的内容。
```

## 1. 生成变量字典

```text
请读取 input/clean_data 中的数据文件，生成 analysis/variable_dictionary.xlsx 的内容草稿。

字段包括：
1. variable_name
2. variable_label
3. type
4. role: IV/DV/M/W/control/id/time/cluster/check
5. coding_or_anchor
6. source
7. expected_range
8. reverse_code
9. missing_rule
10. transformation
11. analysis_use
12. notes

不要改变原始数据。无法判断的字段写“待人工核验”。
```

## 2. 数据审计

```text
请基于 input/clean_data 和 analysis/variable_dictionary.xlsx，生成 analysis/data_audit.md。

请检查：
1. 样本量
2. 变量数量
3. 缺失值
4. 重复值
5. 异常值
6. 取值范围
7. 条件/处理组分布
8. 时间和面板结构
9. 聚类或嵌套结构
10. 不能直接分析的问题

不要删除数据，只报告问题和建议。
```

## 3. 假设到模型映射

```text
请读取 input/lesson05_outputs/hypothesis_set.md、analysis/variable_dictionary.xlsx 和 analysis/data_audit.md，生成 analysis/hypothesis_model_map.xlsx 的内容草稿。

每个假设包括：
1. hypothesis_id
2. hypothesis_text
3. X
4. Y
5. mediator
6. moderator
7. controls
8. design_type
9. recommended_model
10. model_reason
11. causal_language_allowed
12. required_diagnostics
13. output_table
```

## 4. 模型选择

```text
请基于 analysis/hypothesis_model_map.xlsx 和 analysis/data_audit.md，生成 analysis/model_selection.md。

请判断每个假设适合：
- t-test / ANOVA
- OLS / logistic regression
- PROCESS mediation/moderation
- SEM / CFA / path analysis
- multilevel / longitudinal model
- DID / event study
- PSM
- IV
- RDD
- DML

每个模型必须说明为什么适合、需要什么数据结构、核心假设、主要诊断和替代方案。
```

## 5. PROCESS 机制检验计划

```text
请基于 analysis/hypothesis_model_map.xlsx，使用 process-mediation-moderation，生成 PROCESS 风格机制检验计划，写入 analysis/analysis_plan.md 的机制检验部分。

请包括：
1. 模型图
2. X/Y/M/W 和协变量
3. 直接效应、间接效应、总效应是否需要
4. bootstrap 次数和置信区间
5. simple slopes 或 Johnson-Neyman 是否需要
6. conditional indirect effects 是否需要
7. 因果语言限制
```

## 6. SEM/CFA 计划

```text
请基于变量字典、量表题项和理论模型，使用 sem-cfa-path-latent，生成 SEM/CFA 分析计划。

请包括：
1. SEM 是否必要，回归是否足够
2. 测量模型
3. 结构模型
4. 估计方法和缺失值处理
5. 拟合指标：CFI、TLI、RMSEA、SRMR、chi-square、df
6. 路径表
7. 备择模型
8. 报告段落
9. 不允许为了拟合随意加相关误差
```

## 7. 多层/纵向模型计划

```text
请基于 data_audit 中的数据结构，使用 multilevel-longitudinal-modeling，生成多层/纵向模型计划。

请包括：
1. 数据层级
2. 单位分析
3. ICC 是否需要
4. 随机截距和随机斜率
5. 中心化方案：grand-mean / group-mean / person-mean
6. 跨层交互
7. 模型公式
8. 结果表
9. 哪些是 within-person，哪些是 between-person 解释
```

## 8. 因果识别审计

```text
请基于研究问题、数据结构和变量字典，使用 causal-inference-design-audit 和 did-psm-iv-rdd-dml-event-study，生成 analysis/causal_identification_audit.md。

请包括：
1. causal estimand
2. treatment/exposure
3. outcome
4. timing
5. DAG/confounding audit
6. bad controls
7. 推荐方法：DID/event study/PSM/IV/RDD/DML/OLS
8. 识别假设
9. 诊断和稳健性
10. 可以说的因果结论
11. 不能说的因果结论
```

## 9. 分析计划和脚本骨架

```text
请基于前面所有输出，生成 analysis/analysis_plan.md 和 analysis/scripts/analysis_template.py。

分析计划包括：
1. 数据读取和只读备份
2. 数据审计
3. 缺失值和异常值处理
4. 变量构造
5. 描述统计
6. 相关矩阵
7. 主效应模型
8. 机制/边界模型
9. 因果识别模型，如适用
10. 稳健性
11. 图表
12. 输出路径

脚本要求：
- 不覆盖原始数据
- 所有输出写到 output 或 analysis/results
- 代码注释清楚
```

## 10. 结果表

```text
请使用 statistical-results-tables，基于模型输出或结果占位，生成 analysis/results_tables.xlsx 的表结构。

至少包括：
1. 描述统计表
2. 相关矩阵
3. 主效应模型表
4. 中介/调节/SEM/多层/因果模型表，按实际研究选择
5. 稳健性表
6. 附录表

表注必须说明标准误类型、固定效应、控制变量、N、显著性标记和变量编码。
```

## 11. 结果段落

```text
请基于 analysis/results_tables.xlsx 和 analysis/model_selection.md，生成 analysis/result_writeup.md。

要求：
1. 按假设顺序写
2. 报告系数、SE 或 CI、p 值、效应量、N
3. 解释效应方向和实际意义
4. 不隐藏非显著结果
5. 明确哪些结果支持假设，哪些不支持
6. 标注因果语言边界
7. 写成 APA 或目标期刊风格
```

## 12. 统计结论审计

```text
请以严格审稿人视角，审计 analysis/analysis_plan.md、analysis/results_tables.xlsx 和 analysis/result_writeup.md，生成 qc/statistical_claims_audit.md。

检查：
1. 模型是否匹配研究问题
2. 变量编码是否清楚
3. 是否控制了坏控制
4. 是否把关联写成因果
5. 是否把稳健性写成识别
6. 中介/调节是否有理论依据
7. SEM/CFA 是否过度调拟合
8. DID/IV/RDD/DML 假设是否说明
9. 是否只看 p 值不看效应量
10. 是否隐藏非显著结果

输出：致命问题、重要问题、可修改问题、允许保留的结论、必须删除或降级的结论。
```

