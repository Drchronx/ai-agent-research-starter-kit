#!/usr/bin/env python
import argparse
from datetime import date
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Create a weekly research plan template.")
    parser.add_argument("--out", default="weekly_plan.md")
    args = parser.parse_args()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(f"""# Weekly Research Plan

Week starting: {date.today().isoformat()}

## Main Goal

TBD

## Must Do

| Task | Input | Output | Estimate | Dependency | Status |
|---|---|---|---|---|---|

## Should Do

| Task | Input | Output | Estimate | Dependency | Status |
|---|---|---|---|---|---|

## Can Wait

| Task | Reason to defer | Revisit date |
|---|---|---|

## Advisor Questions

- TBD

## End-of-Week Review

Completed:
- TBD

Unfinished:
- TBD

Blockers:
- TBD

Next week:
- TBD
""", encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()

