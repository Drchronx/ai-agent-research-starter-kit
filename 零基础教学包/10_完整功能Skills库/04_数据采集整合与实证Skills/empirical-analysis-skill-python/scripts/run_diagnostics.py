from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from common import DEFAULT_OUTPUT, add_common_io, add_table_format_arg, export_table, import_matplotlib, parse_cols, read_data, save_figure, write_json
from model_utils import build_formula, fit_model


def run(args: argparse.Namespace) -> dict[str, object]:
    df = read_data(args.input, args.sheet)
    outdir = Path(args.output_dir)
    controls = parse_cols(args.controls)
    fixed_effects = parse_cols(args.fixed_effects)
    formula = args.formula or build_formula(args.outcome, args.treatment, controls, fixed_effects)
    fitted = fit_model(df, formula, "ols", args.cluster, args.cov_type, "diagnostic_base")

    import statsmodels.formula.api as smf
    from statsmodels.stats.diagnostic import acorr_ljungbox, het_breuschpagan, het_white
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    from statsmodels.stats.stattools import durbin_watson, jarque_bera

    result = smf.ols(formula, data=df).fit()
    resid = result.resid
    exog = result.model.exog
    exog_names = result.model.exog_names

    rows = []
    jb_stat, jb_p, skew, kurt = jarque_bera(resid)
    rows.append({"test": "Jarque-Bera normality", "statistic": jb_stat, "pvalue": jb_p, "note": f"skew={skew:.4f}; kurtosis={kurt:.4f}"})
    bp = het_breuschpagan(resid, exog)
    rows.append({"test": "Breusch-Pagan heteroskedasticity", "statistic": bp[0], "pvalue": bp[1], "note": "Use robust or cluster SE if p<0.05."})
    white = het_white(resid, exog)
    rows.append({"test": "White heteroskedasticity", "statistic": white[0], "pvalue": white[1], "note": "Use robust or cluster SE if p<0.05."})
    rows.append({"test": "Durbin-Watson autocorrelation", "statistic": durbin_watson(resid), "pvalue": np.nan, "note": "Near 2 is low serial correlation."})
    try:
        lb = acorr_ljungbox(resid, lags=[min(10, max(1, int(len(resid) / 5)))], return_df=True)
        rows.append({"test": "Ljung-Box autocorrelation", "statistic": float(lb["lb_stat"].iloc[0]), "pvalue": float(lb["lb_pvalue"].iloc[0]), "note": "Serial correlation diagnostic."})
    except Exception as exc:
        rows.append({"test": "Ljung-Box autocorrelation", "statistic": np.nan, "pvalue": np.nan, "note": f"Skipped: {exc}"})
    rows.append({"test": "Condition number", "statistic": float(np.linalg.cond(exog)), "pvalue": np.nan, "note": "Large values indicate collinearity or scaling issues."})

    export_table(pd.DataFrame(rows).round(6), outdir / "diagnostic_tests", parse_cols(args.formats))

    vif_rows = []
    for idx, name in enumerate(exog_names):
        if name.lower() in {"intercept", "const"}:
            continue
        try:
            vif = variance_inflation_factor(exog, idx)
        except Exception:
            vif = np.nan
        vif_rows.append({"variable": name, "VIF": vif})
    export_table(pd.DataFrame(vif_rows).round(4), outdir / "vif", parse_cols(args.formats))

    if not args.no_figures:
        plt = import_matplotlib()
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.scatter(result.fittedvalues, resid, s=12, alpha=0.6)
        ax.axhline(0, linestyle="--", linewidth=0.8, color="gray")
        ax.set_xlabel("Fitted values")
        ax.set_ylabel("Residuals")
        ax.spines[["top", "right"]].set_visible(False)
        fig.tight_layout()
        save_figure(fig, outdir / "fig_residuals")
        plt.close(fig)

    manifest = {"formula": formula, "robust_formula_summary": fitted.formula, "output_dir": str(outdir)}
    write_json(manifest, outdir / "diagnostics_manifest.json")
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run empirical diagnostic tests.")
    add_common_io(parser)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT / "tables"))
    parser.add_argument("--outcome", required=True)
    parser.add_argument("--treatment", required=True)
    parser.add_argument("--controls", default="")
    parser.add_argument("--fixed-effects", default="")
    parser.add_argument("--formula", default=None)
    parser.add_argument("--cluster", default=None)
    parser.add_argument("--cov-type", default="HC3")
    parser.add_argument("--no-figures", action="store_true")
    add_table_format_arg(parser)
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    print(json.dumps(run(args), indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
