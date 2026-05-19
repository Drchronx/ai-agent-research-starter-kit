# 机器学习法情感分析

## 适用任务

当用户提供已标注情感数据，要求训练情感分类器，或使用已保存模型对新文本预测时使用本说明。

本方法的 TF-IDF 特征固定使用 gensim `TfidfModel` 生成；分类器使用 sklearn。不要改回 sklearn `TfidfVectorizer`，避免小规模语料下 IDF 平滑导致结果接近词频统计。

## 调用脚本

脚本：`scripts/ml_sentiment.py`

## 训练命令

```bash
python scripts/ml_sentiment.py train --input "train.csv" --text-column "text" --label-column "label" --method tfidf-logreg --model-output "models/sentiment.joblib"
```

可选方法：

- `tfidf-logreg`
- `tfidf-svm`
- `tfidf-nb`
- `tfidf-rf`

## 预测命令

```bash
python scripts/ml_sentiment.py predict --model "models/sentiment.joblib" --input "new_texts.csv" --text-column "text" --output "predictions.csv"
```

## 输出

训练会输出：

- `.joblib` 模型文件。
- `.metrics.json` 评估结果，含 accuracy 和 classification report。

预测会输出 CSV，新增：

- `sentiment_label`
- `sentiment_confidence`，仅当分类器支持概率时生成。

## 边界

该脚本固定使用 gensim TF-IDF 特征，不负责深度学习情感模型训练。
