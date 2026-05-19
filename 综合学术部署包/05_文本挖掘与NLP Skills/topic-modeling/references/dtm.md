# DTM 动态主题模型

## 适用任务

当用户要求分析主题随年份、月份、批次等时间片变化，或要求训练动态主题模型时使用本说明。

## 调用脚本

脚本：`scripts/dtm_model.py`

## 常用命令

```bash
python scripts/dtm_model.py --input "texts.csv" --text-column "text" --time-column "year" --output-dir "DTM_result" --num-topics 6 --passes 5
```

已分词输入：

```bash
python scripts/dtm_model.py --input "tokenized.csv" --text-column "tokens" --time-column "year" --tokenized --output-dir "DTM_result" --num-topics 6
```

## 参数

- `--time-column`：时间片列，脚本会按排序后的唯一值形成时间片。
- `--num-topics`：主题数。
- `--passes`：训练轮数。
- `--topn`：每个主题每个时间片导出的词数。

## 输出

- `dtm_model.gensim`
- `dictionary.gensim`
- `time_slices.json`
- `topics_by_time.csv`
- `document_topics.csv`

## 边界

DTM 需要每个时间片有足够文档。若某些时间片文档过少，应先聚合时间粒度。
