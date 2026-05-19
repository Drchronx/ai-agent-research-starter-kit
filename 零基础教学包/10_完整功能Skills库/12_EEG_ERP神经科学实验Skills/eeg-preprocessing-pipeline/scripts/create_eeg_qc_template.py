#!/usr/bin/env python
import argparse
import csv
from pathlib import Path


COLUMNS = [
    "participant_id",
    "raw_file",
    "sampling_rate",
    "bad_channels",
    "interpolated_channels",
    "ica_components_removed",
    "epochs_total",
    "epochs_rejected",
    "epochs_retained",
    "conditions_balanced",
    "notes",
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="eeg_qc_template.csv")
    args = parser.parse_args()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(COLUMNS)
    print(out)


if __name__ == "__main__":
    main()

