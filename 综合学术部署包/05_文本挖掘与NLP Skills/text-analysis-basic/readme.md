# 文本分析基础 Skill

本 skill 面向中文文本分析基础流程，参考当前课程中的 PDF 处理、jieba 分词、文本表示和文本相似度课件整理。

## 能力范围

- PDF 文字提取、PDF 表格提取
- jieba 分词、自定义词典、停用词过滤
- 词频统计、句频统计
- 词云图生成
- TF-IDF 特征提取
- Word2Vec 训练与词向量导出
- Sentence Embedding 句向量生成
- 文本相似度计算：BOW、TF-IDF、Jaccard、Word2Vec、Embedding

## 使用方式

AI 会先判断你的任务是否在本 skill 能力范围内。若支持，AI 会给出 plan，说明将使用哪个 reference 文件、哪个 Python 脚本、需要哪些参数和数据路径，然后通过命令行调用脚本完成任务。

## 项目结构

- `SKILL.md`：AI 读取入口，说明触发条件和工作规则。
- `readme.md`：用户预览入口，说明本 skill 的能力范围。
- `scripts/`：固定好的 Python 命令行脚本。
- `references/`：每个功能的调用说明，告诉 AI 应调用哪个脚本以及如何传参。

## 输入数据

常用输入为 `.txt`、`.csv`、`.xlsx`、`.pdf`。CSV/XLSX 需要明确文本列名，例如 `text`、`content`、`comment` 等。
