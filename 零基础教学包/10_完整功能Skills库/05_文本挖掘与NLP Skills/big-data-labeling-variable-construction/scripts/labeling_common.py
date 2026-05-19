import json
import re
from pathlib import Path

import jieba
import pandas as pd


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
            extra = {
                line.strip()
                for line in path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            }
            words.update(extra)
    return words


def normalize_text(text: str) -> str:
    text = "" if text is None else str(text)
    text = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def tokenize_text(text: str, stopwords: set[str], min_token_len: int = 2) -> list[str]:
    normalized = normalize_text(text)
    tokens = [token.strip() for token in jieba.lcut(normalized) if token.strip()]
    return [
        token
        for token in tokens
        if token not in stopwords and len(token) >= min_token_len and not token.isdigit()
    ]


def require_columns(df: pd.DataFrame, columns: list[str]) -> None:
    missing = [column for column in columns if column not in df.columns]
    if missing:
        raise ValueError(f"Input is missing required columns: {missing}")


def save_json(path: Path, payload: dict | list) -> Path:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def average_text_length(series: pd.Series) -> float:
    values = series.fillna("").astype(str)
    if values.empty:
        return 0.0
    return float(values.map(len).mean())


def infer_id_column(df: pd.DataFrame) -> str | None:
    candidates = ["doc_id", "id", "document_id", "docid", "编号", "序号"]
    lowered = {str(column).lower(): column for column in df.columns}
    for candidate in candidates:
        if candidate.lower() in lowered:
            return str(lowered[candidate.lower()])
    for column in df.columns:
        if df[column].is_unique and not df[column].isna().any():
            return str(column)
    return None


def infer_text_column(df: pd.DataFrame) -> str | None:
    best_column = None
    best_score = -1.0
    for column in df.columns:
        series = df[column]
        if pd.api.types.is_numeric_dtype(series):
            continue
        avg_len = average_text_length(series)
        unique_ratio = float(series.astype(str).nunique()) / max(len(series), 1)
        score = avg_len + unique_ratio * 10
        if avg_len >= 8 and score > best_score:
            best_score = score
            best_column = str(column)
    return best_column


def infer_label_column(df: pd.DataFrame, text_column: str | None = None) -> str | None:
    best_column = None
    best_score = -1.0
    row_count = max(len(df), 1)
    for column in df.columns:
        if text_column and str(column) == text_column:
            continue
        series = df[column]
        unique_count = int(series.astype(str).nunique())
        if unique_count < 2 or unique_count > min(50, row_count):
            continue
        if pd.api.types.is_numeric_dtype(series) and unique_count > 20:
            continue
        avg_len = average_text_length(series)
        score = (20 - min(avg_len, 20)) + (10 / unique_count)
        if score > best_score:
            best_score = score
            best_column = str(column)
    return best_column
