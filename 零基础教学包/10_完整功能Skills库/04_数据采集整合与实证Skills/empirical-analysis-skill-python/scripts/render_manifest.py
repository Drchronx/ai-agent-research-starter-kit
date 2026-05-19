from __future__ import annotations

import argparse
import json
import os
import platform
import sys
from pathlib import Path

from common import DEFAULT_OUTPUT, ensure_dir, write_json


def run(args: argparse.Namespace) -> dict[str, object]:
    results_dir = Path(args.results_dir)
    outdir = ensure_dir(Path(args.output_dir))
    manifest = {
        "results_dir": str(results_dir),
        "tables": sorted(str(p) for p in results_dir.rglob("*") if p.suffix.lower() in {".csv", ".xlsx", ".tex", ".html", ".docx"}),
        "figures": sorted(str(p) for p in results_dir.rglob("*") if p.suffix.lower() in {".png", ".pdf"}),
        "runtime": {
            "python": sys.version,
            "platform": platform.platform(),
            "cwd": os.getcwd(),
        },
    }
    write_json(manifest, outdir / "artifact_manifest.json")
    lines = ["# Empirical Artifact Manifest", "", "## Tables"]
    lines.extend([f"- {item}" for item in manifest["tables"]] or ["- None found"])
    lines.extend(["", "## Figures"])
    lines.extend([f"- {item}" for item in manifest["figures"]] or ["- None found"])
    (outdir / "artifact_manifest.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Collect empirical tables and figures into a manifest.")
    parser.add_argument("--results-dir", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT))
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    print(json.dumps(run(args), indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
