# 词云图

## 适用任务

当用户要求根据中文文本、分词结果或某一文本列生成词云图时使用本说明。

## 调用脚本

脚本：`scripts/wordcloud_generate.py`

## 常用命令

从原始文本生成词云：

```bash
python scripts/wordcloud_generate.py --input "texts.csv" --text-column "text" --output "wordcloud.png" --stopwords "stopwords.txt" --font-path "simhei.ttf"
```

从已分词列生成词云：

```bash
python scripts/wordcloud_generate.py --input "tokenized.csv" --text-column "tokens" --tokenized --output "wordcloud.png"
```

## 参数

- `--font-path`：中文字体路径。课程目录中已有 `simhei.ttf`，可直接使用。
- `--tokenized`：文本已经用空格分词时使用。
- `--width`、`--height`：图片尺寸。
- `--max-words`：词云最大词数。

## 输出

输出 PNG 图片。
