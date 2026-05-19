import argparse
import csv
import json
from pathlib import Path


def parse_pages(spec, total_pages):
    if not spec:
        return list(range(total_pages))
    pages = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = part.split("-", 1)
            start_i = int(start)
            end_i = int(end)
            pages.update(range(start_i - 1, end_i))
        else:
            pages.add(int(part) - 1)
    return [p for p in sorted(pages) if 0 <= p < total_pages]


def extract_text(pdf_path, output_path, pages_spec=None):
    try:
        import pymupdf
    except ImportError as exc:
        raise SystemExit("Missing dependency: install pymupdf to extract PDF text.") from exc

    doc = pymupdf.open(str(pdf_path))
    page_indexes = parse_pages(pages_spec, len(doc))
    chunks = []
    for page_index in page_indexes:
        page = doc[page_index]
        chunks.append(f"\n\n--- page {page_index + 1} ---\n")
        chunks.append(page.get_text("text"))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("".join(chunks).strip() + "\n", encoding="utf-8")
    return {"pages": [p + 1 for p in page_indexes], "text_output": str(output_path)}


def write_table(table, output_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        for row in table:
            writer.writerow(["" if cell is None else cell for cell in row])


def extract_tables(pdf_path, output_dir, pages_spec=None):
    try:
        import pdfplumber
    except ImportError as exc:
        raise SystemExit("Missing dependency: install pdfplumber to extract PDF tables.") from exc

    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        page_indexes = parse_pages(pages_spec, len(pdf.pages))
        for page_index in page_indexes:
            page = pdf.pages[page_index]
            tables = page.extract_tables() or []
            for table_index, table in enumerate(tables, start=1):
                out = output_dir / f"page_{page_index + 1}_table_{table_index}.csv"
                write_table(table, out)
                outputs.append(str(out))
    return {"table_outputs": outputs}


def main():
    parser = argparse.ArgumentParser(description="Extract text and tables from a PDF.")
    parser.add_argument("--input", required=True, help="Input PDF path.")
    parser.add_argument("--output", required=True, help="Output file for text mode, or output directory for table/both mode.")
    parser.add_argument("--mode", choices=["text", "tables", "both"], default="text")
    parser.add_argument("--pages", help="1-based page range, e.g. 1-3,5.")
    args = parser.parse_args()

    pdf_path = Path(args.input)
    if not pdf_path.exists():
        raise SystemExit(f"Input PDF not found: {pdf_path}")

    out = Path(args.output)
    result = {"input": str(pdf_path), "mode": args.mode}
    if args.mode == "text":
        result.update(extract_text(pdf_path, out, args.pages))
    elif args.mode == "tables":
        result.update(extract_tables(pdf_path, out, args.pages))
    else:
        out.mkdir(parents=True, exist_ok=True)
        result.update(extract_text(pdf_path, out / "extracted_text.txt", args.pages))
        result.update(extract_tables(pdf_path, out / "tables", args.pages))

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
