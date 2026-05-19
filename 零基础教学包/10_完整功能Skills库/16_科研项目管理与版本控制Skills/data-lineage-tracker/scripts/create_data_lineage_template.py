#!/usr/bin/env python
import argparse
import csv
from pathlib import Path


COLUMNS = [
    "raw_file",
    "raw_file_status",
    "script_or_manual_step",
    "processed_file",
    "output_file",
    "cleaning_or_transformation",
    "exclusion_rule",
    "date",
    "reproducible",
    "notes",
]


def main():
    parser = argparse.ArgumentParser(description="Create a data lineage template.")
    parser.add_argument("--out", default="data_lineage.csv")
    args = parser.parse_args()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(COLUMNS)
    print(out)


if __name__ == "__main__":
    main()

