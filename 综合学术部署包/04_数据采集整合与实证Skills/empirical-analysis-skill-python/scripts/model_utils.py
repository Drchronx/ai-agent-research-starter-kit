from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from common import parse_cols, parse_semicolon, require_columns


def build_formula(outcome: str, treatment: str, controls: list[str], fixed_effects: list[str]) -> str:
    rhs_terms = [treatment] + controls + [f"C({fe})" for fe in fixed_effects]
    rhs = " + ".join(rhs_terms) if rhs_terms else "1"
    return f"{outcome} ~ {rhs}"


def control_sets(args: argparse.Namespace) -> list[list[str]]:
    explicit = parse_semicolon(getattr(args, "control_sets", None))
    if explicit:
        return [parse_cols(item.replace("+", ",")) for item in explicit]
    controls = parse_cols(getattr(args, "controls", None))
    if not controls:
        return [[]]
    if getattr(args, "progressive", False):
        return [controls[:idx] for idx in range(0, len(controls) + 1)]
    return [controls]


@dataclass
class FitResult:
    name: str
    formula: str
    params: pd.Series
    bse: pd.Series
    pvalues: pd.Series
    nobs: float
    rsquared: float | None
    text_summary: str


def fit_model(
    df: pd.DataFrame,
    formula: str,
    model_type: str,
    cluster: str | None,
    cov_type: str,
    name: str,
) -> FitResult:
    if model_type == "iv":
        try:
            from linearmodels.iv import IV2SLS
        except ImportError as exc:
            raise RuntimeError("Install linearmodels to run IV models.") from exc
        cov = "clustered" if cluster else ("robust" if cov_type.upper() in {"HC1", "HC2", "HC3", "ROBUST"} else "unadjusted")
        kwargs: dict[str, Any] = {"clusters": df[cluster]} if cluster else {}
        result = IV2SLS.from_formula(formula, data=df).fit(cov_type=cov, **kwargs)
        return FitResult(
            name=name,
            formula=formula,
            params=result.params,
            bse=result.std_errors,
            pvalues=result.pvalues,
            nobs=float(result.nobs),
            rsquared=float(result.rsquared) if result.rsquared is not None else None,
            text_summary=str(result.summary),
        )

    import statsmodels.formula.api as smf

    model_type = model_type.lower()
    if model_type == "ols":
        model = smf.ols(formula, data=df)
    elif model_type == "logit":
        model = smf.logit(formula, data=df)
    elif model_type == "probit":
        model = smf.probit(formula, data=df)
    elif model_type == "poisson":
        model = smf.poisson(formula, data=df)
    else:
        raise ValueError(f"Unsupported model type: {model_type}")

    if cluster:
        require_columns(df, [cluster], "cluster column")
        result = model.fit(cov_type="cluster", cov_kwds={"groups": df[cluster]}, disp=False)
    elif cov_type.lower() == "nonrobust":
        result = model.fit(disp=False)
    else:
        result = model.fit(cov_type=cov_type, disp=False)
    return FitResult(
        name=name,
        formula=formula,
        params=result.params,
        bse=result.bse,
        pvalues=result.pvalues,
        nobs=float(getattr(result, "nobs", np.nan)),
        rsquared=float(getattr(result, "rsquared", np.nan)) if hasattr(result, "rsquared") else None,
        text_summary=str(result.summary()),
    )


def fit_result_rows(result: FitResult, keep_terms: list[str] | None = None) -> list[dict[str, Any]]:
    rows = []
    terms = keep_terms or list(result.params.index)
    for term in terms:
        if term in result.params.index:
            rows.append(
                {
                    "model": result.name,
                    "term": term,
                    "coef": float(result.params[term]),
                    "se": float(result.bse[term]),
                    "pvalue": float(result.pvalues[term]),
                    "nobs": result.nobs,
                    "rsquared": result.rsquared,
                    "formula": result.formula,
                }
            )
    return rows
