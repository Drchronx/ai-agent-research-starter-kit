#!/usr/bin/env python
import argparse
from pathlib import Path

import numpy as np
import pandas as pd

if not hasattr(np, "MachAr"):
    from numpy.core._machar import MachAr as _MachAr
    np.MachAr = _MachAr

try:
    import statsmodels.formula.api as smf
    from scipy import stats
except Exception as exc:
    raise SystemExit(f"Missing dependency: {exc}. Install pandas, scipy, and statsmodels.")


def fmt_p(p):
    if pd.isna(p):
        return ""
    if p < .001:
        return "< .001"
    return f"{p:.3f}"


def cohen_d(x, g):
    vals = [x[g == v].dropna().astype(float) for v in sorted(pd.unique(g.dropna()))]
    if len(vals) != 2:
        return np.nan
    a, b = vals
    if len(a) < 2 or len(b) < 2:
        return np.nan
    pooled = np.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2))
    return (a.mean() - b.mean()) / pooled if pooled else np.nan


def regression_table(model):
    out = pd.DataFrame({
        "term": model.params.index,
        "estimate": model.params.values,
        "se": model.bse.values,
        "t": model.tvalues.values,
        "p": model.pvalues.values,
        "ci_low": model.conf_int()[0].values,
        "ci_high": model.conf_int()[1].values,
    })
    out["p_formatted"] = out["p"].map(fmt_p)
    return out


def cronbach_alpha(frame):
    items = frame.dropna()
    if items.shape[0] < 2 or items.shape[1] < 2:
        return np.nan
    item_vars = items.var(axis=0, ddof=1)
    total_var = items.sum(axis=1).var(ddof=1)
    if total_var == 0:
        return np.nan
    k = items.shape[1]
    return (k / (k - 1)) * (1 - item_vars.sum() / total_var)


def predictor_coef(model, predictor):
    if predictor in model.params.index:
        return model.params[predictor]
    matches = [idx for idx in model.params.index if idx.startswith(f"{predictor}[T.")]
    if len(matches) == 1:
        return model.params[matches[0]]
    return np.nan


def run_model(df, dv, ivs, covariates=None):
    terms = list(ivs)
    if covariates:
        terms += list(covariates)
    formula = f"{dv} ~ " + " + ".join(terms)
    return formula, smf.ols(formula, data=df).fit()


def bootstrap_indirect(df, x, m, y, n_boot=5000, seed=42):
    rng = np.random.default_rng(seed)
    effects = []
    clean = df[[x, m, y]].dropna()
    if clean.empty:
        return None
    for _ in range(n_boot):
        sample = clean.sample(len(clean), replace=True, random_state=int(rng.integers(0, 1_000_000_000)))
        a_model = smf.ols(f"{m} ~ {x}", data=sample).fit()
        b_model = smf.ols(f"{y} ~ {x} + {m}", data=sample).fit()
        a = predictor_coef(a_model, x)
        b = predictor_coef(b_model, m)
        effects.append(a * b)
    effects = np.array(effects, dtype=float)
    return {
        "indirect": float(np.nanmean(effects)),
        "ci_low": float(np.nanpercentile(effects, 2.5)),
        "ci_high": float(np.nanpercentile(effects, 97.5)),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--dv", required=True)
    ap.add_argument("--ivs", nargs="+", required=True)
    ap.add_argument("--mediators", nargs="*", default=[])
    ap.add_argument("--moderators", nargs="*", default=[])
    ap.add_argument("--covariates", nargs="*", default=[])
    ap.add_argument("--checks", nargs="*", default=[])
    ap.add_argument("--scale", action="append", default=[], help="Composite scale as name:item1,item2,item3")
    ap.add_argument("--outdir", default="scenario_analysis_output")
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(args.data)
    report = []
    report.append(f"# Scenario Experiment Analysis Report\n")
    report.append(f"Data: `{args.data}`")
    report.append(f"Rows: {len(df)}, Columns: {len(df.columns)}")
    report.append(f"DV: `{args.dv}`")
    report.append(f"IVs: {', '.join(args.ivs)}")

    miss = df.isna().mean().sort_values(ascending=False)
    miss.to_csv(outdir / "missingness.csv")

    reliability_rows = []
    for spec in args.scale:
        if ":" not in spec:
            report.append(f"\nWARN invalid scale spec ignored: `{spec}`")
            continue
        name, item_text = spec.split(":", 1)
        items = [c.strip() for c in item_text.split(",") if c.strip()]
        missing_items = [c for c in items if c not in df.columns]
        if missing_items:
            report.append(f"\nWARN scale `{name}` missing items: {', '.join(missing_items)}")
            continue
        alpha = cronbach_alpha(df[items].apply(pd.to_numeric, errors="coerce"))
        df[name] = df[items].apply(pd.to_numeric, errors="coerce").mean(axis=1)
        reliability_rows.append({
            "scale": name,
            "items": ", ".join(items),
            "n_items": len(items),
            "cronbach_alpha": alpha,
        })
    if reliability_rows:
        pd.DataFrame(reliability_rows).to_csv(outdir / "reliability.csv", index=False)
        report.append("\n## Reliability\nCreated composite scale columns from `--scale` specifications. See `reliability.csv`.")

    desc_cols = [args.dv] + args.ivs + args.mediators + args.moderators + args.covariates + args.checks
    desc_cols = [c for c in dict.fromkeys(desc_cols) if c in df.columns]
    df[desc_cols].describe(include="all").to_csv(outdir / "descriptives.csv")

    formula, model = run_model(df, args.dv, args.ivs, args.covariates)
    regression_table(model).to_csv(outdir / "model_primary.csv", index=False)
    report.append(f"\n## Primary Model\nFormula: `{formula}`")
    report.append(f"R-squared: {model.rsquared:.3f}")

    if len(args.ivs) == 1:
        iv = args.ivs[0]
        d = cohen_d(df[args.dv], df[iv]) if iv in df.columns else np.nan
        if not pd.isna(d):
            report.append(f"Cohen's d for `{iv}` groups on `{args.dv}`: {d:.3f}")

    for check in args.checks:
        if check in df.columns:
            formula_c, model_c = run_model(df, check, args.ivs, args.covariates)
            regression_table(model_c).to_csv(outdir / f"manipulation_check_{check}.csv", index=False)
            report.append(f"\n## Manipulation Check: `{check}`\nFormula: `{formula_c}`; R-squared: {model_c.rsquared:.3f}")

    for med in args.mediators:
        if med in df.columns and len(args.ivs) == 1:
            res = bootstrap_indirect(df, args.ivs[0], med, args.dv)
            if res:
                report.append(f"\n## Mediation: `{args.ivs[0]}` -> `{med}` -> `{args.dv}`")
                report.append(f"Bootstrap indirect effect = {res['indirect']:.4f}, 95% CI [{res['ci_low']:.4f}, {res['ci_high']:.4f}]")

    for mod in args.moderators:
        if mod in df.columns and len(args.ivs) == 1:
            f = f"{args.dv} ~ {args.ivs[0]} * {mod}"
            if args.covariates:
                f += " + " + " + ".join(args.covariates)
            m = smf.ols(f, data=df).fit()
            regression_table(m).to_csv(outdir / f"moderation_{mod}.csv", index=False)
            report.append(f"\n## Moderation: `{mod}`\nFormula: `{f}`; R-squared: {m.rsquared:.3f}")

    report.append("\n## Notes\nReview all outputs manually. This script is a first-pass helper and does not replace preregistered analysis decisions.")
    (outdir / "analysis_report.md").write_text("\n\n".join(report), encoding="utf-8")
    print(outdir / "analysis_report.md")


if __name__ == "__main__":
    main()
