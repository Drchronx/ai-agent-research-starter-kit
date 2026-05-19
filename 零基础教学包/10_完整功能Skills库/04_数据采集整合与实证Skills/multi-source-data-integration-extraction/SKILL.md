---
name: multi-source-data-integration-extraction
description: Automatically merge scattered Excel and CSV files, normalize column names, and extract structured tables from PDF, HTML, TXT, or Markdown documents. Supports OCR for scanned PDFs. Use when the user wants 多源数据整合、Excel/CSV 自动合并、PDF 表格提取、年报表格提取、政策文件表格抽取、OCR 文字识别，or needs a directory of mixed tabular sources transformed into consolidated CSV outputs.
---

# Multi Source Data Integration Extraction

**位置**: `/root/.openclaw/skills/multi-source-data-integration-extraction`

## 功能特性

✅ **多源数据合并**: 自动合并 CSV/Excel 文件，标准化列名
✅ **PDF 表格提取**: 使用 PyMuPDF 提取 PDF 中的表格
✅ **OCR 支持**: 使用 PaddleOCR 识别扫描版 PDF 和图片中的文字/表格
✅ **HTML/TXT 表格**: 从网页和文本文件中提取结构化表格
✅ **来源追踪**: 保留每个数据行的来源文件和页码信息

## 快速开始

### 1. 安装依赖

```bash
pip install -r scripts/requirements.txt
```

依赖包括：
- `pandas`, `openpyxl` - Excel/CSV 处理
- `lxml`, `beautifulsoup4` - HTML 解析
- `pdfplumber`, `PyMuPDF` - PDF 处理
- `paddlepaddle`, `paddleocr` - OCR 文字识别

### 2. 基本用法

```bash
# 基本用法
python scripts/merge_extract_sources.py /path/to/data --output-dir /path/to/output

# 启用 OCR（用于扫描版 PDF）
python scripts/merge_extract_sources.py /path/to/data --output-dir /path/to/output --ocr
```

### 3. 输出文件

```
output/
├── merged_dataset.csv          # 合并后的数据集
├── extraction_manifest.json    # 提取清单（包含表格信息）
└── extracted_tables/
    ├── file1_table_1.csv       # 提取的表格 1
    ├── file1_table_2.csv       # 提取的表格 2
    └── file2_table_1.csv       # 提取的表格 3
```

## 支持的格式

| 格式 | 提取方式 | 说明 |
|------|----------|------|
| CSV | pandas | 直接读取合并 |
| Excel (.xlsx, .xls) | pandas + openpyxl | 读取所有工作表 |
| PDF | PyMuPDF | 提取标准表格 |
| PDF (扫描版) | PaddleOCR | OCR 识别（需 --ocr 参数） |
| HTML | pandas.read_html | 提取 HTML 表格 |
| TXT/MD | 正则解析 | 提取 `|` 或 Tab 分隔的表格 |

## 使用示例

### 示例 1: 合并多年 Excel 报表

```bash
python scripts/merge_extract_sources.py \
  ./annual_reports_2020-2024 \
  --output-dir ./merged_reports
```

### 示例 2: 提取 PDF 年报中的表格

```bash
python scripts/merge_extract_sources.py \
  ./company_reports \
  --output-dir ./extracted_tables
```

### 示例 3: 处理扫描版 PDF（启用 OCR）

```bash
python scripts/merge_extract_sources.py \
  ./scanned_documents \
  --output-dir ./ocr_output \
  --ocr
```

## 输出字段说明

合并后的数据集包含：
- 所有原始数据列
- `source_file`: 来源文件名
- `source_sheet_index`: Excel 工作表索引（如适用）

提取的表格清单 (`extraction_manifest.json`) 包含：
- `source_file`: 源文件名
- `table_index`: 表格序号
- `output_csv`: 输出文件名
- `rows`: 行数
- `columns`: 列数

## 注意事项

⚠️ **PDF 表格识别限制**:
- 标准 PDF（文字版）：PyMuPDF 可以准确提取表格结构
- 扫描版 PDF：需要 `--ocr` 参数，使用 PaddleOCR 识别
- 复杂表格（合并单元格等）：可能无法完美识别

⚠️ **OCR 性能**:
- 首次使用会自动下载模型（约 200MB）
- 建议使用 GPU 加速（如有 NVIDIA 显卡）
- CPU 模式下速度较慢但可用

⚠️ **内存使用**:
- 大文件处理时注意内存使用
- 建议分批处理超过 100 页的 PDF
