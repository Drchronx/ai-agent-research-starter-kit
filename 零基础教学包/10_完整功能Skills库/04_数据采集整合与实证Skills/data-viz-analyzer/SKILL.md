---
name: data-viz-analyzer
description: 对CSV或Excel数据进行全面的可视化分析，包括描述性统计、相关性分析、特征分布图和热力图，并生成HTML格式的交互式分析报告；当用户需要数据分析、数据可视化、探索性数据分析或生成数据报告时使用
dependency:
  python:
    - pandas>=1.3.0
    - numpy>=1.21.0
    - matplotlib>=3.4.0
    - seaborn>=0.11.0
    - openpyxl>=3.0.0
    - jinja2>=3.0.0
---

# 数据可视化分析

## 任务目标
- 本 Skill 用于：对用户上传的 CSV 或 Excel 数据进行全面的可视化分析
- 能力包含：描述性统计分析、相关性分析、特征分布可视化、相关性热力图、HTML 报告生成
- 触发条件：用户提供数据文件并要求数据分析、数据可视化、探索性分析或生成分析报告

## 前置准备
- 依赖说明：scripts 脚本所需的依赖包及版本
  ```
  pandas>=1.3.0
  numpy>=1.21.0
  matplotlib>=3.4.0
  seaborn>=0.11.0
  openpyxl>=3.0.0
  jinja2>=3.0.0
  ```

## 操作步骤

### 步骤 1：数据验证与加载
- 智能体首先验证用户上传的文件格式（支持 .csv、.xlsx、.xls）
- 检查文件是否存在且可读取
- 调用 `scripts/data_visualizer.py` 加载数据并进行初步验证
- 如果数据格式不符合要求，提示用户参考 [references/input_format.md](references/input_format.md)

### 步骤 2：执行可视化分析
- 调用脚本执行完整的数据分析流程：
  ```bash
  python /workspace/projects/data-viz-analyzer/scripts/data_visualizer.py <input_file> --output <output_dir>
  ```
- 脚本将自动完成：
  1. 描述性统计分析（均值、中位数、标准差、分位数等）
  2. 相关性分析（计算特征间的相关系数矩阵）
  3. 特征分布可视化（直方图、箱线图）
  4. 相关性热力图生成
  5. HTML 报告生成

### 步骤 3：查看分析结果
- 脚本执行完成后，在指定的输出目录生成：
  - `data_analysis_report.html`：交互式分析报告
  - `figures/`：所有可视化图表（PNG 格式）
- 智能体向用户展示报告关键内容并解释分析结果

### 步骤 4：结果解读与建议
- 智能体根据分析结果提供：
  - 数据质量评估（缺失值、异常值情况）
  - 特征分布特征解读
  - 相关性发现与业务洞察
  - 后续分析建议

## 资源索引
- 核心脚本：见 [scripts/data_visualizer.py](scripts/data_visualizer.py)（用途：执行完整的数据分析和可视化流程）
- 输入规范：见 [references/input_format.md](references/input_format.md)（何时读取：数据格式不符合要求或需要了解输入规范时）

## 注意事项
- 数据文件大小建议不超过 100MB，过大的文件可能导致处理缓慢
- 确保数据文件编码为 UTF-8 或 GBK，避免中文乱码
- 数值型特征至少需要 2 个才能进行相关性分析
- 如果数据包含大量缺失值，建议先进行数据清洗
- 生成的 HTML 报告包含所有图表的 Base64 编码，可直接在浏览器中打开查看
- **字体支持**：脚本会自动检测系统中的中文字体（WenQuanYi、Noto Sans CJK、SimHei等），确保中文正常显示

## 使用示例

### 示例 1：分析销售数据
```bash
python /workspace/projects/data-viz-analyzer/scripts/data_visualizer.py ./sales_data.csv --output ./analysis_results
```
输出：包含销售额、利润、客户数等特征的分布图和相关性分析的 HTML 报告

### 示例 2：分析用户行为数据
```bash
python /workspace/projects/data-viz-analyzer/scripts/data_visualizer.py ./user_behavior.xlsx --output ./user_analysis
```
输出：用户活跃度、留存率、转化率等指标的统计分析和可视化报告

### 示例 3：指定输出目录
```bash
python /workspace/projects/data-viz-analyzer/scripts/data_visualizer.py ./data.csv --output ./my_report
```
输出：分析报告保存在 `./my_report/data_analysis_report.html`
