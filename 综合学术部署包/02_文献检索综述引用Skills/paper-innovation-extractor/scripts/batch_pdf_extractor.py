#!/usr/bin/env python3
"""
批量PDF论文文本提取器

功能：
1. 批量读取指定目录下的所有PDF文件
2. 提取每篇PDF的文本内容
3. 输出为JSON格式，包含文件名和提取的文本

依赖：
- pymupdf (fitz)
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any
import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    从PDF文件中提取文本内容

    Args:
        pdf_path: PDF文件路径

    Returns:
        提取的文本内容
    """
    try:
        doc = fitz.open(pdf_path)
        text_content = []

        for page in doc:
            page_text = page.get_text()
            if page_text.strip():
                text_content.append(page_text)

        doc.close()
        return "\n\n".join(text_content)
    except Exception as e:
        print(f"警告：无法提取文件 {pdf_path} 的内容，错误：{str(e)}", file=sys.stderr)
        return ""


def find_pdf_files(input_dir: str) -> List[str]:
    """
    查找指定目录下的所有PDF文件

    Args:
        input_dir: 输入目录路径

    Returns:
        PDF文件路径列表
    """
    input_path = Path(input_dir)
    if not input_path.exists():
        raise FileNotFoundError(f"目录不存在：{input_dir}")

    if not input_path.is_dir():
        raise NotADirectoryError(f"路径不是目录：{input_dir}")

    pdf_files = list(input_path.glob("*.pdf"))
    return [str(f) for f in pdf_files]


def batch_extract_pdfs(input_dir: str) -> Dict[str, Any]:
    """
    批量提取PDF文本

    Args:
        input_dir: PDF文件所在目录

    Returns:
        提取结果字典，包含成功和失败的文件列表
    """
    pdf_files = find_pdf_files(input_dir)

    if not pdf_files:
        print(f"警告：在目录 {input_dir} 中未找到PDF文件", file=sys.stderr)
        return {"papers": [], "errors": []}

    results = []
    errors = []

    for pdf_path in pdf_files:
        print(f"正在处理：{pdf_path}")
        filename = os.path.basename(pdf_path)
        text_content = extract_text_from_pdf(pdf_path)

        if text_content:
            results.append({
                "filename": filename,
                "filepath": pdf_path,
                "text": text_content,
                "length": len(text_content)
            })
            print(f"  ✓ 提取成功，文本长度：{len(text_content)} 字符")
        else:
            errors.append({
                "filename": filename,
                "filepath": pdf_path,
                "error": "提取失败或内容为空"
            })
            print(f"  ✗ 提取失败")

    return {
        "papers": results,
        "errors": errors,
        "total": len(pdf_files),
        "success": len(results),
        "failed": len(errors)
    }


def main():
    parser = argparse.ArgumentParser(
        description="批量提取PDF论文的文本内容",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python batch_pdf_extractor.py --input-dir ./
  python batch_pdf_extractor.py --input-dir ./papers/
  python batch_pdf_extractor.py --input-dir ./ --output extracted_papers.json
        """
    )

    parser.add_argument(
        "--input-dir",
        type=str,
        default="./",
        help="PDF文件所在目录（默认：当前目录）"
    )

    parser.add_argument(
        "--output",
        type=str,
        default="extracted_papers.json",
        help="输出JSON文件路径（默认：extracted_papers.json）"
    )

    args = parser.parse_args()

    print(f"开始批量提取PDF文本...")
    print(f"输入目录：{args.input_dir}")
    print(f"输出文件：{args.output}")
    print("-" * 60)

    try:
        result = batch_extract_pdfs(args.input_dir)

        print("-" * 60)
        print(f"提取完成！")
        print(f"总计：{result['total']} 个PDF文件")
        print(f"成功：{result['success']} 个")
        print(f"失败：{result['failed']} 个")

        if result['errors']:
            print("\n失败的文件：")
            for error in result['errors']:
                print(f"  - {error['filename']}: {error['error']}")

        # 保存结果到JSON文件
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"\n提取结果已保存到：{args.output}")

        return 0

    except Exception as e:
        print(f"错误：{str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
