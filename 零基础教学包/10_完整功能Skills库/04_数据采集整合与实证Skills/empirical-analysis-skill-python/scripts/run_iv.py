from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import statsmodels.api as sm

from common import DEFAULT_OUTPUT, add_common_io, add_table_format_arg, export_table, parse_cols, read_data, require_columns, write_json


def add_fixed_effect_dummies(df: pd.DataFrame, fixed_effects: list[str]) -> tuple[pd.DataFrame, list[str]]:
    data = df.copy()
    dummy_cols: list[str] = []
    for fe in fixed_effects:
        dummies = pd.get_dummies(data[fe], prefix=fe, drop_first=True).astype(float)
        rename = {col: re.sub(r"\W+", "_", str(col)) for col in dummies.columns}
        dummies = dummies.rename(columns=rename)
        data = pd.concat([data, dummies], axis=1)
        dummy_cols.extend(rename.values())
    return data, dummy_cols


def fit_iv(data: pd.DataFrame, formula: str, method: str, cluster: str | None) -> Any:
    try:
        from linearmodels.iv import IV2SLS, IVGMM, IVLIML
    except ImportError as exc:
        raise RuntimeError("Install linearmodels to run IV models.") from exc
    model_cls = {"2sls": IV2SLS, "liml": IVLIML, "gmm": IVGMM}[method]
    model = model_cls.from_formula(formula, data=data)
    if cluster:
        return model.fit(cov_type="clustered", clusters=data[cluster])
    return model.fit(cov_type="robust")


def fit_2sls_fallback(data: pd.DataFrame, outcome: str, endog: str, exog_cols: list[str], instrument_cols: list[str]) -> dict[str, Any]:
    from scipy import stats

    y = pd.to_numeric(data[outcome], errors="coerce")
    exog = data[[endog] + exog_cols].apply(pd.to_numeric, errors="coerce")
    instruments = data[instrument_cols + exog_cols].apply(pd.to_numeric, errors="coerce")
    model_data = pd.concat([y.rename(outcome), exog, instruments], axis=1).dropna()
    y_clean = model_data[outcome].to_numpy(dtype=float)
    exog_clean = sm.add_constant(model_data[[endog] + exog_cols], has_constant="add")
    inst_clean = sm.add_constant(model_data[instrument_cols + exog_cols], has_constant="add")
    x = exog_clean.to_numpy(dtype=float)
    z = inst_clean.to_numpy(dtype=float)
    z_pinv = np.linalg.pinv(z)
    x_hat = z @ (z_pinv @ x)
    beta = np.linalg.pinv(x_hat) @ y_clean
    resid = y_clean - x @ beta
    nobs, k_params = x.shape
    dof = max(nobs - k_params, 1)
    sigma2 = float((resid @ resid) / dof)
    vcov = sigma2 * np.linalg.pinv(x_hat.T @ x_hat)
    se = np.sqrt(np.diag(vcov))
    tvals = beta / se
    pvalues = 2 * (1 - stats.t.cdf(np.abs(tvals), df=dof))
    fitted = x @ beta
    ssr = float(((y_clean - fitted) ** 2).sum())
    tss = float(((y_clean - y_clean.mean()) ** 2).sum())
    rsquared = 1 - ssr / tss if tss else np.nan
    index = exog_clean.columns
    return {
        "params": pd.Series(beta, index=index),
        "std_errors": pd.Series(se, index=index),
        "pvalues": pd.Series(pvalues, index=index),
        "nobs": float(nobs),
        "rsquared": float(rsquared),
        "summary": "Manual 2SLS fallback using projection on instruments and Moore-Penrose pseudoinverse. Install linearmodels for full IV diagnostics.",
        "first_stage": "linearmodels is not installed; manual 2SLS fallback does not expose first-stage diagnostics.",
    }


def diagnostic_value(obj: Any) -> str | float | None:
    if obj is None:
        return None
    try:
        if hasattr(obj, "stat"):
            return float(obj.stat)
        return str(obj)
    except Exception:
        return str(obj)


def run(args: argparse.Namespace) -> dict[str, Any]:
    df = read_data(args.input, args.sheet)
    controls = parse_cols(args.controls)
    instruments = parse_cols(args.instruments)
    fixed_effects = parse_cols(args.fixed_effects)
    required = [args.outcome, args.endog] + controls + instruments + fixed_effects
    if args.cluster:
        required.append(args.cluster)
    require_columns(df, required, "IV columns")

    data, fe_dummy_cols = add_fixed_effect_dummies(df, fixed_effects)
    exog = controls + fe_dummy_cols
    rhs = "1"
    if exog:
        rhs += " + " + " + ".join(exog)
    formula = args.formula or f"{args.outcome} ~ {rhs} + [{args.endog} ~ {' + '.join(instruments)}]"

    rows: list[dict[str, Any]] = []
    summaries: list[str] = []
    diagnostics: dict[str, Any] = {}
    for method in parse_cols(args.methods):
        used_fallback = False
        try:
            result = fit_iv(data, formula, method, args.cluster)
        except RuntimeError:
            if method != "2sls" or args.formula:
                raise
            result = fit_2sls_fallback(data, args.outcome, args.endog, exog, instruments)
            used_fallback = True
        terms = parse_cols(args.keep_terms) or [args.endog]
        for term in terms:
            params = result["params"] if used_fallback else result.params
            std_errors = result["std_errors"] if used_fallback else result.std_errors
            pvalues = result["pvalues"] if used_fallback else result.pvalues
            nobs = result["nobs"] if used_fallback else float(result.nobs)
            rsquared = result["rsquared"] if used_fallback else (float(result.rsquared) if result.rsquared is not None else np.nan)
            if term in params.index:
                rows.append(
                    {
                        "model": method + ("_statsmodels_fallback" if used_fallback else ""),
                        "term": term,
                        "coef": float(params[term]),
                        "se": float(std_errors[term]),
                        "pvalue": float(pvalues[term]),
                        "nobs": nobs,
                        "rsquared": rsquared,
                        "formula": formula,
                    }
                )
        summary_text = result["summary"] if used_fallback else str(result.summary)
        summaries.append(f"[{method}] {formula}\n{summary_text}")
        if method == "2sls":
            diagnostics["first_stage"] = result["first_stage"] if used_fallback else str(result.first_stage)
            diagnostics["used_statsmodels_fallback"] = used_fallback
            if used_fallback:
                continue
            for attr in ["wu_hausman", "sargan", "basmann", "anderson_rubin"]:
                try:
                    value = getattr(result, attr)
                    if callable(value):
                        value = value()
                    diagnostics[attr] = diagnostic_value(value)
                except Exception as exc:
                    diagnostics[attr] = f"unavailable: {exc}"

    outdir = Path(args.output_dir)
    export_table(pd.DataFrame(rows).round(6), outdir / "iv_results", parse_cols(args.formats))
    summary_path = outdir / "iv_summaries.txt"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text("\n\n".join(summaries), encoding="utf-8")
    manifest = {"methods": parse_cols(args.methods), "formula": formula, "diagnostics": diagnostics, "summary": str(summary_path)}
    write_json(manifest, outdir / "iv_manifest.json")
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run fixed IV estimators.")
    add_common_io(parser)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT / "tables"))
    parser.add_argument("--outcome", required=True)
    parser.add_argument("--endog", required=True)
    parser.add_argument("--instruments", required=True)
    parser.add_argument("--controls", default="")
    parser.add_argument("--fixed-effects", default="")
    parser.add_argument("--cluster", default=None)
    parser.add_argument("--methods", default="2sls", help="Comma-separated: 2sls,liml,gmm.")
    parser.add_argument("--formula", default=None)
    parser.add_argument("--keep-terms", default="")
    add_table_format_arg(parser)
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    print(json.dumps(run(args), indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
