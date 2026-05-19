#!/usr/bin/env python3
"""
Retrieval Coordinator for Literature Reviewer Skill

Coordinates three backend retrieval skills:
- cnki-crawler: Chinese papers from CNKI
- academic-research: English papers from OpenAlex
- academic-research-hub: English papers from Google Scholar

Usage:
    python retrieval_coordinator.py \
        --cnki-query "SU='耐心资本'" \
        --english-query "patient capital" \
        --start-year 2020 \
        --end-year 2025 \
        --output-dir ./sessions/20240408_patient_capital
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class RetrievalCoordinator:
    """Coordinates multi-backend literature retrieval."""

    def __init__(
        self,
        output_dir: str,
        cnki_query: Optional[str] = None,
        english_query: Optional[str] = None,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
        cnki_limit_pages: int = 10,
        openalex_limit: int = 50,
        scholar_limit: int = 30,
    ):
        self.output_dir = Path(output_dir)
        self.cnki_query = cnki_query
        self.english_query = english_query
        self.start_year = start_year
        self.end_year = end_year
        self.cnki_limit_pages = cnki_limit_pages
        self.openalex_limit = openalex_limit
        self.scholar_limit = scholar_limit

        self.session_log: List[str] = []
        self.backend_status: Dict[str, Dict] = {}
        self.all_papers: List[Dict] = []

        # Skill paths
        self.base_path = Path(__file__).parent.parent
        self.cnki_path = self.base_path.parent / "cnki-crawler"
        self.openalex_path = self.base_path.parent / "academic-research"
        self.scholar_path = self.base_path.parent / "academic-research-hub"

    def log(self, message: str):
        """Add message to session log."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.session_log.append(f"[{timestamp}] {message}")
        print(f"[{timestamp}] {message}")

    def setup_session(self):
        """Create session directory and initialize log."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / "output").mkdir(exist_ok=True)

        self.log(f"Session initialized: {self.output_dir}")
        self.log(f"CNKI query: {self.cnki_query or 'N/A'}")
        self.log(f"English query: {self.english_query or 'N/A'}")
        self.log(f"Year range: {self.start_year or 'N/A'} - {self.end_year or 'N/A'}")

    def run_cnki_retrieval(self) -> Tuple[bool, int, str]:
        """
        Run CNKI crawler backend.

        Returns:
            (success, paper_count, warning_message)
        """
        if not self.cnki_query:
            self.log("CNKI retrieval skipped: no query provided")
            self.backend_status["cnki"] = {
                "status": "skipped",
                "papers": 0,
                "warning": "No query provided"
            }
            return True, 0, ""

        self.log(f"Starting CNKI retrieval: {self.cnki_query}")
        self.log(f"Limit pages: {self.cnki_limit_pages}")

        try:
            # Build command - use python interpreter
            cmd = [
                sys.executable,
                str(self.cnki_path / "scripts" / "main.py"),
                self.cnki_query,
                "--limit-pages", str(self.cnki_limit_pages),
                "--no-estimated-time",
            ]

            if self.start_year:
                cmd.extend(["--start-year", str(self.start_year)])
            if self.end_year:
                cmd.extend(["--end-year", str(self.end_year)])

            self.log(f"Running: {' '.join(cmd)}")

            # Run crawler
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutes
                cwd=str(self.cnki_path)
            )

            if result.returncode != 0:
                warning = f"CNKI crawler failed: {result.stderr[:200]}"
                self.log(f"❌ {warning}")
                self.backend_status["cnki"] = {
                    "status": "failed",
                    "papers": 0,
                    "warning": warning
                }
                return False, 0, warning

            # Parse output for paper count
            # CNKI crawler outputs: "共抓取 X 篇论文"
            import re
            match = re.search(r'共抓取 (\d+) 篇论文', result.stdout)
            paper_count = int(match.group(1)) if match else 0

            self.log(f"✅ CNKI retrieval complete: {paper_count} papers")
            self.backend_status["cnki"] = {
                "status": "success",
                "papers": paper_count,
                "warning": ""
            }
            return True, paper_count, ""

        except subprocess.TimeoutExpired:
            warning = "CNKI retrieval timeout (5 minutes)"
            self.log(f"❌ {warning}")
            self.backend_status["cnki"] = {
                "status": "timeout",
                "papers": 0,
                "warning": warning
            }
            return False, 0, warning

        except Exception as e:
            warning = f"CNKI retrieval error: {str(e)}"
            self.log(f"❌ {warning}")
            self.backend_status["cnki"] = {
                "status": "error",
                "papers": 0,
                "warning": warning
            }
            return False, 0, warning

    def run_openalex_retrieval(self) -> Tuple[bool, int, str, List[Dict]]:
        """
        Run OpenAlex backend.

        Returns:
            (success, paper_count, warning_message, papers_list)
        """
        if not self.english_query:
            self.log("OpenAlex retrieval skipped: no query provided")
            self.backend_status["openalex"] = {
                "status": "skipped",
                "papers": 0,
                "warning": "No query provided"
            }
            return True, 0, "", []

        self.log(f"Starting OpenAlex retrieval: {self.english_query}")
        self.log(f"Limit: {self.openalex_limit}")

        try:
            # Build command
            cmd = [
                "python3",
                str(self.openalex_path / "scripts" / "scholar-search.py"),
                "search",
                self.english_query,
                "--limit", str(self.openalex_limit),
                "--json",
            ]

            if self.start_year and self.end_year:
                cmd.extend(["--years", f"{self.start_year}-{self.end_year}"])

            self.log(f"Running: {' '.join(cmd)}")

            # Run search
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutes
                cwd=str(self.openalex_path)
            )

            if result.returncode != 0:
                warning = f"OpenAlex search failed: {result.stderr[:200]}"
                self.log(f"❌ {warning}")
                self.backend_status["openalex"] = {
                    "status": "failed",
                    "papers": 0,
                    "warning": warning
                }
                return False, 0, warning, []

            # Parse JSON output
            papers_data = json.loads(result.stdout)
            if isinstance(papers_data, dict) and "results" in papers_data:
                papers_data = papers_data["results"]

            paper_count = len(papers_data)
            self.log(f"✅ OpenAlex retrieval complete: {paper_count} papers")

            # Normalize papers
            normalized_papers = []
            for paper in papers_data:
                normalized = self._normalize_openalex_paper(paper)
                if normalized:
                    normalized_papers.append(normalized)

            self.backend_status["openalex"] = {
                "status": "success",
                "papers": len(normalized_papers),
                "warning": ""
            }
            return True, len(normalized_papers), "", normalized_papers

        except subprocess.TimeoutExpired:
            warning = "OpenAlex retrieval timeout (5 minutes)"
            self.log(f"❌ {warning}")
            self.backend_status["openalex"] = {
                "status": "timeout",
                "papers": 0,
                "warning": warning
            }
            return False, 0, warning, []

        except json.JSONDecodeError as e:
            warning = f"OpenAlex JSON parse error: {str(e)}"
            self.log(f"❌ {warning}")
            self.backend_status["openalex"] = {
                "status": "parse_error",
                "papers": 0,
                "warning": warning
            }
            return False, 0, warning, []

        except Exception as e:
            warning = f"OpenAlex retrieval error: {str(e)}"
            self.log(f"❌ {warning}")
            self.backend_status["openalex"] = {
                "status": "error",
                "papers": 0,
                "warning": warning
            }
            return False, 0, warning, []

    def run_scholar_retrieval(self) -> Tuple[bool, int, str, List[Dict]]:
        """
        Run Google Scholar backend.

        Returns:
            (success, paper_count, warning_message, papers_list)
        """
        if not self.english_query:
            self.log("Google Scholar retrieval skipped: no query provided")
            self.backend_status["google_scholar"] = {
                "status": "skipped",
                "papers": 0,
                "warning": "No query provided"
            }
            return True, 0, "", []

        self.log(f"Starting Google Scholar retrieval: {self.english_query}")
        self.log(f"Limit: {self.scholar_limit}")

        try:
            # Build command
            cmd = [
                "python",
                str(self.scholar_path / "scripts" / "research.py"),
                self.english_query,
                "--max-results", str(self.scholar_limit),
                "--format", "json",
            ]

            if self.start_year:
                cmd.extend(["--start-year", str(self.start_year)])
            if self.end_year:
                cmd.extend(["--end-year", str(self.end_year)])

            self.log(f"Running: {' '.join(cmd)}")

            # Run search
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutes
                cwd=str(self.scholar_path)
            )

            if result.returncode != 0:
                warning = f"Google Scholar search failed: {result.stderr[:200]}"
                self.log(f"❌ {warning}")
                self.backend_status["google_scholar"] = {
                    "status": "failed",
                    "papers": 0,
                    "warning": warning
                }
                return False, 0, warning, []

            # Parse JSON output
            papers_data = json.loads(result.stdout)
            if not isinstance(papers_data, list):
                papers_data = [papers_data]

            paper_count = len(papers_data)
            self.log(f"✅ Google Scholar retrieval complete: {paper_count} papers")

            # Normalize papers
            normalized_papers = []
            for paper in papers_data:
                normalized = self._normalize_scholar_paper(paper)
                if normalized:
                    normalized_papers.append(normalized)

            self.backend_status["google_scholar"] = {
                "status": "success",
                "papers": len(normalized_papers),
                "warning": ""
            }
            return True, len(normalized_papers), "", normalized_papers

        except subprocess.TimeoutExpired:
            warning = "Google Scholar retrieval timeout (5 minutes)"
            self.log(f"❌ {warning}")
            self.backend_status["google_scholar"] = {
                "status": "timeout",
                "papers": 0,
                "warning": warning
            }
            return False, 0, warning, []

        except json.JSONDecodeError as e:
            warning = f"Google Scholar JSON parse error: {str(e)}"
            self.log(f"❌ {warning}")
            self.backend_status["google_scholar"] = {
                "status": "parse_error",
                "papers": 0,
                "warning": warning
            }
            return False, 0, warning, []

        except Exception as e:
            warning = f"Google Scholar retrieval error: {str(e)}"
            self.log(f"❌ {warning}")
            self.backend_status["google_scholar"] = {
                "status": "error",
                "papers": 0,
                "warning": warning
            }
            return False, 0, warning, []

    def _normalize_openalex_paper(self, paper: Dict) -> Optional[Dict]:
        """Normalize OpenAlex paper to unified schema."""
        try:
            # Extract authors - handle case where authorships may contain non-dict items
            authors = []
            if "authorships" in paper and isinstance(paper["authorships"], list):
                for a in paper["authorships"][:5]:
                    if isinstance(a, dict):
                        name = a.get("author", {}).get("display_name", "")
                        if name:
                            authors.append(name)

            # Extract journal/venue
            journal = ""
            if "primary_location" in paper and paper["primary_location"]:
                loc = paper["primary_location"]
                if isinstance(loc, dict):
                    source = loc.get("source", {})
                    if source and isinstance(source, dict):
                        journal = source.get("display_name", "")

            # Extract abstract
            abstract = paper.get("abstract", "")
            if not abstract and "abstract_inverted_index" in paper:
                # Reconstruct abstract from inverted index
                abstract_dict = paper.get("abstract_inverted_index", {})
                if abstract_dict:
                    words = sorted(
                        [(word, idx) for word, indices in abstract_dict.items() for idx in indices],
                        key=lambda x: x[1]
                    )
                    abstract = " ".join([word for word, _ in words])

            # Extract URL
            source_url = paper.get("url", "")
            if "open_access" in paper and paper["open_access"]:
                oa_url = paper["open_access"].get("url", "")
                if oa_url:
                    source_url = oa_url

            return {
                "source_db": "openalex",
                "backend": "academic-research",
                "backend_query": self.english_query or "",
                "title": paper.get("title", ""),
                "authors": authors,
                "organizations": [],
                "journal": journal,
                "year": paper.get("publication_year"),
                "publish_date": "",
                "volume": "",
                "issue": "",
                "pages": "",
                "doi": paper.get("doi", ""),
                "abstract": abstract,
                "keywords": [],
                "funds": [],
                "cited_count": paper.get("cited_by_count", 0),
                "download_count": "",
                "source_url": source_url,
                "language": "en"
            }
        except Exception as e:
            self.log(f"Warning: Failed to normalize OpenAlex paper: {e}")
            return None

    def _normalize_scholar_paper(self, paper: Dict) -> Optional[Dict]:
        """Normalize Google Scholar paper to unified schema."""
        try:
            return {
                "source_db": "google_scholar",
                "backend": "academic-research-hub",
                "backend_query": self.english_query or "",
                "title": paper.get("title", ""),
                "authors": paper.get("authors", []),
                "organizations": [],
                "journal": paper.get("venue", "") or paper.get("journal", ""),
                "year": paper.get("year"),
                "publish_date": "",
                "volume": "",
                "issue": "",
                "pages": "",
                "doi": "",
                "abstract": paper.get("snippet", "") or paper.get("abstract", ""),
                "keywords": [],
                "funds": [],
                "cited_count": paper.get("citations", 0),
                "download_count": "",
                "source_url": paper.get("url", ""),
                "language": "en"
            }
        except Exception as e:
            self.log(f"Warning: Failed to normalize Google Scholar paper: {e}")
            return None

    def save_raw_papers(self, papers: List[Dict]):
        """Save raw papers to JSON file."""
        output_path = self.output_dir / "papers_raw.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(papers, f, ensure_ascii=False, indent=2)
        self.log(f"Saved {len(papers)} raw papers to {output_path}")

    def save_session_log(self):
        """Save session log to markdown file."""
        log_path = self.output_dir / "session_log.md"

        # Build backend status table
        status_lines = [
            "## Phase 2: Backend Retrieval Status",
            "",
            "| Backend | Query | Status | Papers Found | Warnings |",
            "|---------|-------|--------|--------------|----------|",
        ]

        for backend, status in self.backend_status.items():
            status_icon = {
                "success": "✅",
                "failed": "❌",
                "timeout": "⏱️",
                "error": "❌",
                "parse_error": "⚠️",
                "skipped": "⏭️",
                "partial": "⚠️",
            }.get(status["status"], "❓")

            warning_text = status.get("warning", "")[:50] + "..." if len(status.get("warning", "")) > 50 else status.get("warning", "")
            status_lines.append(
                f"| {backend} | - | {status_icon} {status['status']} | {status['papers']} | {warning_text} |"
            )

        total_papers = sum(s["papers"] for s in self.backend_status.values())
        status_lines.extend([
            "",
            f"**Total Raw Papers:** {total_papers}",
            f"**Proceed to Phase 3:** {'Yes' if total_papers >= 20 else 'No (insufficient papers)'}",
            "",
            "## Session Log",
            "",
        ])
        status_lines.extend(self.session_log)

        with open(log_path, "w", encoding="utf-8") as f:
            f.write("\n".join(status_lines))

        self.log(f"Session log saved to {log_path}")

    def run(self) -> bool:
        """
        Execute full retrieval workflow.

        Returns:
            True if retrieval succeeded with sufficient papers, False otherwise.
        """
        self.setup_session()

        all_papers = []

        # Step 1: CNKI Retrieval
        cnki_success, cnki_count, cnki_warning = self.run_cnki_retrieval()
        if cnki_success and cnki_count > 0:
            # Load CNKI papers from database or output
            # For now, we just track the count
            self.log(f"CNKI papers will be loaded from database in post-processing")

        # Step 2: OpenAlex Retrieval
        openalex_success, openalex_count, openalex_warning, openalex_papers = \
            self.run_openalex_retrieval()
        all_papers.extend(openalex_papers)

        # Step 3: Google Scholar Retrieval
        scholar_success, scholar_count, scholar_warning, scholar_papers = \
            self.run_scholar_retrieval()
        all_papers.extend(scholar_papers)

        # Save results
        self.save_raw_papers(all_papers)
        self.save_session_log()

        # Summary
        total_papers = len(all_papers)
        self.log(f"=" * 50)
        self.log(f"Retrieval Summary:")
        self.log(f"  - CNKI: {self.backend_status.get('cnki', {}).get('papers', 0)} papers")
        self.log(f"  - OpenAlex: {self.backend_status.get('openalex', {}).get('papers', 0)} papers")
        self.log(f"  - Google Scholar: {self.backend_status.get('google_scholar', {}).get('papers', 0)} papers")
        self.log(f"  - Total (English): {total_papers} papers")
        self.log(f"=" * 50)

        # CNKI papers are in database, so we check English papers only
        return total_papers >= 20 or (cnki_success and total_papers >= 10)


def main():
    parser = argparse.ArgumentParser(
        description="Coordinate multi-backend literature retrieval"
    )
    parser.add_argument(
        "--cnki-query",
        type=str,
        help="CNKI professional search expression (e.g., \"SU='耐心资本'\")"
    )
    parser.add_argument(
        "--english-query",
        type=str,
        help="English search query (e.g., \"patient capital\")"
    )
    parser.add_argument(
        "--start-year",
        type=int,
        help="Start year for filtering"
    )
    parser.add_argument(
        "--end-year",
        type=int,
        help="End year for filtering"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        required=True,
        help="Output directory for session files"
    )
    parser.add_argument(
        "--cnki-limit-pages",
        type=int,
        default=10,
        help="CNKI crawl limit (pages)"
    )
    parser.add_argument(
        "--openalex-limit",
        type=int,
        default=50,
        help="OpenAlex search limit"
    )
    parser.add_argument(
        "--scholar-limit",
        type=int,
        default=30,
        help="Google Scholar search limit"
    )

    args = parser.parse_args()

    coordinator = RetrievalCoordinator(
        output_dir=args.output_dir,
        cnki_query=args.cnki_query,
        english_query=args.english_query,
        start_year=args.start_year,
        end_year=args.end_year,
        cnki_limit_pages=args.cnki_limit_pages,
        openalex_limit=args.openalex_limit,
        scholar_limit=args.scholar_limit,
    )

    success = coordinator.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
