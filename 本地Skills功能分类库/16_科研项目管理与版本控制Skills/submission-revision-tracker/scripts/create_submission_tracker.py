#!/usr/bin/env python
import argparse
import csv
from pathlib import Path


COLUMNS = [
    "journal",
    "status",
    "fit_reason",
    "format_status",
    "submitted_date",
    "decision_date",
    "decision",
    "revision_due",
    "next_action",
    "notes",
]


def main():
    parser = argparse.ArgumentParser(description="Create a journal submission tracker.")
    parser.add_argument("--out", default="submission_tracker.csv")
    args = parser.parse_args()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(COLUMNS)
    print(out)


if __name__ == "__main__":
    main()

