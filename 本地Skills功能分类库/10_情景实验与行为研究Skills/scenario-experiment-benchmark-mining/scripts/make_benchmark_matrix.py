#!/usr/bin/env python
import argparse
import csv
from pathlib import Path


COLUMNS = [
    "paper_id",
    "verified",
    "title",
    "authors",
    "year",
    "journal",
    "doi_or_url",
    "ranking_claim_checked",
    "topic",
    "theory",
    "study_number",
    "design",
    "iv_manipulation",
    "scenario_context",
    "dv",
    "mediator",
    "moderator",
    "sample",
    "n_final",
    "cell_sizes",
    "exclusions",
    "pretest_or_pilot",
    "manipulation_check",
    "realism_check",
    "confound_check",
    "analysis",
    "effect_reporting",
    "materials_available",
    "transferable_pattern",
    "risk_or_limitation",
]


def main():
    parser = argparse.ArgumentParser(description="Create a blank scenario experiment benchmark matrix CSV.")
    parser.add_argument("--out", default="scenario_experiment_benchmark_matrix.csv")
    args = parser.parse_args()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
    print(out)


if __name__ == "__main__":
    main()

