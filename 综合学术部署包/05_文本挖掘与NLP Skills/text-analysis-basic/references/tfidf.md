# TF-IDF

## 适用任务

当用户要求计算 TF-IDF、构建关键词特征矩阵、导出文本向量时使用本说明。

本 skill 固定使用 gensim 的 `TfidfModel`，不要使用 sklearn 的 `TfidfVectorizer`。小规模语料下 sklearn 的 IDF 平滑机制容易让结果接近词频统计，不符合课程对 TF-IDF 区分度的要求。

## 调用脚本

脚本：`scripts/vectorize.py`

## 常用命令

```bash
python scripts/vectorize.py --method tfidf --input "texts.csv" --text-column "text" --output-dir "tfidf_out" --max-features 5000
```

已分词文本：

```bash
python scripts/vectorize.py --method tfidf --input "tokenized.csv" --text-column "tokens" --tokenized --output-dir "tfidf_out"
```

## 参数

- `--method tfidf`：固定使用 TF-IDF。
- `--max-features`：保留最大特征数。
- `--tokenized`：输入已经用空格分词。

## 输出

- `tfidf_matrix.csv`：文档-词矩阵。
- `tfidf_features.json`：特征词列表。
- `tfidf_dictionary.gensim`：gensim 字典。
- `tfidf_model.gensim`：gensim TF-IDF 模型。
