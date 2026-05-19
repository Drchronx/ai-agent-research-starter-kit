---
name: empirical-paper-writer
description: 依据实证论文的规范结构与写作风格生成学术论文；适用于生成金融、经济、会计等领域的研究论文框架与正文内容
dependency:
  python:
    - requests==2.28.0
---

# Empirical Paper Writer

## 任务目标

依据实证论文的规范结构与写作风格，生成符合学术期刊要求的完整论文框架与正文内容。

## 前置准备

- 明确研究主题与核心假设
- 收集相关文献与数据集信息
- 确认目标期刊格式要求

## 论文结构框架

### 1. 标题页 (Title Page)

**要求**:
- 标题:简洁、准确反映研究核心贡献，控制在20词以内
- 作者信息:姓名、单位、通讯地址、ORCID(可选)
- 脚注:致谢、基金项目、数据可用性说明

**生成指南**:
1. 主标题应体现研究方法(如:Machine Learning、Regression、Panel Data)
2. 使用冒号分隔主副标题(如:Title: Subtitle)
3. 避免使用问句或感叹句

### 2. 摘要 (Abstract)

**规范**:
- 篇幅:150-300词(金融顶刊如RFS、JFE通常250词)
- 结构:研究问题 → 方法 → 主要发现 → 经济含义
- 禁止:公式、参考文献、缩写首次使用不解释

**模板句式**:
```
We study/conduct/investigate [RESEARCH QUESTION]. Using [METHODOLOGY] 
on [DATA SAMPLE], we find that [KEY FINDING]. [ECONOMIC IMPLICATION].
```

### 3. 引言 (Introduction)

**标准结构**:
```
3.1 研究背景与问题 (Research Motivation)
    - 阐述领域核心问题
    - 引用2-3篇经典文献说明研究缺口
    
3.2 研究贡献 (Main Contributions)
    - 理论贡献
    - 方法贡献
    - 实证贡献
    - 实践贡献
    
3.3 论文结构 (Paper Organization)
    - "Section 2 describes... Section 3 presents... Section 4 concludes..."
```

**写作要点**:
- 引言必须回答"为什么研究这个问题"
- 明确列出3-4个具体贡献点
- 控制在1500-3000词

### 4. 文献综述 (Literature Review)

**组织方式**:
```
4.1 [领域主题A]
    - 研究现状
    - 研究空白
    
4.2 [领域主题B]
    - 研究现状
    - 研究空白
```

**注意事项**:
- 按主题而非按作者组织
- 识别研究争议与空白
- 引用最新文献(近5年)与经典文献结合
- 结尾必须过渡到本文研究

### 5. 方法论 (Methodology)

**必要组成部分**:
```
5.1 数据与样本 (Data and Sample)
    - 数据来源
    - 样本选择标准
    - 变量定义
    - 描述性统计
    
5.2 研究设计 (Research Design)
    - 理论框架
    - 模型设定
    - 识别策略
    
5.3 估计方法 (Empirical Methodology)
    - 基准模型
    - 稳健性检验
    - 内生性处理
```

**数学公式规范**:
- 公式居中编号右对齐:式(1)
- 变量首次出现必须定义
- 使用标准符号约定

### 6. 实证结果 (Empirical Results)

**结构模板**:
```
6.1 基准回归 (Baseline Results)
6.2 经济显著性 (Economic Significance)
6.3 稳健性检验 (Robustness Checks)
    - 替代变量
    - 子样本分析
    - 方法稳健性
6.4 内生性分析 (Endogeneity)
```

**结果呈现**:
- 表格优先于文字
- 文字说明核心发现
- 标注统计显著性:*** p<0.01, ** p<0.05, * p<0.1
- 系数解释需结合经济含义

### 7. 结论 (Conclusion)

**结构**:
```
7.1 研究总结
7.2 理论贡献
7.3 实践启示
7.4 研究局限与未来方向
```

## 写作风格规范

### 语言要求

**推荐表达**:
- "We find that..." / "Our results indicate..."
- "Consistent with theory..."
- "However, we acknowledge..."
- "Interestingly, we observe..."

**避免表达**:
- 绝对化:"proves"/"demonstrates conclusively"
- 非正式表达:"a lot"/"very important"
- 模糊表述:"may or might"/"could be"

### 段落结构

**标准段落(5-7句)**:
1. 主题句(核心论点)
2. 背景/上下文
3. 具体证据
4. 分析解释
5. 过渡句

### 引用规范

**文中引用**:
- 单作者:(Smith 2020)
- 两作者:(Smith and Jones 2020)
- 三位及以上:(Smith et al. 2020)
- 直接引用:需注明页码

### 表格与图形

**表格规范**:
- 表标题在上方
- 列标题清晰，标注单位
- 脚注说明数据来源、变量定义
- 使用***/**/*标注显著性

**图形规范**:
- 图标题在下方
- 轴标签清晰
- 图例完整
- 配色专业(避免红绿组合)

## 特殊格式要求

### 金融学论文特殊规范

- R²报告为百分比形式:0.16%而非0.0016
- Sharpe Ratio保留两位小数
- 显著性标注通常为***/**/* 或加粗

### 实证资产定价论文模板

见 [references/asset_pricing_template.md](references/asset_pricing_template.md)

## 使用示例

### 示例1:生成论文框架

**输入**:
研究主题:机器学习在资产定价中的应用
研究假设:神经网络预测股票收益优于线性模型
数据类型:CRSP股票收益数据，1957-2020

**生成步骤**:
1. 生成标题页(参考Abstract模板)
2. 编写引言(动机+贡献结构)
3. 设计方法论(参考Methodology章节)
4. 构建实证结果框架

### 示例2:完善已有框架

**输入**:
已有Introduction草稿，需要润色

**操作**:
1. 检查引言是否包含全部必要元素
2. 调整贡献表述的精确性
3. 优化段落衔接

## 资源索引

- 脚本:无(纯自然语言指导)
- 参考:见 [references/asset_pricing_template.md](references/asset_pricing_template.md)(实证资产定价论文完整模板)
- 资产:无

## 注意事项

- 首次生成建议先生成完整框架，再逐章节填充
- 方法论章节需要具体变量定义和模型设定
- 实证结果必须包含基准结果和稳健性检验
- 结论需平衡贡献与局限性
