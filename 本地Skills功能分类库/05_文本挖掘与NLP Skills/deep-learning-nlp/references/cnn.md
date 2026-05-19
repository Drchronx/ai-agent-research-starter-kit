# CNN/LeNet 图像分类

## 适用任务

当用户要求按照课件中的 CNN 案例训练、评估或预测手写数字图片时使用本说明。课程数据目录应使用 `data/CNN`，其中 `train` 和 `test` 下按类别文件夹 `0` 到 `9` 存放图片。

## 调用脚本

脚本：`scripts/paddle_image_cnn.py`

该脚本固定实现课件中的 LeNet 风格 CNN：

- 输入：灰度图，统一 resize 到 `28x28`
- 归一化：默认 `[0,255] -> [0,1]`
- 网络：`Conv2D -> ReLU -> MaxPool2D -> Conv2D -> ReLU -> MaxPool2D -> Linear -> Linear -> Linear`
- 输出：10 类数字标签，标签来自文件夹名

## 训练命令

```bash
python scripts/paddle_image_cnn.py train --train-dir "data/CNN/train" --test-dir "data/CNN/test" --output-dir "output/cnn_case/model" --epochs 1 --batch-size 128 --learning-rate 0.001
```

## 预测单张图片

```bash
python scripts/paddle_image_cnn.py predict --model-dir "output/cnn_case/model" --input "data/CNN/test/9/284.png" --output "output/cnn_case/predict_one.csv"
```

## 批量预测测试集

```bash
python scripts/paddle_image_cnn.py predict --model-dir "output/cnn_case/model" --input "data/CNN/test" --output "output/cnn_case/cnn_predictions.csv"
```

## 关键参数

- `--train-dir`：训练集根目录，子文件夹名为标签。
- `--test-dir`：测试集根目录，子文件夹名为标签；可选但建议提供。
- `--output-dir`：模型输出目录。
- `--epochs`：训练轮数。
- `--batch-size`：批大小。
- `--learning-rate`：学习率。
- `--image-size`：图片缩放尺寸，默认 `28`。

## 输出

模型目录包含：

- `model.pdparams`
- `labels.json`
- `config.json`
- `metrics.json`

预测输出 CSV 包含：

- `path`
- `predicted_label`
- `confidence`
- `true_label`，当输入是带标签子目录时生成
- `correct`，当可解析真实标签时生成

## 边界

该脚本只支持课件中的灰度数字图像 CNN 案例。如果用户要求 TextCNN 文本分类，本 reference 不适用。
