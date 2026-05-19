# 情感分析 Skill

本 skill 参考当前课程中的情感分析课件整理，面向中文文本的情绪倾向识别。

## 能力范围

- 词典法：正向词、负向词、带分值情感词典。
- 机器学习法：TF-IDF + Logistic Regression / SVM / Naive Bayes / Random Forest。
- 大模型调用法：通过 OpenAI-compatible API 批量判断情感标签。

## 使用方式

AI 会先判断任务属于哪一种情感分析方法，并给出 plan，说明将使用的 reference 文件、脚本、输入列、词典或模型路径、输出路径。随后 AI 通过命令行调用固定脚本，不临时编写分析代码。

## 项目结构

- `SKILL.md`：AI 读取入口。
- `readme.md`：用户预览入口。
- `scripts/`：固定 Python 脚本。
- `references/`：每种方法的调用说明。

## 输入数据

预测任务需要文本列。机器学习训练任务需要文本列和标签列。词典法需要提供情感词典路径，或使用课程目录中的情感词典文件。
