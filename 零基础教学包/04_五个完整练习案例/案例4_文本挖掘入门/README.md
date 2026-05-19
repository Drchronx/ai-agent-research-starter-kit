# 案例 4：文本挖掘入门

## 目标

你将学会对一批中文文本做分词、词频、TF-IDF 和情感分析。

## 练习数据

```text
07_示例科研项目模板/data/raw/sample_texts.csv
```

字段：

- `doc_id`
- `text`
- `group`

## 提示词

```text
请读取 data/raw/sample_texts.csv，对 text 列做文本挖掘入门分析。

要求：
1. 清洗文本；
2. 中文分词；
3. 输出词频表；
4. 输出 TF-IDF 关键词；
5. 尝试做情感倾向分析；
6. 如果主题模型样本太少，请明确说明不适合做正式 LDA；
7. 输出结果到 output/nlp；
8. 用零基础能听懂的话解释每一步。
```

## 输出物

```text
output/nlp/tokenized_texts.csv
output/nlp/word_frequency.csv
output/nlp/tfidf_keywords.csv
output/nlp/sentiment_scores.csv
output/nlp/nlp_report.md
```

## 学习重点

- 文本分析不是把词云做出来就结束。
- 分词和停用词会影响结果。
- 小样本不适合正式主题模型。
- LLM 标注必须做人工核验。

