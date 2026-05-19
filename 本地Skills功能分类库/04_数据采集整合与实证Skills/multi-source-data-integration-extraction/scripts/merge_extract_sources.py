import argparse
import json
import os
import re
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Merge Excel/CSV/PDF files and extract structured tables from text-like documents.")
    parser.add_argument("input_dir", help="Directory containing source files.")
    parser.add_argument("--output-dir", default="reports/multi-source-integration", help="Output directory.")
    parser.add_argument("--ocr", action="store_true", help="Use OCR for scanned PDFs and images.")
    return parser.parse_args()


def normalize_column(name: str) -> str:
    value = re.sub(r"[^0-9a-zA-Z\u4e00-\u9fff]+", "_", str(name).strip().lower())
    return value.strip("_") or "unnamed_column"


def read_table_file(path: Path) -> list[pd.DataFrame]:
    if path.suffix.lower() == ".csv":
        return [pd.read_csv(path)]
    if path.suffix.lower() in {".xlsx", ".xls"}:
        workbook = pd.read_excel(path, sheet_name=None)
        return list(workbook.values())
    return []


def merge_tabular_files(input_dir: Path) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for path in sorted(input_dir.iterdir()):
        if path.suffix.lower() not in {".csv", ".xlsx", ".xls"}:
            continue
        for index, frame in enumerate(read_table_file(path), start=1):
            local = frame.copy()
            local.columns = [normalize_column(col) for col in local.columns]
            local["source_file"] = path.name
            local["source_sheet_index"] = index
            frames.append(local)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True, sort=False)


def extract_html_tables(path: Path) -> list[pd.DataFrame]:
    try:
        tables = pd.read_html(path)
    except ValueError:
        return []
    cleaned = []
    for frame in tables:
        local = frame.copy()
        local.columns = [normalize_column(col) for col in local.columns]
        cleaned.append(local)
    return cleaned


def extract_text_tables(path: Path) -> list[pd.DataFrame]:
    text = path.read_text(encoding="utf-8")
    blocks = [block.strip() for block in re.split(r"\n\s*\n", text) if block.strip()]
    tables: list[pd.DataFrame] = []
    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if len(lines) < 2:
            continue
        if all("|" in line for line in lines):
            rows = [[cell.strip() for cell in line.strip("|").split("|")] for line in lines]
        elif all("\t" in line for line in lines):
            rows = [[cell.strip() for cell in line.split("\t")] for line in lines]
        else:
            continue
        header = [normalize_column(item) for item in rows[0]]
        values = rows[1:]
        if not values:
            continue
        width = len(header)
        valid_values = [row[:width] + [""] * max(0, width - len(row)) for row in values]
        tables.append(pd.DataFrame(valid_values, columns=header))
    return tables


def extract_pdf_tables(path: Path, use_ocr: bool = False) -> list[pd.DataFrame]:
    """Extract tables from PDF files using PyMuPDF and PaddleOCR.
    
    Args:
        path: Path to PDF file
        use_ocr: If True, use OCR for scanned PDFs
    
    Returns:
        List of DataFrames containing extracted tables
    """
    tables: list[pd.DataFrame] = []
    
    try:
        import pymupdf
        
        doc = pymupdf.open(path)
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            
            # Method 1: Try PyMuPDF's built-in table extraction
            try:
                page_tables = page.find_tables()
                if page_tables.tables:
                    for table_idx, table in enumerate(page_tables.tables, start=1):
                        df = table.to_pandas()
                        if len(df) > 1:
                            # Clean column names
                            df.columns = [normalize_column(col) if col else f"column_{i}" for i, col in enumerate(df.columns)]
                            df["source_file"] = f"{path.name} (page {page_num + 1}, table {table_idx})"
                            tables.append(df)
                            print(f"  Page {page_num + 1}: Extracted table {table_idx} with {len(df)} rows")
            except Exception as e:
                print(f"  Warning: PyMuPDF table extraction failed on page {page_num + 1}: {e}")
            
            # Method 2: If no tables found and OCR is enabled, try OCR
            if use_ocr and not tables:
                try:
                    ocr_tables = extract_pdf_page_ocr(page, page_num, path)
                    tables.extend(ocr_tables)
                except Exception as e:
                    print(f"  Warning: OCR extraction failed on page {page_num + 1}: {e}")
        
        doc.close()
        
    except Exception as e:
        print(f"Warning: Failed to process PDF {path.name}: {e}")
    
    return tables


def extract_pdf_page_ocr(page, page_num: int, pdf_path: Path) -> list[pd.DataFrame]:
    """Extract text from a PDF page using PaddleOCR."""
    try:
        from paddleocr import PaddleOCR
        
        # Initialize OCR (cached for performance)
        if not hasattr(extract_pdf_page_ocr, 'ocr'):
            # Set environment variable for model cache
            os.environ.setdefault("PADDLE_PDX_CACHE_HOME", str(pdf_path.parent / ".paddle_models"))
            extract_pdf_page_ocr.ocr = PaddleOCR(use_doc_orientation_classify=False, use_doc_unwarping=False, use_textline_orientation=False, show_log=False)
        
        ocr = extract_pdf_page_ocr.ocr
        
        # Render page to image
        mat = pymupdf.Matrix(2.0, 2.0)  # 2x zoom for better OCR
        pix = page.get_pixmap(matrix=mat)
        
        # Save temporarily
        temp_img = pdf_path.parent / f"_temp_ocr_page_{page_num}.png"
        pix.save(str(temp_img))
        
        try:
            # Run OCR
            result = ocr.predict(str(temp_img))
            
            if result and len(result) > 0:
                rec_texts = result[0].get("rec_texts", [])
                if rec_texts:
                    # Try to detect table structure
                    # Simple heuristic: if lines contain consistent delimiters or look like table rows
                    table_data = []
                    for line in rec_texts:
                        if line.strip():
                            # Split by common delimiters
                            parts = re.split(r'\s{2,}|\t|│|│', line.strip())
                            if len(parts) > 1:
                                table_data.append([p.strip() for p in parts])
                    
                    if len(table_data) > 1:
                        # Check if all rows have similar column count
                        col_counts = [len(row) for row in table_data]
                        if len(set(col_counts)) <= 2:  # Allow some variation
                            df = pd.DataFrame(table_data)
                            if len(df) > 1:
                                df.columns = [normalize_column(col) if col else f"column_{i}" for i, col in enumerate(df.iloc[0])]
                                df = df.iloc[1:].reset_index(drop=True)
                            df["source_file"] = f"{pdf_path.name} (page {page_num + 1}, OCR)"
                            return [df]
        finally:
            # Clean up temp file
            if temp_img.exists():
                temp_img.unlink()
                
    except ImportError as e:
        print(f"  OCR not available: {e}")
    except Exception as e:
        print(f"  OCR extraction error: {e}")
    
    return []


def extract_document_tables(input_dir: Path, output_dir: Path, use_ocr: bool = False) -> tuple[list[Path], Path]:
    extracted_paths: list[Path] = []
    manifest: list[dict[str, str | int]] = []
    table_dir = output_dir / "extracted_tables"
    table_dir.mkdir(parents=True, exist_ok=True)
    
    for path in sorted(input_dir.iterdir()):
        suffix = path.suffix.lower()
        tables: list[pd.DataFrame] = []
        
        print(f"\nProcessing: {path.name}")
        
        if suffix in {".html", ".htm"}:
            tables = extract_html_tables(path)
        elif suffix in {".txt", ".md"}:
            tables = extract_text_tables(path)
        elif suffix == ".pdf":
            tables = extract_pdf_tables(path, use_ocr=use_ocr)
        
        print(f"  Found {len(tables)} table(s)")
        
        for idx, frame in enumerate(tables, start=1):
            csv_path = table_dir / f"{path.stem}_table_{idx}.csv"
            frame.to_csv(csv_path, index=False, encoding="utf-8-sig")
            extracted_paths.append(csv_path)
            manifest.append({
                "source_file": path.name,
                "table_index": idx,
                "output_csv": csv_path.name,
                "rows": len(frame),
                "columns": len(frame.columns)
            })
    
    manifest_path = output_dir / "extraction_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return extracted_paths, manifest_path


def main() -> None:
    args = parse_args()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("Multi-Source Data Integration & Extraction")
    print("=" * 60)
    
    # Step 1: Merge tabular files
    print("\n[Step 1] Merging CSV/Excel files...")
    merged = merge_tabular_files(input_dir)
    merged_path = output_dir / "merged_dataset.csv"
    if not merged.empty:
        merged.to_csv(merged_path, index=False, encoding="utf-8-sig")
        print(f"✓ Merged dataset saved: {merged_path}")
        print(f"  Total rows: {len(merged)}")
    else:
        print("  No CSV/Excel files found.")

    # Step 2: Extract tables from documents
    print("\n[Step 2] Extracting tables from documents (PDF/HTML/TXT)...")
    extracted_paths, manifest_path = extract_document_tables(input_dir, output_dir, use_ocr=args.ocr)
    print(f"\n✓ Extraction manifest saved: {manifest_path}")
    if extracted_paths:
        print(f"✓ Extracted {len(extracted_paths)} table(s):")
        for path in extracted_paths:
            print(f"  - {path.name}")
    else:
        print("  No tables extracted.")
    
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)


if __name__ == "__main__":
    main()
