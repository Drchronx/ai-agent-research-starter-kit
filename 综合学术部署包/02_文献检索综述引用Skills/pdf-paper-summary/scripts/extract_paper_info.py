#!/usr/bin/env python3
"""
PDF论文信息提取脚本
功能:从PDF学术论文中提取标题、作者、单位、期刊信息和全文文本
"""

import sys
import json
import re
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    print(json.dumps({
        "error": "缺少pypdf库，请运行: pip install pypdf==5.1.0"
    }))
    sys.exit(1)


def extract_paper_info(pdf_path: str) -> dict:
    """
    从PDF论文中提取结构化信息

    Args:
        pdf_path: PDF文件路径

    Returns:
        包含提取信息的字典
    """
    result = {
        "title": "",
        "authors": [],
        "affiliations": [],
        "journal": "",
        "publish_date": "",
        "pages": "",
        "full_text": "",
        "abstract": "",
        "error": None
    }

    try:
        reader = PdfReader(pdf_path)

        # 提取元数据
        if reader.metadata:
            result["title"] = reader.metadata.get("/Title", "")
            result["author"] = reader.metadata.get("/Author", "")

        # 提取第一页内容用于获取标题和作者信息
        first_page_text = ""
        if len(reader.pages) > 0:
            first_page_text = reader.pages[0].extract_text()

        # 提取全文文本
        full_text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n\n"

        result["full_text"] = full_text.strip()
        result["page_count"] = len(reader.pages)

        # 解析第一页内容提取标题、作者、单位
        title, authors, affiliations = parse_first_page(first_page_text, result["title"])
        result["title"] = title or result["title"]
        result["authors"] = authors
        result["affiliations"] = affiliations

        # 提取摘要
        result["abstract"] = extract_abstract(full_text)

        # 尝试从全文中提取期刊信息和发表日期
        journal_info = extract_journal_info(full_text)
        result["journal"] = journal_info.get("journal", "")
        result["publish_date"] = journal_info.get("date", "")
        result["pages"] = journal_info.get("pages", "")

    except FileNotFoundError:
        result["error"] = f"文件未找到: {pdf_path}"
    except Exception as e:
        result["error"] = f"解析PDF时出错: {str(e)}"

    return result


def parse_first_page(text: str, metadata_title: str) -> tuple:
    """
    解析第一页内容，提取标题、作者、单位

    Args:
        text: 第一页文本内容
        metadata_title: PDF元数据中的标题

    Returns:
        (标题, 作者列表, 单位列表)
    """
    lines = text.strip().split("\n")
    lines = [line.strip() for line in lines if line.strip()]

    title = ""
    authors = []
    affiliations = []

    # 如果有元数据标题，优先使用
    if metadata_title:
        title = metadata_title

    # 尝试从文本中提取标题（通常是第一行或前几行）
    if not title and lines:
        # 标题通常较短且位于最上方
        for i, line in enumerate(lines[:5]):
            # 跳过可能是作者的行（包含邮箱格式或"@"
            if "@" in line or re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", line):
                continue
            # 跳过可能是日期的行
            if re.search(r"\d{4}", line) and len(line) < 30:
                continue
            # 跳过可能是期刊信息的行
            if any(kw in line.lower() for kw in ["doi", "journal", "vol", "issue"]):
                continue
            # 找到第一个可能是标题的行
            if len(line) > 10 and len(line) < 200:
                title = line
                break

    # 提取作者信息
    # 常见模式: 多个名字用逗号、分号或换行分隔
    author_pattern = re.compile(r"^([A-Z][a-zàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ]+(?:\s+[A-Z]\.?)?(?:\s+[A-Z][a-zàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ]+)*)$")

    for line in lines:
        # 匹配邮箱模式（作者行通常包含邮箱）
        email_match = re.search(r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})", line)
        if email_match:
            # 提取作者名字（在邮箱之前）
            before_email = line[:email_match.start()].strip()
            if before_email:
                # 清理并分割多个作者
                authors_part = re.split(r"[,，;；\t]", before_email)
                for author in authors_part:
                    author = author.strip()
                    if author and len(author) > 2:
                        authors.append(author)
            continue

        # 尝试匹配纯名字行
        match = author_pattern.match(line)
        if match and len(line) > 5 and len(line) < 50:
            name = match.group(1).strip()
            if name and not any(kw in name.lower() for kw in ["abstract", "introduction", "conclusion"]):
                authors.append(name)

    # 提取单位信息（通常包含大学、学院、研究所等关键词）
    affiliation_keywords = ["university", "college", "institute", "school", "department",
                            "大学", "学院", "研究所", "实验室", "医院", "center", "centre"]

    for line in lines:
        if any(kw in line.lower() for kw in affiliation_keywords):
            affiliation = line.strip()
            if affiliation and affiliation not in affiliations:
                affiliations.append(affiliation)

    return title, authors[:10], affiliations[:5]  # 限制数量避免过多


def extract_abstract(text: str) -> str:
    """
    从全文中提取摘要部分

    Args:
        text: 论文全文

    Returns:
        摘要文本
    """
    # 常见的摘要标记模式
    abstract_patterns = [
        r"(?:Abstract|摘要)\s*[:：]?\s*(.*?)(?=\n\s*(?:Keywords|关键词|1\.|Introduction|引言))",
        r"(?:Abstract|摘要)\s*\n(.*?)(?=\n\s*(?:Keywords|关键词))",
    ]

    for pattern in abstract_patterns:
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            abstract = match.group(1).strip()
            # 清理多余的空白
            abstract = re.sub(r"\n\s+", " ", abstract)
            abstract = re.sub(r"\s+", " ", abstract)
            if len(abstract) > 50:  # 确保摘要有足够长度
                return abstract[:2000]  # 限制长度

    return ""


def extract_journal_info(text: str) -> dict:
    """
    从全文中提取期刊信息、发表日期、页码

    Args:
        text: 论文全文

    Returns:
        包含期刊信息的字典
    """
    info = {"journal": "", "date": "", "pages": ""}

    # 提取日期
    date_patterns = [
        r"(\d{4})(?:\s*年)?",  # 2023年 或 2023
        r"(?:Published|Received|Accepted)\s*:?\s*(\d{1,2}\s+\w+\s+\d{4})",
        r"(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}",
    ]

    for pattern in date_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            info["date"] = match.group(1).strip()
            break

    # 提取页码
    page_patterns = [
        r"PP?\.\s*(\d+[-–]\d+)",
        r"Pages?\s*:?\s*(\d+[-–]\d+)",
        r":\s*(\d+[-–]\d+)\s*(?:https?|doi|$)",
    ]

    for pattern in page_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            info["pages"] = match.group(1).strip()
            break

    # 提取期刊名（通常在标题附近或关键词附近）
    journal_patterns = [
        r"(?:Journal|期刊|Volume|Vol\.)\s*:?\s*([^\n]+?)(?:\s+\d{4}|\s+Vol|\s+Issue)",
        r"([A-Z][^\n]{10,50}?(?:Journal|Review|Letter|Report))",
    ]

    for pattern in journal_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            info["journal"] = match.group(1).strip()
            break

    return info


def main():
    """主函数:从命令行参数获取PDF路径并输出结果"""
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "请提供PDF文件路径作为参数",
            "usage": "python extract_paper_info.py <pdf_file_path>"
        }))
        sys.exit(1)

    pdf_path = sys.argv[1]

    # 如果是相对路径，转换为绝对路径
    if not Path(pdf_path).is_absolute():
        pdf_path = str(Path.cwd() / pdf_path)

    result = extract_paper_info(pdf_path)

    # 输出JSON格式结果
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
