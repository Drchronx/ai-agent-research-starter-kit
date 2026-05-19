# Word2Vec

## 适用任务

当用户要求训练 Word2Vec、导出词向量、为后续相似度或扩词任务准备词向量模型时使用本说明。

## 调用脚本

脚本：`scripts/vectorize.py`

## 常用命令

```bash
python scripts/vectorize.py --method word2vec --input "texts.csv" --text-column "text" --output-dir "w2v_out" --vector-size 100 --window 5 --min-count 2 --epochs 10
```

已分词输入：

```bash
python scripts/vectorize.py --method word2vec --input "tokenized.csv" --text-column "tokens" --tokenized --output-dir "w2v_out"
```

## 参数

- `--vector-size`：词向量维度。
- `--window`：上下文窗口。
- `--min-count`：最低词频。
- `--epochs`：训练轮数。
- `--workers`：并行进程数。

## 输出

- `word2vec.model`：gensim 模型。
- `word_vectors.csv`：词向量表。
