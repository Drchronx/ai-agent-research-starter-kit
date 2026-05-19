#!/usr/bin/env python
import argparse
from datetime import date
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Append a structured research log entry.")
    parser.add_argument("--log", required=True)
    parser.add_argument("--task", required=True)
    parser.add_argument("--summary", default="")
    parser.add_argument("--files", default="")
    parser.add_argument("--decisions", default="")
    parser.add_argument("--next", default="")
    args = parser.parse_args()

    log = Path(args.log)
    log.parent.mkdir(parents=True, exist_ok=True)
    entry = f"""
## {date.today().isoformat()} - {args.task}

### Summary
{args.summary}

### Files
{args.files}

### Decisions
{args.decisions}

### Next Actions
{args.next}
"""
    with log.open("a", encoding="utf-8") as f:
        f.write(entry)
    print(log)


if __name__ == "__main__":
    main()

