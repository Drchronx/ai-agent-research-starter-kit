# LDA 主题建模

## 适用任务

当用户要求使用 LDA 发现主题、选择主题数、计算困惑度和一致性、输出主题词、输出文档主题分布或生成 LDA 可视化时使用本说明。

## 调用脚本

脚本：`scripts/lda_model.py`

## 核心原则

LDA 不是一次性自动出结论的任务。主题数选择必须采用“机器诊断 + 用户决策 + 最终训练”的流程：

1. 诊断阶段：脚本完成清洗、分词、词典、TF-IDF、候选主题数训练、困惑度、一致性、指标图、候选主题词和候选 pyLDAvis。
2. 用户决策：AI 必须把诊断材料展示给用户，说明机器建议只是参考，请用户根据研究问题和主题可解释性确认最终主题数。
3. 最终训练：只有用户确认主题数 K 后，才运行带 `--num-topics K` 的最终训练命令。

不要在用户没有确认主题数时自动进入最终训练。

## 标准处理逻辑

脚本采用通用 LDA 标准流程，不绑定任何课程数据或固定主题数：

- 自动识别常见文本列：`tokens`、`text`、`content`、`abstract`、`summary`、`review`、`comment`、`正文`、`内容`、`摘要`、`文本`、`评论`。
- 原始中文文本默认执行：OpenCC 繁转简、只保留中文和英文、jieba 分词、停用词过滤、短词过滤。
- 已分词输入支持两种格式：空格分隔 tokens，或形如 `['词1', '词2']` 的 Python list 字符串。
- 默认尝试自动加载工作区 `stopwords/` 下的常见停用词表；用户也可以显式传 `--stopwords`。
- 默认不做词典高低频过滤，避免在用户不知情时改变结果；需要过滤时显式传 `--no-below`、`--no-above`、`--keep-n`。
- 默认使用 gensim `TfidfModel` 生成训练语料；也可用 `--corpus-weighting bow` 切换为 BOW。
- 默认采用课件流程与相关文献中常用的 LDA 先验设定：`alpha=50/K`、`eta=0.01`、`passes=10`、`random_state=100`，但不固定主题数；如需改用 gensim 的其他先验，可显式传 `--alpha symmetric`、`--alpha asymmetric`、`--alpha auto` 或调整 `--eta`。
- 困惑度图默认画 gensim `log_perplexity()` 原值，以复现课件中“困惑度曲线一路下降”的展示方式；判断时 `log_perplexity` 越高、越接近 0 通常越好。CSV 同时保留换算后的 `perplexity = 2 ** (-log_perplexity)`，该正值越低越好。

所有预处理选择会写入 `preprocessing_config.json`，便于复现。

## 诊断阶段：选择主题数

用户没有明确指定主题数时，先运行诊断：

```bash
python scripts/lda_model.py --input "texts.csv" --output-dir "LDA_result" --topic-min 2 --topic-max 15
```

如果文本列不能自动识别，AI 应先查看列名并询问用户；不能猜。

指定文本列：

```bash
python scripts/lda_model.py --input "texts.csv" --text-column "摘要" --output-dir "LDA_result" --topic-min 2 --topic-max 15
```

已分词输入：

```bash
python scripts/lda_model.py --input "tokenized.csv" --text-column "tokens" --tokenized --output-dir "LDA_result" --topic-min 2 --topic-max 15
```

诊断阶段只输出选题材料，并在 JSON 中返回：

- `stage: topic_selection_only`
- `final_model_trained: false`
- `user_action_required`

AI 看到这些字段后必须暂停，把结果展示给用户并询问最终主题数。

## 诊断阶段输出

输出目录包含：

- `preprocessed_tokens.csv`：清洗和分词后的文档。
- `preprocessing_config.json`：预处理、停用词、词典过滤和训练语料配置。
- `tfidf_model.gensim`：gensim TF-IDF 模型。

`topic_selection/` 下会保留：

- `topic_selection_report.md`：给用户看的选题报告。
- `lda_topic_selection_metrics.csv`：每个候选主题数的困惑度、一致性。
- `topic_selection_summary.json`：机器建议、课件式 `log_perplexity` 最高主题数、换算后 `perplexity` 最低主题数、判断规则。
- `lda_metrics_combined_*.png`：困惑度和一致性双轴图。
- `lda_metrics_separate_*.png`：困惑度和一致性分图。
- `candidate_topics/topics_k_*.csv`：每个候选主题数的主题词。
- `candidate_visualizations/lda_k_*.html`：候选 pyLDAvis 文件。K=1 自动跳过，因为单主题模型没有实际比较意义。
- `candidate_models/k_*/lda_model.gensim`：候选模型，默认保留。

## 展示给用户的内容

诊断结束后，AI 必须用简洁中文展示：

- 机器按 `coherence_c_v` 给出的建议主题数。
- 课件口径 `log_perplexity` 最高对应的主题数。
- 换算后 `perplexity` 最低对应的主题数，仅作为补充说明。
- 指标表路径。
- 指标图路径。
- 候选主题词目录。
- 候选 pyLDAvis HTML 路径。
- 关键预处理配置路径。
- 明确说明：最终主题数应由用户结合研究问题、主题词可解释性和 pyLDAvis 分布决定。

然后询问用户：“你希望最终使用几个主题？”

## 最终训练阶段

用户确认主题数后再运行：

```bash
python scripts/lda_model.py --input "texts.csv" --text-column "摘要" --output-dir "LDA_result_final" --num-topics 8
```

如果用户已选主题数，但仍希望保留一份诊断材料：

```bash
python scripts/lda_model.py --input "texts.csv" --text-column "摘要" --output-dir "LDA_result_final" --num-topics 8 --select-topics --topic-min 2 --topic-max 15
```

## 最终训练输出

最终输出目录包含：

- `preprocessed_tokens.csv`
- `preprocessing_config.json`
- `tfidf_model.gensim`
- `lda_model.gensim`
- `dictionary.gensim`
- `bow_corpus.mm`
- `training_corpus.mm`
- `topics.csv`
- `document_topics.csv`
- `dominant_topics.csv`
- `topic_summary.md`
- `metrics.json`
- `lda_visualization.html`

## 关键参数

- `--num-topics`：最终训练主题数。只有用户确认后才能传入。
- `--topic-min`、`--topic-max`、`--topic-step`：诊断阶段候选主题数范围。
- `--candidate-vis-top-n`：为一致性最高的前 N 个候选主题数生成 pyLDAvis，默认 3；传 0 可关闭。
- `--stopwords`：停用词表路径。
- `--auto-stopwords` / `--no-auto-stopwords`：是否自动从 `stopwords/` 目录查找停用词。
- `--clean-text` / `--no-clean-text`：是否只保留中文和英文。
- `--opencc`：繁简转换配置，默认 `t2s`；传 `none` 关闭。
- `--min-token-length`：最短 token 长度。
- `--no-below`、`--no-above`、`--keep-n`：词典过滤参数；默认不主动过滤。
- `--corpus-weighting`：训练语料权重，默认 `tfidf`；可选 `bow`。
- `--alpha`：文档-主题先验，默认 `scaled`，即 `50/num_topics`；可传 `symmetric`、`asymmetric`、`auto`、浮点数或 `50/k`。
- `--eta`：主题-词先验，默认 `0.01`；可传 `auto`、`symmetric` 或浮点数。
- `--passes`、`--iterations`：训练强度。
- `--topn`：每个主题导出的主题词数量。

## 判断规则

- 课件中的“困惑度图”实际使用 gensim `log_perplexity()` 原值，通常会随着主题数增加而下降；本 skill 的图像默认复现这一口径。
- `log_perplexity` 越高、越接近 0 通常越好；不要把课件图中最向下的点直接解释为最优。
- CSV 中的 `perplexity` 是由 `2 ** (-log_perplexity)` 换算得到的正值，越低越好，走势可能与课件图相反，不作为默认展示图口径。
- `coherence_c_v` 越高通常表示主题语义一致性越好。
- 机器建议默认以 `coherence_c_v` 最大为准，因为一致性更贴近主题可解释性。
- 机器建议只是参考，最终主题数必须由用户结合研究问题、主题词可解释性和 pyLDAvis 分布决定。
