import json
import math
import os
import re
from collections import Counter
from pathlib import Path
from typing import Iterable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import font_manager

import jieba

try:
    from opencc import OpenCC  # type: ignore
except ImportError:  # pragma: no cover
    OpenCC = None


FONT_PATH_CANDIDATES = [
    os.getenv("OPENCLAW_CJK_FONT", "").strip(),
    r"C:\Program Files\Microsoft Office\root\vfs\Fonts\private\STSONG.TTF",
    r"C:\Windows\Fonts\msyh.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
]
FONT_NAME_CANDIDATES = [
    "STSong",
    "Microsoft YaHei",
    "SimHei",
    "Noto Sans CJK SC",
    "Source Han Sans SC",
    "DejaVu Sans",
]
DEFAULT_STOPWORDS = {
    "我们",
    "你们",
    "他们",
    "以及",
    "进行",
    "实现",
    "研究",
    "分析",
    "相关",
    "可以",
    "具有",
    "通过",
    "对于",
    "一个",
    "这种",
    "其中",
    "因此",
    "进一步",
    "本文",
    "本研究",
}


def configure_matplotlib() -> str:
    plt.rcParams["figure.dpi"] = 180
    plt.rcParams["savefig.dpi"] = 300
    plt.rcParams["axes.unicode_minus"] = False
    installed_names = {font.name for font in font_manager.fontManager.ttflist}

    for raw_path in FONT_PATH_CANDIDATES:
        if not raw_path:
            continue
        font_path = Path(raw_path)
        if font_path.exists() and font_path.is_file():
            font_manager.fontManager.addfont(str(font_path))
            font_name = font_manager.FontProperties(fname=str(font_path)).get_name()
            plt.rcParams["font.family"] = font_name
            plt.rcParams["font.sans-serif"] = [font_name, *FONT_NAME_CANDIDATES]
            return font_name

    for font_name in FONT_NAME_CANDIDATES:
        if font_name in installed_names:
            plt.rcParams["font.family"] = font_name
            plt.rcParams["font.sans-serif"] = [font_name, *FONT_NAME_CANDIDATES]
            return font_name

    plt.rcParams["font.family"] = "DejaVu Sans"
    return "DejaVu Sans"


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_table(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    raise ValueError(f"Unsupported file type: {path.suffix}")


def load_stopwords(stopwords_path: str | None = None) -> set[str]:
    words = set(DEFAULT_STOPWORDS)
    if stopwords_path:
        path = Path(stopwords_path)
        if path.exists():
            loaded = {
                line.strip()
                for line in path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            }
            words.update(loaded)
    return words


def normalize_text(text: str) -> str:
    text = "" if text is None else str(text)
    if OpenCC is not None:
        text = OpenCC("t2s").convert(text)
    text = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def tokenize_text(text: str, stopwords: set[str], min_token_len: int = 2) -> list[str]:
    normalized = normalize_text(text)
    tokens = [token.strip() for token in jieba.lcut(normalized) if token.strip()]
    cleaned = [
        token
        for token in tokens
        if token not in stopwords and len(token) >= min_token_len and not token.isdigit()
    ]
    return cleaned


def build_preprocessed_frame(
    df: pd.DataFrame,
    text_col: str,
    id_col: str,
    stopwords: set[str],
    min_token_len: int = 2,
) -> pd.DataFrame:
    if text_col not in df.columns or id_col not in df.columns:
        raise ValueError(f"Input must contain '{id_col}' and '{text_col}' columns.")
    local = df[[id_col, text_col]].copy()
    local[text_col] = local[text_col].fillna("").astype(str)
    local["normalized_text"] = local[text_col].apply(normalize_text)
    local["tokens"] = local[text_col].apply(lambda text: tokenize_text(text, stopwords, min_token_len=min_token_len))
    local["token_count"] = local["tokens"].apply(len)
    local = local[local["token_count"] > 0].reset_index(drop=True)
    if local.empty:
        raise ValueError("No valid documents remain after preprocessing.")
    local["joined_tokens"] = local["tokens"].apply(lambda values: " ".join(values))
    return local


def save_preprocessed_outputs(df: pd.DataFrame, output_dir: Path) -> tuple[Path, Path]:
    processed_path = output_dir / "preprocessed_documents.csv"
    tokens_path = output_dir / "token_lists.json"
    export = df.copy()
    export["tokens"] = export["tokens"].apply(lambda values: "|".join(values))
    export.to_csv(processed_path, index=False, encoding="utf-8-sig")
    tokens_path.write_text(
        json.dumps(df["tokens"].tolist(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return processed_path, tokens_path


def save_token_frequency(tokens: Iterable[list[str]], output_dir: Path, top_n: int = 50) -> Path:
    counter = Counter(token for doc in tokens for token in doc)
    frame = pd.DataFrame(counter.most_common(top_n), columns=["token", "count"])
    path = output_dir / "token_frequency.csv"
    frame.to_csv(path, index=False, encoding="utf-8-sig")
    return path


def topic_diversity(topic_words: list[list[str]]) -> float:
    filtered = [words for words in topic_words if words]
    if not filtered:
        return 0.0
    unique_words = {word for words in filtered for word in words}
    total_words = sum(len(words) for words in filtered)
    return round(len(unique_words) / total_words, 6) if total_words else 0.0


def plot_metric_lines(
    evaluation_df: pd.DataFrame,
    x_col: str,
    output_path: Path,
    title: str,
    primary_cols: list[str],
    secondary_cols: list[str] | None = None,
) -> Path:
    configure_matplotlib()
    fig, ax1 = plt.subplots(figsize=(8.5, 5.2))
    for column in primary_cols:
        ax1.plot(evaluation_df[x_col], evaluation_df[column], marker="o", label=column)
    ax1.set_xlabel(x_col)
    ax1.set_ylabel(", ".join(primary_cols))
    ax1.grid(alpha=0.3, linestyle="--")

    handles, labels = ax1.get_legend_handles_labels()
    if secondary_cols:
        ax2 = ax1.twinx()
        for column in secondary_cols:
            ax2.plot(evaluation_df[x_col], evaluation_df[column], marker="s", linestyle=":", label=column)
        ax2.set_ylabel(", ".join(secondary_cols))
        secondary_handles, secondary_labels = ax2.get_legend_handles_labels()
        handles += secondary_handles
        labels += secondary_labels
    ax1.set_title(title)
    ax1.legend(handles, labels, loc="best")
    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    return output_path


def integer_range(spec: str) -> list[int]:
    values: list[int] = []
    for part in spec.split(","):
        item = part.strip()
        if not item:
            continue
        if "-" in item:
            start, end = item.split("-", 1)
            values.extend(range(int(start), int(end) + 1))
        else:
            values.append(int(item))
    unique = sorted({value for value in values if value > 0})
    if not unique:
        raise ValueError("Topic range must contain at least one positive integer.")
    return unique


def safe_mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan
