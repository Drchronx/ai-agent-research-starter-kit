# 文本相似度

## 适用任务

当用户要求比较两段文本相似度、计算一组文本的两两相似度矩阵时使用本说明。

## 调用脚本

脚本：`scripts/similarity.py`

## 常用命令

两段文本直接比较：

```bash
python scripts/similarity.py --method tfidf --text-a "文本一" --text-b "文本二"
```

一组文本两两相似度矩阵：

```bash
python scripts/similarity.py --method embedding --input "texts.csv" --text-column "text" --output "similarity.csv"
```

## 方法

- `bow`：词频向量余弦相似度。
- `tfidf`：gensim `TfidfModel` 生成 TF-IDF 权重，再计算余弦相似度；不要使用 sklearn 的 `TfidfVectorizer`。
- `jaccard`：分词集合 Jaccard 相似度。
- `embedding`：SentenceTransformer 句向量余弦相似度。

## 输出

两段文本模式输出 JSON；批量模式输出相似度矩阵 CSV。
