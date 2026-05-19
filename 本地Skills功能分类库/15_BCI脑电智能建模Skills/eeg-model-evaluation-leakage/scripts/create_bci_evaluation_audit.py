#!/usr/bin/env python
import argparse
import csv
from pathlib import Path


ROWS = [
    ("split_unit", "Is the split unit aligned with the claim: trial, session, subject, or dataset?", ""),
    ("window_leakage", "Can windows from the same trial appear in both train and test?", ""),
    ("preprocessing_leakage", "Were filters, scalers, CSP, PCA, or feature selection fit on all data?", ""),
    ("augmentation_leakage", "Was augmentation applied before splitting?", ""),
    ("hyperparameter_leakage", "Was the test set used for tuning or early stopping?", ""),
    ("subject_reporting", "Are metrics reported per subject as well as pooled?", ""),
    ("chance_level", "Is chance level or balanced chance reported?", ""),
    ("uncertainty", "Are confidence intervals, SD across subjects, or paired tests reported?", ""),
    ("baseline", "Are simple baselines reported before complex models?", ""),
    ("online_claim", "Are offline, pseudo-online, and online claims separated?", ""),
]


def main():
    parser = argparse.ArgumentParser(description="Create a BCI model evaluation and leakage audit template.")
    parser.add_argument("--out", default="bci_evaluation_leakage_audit.csv")
    args = parser.parse_args()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["audit_item", "question", "status", "evidence", "fix_needed"])
        for item, question, evidence in ROWS:
            writer.writerow([item, question, "pending", evidence, ""])
    print(out)


if __name__ == "__main__":
    main()

