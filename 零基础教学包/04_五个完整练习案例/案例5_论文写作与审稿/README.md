# 案例 5：论文写作与审稿

## 目标

你将学会让 Agent 帮你写论文段落，并让另一个审稿视角检查问题。

## 练习材料

```text
07_示例科研项目模板/manuscript/mini_outline.md
```

## 第一步：写 Introduction 片段

提示词：

```text
请读取 manuscript/mini_outline.md，写一个 SSCI 风格 Introduction 草稿。

要求：
1. 先写中文逻辑版，再写英文投稿版；
2. 必须包含研究背景、研究缺口、理论机制、研究设计和贡献；
3. 不要编造引用；
4. 如果需要文献支持，请列出需要补充检索的文献类型，而不是虚构文献。
```

## 第二步：审稿式检查

提示词：

```text
请以严苛 SSCI 审稿人视角审查刚才的 Introduction 草稿。

重点检查：
1. 研究问题是否清楚；
2. 理论机制是否具体；
3. 缺口是否真实；
4. 贡献是否夸大；
5. 哪些地方需要真实文献支持；
6. 给出逐条修改建议。
```

## 输出物

```text
manuscript/introduction_draft.md
manuscript/introduction_review.md
```

## 学习重点

- AI 可以帮你表达，但不能替你判断理论贡献。
- 没有真实文献支持的地方必须标注。
- 审稿视角比润色更重要。

