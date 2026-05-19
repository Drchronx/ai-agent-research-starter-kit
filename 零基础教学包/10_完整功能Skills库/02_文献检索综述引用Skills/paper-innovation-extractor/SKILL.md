---
name: paper-innovation-extractor
description: 批量提取PDF论文的创新点并生成结构化markdown文档；当用户需要分析学术论文、总结研究贡献或整理技术要点时使用
dependency:
  python:
    - pymupdf>=1.23.0
---

# 论文创新点提取器

## 任务目标
- 本 Skill 用于：批量处理用户上传的多个PDF论文文件，提取每篇论文的创新点并生成结构化markdown文档
- 能力包含：批量PDF文本提取、创新点识别与分析、结构化markdown输出
- 触发条件：用户上传多篇学术论文PDF并要求提取创新点、总结研究贡献或整理技术要点

## 前置准备
- 依赖说明：scripts脚本所需的依赖包及版本
  ```
  pymupdf>=1.23.0
  ```
- 非标准文件/文件夹准备：如果Skill执行过程中需要使用除「Skill固定结构」外的文件或文件夹，需前置创建。当前路径视为相对于Skill目录的父目录
  ```bash
  # 无需额外创建，用户上传的PDF文件位于当前目录(.)
  ```

## 操作步骤
- 标准流程：
  1. 批量提取PDF文本
     - 调用 `scripts/batch_pdf_extractor.py` 提取所有PDF文件的文本内容
     - 参数：`--input-dir` 指定PDF文件所在目录（默认当前目录 `./`）
     - 输出：JSON格式的文本提取结果，包含每篇论文的文件名和文本内容

  2. 分析创新点
     - 根据 [references/innovation_extraction_guide.md](references/innovation_extraction_guide.md) 中的指导，智能体将：
       - 逐篇阅读提取的论文文本
       - 识别论文的研究问题、方法和结论
       - 提取核心创新点（方法论创新、数据创新、结论创新、应用创新等）

  3. 生成markdown文档
     - 将所有论文的创新点汇总到一个markdown文件中
     - 每篇论文的创新点整理为一段话（约500字）
     - 包含论文标题和完整的创新点描述

- 可选分支：
  - 当 需要汇总多篇论文：生成汇总文档，对比各论文创新点的异同
  - 当 需要分篇输出：为每篇论文生成独立的markdown文件

## 资源索引
- 必要脚本：见 [scripts/batch_pdf_extractor.py](scripts/batch_pdf_extractor.py)(用途与参数：批量提取PDF文件文本，支持自定义输入目录)
- 领域参考：见 [references/innovation_extraction_guide.md](references/innovation_extraction_guide.md)(何时读取：执行创新点分析时，识别创新点类型和维度)
- 输出资产：见 [assets/markdown_template.md](assets/markdown_template.md)(直接用于生成/修饰输出：提供创新点段落式整理的输出格式)

## 注意事项
- 仅在需要时读取参考，保持上下文简洁。
- 创新点提取应基于论文原文，避免主观臆断。
- 对于技术性细节，优先提取方法论和实现层面的创新。
- 充分利用智能体的语言理解和推理能力，避免为简单任务编写脚本。

## 使用示例
### 示例1：批量处理当前目录下的所有PDF
```bash
# 提取当前目录下所有PDF文件的文本
python scripts/batch_pdf_extractor.py --input-dir ./

# 智能体分析提取结果并生成创新点总结
# 输出文件：innovation_summary.md（所有论文创新点汇总）
```

### 示例2：处理指定目录下的PDF
```bash
# 提取指定目录的PDF文本
python scripts/batch_pdf_extractor.py --input-dir ./papers/

# 生成创新点文档，每篇论文一段话，约500字
# 输出文件：innovation_summary.md
```

### 示例3：自定义输出文件名
```python
# 调用脚本提取文本
# 智能体汇总所有论文的创新点到一个文件
# 输出文件：papers_innovation.md
```
