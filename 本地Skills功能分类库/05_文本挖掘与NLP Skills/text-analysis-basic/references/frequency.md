# 词频和句频统计

## 适用任务

当用户要求统计高频词、统计高频句子、输出 top-N 频率表时使用本说明。

## 调用脚本

脚本：`scripts/frequencies.py`

## 常用命令

词频统计：

```bash
python scripts/frequencies.py --input "texts.csv" --text-column "text" --mode word --output "word_freq.csv" --stopwords "stopwords.txt" --top-n 200
```

已分词文本统计：

```bash
python scripts/frequencies.py --input "tokenized.txt" --mode word --tokenized --output "word_freq.csv"
```

句频统计：

```bash
python scripts/frequencies.py --input "texts.csv" --text-column "text" --mode sentence --output "sentence_freq.csv" --top-n 100
```

## 参数

- `--mode word`：调用 jieba 分词后统计词频。
- `--mode sentence`：按中文和英文句末标点切句后统计句频。
- `--tokenized`：输入已经以空格分词时使用。
- `--top-n`：输出前 N 项；小于等于 0 表示全部输出。

## 输出

CSV 字段为 `item,count,frequency`。
