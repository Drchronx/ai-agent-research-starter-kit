#!/usr/bin/env python
import argparse
from datetime import date
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Create a manuscript version log.")
    parser.add_argument("--out", default="manuscript_versions.md")
    parser.add_argument("--version", default="v1")
    parser.add_argument("--goal", default="Initial draft")
    args = parser.parse_args()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    if not out.exists():
        out.write_text("# Manuscript Versions\n\n", encoding="utf-8")
    with out.open("a", encoding="utf-8") as f:
        f.write(f"""## {args.version} - {date.today().isoformat()}

Goal: {args.goal}

Changed sections:
- TBD

Updated analyses/tables/figures:
- TBD

Unresolved issues:
- TBD

Next version target:
- TBD

""")
    print(out)


if __name__ == "__main__":
    main()

