from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from common import DEFAULT_OUTPUT, import_matplotlib, read_data, require_columns, save_figure, write_json


def plot_coef(df: pd.DataFrame, args: argparse.Namespace) -> list[str]:
    require_columns(df, [args.coef_col, args.se_col, args.label_col], "coef plot columns")
    data = df.copy()
    if args.term and "term" in data.columns:
        data = data.loc[data["term"] == args.term].copy()
    data = data.dropna(subset=[args.coef_col, args.se_col])
    plt = import_matplotlib()
    fig, ax = plt.subplots(figsize=(7, max(4, 0.35 * len(data))))
    y = np.arange(len(data))
    ax.errorbar(data[args.coef_col], y, xerr=1.96 * data[args.se_col], fmt="o", capsize=3)
    ax.axvline(0, linestyle="--", linewidth=0.8, color="gray")
    ax.set_yticks(y, labels=data[args.label_col].astype(str))
    ax.set_xlabel(args.xlabel or "Coefficient")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    written = save_figure(fig, Path(args.output_dir) / args.stem)
    plt.close(fig)
    return written


def plot_event(df: pd.DataFrame, args: argparse.Namespace) -> list[str]:
    require_columns(df, [args.rel_col, args.coef_col, args.se_col], "event plot columns")
    data = df.dropna(subset=[args.rel_col, args.coef_col, args.se_col]).sort_values(args.rel_col)
    plt = import_matplotlib()
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.errorbar(data[args.rel_col], data[args.coef_col], yerr=1.96 * data[args.se_col], fmt="o-", capsize=3)
    ax.axhline(0, linestyle="--", linewidth=0.8, color="gray")
    ax.axvline(args.ref_period, linestyle=":", linewidth=0.8, color="gray")
    ax.set_xlabel(args.xlabel or "Relative time")
    ax.set_ylabel(args.ylabel or "Effect")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    written = save_figure(fig, Path(args.output_dir) / args.stem)
    plt.close(fig)
    return written


def plot_binscatter(df: pd.DataFrame, args: argparse.Namespace) -> list[str]:
    require_columns(df, [args.x, args.y], "binscatter columns")
    data = df[[args.x, args.y]].dropna().copy()
    data["bin"] = pd.qcut(data[args.x], q=args.bins, duplicates="drop")
    plot_df = data.groupby("bin", observed=True).agg(x_mean=(args.x, "mean"), y_mean=(args.y, "mean")).reset_index()
    plt = import_matplotlib()
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(plot_df["x_mean"], plot_df["y_mean"])
    ax.set_xlabel(args.xlabel or args.x)
    ax.set_ylabel(args.ylabel or args.y)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    written = save_figure(fig, Path(args.output_dir) / args.stem)
    plt.close(fig)
    return written


def plot_love(df: pd.DataFrame, args: argparse.Namespace) -> list[str]:
    require_columns(df, [args.var_col, args.pre_col, args.post_col], "love plot columns")
    data = df.copy().sort_values(args.pre_col)
    plt = import_matplotlib()
    fig, ax = plt.subplots(figsize=(7, max(4, 0.28 * len(data))))
    y = np.arange(len(data))
    ax.scatter(data[args.pre_col].abs(), y, label="pre")
    ax.scatter(data[args.post_col].abs(), y, label="post")
    ax.axvline(0.1, linestyle="--", linewidth=0.8, color="gray")
    ax.set_yticks(y, labels=data[args.var_col].astype(str))
    ax.set_xlabel("Absolute standardized mean difference")
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    written = save_figure(fig, Path(args.output_dir) / args.stem)
    plt.close(fig)
    return written


def run(args: argparse.Namespace) -> dict[str, object]:
    df = read_data(args.input, args.sheet)
    if args.kind == "coef":
        written = plot_coef(df, args)
    elif args.kind == "event":
        written = plot_event(df, args)
    elif args.kind == "binscatter":
        written = plot_binscatter(df, args)
    elif args.kind == "love":
        written = plot_love(df, args)
    else:
        raise ValueError(f"Unsupported plot kind: {args.kind}")
    manifest = {"input": args.input, "kind": args.kind, "written": written}
    write_json(manifest, Path(args.output_dir) / f"{args.stem}_manifest.json")
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create fixed empirical plots.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--sheet", default=None)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT / "figures"))
    parser.add_argument("--kind", required=True, choices=["coef", "event", "binscatter", "love"])
    parser.add_argument("--stem", default="figure")
    parser.add_argument("--coef-col", default="coef")
    parser.add_argument("--se-col", default="se")
    parser.add_argument("--label-col", default="model")
    parser.add_argument("--term", default=None)
    parser.add_argument("--rel-col", default="rel_time")
    parser.add_argument("--ref-period", type=float, default=-1)
    parser.add_argument("--x", default=None)
    parser.add_argument("--y", default=None)
    parser.add_argument("--bins", type=int, default=20)
    parser.add_argument("--var-col", default="variable")
    parser.add_argument("--pre-col", default="SMD_pre")
    parser.add_argument("--post-col", default="SMD_post")
    parser.add_argument("--xlabel", default=None)
    parser.add_argument("--ylabel", default=None)
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    print(json.dumps(run(args), indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
