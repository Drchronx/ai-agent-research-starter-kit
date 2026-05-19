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
    controls = parse_cols(args.controls)
    fixed_effects = parse_cols(args.fixed_effects)
    require_columns(df, [args.outcome, args.treatment] + controls + fixed_effects, "robustness columns")

    rows: list[dict[str, object]] = []
    base_formula = args.formula or build_formula(args.outcome, args.treatment, controls, fixed_effects)
    variants: list[tuple[str, pd.DataFrame, str | None, str, str]] = [
        ("base_HC3", df, args.cluster, "HC3", base_formula),
        ("base_nonrobust", df, None, "nonrobust", base_formula),
    ]

    for cluster in parse_cols(args.cluster_vars):
        require_columns(df, [cluster], "cluster variable")
        variants.append((f"cluster_{cluster}", df, cluster, "HC3", base_formula))
    for idx, query in enumerate(parse_semicolon(args.filters)):
        subset = df.query(query).copy()
        variants.append((f"filter_{idx + 1}", subset, args.cluster if args.cluster in subset.columns else None, "HC3", base_formula))
    for placebo in parse_cols(args.placebo_vars):
        require_columns(df, [placebo], "placebo variable")
        variants.append((f"placebo_{placebo}", df, args.cluster, "HC3", base_formula.replace(args.treatment, placebo)))
    for idx, controls_set in enumerate(control_sets(args)):
        variants.append((f"controls_{idx + 1}", df, args.cluster, "HC3", build_formula(args.outcome, args.treatment, controls_set, fixed_effects)))

    term = args.plot_term or args.treatment
    for name, data, cluster, cov_type, formula in variants:
        if len(data) < args.min_n:
            continue
        try:
            fitted = fit_model(data, formula, args.model_type, cluster, cov_type, name)
            rows.extend(fit_result_rows(fitted, [term]))
        except Exception as exc:
            rows.append({"model": name, "term": term, "coef": np.nan, "se": np.nan, "pvalue": np.nan, "nobs": len(data), "rsquared": np.nan, "formula": formula, "error": str(exc)})

    table = pd.DataFrame(rows).round(6)
    export_table(table, outdir / "table5_robustness", parse_cols(args.formats))

    if not args.no_figures and not table.empty and table["coef"].notna().any():
        plot_df = table.dropna(subset=["coef", "se"]).copy().sort_values("coef")
        plt = import_matplotlib()
        fig, ax = plt.subplots(figsize=(8, max(4, 0.28 * len(plot_df))))
        y = np.arange(len(plot_df))
        ax.errorbar(plot_df["coef"], y, xerr=1.96 * plot_df["se"], fmt="o", capsize=3)
        ax.axvline(0, linestyle="--", linewidth=0.8, color="gray")
        ax.set_yticks(y, labels=plot_df["model"])
        ax.set_xlabel(f"Coefficient on {term}")
        ax.spines[["top", "right"]].set_visible(False)
        fig.tight_layout()
        save_figure(fig, outdir / "fig4_sensitivity")
        plt.close(fig)

    manifest = {"variants": [v[0] for v in variants], "output_dir": str(outdir)}
    write_json(manifest, outdir / "robustness_manifest.json")
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run fixed robustness variants.")
    add_common_io(parser)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT / "tables"))
    parser.add_argument("--outcome", required=True)
    parser.add_argument("--treatment", required=True)
    parser.add_argument("--controls", default="")
    parser.add_argument("--control-sets", default="")
    parser.add_argument("--progressive", action="store_true")
    parser.add_argument("--fixed-effects", default="")
    parser.add_argument("--formula", default=None)
    parser.add_argument("--model-type", default="ols", choices=["ols", "logit", "probit", "poisson"])
    parser.add_argument("--cluster", default=None)
    parser.add_argument("--cluster-vars", default="")
    parser.add_argument("--filters", default="")
    parser.add_argument("--placebo-vars", default="")
    parser.add_argument("--plot-term", default=None)
    parser.add_argument("--min-n", type=int, default=20)
    parser.add_argument("--no-figures", action="store_true")
    add_table_format_arg(parser)
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    print(json.dumps(run(args), indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
