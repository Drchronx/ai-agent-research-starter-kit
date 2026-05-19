import hashlib
import os
import re
from urllib.parse import urljoin

from settings import CNKI_BASE_URL, DB_DSN_ENV


class CNKIPaperRepository:
    def __init__(self, dsn=None, ensure_table=True):
        psycopg2, extras = self._load_psycopg2()
        self.psycopg2 = psycopg2
        self.extras = extras
        self.conn = psycopg2.connect(dsn or os.getenv(DB_DSN_ENV) or "")
        if ensure_table:
            self.ensure_table()

    @staticmethod
    def _load_psycopg2():
        try:
            import psycopg2
            from psycopg2 import extras
        except ImportError as e:
            raise ImportError("缺少 psycopg2，请先安装 psycopg2-binary 后再启用数据库保存。") from e
        return psycopg2, extras

    @staticmethod
    def build_search_id(title, journal, year):
        raw = f"{title or ''}|{journal or ''}|{year or ''}"
        return hashlib.md5(raw.encode("utf-8")).hexdigest()

    @staticmethod
    def parse_query_pattern(query_pattern):
        query_pattern = (query_pattern or "").strip()
        simple_match = re.fullmatch(r"([A-Za-z]+)\s*(=|%)\s*'([^']+)'", query_pattern)
        if simple_match:
            return simple_match.group(3), simple_match.group(1).upper()
        return query_pattern, ""

    @staticmethod
    def split_items(value):
        if not value:
            return []
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]

        value = re.sub(r"^(关键词|基金|基金资助|作者|组织|机构)[:：]\s*", "", value.strip())
        items = []
        for item in re.split(r"[;；]", value):
            item = item.strip()
            if not item:
                continue
            item = item.replace("【", "[").replace("】", "]")
            items.append(item)
        return items

    @staticmethod
    def extract_year(paper):
        publish_date = paper.get("发表时间") or paper.get("publish_date") or ""
        year = paper.get("年") or paper.get("year") or ""
        match = re.search(r"\d{4}", year or publish_date)
        if match:
            return match.group(0)
        return year

    @staticmethod
    def normalize_detail_url(detail_url):
        if not detail_url:
            return ""
        return urljoin(CNKI_BASE_URL, detail_url)

    def ensure_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS cnki_papers (
            id SERIAL PRIMARY KEY,
            search_id VARCHAR(64) UNIQUE NOT NULL,
            title VARCHAR(500) NOT NULL,
            journal VARCHAR(200),
            publish_date VARCHAR(50),
            year VARCHAR(10),
            issue VARCHAR(20),
            authors TEXT[],
            organizations TEXT[],
            abstract TEXT,
            keywords TEXT[],
            funds TEXT[],
            cited_count VARCHAR(20),
            download_count VARCHAR(20),
            detail_url VARCHAR(500),
            search_terms VARCHAR(200),
            field_code VARCHAR(20),
            source_categories TEXT[],
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        with self.conn:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)

    def build_record(self, paper, query_pattern, source_categories=None):
        title = paper.get("篇名") or paper.get("title") or ""
        journal = paper.get("刊名") or paper.get("journal") or ""
        publish_date = paper.get("发表时间") or paper.get("publish_date") or ""
        year = self.extract_year(paper)
        detail_url = self.normalize_detail_url(paper.get("详情页链接") or paper.get("detail_url") or "")
        search_terms, field_code = self.parse_query_pattern(query_pattern)

        return {
            "search_id": self.build_search_id(title, journal, year),
            "title": title,
            "journal": journal,
            "publish_date": publish_date,
            "year": year,
            "issue": paper.get("期") or paper.get("issue") or "",
            "authors": self.split_items(paper.get("作者") or paper.get("authors") or ""),
            "organizations": self.split_items(paper.get("组织") or paper.get("organizations") or ""),
            "abstract": paper.get("摘要") or paper.get("abstract") or "",
            "keywords": self.split_items(paper.get("关键词") or paper.get("keywords") or ""),
            "funds": self.split_items(paper.get("基金资助") or paper.get("funds") or ""),
            "cited_count": paper.get("被引数") or paper.get("cited_count") or "",
            "download_count": paper.get("下载数") or paper.get("download_count") or "",
            "detail_url": detail_url,
            "search_terms": search_terms,
            "field_code": field_code,
            "source_categories": source_categories or [],
        }

    def save_papers(self, papers, query_pattern, source_categories=None):
        if not papers:
            return 0

        columns = [
            "search_id",
            "title",
            "journal",
            "publish_date",
            "year",
            "issue",
            "authors",
            "organizations",
            "abstract",
            "keywords",
            "funds",
            "cited_count",
            "download_count",
            "detail_url",
            "search_terms",
            "field_code",
            "source_categories",
        ]
        records = [self.build_record(paper, query_pattern, source_categories) for paper in papers]
        values = [tuple(record[column] for column in columns) for record in records]
        sql = f"""
        INSERT INTO cnki_papers ({', '.join(columns)})
        VALUES %s
        ON CONFLICT (search_id) DO UPDATE SET
            title = EXCLUDED.title,
            journal = EXCLUDED.journal,
            publish_date = EXCLUDED.publish_date,
            year = EXCLUDED.year,
            issue = EXCLUDED.issue,
            authors = EXCLUDED.authors,
            organizations = EXCLUDED.organizations,
            abstract = EXCLUDED.abstract,
            keywords = EXCLUDED.keywords,
            funds = EXCLUDED.funds,
            cited_count = EXCLUDED.cited_count,
            download_count = EXCLUDED.download_count,
            detail_url = EXCLUDED.detail_url,
            search_terms = EXCLUDED.search_terms,
            field_code = EXCLUDED.field_code,
            source_categories = EXCLUDED.source_categories,
            updated_at = CURRENT_TIMESTAMP;
        """

        with self.conn:
            with self.conn.cursor() as cursor:
                self.extras.execute_values(cursor, sql, values)
        return len(records)

    def close(self):
        if self.conn:
            self.conn.close()
