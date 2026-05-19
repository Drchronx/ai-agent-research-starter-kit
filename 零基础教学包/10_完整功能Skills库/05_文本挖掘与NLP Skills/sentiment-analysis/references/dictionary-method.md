# 词典法情感分析

## 适用任务

当用户提供情感词典，或要求按照正负词、带分值情感词典计算文本情感分数时使用本说明。

## 调用脚本

脚本：`scripts/dictionary_sentiment.py`

## 常用命令

正负词典：

```bash
python scripts/dictionary_sentiment.py --input "texts.csv" --text-column "text" --positive-lexicon "positive.txt" --negative-lexicon "negative.txt" --output "sentiment_dict.csv"
```

带分值词典：

```bash
python scripts/dictionary_sentiment.py --input "texts.csv" --text-column "text" --scored-lexicon "sentiment.xlsx" --word-column "词语" --score-column "情感强度" --output "sentiment_dict.csv"
```

## 参数

- `--positive-lexicon`：正向词表，一行一个词，或含词列的 CSV/XLSX。
- `--negative-lexicon`：负向词表。
- `--scored-lexicon`：带分值词典，支持 TXT/CSV/XLSX。
- `--word-column`、`--score-column`：带分值词典的词列和分值列。

## 输出

输出 CSV，新增：

- `sentiment_score`
- `sentiment_label`
- `matched_words`

## 边界

词典法只能反映词表命中情况，不处理复杂上下文、反讽和长距离否定。
