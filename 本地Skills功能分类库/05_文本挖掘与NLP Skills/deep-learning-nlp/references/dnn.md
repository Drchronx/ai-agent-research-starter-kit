# DNN 文本分类

## 适用任务

当用户要求使用深度神经网络、全连接网络、DNN 做文本分类时使用本说明。

## 调用脚本

脚本：`scripts/paddle_text_classifier.py`

## 训练命令

```bash
python scripts/paddle_text_classifier.py train --model-type dnn --input "train.csv" --text-column "text" --label-column "label" --output-dir "models/dnn_text"
```

## 预测命令

```bash
python scripts/paddle_text_classifier.py predict --model-dir "models/dnn_text" --input "new_texts.csv" --text-column "text" --output "dnn_predictions.csv"
```

## 关键参数

- `--max-len`：每条文本最大 token 长度。
- `--max-vocab`：最大词表规模。
- `--embed-dim`：词向量维度。
- `--hidden-size`：隐藏层宽度。
- `--epochs`：训练轮数。

## 输出

模型目录包含 `model.pdparams`、`vocab.json`、`labels.json`、`config.json`、`metrics.json`。
