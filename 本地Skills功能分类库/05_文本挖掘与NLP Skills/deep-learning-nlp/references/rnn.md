# RNN/GRU 文本分类

## 适用任务

当用户要求使用 RNN、GRU、循环神经网络做文本分类时使用本说明。

## 调用脚本

脚本：`scripts/paddle_text_classifier.py`

## 训练命令

```bash
python scripts/paddle_text_classifier.py train --model-type rnn --input "train.csv" --text-column "text" --label-column "label" --output-dir "models/rnn_text" --hidden-size 128
```

## 预测命令

```bash
python scripts/paddle_text_classifier.py predict --model-dir "models/rnn_text" --input "new_texts.csv" --text-column "text" --output "rnn_predictions.csv"
```

## 关键参数

- `--hidden-size`：GRU 隐状态维度。
- `--max-len`：输入序列长度。
- `--embed-dim`：词向量维度。
- `--epochs`：训练轮数。

## 输出

模型目录包含 `model.pdparams`、`vocab.json`、`labels.json`、`config.json`、`metrics.json`。
