---
name: decision-tree-modeling
description: 提供决策树分类建模与超参数优化能力；当用户需要建立分类模型、优化模型参数、生成可视化决策树或输出完整建模报告时使用
dependency:
  python:
    - scikit-learn==1.3.0
    - pandas==2.0.3
    - numpy==1.24.3
    - matplotlib==3.7.2
    - openpyxl==3.1.2
    - joblib==1.3.1
---

# 决策树建模分析

## 任务目标
- 本 Skill 用于: 对CSV或Excel数据进行决策树分类建模，通过网格搜索交叉验证优化超参数
- 能力包含: 数据预处理、超参数优化、模型训练、性能评估、决策树可视化、特征重要性分析
- 触发条件: 用户需要建立分类模型、优化模型参数、生成可视化决策树、输出建模分析报告

## 操作步骤
1. 数据准备
   - 确认输入数据格式为CSV或Excel（.xlsx, .xls）
   - 识别目标列名称（分类标签列）
   - 验证特征列数据类型（数值型或可编码的分类变量）
   - 参见 [数据格式规范](references/data_format.md) 确保数据符合要求

2. 执行建模分析
   - 调用 `scripts/decision_tree_modeling.py` 进行建模
   - 必需参数:
     - `--input`: 输入数据文件路径
     - `--target`: 目标列名
   - 可选参数:
     - `--output_dir`: 输出目录（默认：./output）
     - `--test_size`: 测试集比例（默认：0.2）
     - `--cv_folds`: 交叉验证折数（默认：5）
     - `--random_state`: 随机种子（默认：42）
   - 示例命令:
     ```bash
     python scripts/decision_tree_modeling.py --input ./iris.csv --target species --output_dir ./output
     ```

3. 解读分析报告
   - 读取生成的评估报告：`output_dir/evaluation_report.json`
   - 查看决策树可视化：`output_dir/decision_tree.png`
   - 分析特征重要性：`output_dir/feature_importance.png`
   - 智能体基于脚本输出生成完整的建模分析报告

## 资源索引
- 核心脚本: [scripts/decision_tree_modeling.py](scripts/decision_tree_modeling.py) (完整的决策树建模流程，包含网格搜索和可视化)
- 数据格式: [references/data_format.md](references/data_format.md) (输入数据格式要求与示例)
- 报告模板: [references/model_report.md](references/model_report.md) (建模分析报告结构与内容)

## 注意事项
- 确保目标列包含分类标签（非数值型或离散数值型）
- 特征列应为数值型；如包含分类变量需先进行编码
- 输出目录会自动创建，包含模型文件、评估报告、可视化图片和预测结果
- 脚本会自动处理缺失值，建议检查数据质量
- 网格搜索可能耗时，根据数据量调整cv_folds参数

## 使用示例

### 示例1: 鸢尾花数据集分类
```bash
python scripts/decision_tree_modeling.py \
  --input ./iris.csv \
  --target species \
  --output_dir ./iris_output
```

### 示例2: 自定义交叉验证折数
```bash
python scripts/decision_tree_modeling.py \
  --input ./data.xlsx \
  --target category \
  --cv_folds 10 \
  --test_size 0.3
```

### 示例3: 固定随机种子以保证可复现性
```bash
python scripts/decision_tree_modeling.py \
  --input ./training_data.csv \
  --target class_label \
  --random_state 2024
```
