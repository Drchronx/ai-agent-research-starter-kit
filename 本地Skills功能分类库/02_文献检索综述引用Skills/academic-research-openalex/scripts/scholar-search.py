#!/usr/bin/env python3
"""
Academic paper search via OpenAlex API (free, no key needed).
Part of the academic-research skill for OpenClaw.

Built by Topanga (topanga.ludwitt.com) — AI Research Consultant
"""
import argparse
import json
import sys
import time
import requests

BASE = "https://api.openalex.org"
MAILTO = "topanga@ludwitt.com"  # polite pool (faster rate limits)


def _get(url, params=None):
    params = params or {}
    params["mailto"] = MAILTO
    for attempt in range(3):
        try:
            r = requests.get(url, params=params, timeout=20)
            if r.status_code == 429:
                time.sleep(2 ** attempt)
                continue
            r.raise_for_status()
            return r.json()
        except requests.exceptions.RequestException as e:
            if attempt == 2:
                print(f"Error: {e}", file=sys.stderr)
                return None
            time.sleep(1)
    return None


def _parse_work(w):
    """Extract structured data from an OpenAlex work object."""
    loc = w.get("primary_location") or {}
    source = loc.get("source") or {}
    oa = w.get("open_access") or {}

    authors = []
    for a in w.get("authorships", [])[:5]:
        auth = a.get("author") or {}
        authors.append(auth.get("display_name", "Unknown"))

    # Get abstract from inverted index
    abstract = None
    inv = w.get("abstract_inverted_index")
    if inv:
        words = [""] * (max(max(pos) for pos in inv.values()) + 1)
        for word, positions in inv.items():
            for p in positions:
                words[p] = word
        abstract = " ".join(words).strip()

    return {
        "title": w.get("display_name", "N/A"),
        "year": w.get("publication_year"),
        "authors": authors,
        "abstract": abstract,
        "citations": w.get("cited_by_count", 0),
        "doi": (w.get("doi") or "").replace("https://doi.org/", "") or None,
        "open_access": oa.get("is_oa", False),
        "oa_url": oa.get("oa_url"),
        "landing_url": loc.get("landing_page_url"),
        "source": source.get("display_name"),
        "type": w.get("type"),
        "openalex_id": w.get("id"),
    }


def search(query, limit=10, sort="relevance", year_range=None, oa_only=False):
    """Search works by topic."""
    params = {"search": query, "per_page": min(limit, 50)}
    if sort == "citations":
        params["sort"] = "cited_by_count:desc"
    if year_range:
        params["filter"] = f"publication_year:{year_range}"
    if oa_only:
        f = params.get("filter", "")
        params["filter"] = (f + "," if f else "") + "open_access.is_oa:true"

    data = _get(f"{BASE}/works", params)
    if not data:
        return []
    return [_parse_work(w) for w in data.get("results", [])]


def search_author(name, limit=5):
    """Search for papers by a specific author."""
    # First find the author
    data = _get(f"{BASE}/authors", {"search": name, "per_page": 1})
    if not data or not data.get("results"):
        print(f"Author '{name}' not found", file=sys.stderr)
        return []

    author = data["results"][0]
    author_id = author["id"]
    print(f"Found: {author['display_name']} ({author.get('works_count', '?')} works, "
          f"h-index: {author.get('summary_stats', {}).get('h_index', '?')})", file=sys.stderr)

    # Get their works
    works = _get(f"{BASE}/works", {
        "filter": f"authorships.author.id:{author_id}",
        "sort": "cited_by_count:desc",
        "per_page": min(limit, 50),
    })
    if not works:
        return []
    return [_parse_work(w) for w in works.get("results", [])]


def lookup_doi(doi):
    """Get paper details by DOI."""
    doi = doi.strip().removeprefix("https://doi.org/")
    data = _get(f"{BASE}/works/https://doi.org/{doi}")
    if not data:
        return None
    return _parse_work(data)


def get_citations(doi, direction="cited_by", limit=10):
    """Get citation chain for a paper.
    direction: 'cited_by' (papers citing this), 'references' (papers this cites), 'both'
    """
    doi = doi.strip().removeprefix("https://doi.org/")
    work = _get(f"{BASE}/works/https://doi.org/{doi}")
    if not work:
        return {"cited_by": [], "references": []}

    result = {}
    work_id = work.get("id", "").split("/")[-1]

    if direction in ("cited_by", "both"):
        cited = _get(f"{BASE}/works", {
            "filter": f"cites:{work_id}",
            "sort": "cited_by_count:desc",
            "per_page": min(limit, 50),
        })
        result["cited_by"] = [_parse_work(w) for w in (cited or {}).get("results", [])]

    if direction in ("references", "both"):
        refs = _get(f"{BASE}/works", {
            "filter": f"cited_by:{work_id}",
            "sort": "cited_by_count:desc",
            "per_page": min(limit, 50),
        })
        result["references"] = [_parse_work(w) for w in (refs or {}).get("results", [])]

    return result


def deep_read(doi):
    """Fetch detailed paper info including abstract and full text URL."""
    paper = lookup_doi(doi)
    if not paper:
        print("Paper not found", file=sys.stderr)
        return None

    # Try Unpaywall for better PDF URL
    try:
        r = requests.get(f"https://api.unpaywall.org/v2/{paper['doi']}?email={MAILTO}", timeout=10)
        if r.status_code == 200:
            up = r.json()
            best = up.get("best_oa_location") or {}
            if best.get("url_for_pdf"):
                paper["pdf_url"] = best["url_for_pdf"]
            elif best.get("url"):
                paper["pdf_url"] = best["url"]
    except Exception:
        pass

    return paper


def _format_paper(p, idx=None):
    prefix = f"{idx}. " if idx else ""
    oa = "🔓" if p.get("open_access") else "🔒"
    year = f"({p['year']})" if p.get("year") else ""
    cites = f"[{p['citations']} citations]" if p.get("citations") else ""
    authors = ", ".join(p.get("authors", [])[:3])
    if len(p.get("authors", [])) > 3:
        authors += " et al."

    lines = [f"{prefix}{oa} {p['title']} {year} {cites}"]
    if authors:
        lines.append(f"   Authors: {authors}")
    if p.get("source"):
        lines.append(f"   Source: {p['source']}")
    if p.get("doi"):
        lines.append(f"   DOI: {p['doi']}")
    if p.get("oa_url"):
        lines.append(f"   URL: {p['oa_url']}")
    if p.get("pdf_url"):
        lines.append(f"   PDF: {p['pdf_url']}")
    if p.get("abstract"):
        ab = p["abstract"][:300] + ("..." if len(p["abstract"]) > 300 else "")
        lines.append(f"   Abstract: {ab}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Academic paper search (OpenAlex)")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    sub = parser.add_subparsers(dest="cmd")

    s = sub.add_parser("search", help="Search papers by topic")
    s.add_argument("query")
    s.add_argument("--limit", "-l", type=int, default=10)
    s.add_argument("--sort", choices=["relevance", "citations"], default="relevance")
    s.add_argument("--years", help="Year range, e.g. 2020-2025")
    s.add_argument("--oa", action="store_true", help="Open access only")
    s.add_argument("--json", action="store_true")

    a = sub.add_parser("author", help="Search by author name")
    a.add_argument("name")
    a.add_argument("--limit", "-l", type=int, default=5)
    a.add_argument("--json", action="store_true")

    d = sub.add_parser("doi", help="Look up paper by DOI")
    d.add_argument("doi")
    d.add_argument("--json", action="store_true")

    c = sub.add_parser("citations", help="Get citation chain")
    c.add_argument("doi")
    c.add_argument("--direction", "-d", choices=["cited_by", "references", "both"], default="cited_by")
    c.add_argument("--limit", "-l", type=int, default=10)
    c.add_argument("--json", action="store_true")

    dp = sub.add_parser("deep", help="Deep read — full details + PDF URL")
    dp.add_argument("doi")
    dp.add_argument("--json", action="store_true")

    args = parser.parse_args()
    use_json = getattr(args, "json", False) or parser.parse_known_args()[0].json

    if args.cmd == "search":
        year_range = None
        if args.years:
            parts = args.years.split("-")
            year_range = f"{parts[0]}-{parts[1]}" if len(parts) == 2 else args.years
        results = search(args.query, args.limit, args.sort, year_range, args.oa)
        if use_json:
            print(json.dumps(results, indent=2))
        else:
            print(f"🔍 Found {len(results)} results for: {args.query}\n")
            for i, p in enumerate(results, 1):
                print(_format_paper(p, i))
                print()

    elif args.cmd == "author":
        results = search_author(args.name, args.limit)
        if use_json:
            print(json.dumps(results, indent=2))
        else:
            for i, p in enumerate(results, 1):
                print(_format_paper(p, i))
                print()

    elif args.cmd == "doi":
        paper = lookup_doi(args.doi)
        if use_json:
            print(json.dumps(paper, indent=2))
        elif paper:
            print(_format_paper(paper))
        else:
            print("❌ Not found")

    elif args.cmd == "citations":
        result = get_citations(args.doi, args.direction, args.limit)
        if use_json:
            print(json.dumps(result, indent=2))
        else:
            for dir_name, papers in result.items():
                print(f"\n{'📥' if dir_name == 'cited_by' else '📤'} {dir_name.replace('_', ' ').title()} ({len(papers)}):\n")
                for i, p in enumerate(papers, 1):
                    print(_format_paper(p, i))
                    print()

    elif args.cmd == "deep":
        paper = deep_read(args.doi)
        if use_json:
            print(json.dumps(paper, indent=2))
        elif paper:
            print(_format_paper(paper))
        else:
            print("❌ Not found")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
