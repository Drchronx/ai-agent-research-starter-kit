# BERTopic 主题建模

## 适用任务

当用户要求使用 embedding、BERTopic、语义聚类方式发现主题，或 LDA 效果不佳希望使用语义主题模型时使用本说明。

## 调用脚本

脚本：`scripts/bertopic_model.py`

## 常用命令

```bash
python scripts/bertopic_model.py --input "texts.csv" --text-column "text" --output-dir "BERTopic_result" --embedding-model "paraphrase-multilingual-MiniLM-L12-v2" --min-topic-size 10
```

指定主题合并策略：

```bash
python scripts/bertopic_model.py --input "texts.csv" --text-column "text" --output-dir "BERTopic_result" --nr-topics auto
```

生成可视化：

```bash
python scripts/bertopic_model.py --input "texts.csv" --text-column "text" --output-dir "BERTopic_result" --vis-html
```

## 参数

- `--embedding-model`：sentence-transformers 模型名或本地模型路径。
- `--min-topic-size`：每个主题的最小文档数。
- `--nr-topics`：可为整数、`auto` 或不填。
- `--ngram-min`、`--ngram-max`：关键词 ngram 范围。
- `--min-df`：CountVectorizer 最小文档频次。

## 输出

- `bertopic_model/`
- `topics.csv`
- `document_topics.csv`
- `bertopic_topics.html`、`bertopic_barchart.html`，仅在 `--vis-html` 成功时生成。

## 边界

BERTopic 依赖较重，首次使用模型可能需要联网下载。若用户环境不能安装或下载模型，应直接说明当前 skill 无法完成 BERTopic。
