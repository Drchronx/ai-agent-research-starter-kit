# Python 实证分析 Skill

这是一个面向论文复现、实证研究、机器学习、因果推断和应用计量分析的 Python Skill。它的核心目标是：让 AI 不再临时“手搓”分析代码，而是通过已经写好的固定脚本完成清洗、特征工程、监督学习建模、因果识别、稳健性检验、异质性分析、表格和图片输出。

所有可执行代码都放在 `scripts/` 目录。`SKILL.md` 和 `references/*.md` 只负责告诉 AI 应该调用哪个脚本、传入哪些参数、检查哪些结果。

## 它能做什么

### 1. 数据清洗与变量构造

- 读取 CSV、Excel、Parquet、JSON、Stata 等常见数据文件。
- 检查缺失值、重复值、样本筛选和关键变量完整性。
- 做字符串清理、类型转换、去重、样本流失记录。
- 构造 log、IHS、winsorize、标准化、dummy、lag、lead、diff、事件时间等变量。

对应脚本：

- `scripts/clean_data.py`
- `scripts/transform_data.py`

### 2. 描述性统计与诊断

- 生成 Table 1 描述性统计。
- 生成处理组/控制组 balance table。
- 输出分类变量频数、相关系数矩阵、趋势图和热力图。
- 做残差正态性、异方差、自相关、条件数和 VIF 多重共线性诊断。

对应脚本：

- `scripts/describe_data.py`
- `scripts/run_diagnostics.py`

### 3. 机器学习基础工作流

- 支持监督学习的标准流程：构造特征矩阵 X 和目标向量 y。
- 支持训练集、验证集、测试集划分。
- 支持简单缺失值处理、类别变量 one-hot 编码、数值变量标准化。
- 支持回归任务和分类任务。
- 回归评价指标：MAE、MSE、RMSE、R²。
- 分类评价指标：准确率、精确率、召回率、F1、ROC AUC。

对应脚本：

- `scripts/prepare_ml_data.py`
- `scripts/run_supervised_ml.py`

### 4. 常见机器学习模型

- 线性回归：`LinearRegression`。
- 惩罚性回归：`Ridge`、`Lasso`。
- 弹性网络：`ElasticNet`，支持 L1 + L2 混合正则。
- 树模型：决策树、随机森林、梯度提升树 GBDT。
- 分类模型：Logistic、决策树、随机森林、GBDT。
- 输出模型指标、预测结果、系数表、非零特征、特征重要性和特征效果图。

对应脚本：

- `scripts/run_supervised_ml.py`

### 5. 经典计量模型

- OLS、Logit、Probit、Poisson。
- 多列渐进回归表。
- 固定效应公式、聚类标准误、稳健标准误。
- Panel FE、TWFE、between、first-difference、random effects。
- IV、2SLS、LIML、GMM，并尽量输出一阶段和过度识别诊断。

对应脚本：

- `scripts/run_model.py`
- `scripts/run_panel.py`
- `scripts/run_iv.py`

### 6. 准实验与因果推断

- DID、TWFE DID、事件研究、pretrend test。
- Sharp RD、Fuzzy RD、带宽稳健性和 RD 图。
- 倾向得分 IPW、最近邻匹配、协变量平衡和 love plot。
- Synthetic Control，输出 donor weights、treated-vs-synthetic trajectory 和 gap。
- DML / Double Machine Learning，固定调用 `econml.dml.LinearDML`。
- CATE：T-learner、S-learner、`econml` causal forest。

对应脚本：

- `scripts/run_did.py`
- `scripts/run_rd.py`
- `scripts/run_matching.py`
- `scripts/run_synth.py`
- `scripts/run_dml.py`
- `scripts/run_cate.py`

### 7. 稳健性、敏感性和进一步分析

- 替换控制变量、替换聚类层级、子样本、placebo、specification-style 稳健性表。
- Oster delta。
- E-value。
- Randomization inference。
- 机制分析、异质性分析、简单 mediation。
- Kaplan-Meier、Cox、Weibull AFT 生存分析。

对应脚本：

- `scripts/run_robustness.py`
- `scripts/run_sensitivity.py`
- `scripts/run_further_analysis.py`
- `scripts/run_survival.py`

### 8. 论文级输出

- 回归结果整理成宽表。
- 显著性星号、标准误括号、CSV/XLSX/LaTeX 多格式导出。
- 可以直接导出 LaTeX 三线表。
- coefficient plot、event-study plot、binscatter、love plot。
- 汇总所有表格和图片，生成 artifact manifest。

对应脚本：

- `scripts/table_factory.py`
- `scripts/plot_factory.py`
- `scripts/render_manifest.py`

## 怎么使用

让 AI 先读 `SKILL.md`，再根据任务读 `references/method-index.md` 或对应 reference 文件。用户只需要用自然语言描述研究设计、变量名和数据位置，AI 应该选择固定脚本并传参执行。

常见入口：

- 数据清洗：`python scripts/clean_data.py --help`
- 变量构造：`python scripts/transform_data.py --help`
- 机器学习数据准备：`python scripts/prepare_ml_data.py --help`
- 监督学习模型：`python scripts/run_supervised_ml.py --help`
- 描述统计：`python scripts/describe_data.py --help`
- 主回归：`python scripts/run_model.py --help`
- Panel：`python scripts/run_panel.py --help`
- DID / Event Study：`python scripts/run_did.py --help`
- IV：`python scripts/run_iv.py --help`
- RD：`python scripts/run_rd.py --help`
- Matching / IPW：`python scripts/run_matching.py --help`
- Synthetic Control：`python scripts/run_synth.py --help`
- DML：`python scripts/run_dml.py --help`
- CATE：`python scripts/run_cate.py --help`
- Robustness：`python scripts/run_robustness.py --help`
- Sensitivity：`python scripts/run_sensitivity.py --help`
- Survival：`python scripts/run_survival.py --help`
- 表格整理：`python scripts/table_factory.py --help`
- 图片生成：`python scripts/plot_factory.py --help`

也可以使用兼容调度入口 `scripts/empirical_cli.py`，但优先建议直接调用具体脚本，因为每个脚本的职责更清晰。

## 典型产物

- `table1_summary`：描述性统计表。
- `table1_balance`：平衡性检验表。
- `table2_main` / `table2_main_tidy`：主回归表。
- `ml_dataset_split`：机器学习训练/验证/测试划分数据。
- `ml_metrics`：机器学习回归或分类指标。
- `ml_predictions`：机器学习预测结果。
- `ml_feature_effects`：线性模型系数、ElasticNet/Lasso 非零特征或树模型特征重要性。
- `panel_results`：面板模型结果。
- `did_results`：DID 和事件研究结果。
- `iv_results`：工具变量结果。
- `rd_results`：断点回归结果。
- `matching_effects`：匹配和 IPW 估计结果。
- `synthetic_trajectory`：合成控制轨迹。
- `dml_results`：双重机器学习结果。
- `cate_summary`：异质性处理效应汇总。
- `table5_robustness`：稳健性检验表。
- `sensitivity_results`：敏感性分析表。
- `artifact_manifest.json` / `artifact_manifest.md`：最终产物索引。

## 设计原则

- 代码固定：实证流程通过 `scripts/*.py` 执行，不在 markdown 中临时写 Python。
- 功能解耦：每类方法都有独立脚本，避免一个大脚本塞所有功能。
- 参数驱动：通过变量名、公式、控制变量、固定效应、聚类变量、输出路径等参数改变分析。
- 结果可追溯：脚本会输出 manifest，记录输入、参数、公式和产物路径。
- reference 只做教学：`references/*.md` 解释什么时候用哪个脚本，不承载可执行实现。

## 依赖边界

基础清洗、描述统计、监督学习、LinearRegression、Ridge、Lasso、ElasticNet、决策树、随机森林、GBDT、OLS、DID、RD、matching、SCM 基础实现、表格和绘图主要依赖 pandas、numpy、statsmodels、scikit-learn、matplotlib 等常见包。

部分高级方法需要额外依赖：

- `linearmodels`：更完整的 IV、LIML、GMM、Random Effects。
- `econml`：DML 和 causal forest。
- `lifelines`：Cox 和 Weibull AFT 生存模型。
- `python-docx`：导出 Word 表格。

如果依赖不存在，脚本应给出明确错误或使用已实现的降级路径，而不是让 AI 在 markdown 里重新编写分析代码。
