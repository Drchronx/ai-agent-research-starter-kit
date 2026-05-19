# 第 07 讲 Agent 提示词库

每次只复制一个任务给 Agent，确认输出质量后再进入下一步。

## 0. 通用安全提示词

```text
请遵守以下规则：
1. 不编造顶刊论文、实验结果、样本量、DOI、量表来源或信度。
2. 无法核验的论文、量表或数据标注“待核验”。
3. 情景操纵必须对应理论构念。
4. 各实验条件只改变目标操纵，不引入无关混淆。
5. 操纵检验不能替代干净的操纵设计。
6. 翻译量表不等于验证量表。
7. 不把情景实验过度解释为真实现场行为。
8. 所有伦理风险必须标注。
```

## 1. 生成因果结构

```text
请读取 input/lesson05_outputs、input/lesson06_outputs 和 input/initial_experiment_idea.md，生成 experiment/causal_model.md。

请提取：
1. 研究问题
2. 自变量/操纵变量
3. 因变量
4. 中介机制
5. 调节变量或边界条件
6. 竞争解释
7. 目标被试
8. 单位随机化
9. 理论机制
10. 哪些关系能用情景实验检验，哪些不能

如果研究想法还不能实验化，请直接指出问题并给出修改方案。
```

## 2. 顶刊实验 benchmark

```text
请基于 input/target_journal_examples 中的真实论文，使用 scenario-experiment-benchmark-mining，生成 experiment/benchmark_matrix.xlsx 的内容草稿。

每篇论文提取：
- title
- authors
- journal
- year
- DOI or URL
- study number
- experiment type
- IV / manipulation
- DV
- mediator
- moderator
- sample source and N
- scenario structure
- manipulation check
- realism check
- attention check
- confound check
- exclusion rules
- analysis model
- reporting style
- reusable design lesson
- verification_status

不能编造论文。无法确认的字段写 not verified。
```

## 3. 推荐实验类型

```text
请基于 experiment/causal_model.md 和 experiment/benchmark_matrix.xlsx，推荐最简洁但能检验理论的实验类型。

请输出：
1. 推荐设计
2. 为什么不是更复杂设计
3. 条件数量
4. 每个条件操纵点
5. 需要的预测试
6. 主实验最小可行版本
7. 如果投顶刊，后续需要补哪些研究
```

## 4. 生成情景材料

```text
请基于 experiment/causal_model.md，生成 experiment/stimuli.md。

要求：
1. 写出所有条件的情景材料。
2. 各条件长度尽量一致。
3. 保持角色、任务、背景、风险、成本、结果和语气一致。
4. 只改变目标操纵。
5. 标注每个操纵句对应的构念。
6. 不要让材料直接暴露假设。
7. 给出中英文版本，如适用。
```

## 5. 生成条件差异表

```text
请基于 experiment/stimuli.md，生成 experiment/condition_difference_table.xlsx 的内容草稿。

字段包括：
- condition_id
- condition_name
- manipulated_construct
- exact_manipulated_text
- constant_elements
- length_words
- potential_confound
- confound_control
- expected_manipulation_check_direction
- revision_notes
```

## 6. 设计检查项

```text
请基于 experiment/stimuli.md，生成 experiment/checks_and_attention.md。

请设计：
1. 操纵检验
2. 现实感检验
3. 清晰度检验
4. 注意力检验
5. 混淆检验
6. 怀疑检验
7. 排除规则

要求：
- 操纵检验测目标操纵，不要和中介或因变量措辞高度重叠。
- 混淆检验覆盖能力、风险、成本、友好度、任务难度、隐私等替代解释。
- 排除规则必须在看结果前确定。
```

## 7. 选择和适配量表

```text
请基于 experiment/causal_model.md，使用 scale-selection-adaptation，生成 experiment/scales.xlsx 的内容草稿。

每个构念包括：
1. construct_name
2. conceptual_definition
3. operational_definition
4. scale_source
5. source_verification_status
6. original_items
7. translated_items
8. response_anchor
9. reverse_coded
10. adaptation_notes
11. copyright_or_permission_notes
12. reliability_from_prior_studies
13. pilot_plan
14. measurement_risks

不要编造量表来源或信度。
```

## 8. 规划预测试

```text
请基于 experiment/stimuli.md、experiment/checks_and_attention.md 和 experiment/scales.xlsx，生成 experiment/pretest_plan.md。

请包含：
1. 预测试目的
2. 样本来源和建议 N
3. 随机分配方式
4. 操纵检验判据
5. 现实感和清晰度判据
6. 混淆检验判据
7. 修改规则
8. 进入主实验的标准
```

## 9. 主实验流程

```text
请生成 experiment/procedure.md。

包括：
1. 招募平台和目标被试
2. 知情同意
3. 随机分配
4. 情景阅读
5. 操纵检验
6. 中介和因变量测量
7. 注意力/现实感/混淆检验
8. 人口统计变量
9. 退出权和伦理说明
10. 排除规则
11. 数据保存和匿名化
```

## 10. 分析计划

```text
请基于 experiment/causal_model.md、experiment/procedure.md 和 hypotheses，生成 analysis/analysis_plan.md。

按以下顺序写：
1. 数据审计
2. 缺失值和重复值
3. 排除规则
4. 随机化检验
5. 操纵检验
6. 信度检验
7. 主效应模型
8. 中介或调节模型
9. 效应量
10. 稳健性分析
11. 哪些结论可以说因果，哪些不能
12. 表格和图形计划
```

## 11. Method / Results 模板

```text
请使用 scenario-experiment-reporting 和 questionnaire-reporting-template，生成 reporting/method_results_template.md。

包括：
1. Method section draft
2. Design and participants
3. Procedure
4. Stimuli and manipulation
5. Measures
6. Manipulation checks
7. Analysis plan
8. Results reporting template
9. Table plan
10. Figure plan
11. Appendix materials
12. Transparency statement
```

## 12. 设计审计

```text
请以严格审稿人视角，审计本工作区所有实验设计文件，生成 qc/experiment_design_audit.md。

检查：
1. 情景是否真实可信
2. 操纵是否只影响目标构念
3. 是否存在能力、风险、成本、隐私、情绪、严重性等混淆
4. 操纵检验是否与中介/DV 重叠
5. 量表来源是否真实可核验
6. 预测试判据是否明确
7. 排除规则是否透明
8. 分析计划是否匹配假设
9. 因果语言是否过度
10. 伦理风险是否处理

输出：致命问题、重要问题、可修改问题、建议保留内容、下一步行动。
```

