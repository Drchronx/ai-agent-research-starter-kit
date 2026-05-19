from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from common import DEFAULT_OUTPUT, add_common_io, add_table_format_arg, export_table, import_matplotlib, parse_cols, parse_semicolon, read_data, require_columns, save_figure, write_json
from model_utils import build_formula, control_sets, fit_model, fit_result_rows


def run(args: argparse.Namespace) -> dict[str, object]:
    df = read_data(args.input, args.sheet)
    outdir = Path(args.output_dir)
    fixed_effects = parse_cols(args.fixed_effects)
    controls = parse_cols(args.controls)

    if args.formulas:
        formulas = parse_semicolon(args.formulas)
    elif args.formula:
        formulas = [args.formula]
    else:
        require_columns(df, [args.outcome, args.treatment] + controls + fixed_effects, "model columns")
        formulas = [build_formula(args.outcome, args.treatment, controls_set, fixed_effects) for controls_set in control_sets(args)]

    names = parse_cols(args.model_names) or [f"M{idx + 1}" for idx in range(len(formulas))]
    if len(names) != len(formulas):
        raise ValueError("--model-names must have the same length as formulas/specifications.")

    results = []
    all_rows = []
    keep_terms = parse_cols(args.keep_terms)
    for name, formula in zip(names, formulas):
        fitted = fit_model(df, formula, args.model_type, args.cluster, args.cov_type, name)
        results.append(fitted)
        all_rows.extend(fit_result_rows(fitted, keep_terms or None))

    tidy = pd.DataFrame(all_rows).round(6)
    export_table(tidy, outdir / "table2_main_tidy", parse_cols(args.formats))
    wide = tidy.pivot_table(index="term", columns="model", values="coef", aggfunc="first").reset_index()
    export_table(wide.round(6), outdir / "table2_main", parse_cols(args.formats))
    summary_path = outdir / "model_summaries.txt"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text("\n\n".join(f"[{r.name}] {r.formula}\n{r.text_summary}" for r in results), encoding="utf-8")

    target_term = args.plot_term or args.treatment
    if target_term and not tidy.empty and target_term in tidy["term"].unique() and not args.no_figures:
        subset = tidy.loc[tidy["term"] == target_term].copy()
        plt = import_matplotlib()
        fig, ax = plt.subplots(figsize=(7, 4))
        x = np.arange(len(subset))
        ax.errorbar(x, subset["coef"], yerr=1.96 * subset["se"], fmt="o", capsize=4)
        ax.axhline(0, linestyle="--", linewidth=0.8, color="gray")
        ax.set_xticks(x, labels=subset["model"], rotation=30, ha="right")
        ax.set_ylabel(f"Coefficient on {target_term}")
        ax.spines[["top", "right"]].set_visible(False)
        fig.tight_layout()
        save_figure(fig, outdir / "fig3_coefplot")
        plt.close(fig)

    manifest = {"models": [{"name": r.name, "formula": r.formula} for r in results], "summary": str(summary_path)}
    write_json(manifest, outdir / "model_manifest.json")
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Fit empirical regression models and export tables.")
    add_common_io(parser)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT / "tables"))
    parser.add_argument("--outcome", default=None)
    parser.add_argument("--treatment", default=None)
    parser.add_argument("--controls", default="")
    parser.add_argument("--control-sets", default="")
    parser.add_argument("--progressive", action="store_true")
    parser.add_argument("--fixed-effects", default="")
    parser.add_argument("--formula", default=None)
    parser.add_argument("--formulas", default=None)
    parser.add_argument("--model-names", default="")
    parser.add_argument("--model-type", default="ols", choices=["ols", "logit", "probit", "poisson", "iv"])
    parser.add_argument("--cluster", default=None)
    parser.add_argument("--cov-type", default="HC3")
    parser.add_argument("--keep-terms", default="")
    parser.add_argument("--plot-term", default=None)
    parser.add_argument("--no-figures", action="store_true")
    add_table_format_arg(parser)
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    print(json.dumps(run(args), indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
