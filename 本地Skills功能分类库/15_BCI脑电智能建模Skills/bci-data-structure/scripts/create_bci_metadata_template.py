#!/usr/bin/env python
import argparse
import csv
from pathlib import Path


COLUMNS = [
    "subject_id",
    "session_id",
    "run_id",
    "trial_id",
    "window_id",
    "raw_file",
    "event_code",
    "label",
    "condition",
    "start_time_sec",
    "end_time_sec",
    "sampling_rate",
    "channels",
    "split_group",
    "notes",
]


def main():
    parser = argparse.ArgumentParser(description="Create a blank BCI metadata template.")
    parser.add_argument("--out", default="bci_metadata_template.csv")
    args = parser.parse_args()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(COLUMNS)
    print(out)


if __name__ == "__main__":
    main()

