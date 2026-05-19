import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path

import pandas as pd
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.shared import Pt


DEFAULT_SECTIONS = [
    "摘要",
    "引言",
    "理论基础与文献综述",
    "研究设计",
    "实证结果",
    "稳健性检验",
    "结论与启示",
]

BODY_PLACEHOLDER = "请在此处继续扩写正文，并补充模型、数据来源、变量定义与结果讨论。"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a paper draft package in LaTeX and Word formats.")
    parser.add_argument("references_path", help="CSV or Excel file with reference metadata.")
    parser.add_argument("--title", required=True, help="Paper title.")
    parser.add_argument("--author", default="OpenClaw Researcher", help="Author name.")
    parser.add_argument("--outline-json", help="Optional JSON file containing section names.")
    parser.add_argument("--output-dir", default="reports/paper-package", help="Output directory.")
    return parser.parse_args()


def load_references(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".csv":
        df = pd.read_csv(path)
    elif path.suffix.lower() in {".xlsx", ".xls"}:
        df = pd.read_excel(path)
    else:
        raise ValueError(f"Unsupported reference file: {path.suffix}")
    required = {"authors", "title", "year", "journal"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing reference columns: {', '.join(sorted(missing))}")
    return df.fillna("")


def load_outline(path: Path | None) -> list[str]:
    if path is None:
        return DEFAULT_SECTIONS
    data = json.loads(path.read_text(encoding="utf-8"))
    sections = data.get("sections", [])
    if not sections:
        raise ValueError("outline JSON must contain a non-empty 'sections' array.")
    return sections


def make_citation_key(row: pd.Series) -> str:
    first_author = str(row["authors"]).split(";")[0].split(",")[0].strip() or "author"
    author_token = re.sub(r"[^A-Za-z]", "", first_author)[:8] or "author"
    title_token = re.sub(r"[^A-Za-z0-9]", "", str(row["title"]))[:10] or "study"
    return f"{author_token}{int(row['year'])}{title_token}"


def infer_section_notes(section: str, refs: pd.DataFrame) -> str:
    text = (refs["title"] + " " + refs.get("abstract", "")).astype(str)
    if "综述" in section or "理论" in section:
        subset = refs[text.str.contains("digital|finance|innovation|policy|治理|创新", case=False, regex=True)]
    elif "设计" in section:
        subset = refs[text.str.contains("method|model|empirical|回归|识别", case=False, regex=True)]
    elif "结果" in section or "稳健" in section:
        subset = refs[text.str.contains("result|effect|evidence|impact|robust|绩效", case=False, regex=True)]
    else:
        subset = refs.head(3)
    chosen = subset.head(3) if not subset.empty else refs.head(3)
    citations = ", ".join(chosen["citation_key"].tolist())
    return f"建议围绕本节整合以下文献：{citations}。"


def infer_keywords(title: str, refs: pd.DataFrame) -> str:
    title_tokens = [token for token in re.split(r"[：:、，,\s]+", title) if token]
    ref_tokens = []
    for item in refs["title"].astype(str).head(5):
        ref_tokens.extend(token for token in re.split(r"[：:、，,\s]+", item) if 1 < len(token) <= 8)
    keywords = []
    for token in title_tokens + ref_tokens:
        if token not in keywords:
            keywords.append(token)
        if len(keywords) >= 4:
            break
    return "；".join(keywords) if keywords else "数字化转型；实证研究；文本分析"


def latex_escape(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "^": r"\^{}",
        "~": r"\~{}",
        "{": r"\{",
        "}": r"\}",
    }
    for src, target in replacements.items():
        text = text.replace(src, target)
    return text


def get_section_demo_content(section: str) -> dict[str, object]:
    if "摘要" in section:
        return {
            "paragraphs": [
                "本文以企业数字化转型为研究对象，构建“数字化转型影响创新效率”的分析框架，结合文本指标与财务面板数据开展实证检验。",
                "基准结果显示，数字化转型水平越高，企业创新效率越高；这一结论在更换变量口径、缩尾处理以及分组样本下保持稳健。",
            ]
        }
    if "引言" in section or "综述" in section or "理论" in section:
        return {
            "paragraphs": [
                "现有研究主要从资源配置、组织学习和外部环境不确定性三个视角解释数字化转型的经济后果，但针对创新效率提升路径的系统证据仍然不足。",
                "本文的边际贡献体现在三个方面：第一，将文本挖掘指标与财务绩效指标结合；第二，区分基准效应与异质性效应；第三，展示可复现实证写作流程。",
            ],
            "bullets": [
                "机制一：数字基础设施降低信息摩擦并提升知识整合效率。",
                "机制二：组织流程重构提高研发资源配置效率。",
                "机制三：数据治理能力增强企业对外部冲击的应对弹性。",
            ],
        }
    if "研究设计" in section:
        return {
            "paragraphs": [
                "样本选取 2015 至 2023 年 A 股上市公司年度数据，剔除金融行业、ST 样本及关键变量缺失观测后，得到平衡面板样本。",
                "被解释变量为创新效率，核心解释变量为数字化转型指数，控制变量包括企业规模、资产负债率、现金流、董事会特征与年份固定效应。",
            ],
            "equation": [
                r"\begin{equation}",
                r"Innovation_{i,t} = \alpha + \beta Digital_{i,t} + \gamma Controls_{i,t} + \mu_i + \lambda_t + \varepsilon_{i,t}",
                r"\end{equation}",
            ],
            "table": {
                "caption": "变量定义示例",
                "columns": ["变量类型", "变量名称", "符号", "说明"],
                "rows": [
                    ["被解释变量", "创新效率", "Innovation", "专利产出与研发投入匹配程度"],
                    ["核心解释变量", "数字化转型", "Digital", "年报文本中数字化词频构造的指数"],
                    ["控制变量", "企业规模", "Size", "期末总资产取自然对数"],
                    ["控制变量", "资产负债率", "Lev", "总负债除以总资产"],
                ],
            },
        }
    if "实证结果" in section:
        return {
            "paragraphs": [
                "基准回归中，数字化转型系数显著为正，说明企业数字化投入与创新效率提升存在稳健的正向关系。",
                "经济意义上，数字化转型指数每提高 1 个标准差，创新效率平均提高约 0.12 个标准差，表明结论不仅统计显著，也具有管理含义。",
            ],
            "table": {
                "caption": "基准回归结果示例",
                "columns": ["变量", "模型(1)", "模型(2)", "模型(3)"],
                "rows": [
                    ["Digital", "0.082***", "0.074***", "0.069**"],
                    ["", "(3.41)", "(3.02)", "(2.55)"],
                    ["Size", "", "0.118***", "0.105***"],
                    ["", "", "(4.26)", "(3.89)"],
                    ["Lev", "", "-0.063*", "-0.058*"],
                    ["", "", "(-1.88)", "(-1.72)"],
                    ["个体固定效应", "是", "是", "是"],
                    ["年份固定效应", "是", "是", "是"],
                    ["样本量", "12,480", "12,480", "12,480"],
                    ["调整后 R^2", "0.214", "0.263", "0.271"],
                ],
            },
        }
    if "稳健" in section or "异质性" in section:
        return {
            "paragraphs": [
                "稳健性检验依次采用替换被解释变量、滞后一期核心解释变量、双向缩尾及剔除极端年份等方式，核心结论未发生实质变化。",
                "异质性结果显示，数字化转型对高技术行业、融资约束较强企业以及治理能力较强企业的促进作用更加显著。",
            ],
            "bullets": [
                "稳健性检验 A：使用全要素生产率替代创新效率指标。",
                "稳健性检验 B：将数字化转型指标滞后一期以缓解反向因果。",
                "异质性检验：按行业属性、地区数字基础设施和产权性质分组。",
            ],
        }
    return {
        "paragraphs": [
            "本文结论表明，数字化转型并非单纯的信息化投入，而是影响企业创新产出、资源配置与治理效率的重要制度性安排。",
            "在政策层面，应完善数字基础设施与数据治理制度；在企业层面，应同步推进组织流程再造与技术能力建设。",
        ]
    }


def render_latex_table(columns: list[str], rows: list[list[str]], caption: str) -> list[str]:
    colspec = "l" * len(columns)
    lines = [
        r"\begin{table}[htbp]",
        r"\centering",
        rf"\caption{{{latex_escape(caption)}}}",
        rf"\begin{{tabular}}{{{colspec}}}",
        r"\toprule",
        " & ".join(latex_escape(col) for col in columns) + r" \\",
        r"\midrule",
    ]
    for row in rows:
        lines.append(" & ".join(latex_escape(cell) for cell in row) + r" \\")
    lines.extend([r"\bottomrule", r"\end{tabular}", r"\end{table}"])
    return lines


def write_bibtex(refs: pd.DataFrame, output_dir: Path) -> Path:
    lines = []
    for _, row in refs.iterrows():
        entry = [
            f"@article{{{row['citation_key']},",
            f"  author = {{{row['authors']}}},",
            f"  title = {{{row['title']}}},",
            f"  journal = {{{row['journal']}}},",
            f"  year = {{{int(row['year'])}}},",
        ]
        if row.get("doi"):
            entry.append(f"  doi = {{{row['doi']}}},")
        entry.append("}")
        lines.append("\n".join(entry))
    output = output_dir / "references.bib"
    output.write_text("\n\n".join(lines) + "\n", encoding="utf-8")
    return output


def write_latex(title: str, author: str, sections: list[str], refs: pd.DataFrame, output_dir: Path) -> Path:
    keywords = infer_keywords(title, refs)
    body_lines = [
        r"\documentclass[12pt,UTF8]{ctexart}",
        r"\usepackage{geometry}",
        r"\usepackage{booktabs}",
        r"\usepackage{natbib}",
        r"\usepackage{setspace}",
        r"\usepackage{fancyhdr}",
        r"\usepackage{titlesec}",
        r"\usepackage{abstract}",
        r"\usepackage{indentfirst}",
        r"\geometry{margin=1in}",
        r"\setstretch{1.35}",
        r"\setlength{\parindent}{2em}",
        r"\setlength{\headheight}{15pt}",
        r"\pagestyle{fancy}",
        r"\fancyhf{}",
        r"\fancyhead[C]{论文草稿}",
        r"\fancyfoot[C]{\thepage}",
        r"\titleformat{\section}{\zihao{-3}\bfseries}{\thesection}{1em}{}",
        r"\renewcommand{\abstractname}{摘要}",
        rf"\title{{{title}}}",
        rf"\author{{{author}}}",
        r"\date{\today}",
        r"\begin{document}",
        r"\maketitle",
        r"\thispagestyle{fancy}",
    ]
    remaining_sections = sections[:]
    if remaining_sections and remaining_sections[0] == "摘要":
        abstract_demo = get_section_demo_content("摘要")
        body_lines.extend(
            [
                r"\begin{abstract}",
                infer_section_notes("摘要", refs),
                *[latex_escape(paragraph) for paragraph in abstract_demo["paragraphs"]],
                r"\end{abstract}",
                rf"\noindent\textbf{{关键词：}} {keywords}",
                "",
            ]
        )
        remaining_sections = remaining_sections[1:]

    for section in remaining_sections:
        demo = get_section_demo_content(section)
        body_lines.append(rf"\section{{{section}}}")
        body_lines.append(infer_section_notes(section, refs))
        for paragraph in demo.get("paragraphs", []):
            body_lines.append(latex_escape(str(paragraph)))
            body_lines.append("")
        bullets = demo.get("bullets", [])
        if bullets:
            body_lines.append(r"\begin{itemize}")
            for bullet in bullets:
                body_lines.append(rf"\item {latex_escape(str(bullet))}")
            body_lines.append(r"\end{itemize}")
            body_lines.append("")
        equation = demo.get("equation", [])
        if equation:
            body_lines.extend(equation)
            body_lines.append("")
        table = demo.get("table")
        if table:
            body_lines.extend(render_latex_table(table["columns"], table["rows"], table["caption"]))
            body_lines.append("")
        body_lines.append(latex_escape(BODY_PLACEHOLDER))
        body_lines.append("")
    body_lines.extend([r"\nocite{*}", r"\bibliographystyle{apalike}", r"\bibliography{references}", r"\end{document}"])
    output = output_dir / "manuscript.tex"
    output.write_text("\n".join(body_lines) + "\n", encoding="utf-8")
    return output


def write_docx(title: str, author: str, sections: list[str], refs: pd.DataFrame, output_dir: Path) -> Path:
    document = Document()
    configure_docx_styles(document)
    add_docx_title_block(document, title, author, infer_keywords(title, refs))

    remaining_sections = sections[:]
    if remaining_sections and remaining_sections[0] == "摘要":
        add_docx_section(document, "摘要", infer_section_notes("摘要", refs), BODY_PLACEHOLDER)
        remaining_sections = remaining_sections[1:]

    for section in remaining_sections:
        add_docx_section(document, section, infer_section_notes(section, refs), BODY_PLACEHOLDER)

    document.add_heading("参考文献", level=1)
    for _, row in refs.iterrows():
        citation = f"{row['authors']} ({int(row['year'])}). {row['title']}. {row['journal']}."
        if row.get("doi"):
            citation += f" DOI: {row['doi']}."
        paragraph = document.add_paragraph(citation)
        apply_body_paragraph_format(paragraph)
    output = output_dir / "manuscript.docx"
    document.save(output)
    return output


def set_run_font(run, east_asia: str, latin: str, size: int, bold: bool = False) -> None:
    run.font.name = latin
    run._element.rPr.rFonts.set(qn("w:eastAsia"), east_asia)
    run.font.size = Pt(size)
    run.font.bold = bold


def configure_docx_styles(document: Document) -> None:
    normal_style = document.styles["Normal"]
    normal_style.font.name = "Times New Roman"
    normal_style._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")
    normal_style.font.size = Pt(12)
    normal_style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    normal_style.paragraph_format.first_line_indent = Pt(24)

    heading_style = document.styles["Heading 1"]
    heading_style.font.name = "Times New Roman"
    heading_style._element.rPr.rFonts.set(qn("w:eastAsia"), "黑体")
    heading_style.font.size = Pt(14)
    heading_style.font.bold = True
    heading_style.paragraph_format.first_line_indent = Pt(0)
    heading_style.paragraph_format.space_before = Pt(12)
    heading_style.paragraph_format.space_after = Pt(6)

    title_style = document.styles["Title"]
    title_style.font.name = "Times New Roman"
    title_style._element.rPr.rFonts.set(qn("w:eastAsia"), "黑体")
    title_style.font.size = Pt(18)
    title_style.font.bold = True


def apply_body_paragraph_format(paragraph) -> None:
    paragraph.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    paragraph.paragraph_format.first_line_indent = Pt(24)
    paragraph.paragraph_format.space_after = Pt(0)
    for run in paragraph.runs:
        set_run_font(run, "宋体", "Times New Roman", 12, bold=False)


def add_docx_title_block(document: Document, title: str, author: str, keywords: str) -> None:
    title_paragraph = document.add_paragraph(style="Title")
    title_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_run = title_paragraph.add_run(title)
    set_run_font(title_run, "黑体", "Times New Roman", 18, bold=True)

    author_paragraph = document.add_paragraph()
    author_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    author_run = author_paragraph.add_run(f"作者：{author}")
    set_run_font(author_run, "宋体", "Times New Roman", 12, bold=False)

    keywords_paragraph = document.add_paragraph()
    keywords_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    keywords_run = keywords_paragraph.add_run(f"关键词：{keywords}")
    set_run_font(keywords_run, "宋体", "Times New Roman", 11, bold=False)

    intro_paragraph = document.add_paragraph("该草稿由自动排版脚本生成，适合作为后续人工润色和补充实证结果的基础文件。")
    apply_body_paragraph_format(intro_paragraph)


def add_docx_section(document: Document, section: str, guidance: str, placeholder: str) -> None:
    heading = document.add_heading(section, level=1)
    for run in heading.runs:
        set_run_font(run, "黑体", "Times New Roman", 14, bold=True)
    guidance_paragraph = document.add_paragraph(guidance)
    apply_body_paragraph_format(guidance_paragraph)
    demo = get_section_demo_content(section)
    for paragraph_text in demo.get("paragraphs", []):
        paragraph = document.add_paragraph(str(paragraph_text))
        apply_body_paragraph_format(paragraph)
    for bullet in demo.get("bullets", []):
        paragraph = document.add_paragraph(str(bullet), style="List Bullet")
        paragraph.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
        for run in paragraph.runs:
            set_run_font(run, "宋体", "Times New Roman", 12, bold=False)
    equation = demo.get("equation", [])
    if equation:
        equation_paragraph = document.add_paragraph("模型设定：Innovation_{i,t} = α + β Digital_{i,t} + γ Controls_{i,t} + μ_i + λ_t + ε_{i,t}")
        equation_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in equation_paragraph.runs:
            set_run_font(run, "宋体", "Times New Roman", 11, bold=False)
    table = demo.get("table")
    if table:
        docx_table = document.add_table(rows=1, cols=len(table["columns"]))
        docx_table.style = "Table Grid"
        header_cells = docx_table.rows[0].cells
        for idx, column in enumerate(table["columns"]):
            header_cells[idx].text = str(column)
            for paragraph in header_cells[idx].paragraphs:
                for run in paragraph.runs:
                    set_run_font(run, "黑体", "Times New Roman", 10, bold=True)
        for row in table["rows"]:
            cells = docx_table.add_row().cells
            for idx, value in enumerate(row):
                cells[idx].text = str(value)
                for paragraph in cells[idx].paragraphs:
                    for run in paragraph.runs:
                        set_run_font(run, "宋体", "Times New Roman", 10, bold=False)
        document.add_paragraph("")
    body_paragraph = document.add_paragraph(placeholder)
    apply_body_paragraph_format(body_paragraph)


def find_executable(name: str, fallback_paths: list[str]) -> str | None:
    found = shutil.which(name)
    if found:
        return found
    for path in fallback_paths:
        candidate = Path(path)
        if candidate.exists():
            return str(candidate)
    return None


def compile_pdf_from_latex(tex_path: Path) -> Path:
    xelatex = find_executable(
        "xelatex",
        [r"C:\Users\11830\AppData\Local\Programs\MiKTeX\miktex\bin\x64\xelatex.exe"],
    )
    bibtex = find_executable(
        "bibtex",
        [r"C:\Users\11830\AppData\Local\Programs\MiKTeX\miktex\bin\x64\bibtex.exe"],
    )
    if not xelatex or not bibtex:
        raise RuntimeError("LaTeX compiler not found. Install MiKTeX or TeX Live to enable PDF export.")

    cwd = tex_path.parent
    stem = tex_path.stem
    xelatex_cmd = [xelatex, "-interaction=nonstopmode", "-halt-on-error", tex_path.name]
    bibtex_cmd = [bibtex, stem]

    for command in (xelatex_cmd, bibtex_cmd, xelatex_cmd, xelatex_cmd):
        result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if result.returncode != 0:
            raise RuntimeError(
                "LaTeX PDF compilation failed.\n"
                f"Command: {' '.join(command)}\n"
                f"STDOUT:\n{result.stdout}\n"
                f"STDERR:\n{result.stderr}"
            )

    pdf_path = cwd / f"{stem}.pdf"
    if not pdf_path.exists():
        raise RuntimeError("LaTeX compilation finished without producing a PDF file.")
    return pdf_path


def write_outline_json(title: str, sections: list[str], refs: pd.DataFrame, output_dir: Path) -> Path:
    payload = {
        "title": title,
        "sections": [{"name": section, "guidance": infer_section_notes(section, refs)} for section in sections],
    }
    output = output_dir / "generated_outline.json"
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return output


def write_reference_table(refs: pd.DataFrame, output_dir: Path) -> Path:
    output = output_dir / "reference_catalog.csv"
    refs.to_csv(output, index=False, encoding="utf-8-sig")
    return output


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    refs = load_references(Path(args.references_path)).copy()
    refs["citation_key"] = refs.apply(make_citation_key, axis=1)
    sections = load_outline(Path(args.outline_json)) if args.outline_json else load_outline(None)

    bib_path = write_bibtex(refs, output_dir)
    tex_path = write_latex(args.title, args.author, sections, refs, output_dir)
    docx_path = write_docx(args.title, args.author, sections, refs, output_dir)
    pdf_path = compile_pdf_from_latex(tex_path)
    outline_path = write_outline_json(args.title, sections, refs, output_dir)
    catalog_path = write_reference_table(refs, output_dir)

    print(f"BibTeX: {bib_path}")
    print(f"LaTeX manuscript: {tex_path}")
    print(f"Word manuscript: {docx_path}")
    print(f"PDF manuscript: {pdf_path}")
    print(f"Outline: {outline_path}")
    print(f"Reference catalog: {catalog_path}")


if __name__ == "__main__":
    main()
