#!/usr/bin/env python3
"""
Shared paper metadata models for the literature reviewer workflow.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class Author:
    name: str = ""
    affiliation: str = ""

    def format_for_citation(self) -> str:
        return self.name


@dataclass
class Paper:
    """
    Normalized paper record returned by retrieval backends.
    """
    id: str = ""
    doi: str = ""
    backend: str = ""
    backend_query: str = ""

    title: str = ""
    authors: List[str] = field(default_factory=list)
    organizations: List[str] = field(default_factory=list)
    abstract: str = ""
    keywords: List[str] = field(default_factory=list)
    funds: List[str] = field(default_factory=list)

    journal: str = ""
    year: Optional[int] = None
    publish_date: str = ""
    volume: str = ""
    issue: str = ""
    pages: str = ""

    language: str = "en"
    source_db: str = ""
    source_url: str = ""
    cited_count: str = ""
    download_count: str = ""

    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "doi": self.doi,
            "backend": self.backend,
            "backend_query": self.backend_query,
            "title": self.title,
            "authors": self.authors,
            "organizations": self.organizations,
            "abstract": self.abstract,
            "keywords": self.keywords,
            "funds": self.funds,
            "journal": self.journal,
            "year": self.year,
            "publish_date": self.publish_date,
            "volume": self.volume,
            "issue": self.issue,
            "pages": self.pages,
            "language": self.language,
            "source_db": self.source_db,
            "source_url": self.source_url,
            "cited_count": self.cited_count,
            "download_count": self.download_count,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Paper":
        return cls(
            id=data.get("id", ""),
            doi=data.get("doi", ""),
            backend=data.get("backend", ""),
            backend_query=data.get("backend_query", ""),
            title=data.get("title", ""),
            authors=data.get("authors", []),
            organizations=data.get("organizations", []),
            abstract=data.get("abstract", ""),
            keywords=data.get("keywords", []),
            funds=data.get("funds", []),
            journal=data.get("journal", ""),
            year=data.get("year"),
            publish_date=data.get("publish_date", ""),
            volume=data.get("volume", ""),
            issue=data.get("issue", ""),
            pages=data.get("pages", ""),
            language=data.get("language", "en"),
            source_db=data.get("source_db", ""),
            source_url=data.get("source_url", ""),
            cited_count=data.get("cited_count", ""),
            download_count=data.get("download_count", ""),
        )

    def get_first_author(self) -> str:
        if self.authors:
            return self.authors[0]
        return "Unknown"