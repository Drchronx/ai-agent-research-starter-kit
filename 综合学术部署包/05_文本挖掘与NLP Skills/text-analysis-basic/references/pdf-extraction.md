# PDF 文字和表格提取

## 适用任务

当用户要求从 PDF 中提取文字、按页抽取文字、从文字版 PDF 中提取表格时使用本说明。

## 调用脚本

脚本：`scripts/pdf_extract.py`

## 常用命令

提取全文：

```bash
python scripts/pdf_extract.py --input "input.pdf" --output "output.txt" --mode text
```

提取指定页文字：

```bash
python scripts/pdf_extract.py --input "input.pdf" --output "output.txt" --mode text --pages 1-3,5
```

提取表格：

```bash
python scripts/pdf_extract.py --input "input.pdf" --output "tables_dir" --mode tables
```

同时提取文字和表格：

```bash
python scripts/pdf_extract.py --input "input.pdf" --output "extract_dir" --mode both
```

## 参数

- `--input`：PDF 路径。
- `--output`：文字模式为 `.txt` 文件路径；表格或 both 模式为输出文件夹。
- `--mode`：`text`、`tables`、`both`。
- `--pages`：可选，1 基页码，例如 `1-3,5`。

## 边界

该脚本处理文字版 PDF 和可被 `pdfplumber` 识别的表格。扫描件 OCR 不在本脚本范围内，需要另行使用 OCR 工具。
