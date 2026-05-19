#!/usr/bin/env python
import argparse
import csv
from pathlib import Path


COLUMNS = [
    "construct",
    "item_id",
    "item_text",
    "source",
    "response_anchor",
    "reverse_coded",
    "adaptation_note",
    "keep_drop_decision",
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="scale_codebook.csv")
    args = parser.parse_args()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(COLUMNS)
    print(out)


if __name__ == "__main__":
    main()

