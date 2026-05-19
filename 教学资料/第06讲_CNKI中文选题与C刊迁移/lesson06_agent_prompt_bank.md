# 第 06 讲 Agent 提示词库

每次只复制一个任务给 Agent。确认输出质量后再进入下一步。

## 0. 通用安全提示词

```text
请遵守以下规则：
1. 不编造 CNKI 检索结果、中文文献、英文文献、DOI、作者、期刊或年份。
2. 无法核验的文献标注“待核验”。
3. 不绕过 CNKI 验证码，不非法下载全文。
4. 政策材料只能作为语境，不能替代学术证据。
5. 中文热点不能直接写成学术贡献。
6. C 刊版本和 SSCI/SCI 版本不能只是互相翻译。
7. 每个判断都说明证据来源或待核验项。
```

## 1. 生成中文关键词表

```text
请基于我的研究方向和第05讲输出，生成 input/cn_keywords.md 的内容。

请包含：
1. 中文主关键词
2. 同义词/近义词
3. 上位词
4. 下位词
5. 排除词
6. 可能学科范围
7. 适合 CNKI 检索的 3 个关键词组合

不要把关键词做得过宽。
```

## 2. 生成英文关键词表

```text
请基于 input/cn_keywords.md 和第05讲理论机制链，生成 input/en_keywords.md 的内容。

请区分：
1. 中文关键词直译
2. 国际构念
3. 理论机制词
4. 方法词
5. 目标领域词

不要只做直译。请说明每个英文词为什么适合。
```

## 3. 生成 CNKI 检索策略

```text
请基于 input/cn_keywords.md，生成 topic/cnki_search_strategy.md。

必须包括：
1. 检索日期
2. 主关键词
3. V1 宽检索
4. V2 学科场景检索
5. V3 排除无关检索
6. 排序策略：PT、CF、DFR、ZH
7. 年份范围
8. 人工核验清单

注意：
- 字段代码以 CNKI 或本地 Skill 字段表为准。
- 引号使用英文半角。
- 逻辑运算符前后有空格。
- 年份范围用参数，不写进检索式。
```

## 4. 整理 CNKI 趋势报告

```text
请读取 reports/cnki_trend 中的趋势报告，生成 topic/cnki_topic_map.md 的“趋势分析”部分。

请解释：
1. 年度趋势
2. 近三年变化
3. 学科分布
4. 期刊分布
5. 机构与基金信号
6. 当前年份 year-to-date 限制

不要使用因果语言。不要把趋势写成研究贡献。
```

## 5. 生成中文文献筛选表内容

```text
请基于 CNKI 导出的题录、摘要或手动整理资料，生成 topic/cnki_literature_screening.xlsx 的内容草稿。

字段包括：
- cn_id
- title
- authors
- journal
- year
- source_type
- keywords
- abstract
- theory
- variables
- method
- data
- contribution_claim
- limitation
- c_journal_relevance
- verification_status

没有依据的字段写“未提供”，不要猜。
```

## 6. 生成中文主题地图

```text
请基于 topic/cnki_literature_screening.xlsx、reports/cnki_trend 和 reports/cnki_auto，生成 topic/cnki_topic_map.md。

请按以下结构输出：
1. 中文议题概览
2. 年度趋势与学科分布
3. 主要中文研究流派
4. 高频理论与解释框架
5. 高频变量和方法
6. C 刊常见问题意识
7. 中文研究不足
8. 可能迁移到国际文献的问题

不要逐篇摘要。不要把热点直接写成贡献。
```

## 7. 生成英文前沿检索策略

```text
请基于 input/cn_keywords.md、topic/cnki_topic_map.md 和第05讲输出，生成英文前沿检索策略。

请输出：
1. 直译词
2. 国际构念词
3. 理论机制词
4. 方法词
5. 推荐检索式
6. 推荐数据库或平台
7. 需要核验的代表文献

不要只使用中文直译词。
```

## 8. 生成中英文桥接表

```text
请基于 topic/cnki_topic_map.md 和 reports/english_frontier，生成 topic/cn_en_bridge_table.xlsx 的内容草稿。

每一行说明：
1. 中文议题
2. 中文政策/实践语境
3. CNKI 代表文献
4. 中文常用理论和方法
5. 国际构念
6. 英文关键词
7. 国际代表文献
8. 国际理论
9. 共同机制
10. 中国情境新增了什么
11. 可用方法
12. C 刊版本选题
13. SSCI/SCI 版本选题
14. 迁移风险
15. 需要人工核验的地方

桥接不是翻译。必须做构念、理论、机制和方法对应。
```

## 9. 生成 C 刊选题库

```text
请基于 topic/cnki_topic_map.md 和 topic/cn_en_bridge_table.xlsx，生成 topic/c_journal_idea_bank.md。

生成 5-8 个 C 刊选题候选。每个选题包含：
1. 中文题目
2. 问题意识
3. 中国情境或制度背景
4. 学术缺口
5. 理论机制
6. 变量和方法
7. 可能数据来源
8. 目标 C 刊方向
9. 可迁移的 SSCI/SCI 版本
10. 审稿风险

禁止只写宏大题目。
```

## 10. 生成 C 刊与 SSCI/SCI 双版本

```text
请基于 topic/c_journal_idea_bank.md，选择最强 2 个选题，生成 topic/c_vs_ssci_topic_versions.md。

每个选题输出：

一、C 刊版本
- 中文题目
- 中国问题意识
- 政策/实践语境
- 中文文献基础
- 理论机制
- 方法设计
- 贡献边界

二、SSCI/SCI 版本
- English title
- International research question
- International theoretical gap
- Why Chinese context matters
- Mechanism and hypotheses
- Research design
- Contribution boundary

两个版本不能只是互相翻译。
```

## 11. 迁移风险审计

```text
请以严格导师和审稿人视角，审计 topic/c_vs_ssci_topic_versions.md，生成 qc/topic_migration_audit.md。

检查：
1. 中文热点是否被误写成学术贡献。
2. 政策材料是否被误写成理论证据。
3. C 刊版本是否有问题意识和机制。
4. SSCI/SCI 版本是否只是中国样本替换。
5. 中英文构念是否真正对应。
6. 方法是否能支撑结论。
7. 引用是否真实可核验。
8. 哪个版本更适合先做。

输出：致命问题、重要问题、可修改问题、推荐优先版本、下一步补充检索清单。
```

