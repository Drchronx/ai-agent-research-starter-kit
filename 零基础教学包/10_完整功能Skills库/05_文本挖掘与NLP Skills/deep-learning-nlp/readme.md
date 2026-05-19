# 深度学习 Skill

本 skill 参考当前课程中的 Paddle 深度学习课件整理，将 DNN、CNN、RNN 三类常用方法固定为可重复调用的文本分类脚本。

## 能力范围

- DNN 文本分类：Embedding + 平均池化 + 多层全连接。
- CNN 图像分类：使用课程 `data/CNN` 手写数字图片目录，训练 LeNet 风格卷积神经网络。
- RNN 文本分类：Embedding + GRU + 分类层。

## 使用方式

AI 会先判断任务属于 DNN、CNN 还是 RNN，并给出 plan，说明使用哪个 reference 文件、脚本、输入列、训练参数、模型保存路径和预测输出路径。随后 AI 通过命令行调用固定脚本，不临时编写训练代码。

## 项目结构

- `SKILL.md`：AI 读取入口。
- `readme.md`：用户预览入口。
- `scripts/`：固定 Python 训练/预测脚本。
- `references/`：DNN、CNN、RNN 的调用说明。

## 输入数据

训练数据需要文本列和标签列。预测数据可以是 TXT、CSV 或 XLSX，CSV/XLSX 需要文本列。
