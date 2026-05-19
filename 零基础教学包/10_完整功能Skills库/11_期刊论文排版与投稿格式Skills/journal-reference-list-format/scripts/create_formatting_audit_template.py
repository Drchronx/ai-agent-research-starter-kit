#!/usr/bin/env python
import argparse
import csv
from pathlib import Path


ROWS = [
    ("title_page", "Title, authors, affiliations, correspondence", ""),
    ("abstract_keywords", "Word count, abstract structure, keywords", ""),
    ("headings", "Heading levels and numbering", ""),
    ("intext_citations", "All in-text citations match target style", ""),
    ("references", "Reference list formatting and metadata", ""),
    ("tables_figures", "Captions, numbering, callouts, notes", ""),
    ("statistics_units", "Statistical notation and units", ""),
    ("footnotes_endnotes", "Note numbering and placement", ""),
    ("layout_spacing", "Margins, spacing, indentation, page elements", ""),
    ("blind_review", "Author identity, self-citations, file metadata", ""),
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="journal_formatting_audit.csv")
    args = parser.parse_args()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["module", "audit_focus", "status", "notes", "manual_review_required"])
        for module, focus, notes in ROWS:
            writer.writerow([module, focus, "pending", notes, ""])
    print(out)


if __name__ == "__main__":
    main()

