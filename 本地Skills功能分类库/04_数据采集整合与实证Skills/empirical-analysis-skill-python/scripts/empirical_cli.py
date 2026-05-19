from __future__ import annotations

import argparse

import clean_data
import describe_data
import plot_factory
import prepare_ml_data
import render_manifest
import run_cate
import run_diagnostics
import run_did
import run_dml
import run_further_analysis
import run_iv
import run_matching
import run_model
import run_panel
import run_rd
import run_robustness
import run_sensitivity
import run_survival
import run_synth
import run_supervised_ml
import table_factory
import transform_data


COMMANDS = {
    "cate": run_cate.main,
    "clean": clean_data.main,
    "describe": describe_data.main,
    "diagnostics": run_diagnostics.main,
    "did": run_did.main,
    "dml": run_dml.main,
    "further": run_further_analysis.main,
    "iv": run_iv.main,
    "matching": run_matching.main,
    "model": run_model.main,
    "panel": run_panel.main,
    "prepare-ml": prepare_ml_data.main,
    "plot": plot_factory.main,
    "rd": run_rd.main,
    "robustness": run_robustness.main,
    "sensitivity": run_sensitivity.main,
    "supervised-ml": run_supervised_ml.main,
    "survival": run_survival.main,
    "synth": run_synth.main,
    "render": render_manifest.main,
    "table": table_factory.main,
    "transform": transform_data.main,
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compatibility dispatcher. Prefer direct step scripts.")
    parser.add_argument("command", choices=sorted(COMMANDS))
    parser.add_argument("args", nargs=argparse.REMAINDER)
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    COMMANDS[args.command](args.args)


if __name__ == "__main__":
    main()
