# Sentence Embedding

## 适用任务

当用户要求生成句向量、文本 embedding、用于深度语义相似度或聚类的向量表示时使用本说明。

## 调用脚本

脚本：`scripts/vectorize.py`

## 常用命令

```bash
python scripts/vectorize.py --method embedding --input "texts.csv" --text-column "text" --output-dir "embedding_out" --embedding-model "paraphrase-multilingual-MiniLM-L12-v2"
```

## 参数

- `--embedding-model`：sentence-transformers 模型名或本地模型路径。

## 输出

- `embeddings.npy`：numpy 向量矩阵。
- `embeddings.csv`：CSV 格式向量矩阵。

## 注意

首次调用在线模型可能需要联网下载模型。若用户提供本地模型路径，优先使用本地路径。
