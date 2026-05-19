# 主题建模 Skill

本 skill 参考当前课程的主题建模课件整理，提供 LDA、DTM、BERTopic 三类主题模型的固定命令行流程。

## 能力范围

- LDA：中文语料清洗、繁简转换、jieba 分词、停用词过滤、已分词列解析、gensim TF-IDF 语料构建、候选主题数诊断、困惑度和一致性评估、指标图、候选主题词和 pyLDAvis 材料；默认采用 `alpha=50/K`、`eta=0.01` 这一课件与文献常用的先验设定。困惑度图按课件口径绘制 gensim `log_perplexity()` 原值，判断时 `log_perplexity` 越高越好，换算后的 `perplexity` 越低越好，由用户确认主题数后再训练最终模型。
- DTM：按时间列建模主题演化，导出不同时间片的主题词。
- BERTopic：使用 sentence-transformers + BERTopic 进行语义主题建模。

## 使用方式

AI 会先判断你的任务属于 LDA、DTM 还是 BERTopic，并给出 plan，说明使用哪个 reference 文件、哪个脚本、输入列、参数和输出目录。LDA 的主题数选择会先生成诊断材料，让用户确认最终主题数后再继续训练最终模型。随后 AI 通过命令行调用固定脚本，不临时编写建模代码。

## 项目结构

- `SKILL.md`：AI 读取入口。
- `readme.md`：用户预览入口。
- `scripts/`：固定 Python 脚本。
- `references/`：每类主题模型的调用说明。

## 输入数据

LDA 和 BERTopic 需要文本列。DTM 需要文本列和时间列，时间列会按排序后的唯一值形成时间片。
