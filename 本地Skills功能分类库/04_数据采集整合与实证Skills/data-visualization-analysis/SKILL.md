---
name: data-visualization-analysis
description: 对CSV/Excel数据进行全面的统计描述、相关性分析和可视化；当用户需要数据分析、数据探索、统计摘要、特征分布分析或相关性分析时使用
dependency:
  python:
    - pandas>=2.0.0
    - numpy>=1.24.0
    - matplotlib>=3.7.0
    - seaborn>=0.12.0
    - openpyxl>=3.1.0
---

# 数据可视化分析 Skill

## 任务目标
- 本 Skill 用于对用户上传的 CSV 或 Excel 数据进行全面的统计分析和可视化
- 能力包含：描述性统计、相关性分析、特征分布可视化、相关性可视化
- 触发条件：用户上传数据文件并请求"数据分析"、"统计描述"、"相关性分析"、"数据可视化"等

## 前置准备
- 依赖说明：scripts脚本所需的依赖包及版本
  ```
  pandas>=2.0.0
  numpy>=1.24.0
  matplotlib>=3.7.0
  seaborn>=0.12.0
  openpyxl>=3.1.0
  ```

## 操作步骤

### 标准流程

**步骤1：数据验证**
- 确认用户上传的数据文件格式（.csv、.xlsx、.xls）
- 检查文件路径是否正确
- 如果数据格式不符合要求，提示用户参考 [references/input_format.md](references/input_format.md) 修正

**步骤2：执行数据分析**
调用 `scripts/analyze_data.py` 脚本执行全面分析：

```bash
python /workspace/projects/data-visualization-analysis/scripts/analyze_data.py \
  --input_file <用户数据文件路径> \
  --output_dir <输出目录路径>
```

**参数说明**：
- `--input_file`：必需，CSV或Excel文件的完整路径
- `--output_dir`：可选，分析结果输出目录，默认为 `./analysis_output`
- `--target_column`：可选，目标变量列名（用于重点分析相关性）

**步骤3：查看HTML报告**
脚本执行完成后，会生成一个完整的HTML分析报告文件：
- `analysis_report.html` - 包含所有统计结果、图表和分析的HTML报告

**步骤4：智能解读与洞察**
智能体基于HTML报告内容提供：
- 数据质量评估（缺失值、异常值情况）
- 关键统计指标解读（均值、中位数、标准差等）
- 特征分布特征分析（偏态、峰度、异常值）
- 相关性模式识别（强相关、弱相关、负相关）
- 业务建议和后续分析方向
- 用户可以直接在浏览器中打开HTML报告查看所有可视化图表

### 可选分支

**场景A：用户指定目标变量**
- 添加 `--target_column` 参数
- 脚本会额外生成目标变量与其他特征的相关性排序图

**场景B：大数据集优化**
- 当数据行数超过10万行时，脚本自动采用采样策略
- 提示用户数据集较大，部分可视化采用采样方式

**场景C：非数值型数据处理**
- 自动识别非数值型特征（分类、文本等）
- 对分类特征生成频数统计和柱状图
- 相关性分析仅针对数值型特征

## 资源索引
- 分析脚本：[scripts/analyze_data.py](scripts/analyze_data.py)（主分析程序，处理数据读取、统计计算、可视化生成、HTML报告输出）
- 输入格式规范：[references/input_format.md](references/input_format.md)（数据文件格式要求和示例）
- 输出说明：[references/output_description.md](references/output_description.md)（HTML报告的结构和内容说明）

## 注意事项
- 脚本会自动配置中文字体支持，确保HTML报告中的图表正确显示中文
- HTML报告使用响应式设计，可在桌面和移动设备上良好显示
- 所有图表以base64编码嵌入HTML，生成单个文件便于分享和存档
- 对于包含中文的数据文件，脚本会自动处理编码问题
- 大数据集（>10万行）可能需要较长处理时间，建议提前告知用户

## 使用示例

**示例1：基础分析**
```bash
python /workspace/projects/data-visualization-analysis/scripts/analyze_data.py \
  --input_file ./sales_data.csv
```

**示例2：指定目标变量**
```bash
python /workspace/projects/data-visualization-analysis/scripts/analyze_data.py \
  --input_file ./customer_data.xlsx \
  --target_column purchase_amount \
  --output_dir ./my_analysis
```

**示例3：智能体解读流程**
1. 调用脚本执行分析
2. 在浏览器中打开 `analysis_report.html` 查看完整报告
3. 读取HTML报告中的统计表格和可视化图表
4. 分析相关性热力图识别相关特征
5. 检查特征分布图理解数据分布特征
6. 综合所有信息向用户提供业务洞察
