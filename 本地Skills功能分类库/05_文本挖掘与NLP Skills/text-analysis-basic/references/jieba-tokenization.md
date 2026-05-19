# jieba 分词

## 适用任务

当用户要求中文分词、加载自定义词典、过滤停用词、给 CSV/XLSX 增加分词结果列时使用本说明。

## 调用脚本

脚本：`scripts/jieba_tokenize.py`

## 常用命令

TXT 分词：

```bash
python scripts/jieba_tokenize.py --input "input.txt" --output "tokens.txt" --mode precise
```

CSV 分词并增加 `tokens` 列：

```bash
python scripts/jieba_tokenize.py --input "data.csv" --text-column "正文" --output "tokenized.csv" --user-dict "custom_dict.txt" --stopwords "stopwords.txt"
```

搜索引擎模式：

```bash
python scripts/jieba_tokenize.py --input "data.csv" --text-column "text" --output "tokenized.csv" --mode search
```

## 参数

- `--input`：`.txt`、`.csv`、`.xlsx`。
- `--text-column`：CSV/XLSX 的文本列名。
- `--mode`：`precise` 精确模式、`full` 全模式、`search` 搜索引擎模式。
- `--user-dict`：jieba 用户词典。
- `--stopwords`：停用词表，一行一个词。
- `--separator`：tokens 之间的分隔符，默认空格。

## 输出

TXT 输出每行对应一行分词结果。CSV/XLSX 输入输出为 CSV，并新增 `tokens` 列。
