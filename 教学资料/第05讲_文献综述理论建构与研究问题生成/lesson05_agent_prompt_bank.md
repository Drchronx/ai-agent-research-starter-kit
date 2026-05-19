# 第 05 讲 Agent 提示词库

本文件用于学生复制给 Codex、Claude Code、OpenClaw、Hermes 或其他 Agent。每次只执行一个任务，确认输出质量后再进入下一步。

## 0. 通用安全提示词

```text
请遵守以下规则：
1. 只使用我提供的真实文献、论文卡片、BibTeX、表格和可核验检索结果。
2. 禁止编造作者、题名、期刊、年份、DOI、数据结果。
3. 无法确认真实性的引用必须标注“待核验”。
4. 不要把“我没有读到”写成“文献没有”。
5. 理论必须解释机制，不能只贴理论标签。
6. 没有实验、准实验或可信识别策略时，不要使用因果语言。
7. 输出到指定文件，并在最后列出需要人工核验的项目。
```

## 1. 生成证据表

```text
请读取 input/paper_cards、input/candidate_papers.xlsx 和 input/matrices 中的材料，生成 review/evidence_table.md。

不要写综述正文。每篇文献至少提取：
- citation_key 或待核验标识
- 研究问题
- 理论或解释框架
- 自变量/操纵变量
- 中介机制
- 调节变量/边界条件
- 因变量
- 数据来源或实验设计
- 分析方法
- 核心发现
- 局限
- 可复用启发

没有依据的字段写“未提供”，不要猜。
```

## 2. 生成文献树

```text
基于 review/evidence_table.md，生成 review/literature_tree.md。

建立两棵树：
1. Novelty Tree：理论解释、新变量/新构念、新情境/新对象、新方法/新数据、新机制/边界条件。
2. Challenge-Insight Tree：核心挑战、已有解决方式、未解决问题、对我选题的启发。

要求：
- 不按年份排列。
- 不逐篇摘要。
- 每个分支列代表文献或待核验文献。
- 每个分支说明对我研究方向的启发。
```

## 3. 识别研究流派与争议

```text
基于 review/evidence_table.md 和 review/literature_tree.md，生成 review/research_streams_and_controversies.md。

请列出：
1. 3-5 个研究流派。
2. 每个流派的核心问题、常用理论、关键变量、常用方法、代表文献和局限。
3. 2-4 个主要争议。
4. 每个争议的来源：理论、样本、测量、方法、数据或情境。
5. 每个争议是否能转化为我的研究缺口。

不要把所有差异都写成“研究视角不同”。
```

## 4. 生成研究缺口候选

```text
基于 review/literature_tree.md、review/research_streams_and_controversies.md 和 review/evidence_table.md，生成 5-8 个研究缺口候选，输出 review/research_gap_candidates.md。

每个缺口必须包含：
1. gap_id
2. 缺口类型：理论/机制/边界/测量/方法/情境
3. 已知内容
4. 未知内容
5. 为什么重要
6. 支持证据
7. 可能研究问题
8. 可行方法
9. 审稿风险
10. 需要补充检索什么

禁止空话。不要使用“研究较少”“填补空白”这类表达，除非给出具体证据。
```

## 5. 审计研究缺口

```text
请基于 review/research_gap_candidates.md，使用严格导师和审稿人标准生成 review/research_gap_audit.md。

对每个 gap 审计：
1. 是否已经被已有研究解决？
2. 是否只是新样本、新平台或新情境？
3. 是否需要新理论、新机制、新测量或新方法？
4. 是否有真实文献证据支持“现有解释不足”？
5. 是否能在 3-6 个月内完成最小可行研究？
6. 最大审稿风险是什么？
7. 最终判断：keep / revise / drop。

不要迎合我。弱 gap 必须指出。
```

## 6. 缺口评分与研究问题生成

```text
请基于 review/research_gap_audit.md，对所有 keep/revise 的 gap 打分。

评分维度：
- importance 1-5
- novelty 1-5
- feasibility 1-5
- theory_value 1-5
- method_fit 1-5
- evidence_support 1-5

请输出：
1. gap_score_table
2. 排名前 2 的 gap
3. 推荐主选题
4. 备选选题
5. 为什么其他 gap 暂时不做
6. 主选题的一句话研究问题

研究问题公式：
在 [具体情境] 中，[核心自变量/刺激/技术特征] 如何通过 [心理/认知/神经/组织机制] 影响 [结果变量]，并受到 [边界条件] 的影响？
```

## 7. 建立理论机制链

```text
请基于我选择的最强研究问题，使用 theory_mechanism_chain_template.md，生成 theory/theory_mechanism_chain.md。

要求：
1. 明确情境/刺激/技术变化。
2. 明确心理、认知、神经或组织机制。
3. 区分构念、变量、测量和操纵。
4. 说明理论为什么能解释这个机制。
5. 指出理论不能解释或需要谨慎的地方。
6. 给出适合的研究设计。
7. 禁止只写理论名称。
```

## 8. 生成假设组

```text
请基于 theory/theory_mechanism_chain.md，使用 hypothesis_set_template.md，生成 hypotheses/hypothesis_set.md。

每个假设包括：
- 假设编号
- 假设文本
- 机制解释
- 文献支持或待核验文献
- 操纵或测量方式
- 数据分析方法
- 因果语言风险

只生成理论上必要的假设。不要为了复杂而添加中介、调节或调节中介。
```

## 9. 生成综述提纲

```text
请基于 review/literature_tree.md、review/research_gap_audit.md 和 theory/theory_mechanism_chain.md，生成 review/synthesis_outline.md。

综述提纲必须按以下逻辑组织：
1. 研究现象与核心问题
2. 已有理论解释
3. 关键变量与机制
4. 方法和证据类型
5. 争议与不足
6. 我的研究如何进入这个缺口

不要按年份写。不要逐篇文献摘要。每一节都要说明它如何推进到我的研究问题。
```

## 10. 生成一页研究方案

```text
请基于前面所有输出，使用 one_page_research_proposal_template.md，生成 proposal/one_page_research_proposal.md。

一页方案必须包含：
1. 暂定题目：中文与英文
2. 一句话研究问题
3. 为什么重要
4. 文献缺口
5. 理论机制
6. 研究模型
7. 假设组
8. 研究设计
9. 数据与分析方法
10. 预期贡献
11. 最大风险
12. 下一步计划

控制在 1-2 页以内。不要夸大贡献。所有引用标注已核验或待核验。
```

## 11. 导师前审计

```text
请以严格审稿人和导师视角，基于 proposal/one_page_research_proposal.md，生成 qc/gap_and_theory_audit.md。

检查：
1. 研究问题是否过大。
2. 缺口是否成立。
3. 是否只是换情境或换样本。
4. 理论是否真正解释机制。
5. 构念、变量、测量是否一致。
6. 假设是否可检验。
7. 方法能否支持因果语言。
8. 文献是否真实可核验。
9. 贡献是否夸大。
10. 下一步最应该补什么。

输出：致命问题、重要问题、可修改问题、建议保留内容、下一步行动清单。
```

