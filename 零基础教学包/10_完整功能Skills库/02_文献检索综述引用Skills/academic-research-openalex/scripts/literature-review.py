#!/usr/bin/env python3
"""
Automated literature review workflow using OpenAlex.
Searches, deduplicates, clusters by theme, and generates a synthesis.

Built by Topanga (topanga.ludwitt.com) — AI Research Consultant
"""
import argparse
import hashlib
import json
import os
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import requests

BASE = "https://api.openalex.org"
MAILTO = "topanga@ludwitt.com"
CACHE_DIR = Path("/tmp/litreview_cache")


def _get(url, params=None):
    params = params or {}
    params["mailto"] = MAILTO

    # Simple disk cache
    cache_key = hashlib.md5(f"{url}{json.dumps(params, sort_keys=True)}".encode()).hexdigest()
    CACHE_DIR.mkdir(exist_ok=True)
    cache_file = CACHE_DIR / f"{cache_key}.json"
    if cache_file.exists():
        age = time.time() - cache_file.stat().st_mtime
        if age < 86400:  # 24h cache
            return json.loads(cache_file.read_text())

    for attempt in range(3):
        try:
            r = requests.get(url, params=params, timeout=20)
            if r.status_code == 429:
                time.sleep(2 ** attempt)
                continue
            r.raise_for_status()
            data = r.json()
            cache_file.write_text(json.dumps(data))
            return data
        except Exception as e:
            if attempt == 2:
                print(f"  Warning: {e}", file=sys.stderr)
                return None
            time.sleep(1)
    return None


def _parse_work(w):
    loc = w.get("primary_location") or {}
    source = loc.get("source") or {}
    oa = w.get("open_access") or {}

    authors = [a.get("author", {}).get("display_name", "?") for a in w.get("authorships", [])[:5]]

    abstract = None
    inv = w.get("abstract_inverted_index")
    if inv:
        try:
            words = [""] * (max(max(pos) for pos in inv.values()) + 1)
            for word, positions in inv.items():
                for p in positions:
                    words[p] = word
            abstract = " ".join(words).strip()
        except (ValueError, IndexError):
            pass

    concepts = []
    for c in w.get("concepts", []):
        if c.get("score", 0) > 0.3:
            concepts.append(c.get("display_name", ""))

    return {
        "title": w.get("display_name", "N/A"),
        "year": w.get("publication_year"),
        "authors": authors,
        "abstract": abstract,
        "citations": w.get("cited_by_count", 0),
        "doi": (w.get("doi") or "").replace("https://doi.org/", "") or None,
        "open_access": oa.get("is_oa", False),
        "oa_url": oa.get("oa_url"),
        "source_journal": source.get("display_name"),
        "concepts": concepts,
        "openalex_id": w.get("id"),
    }


def _generate_query_variations(topic):
    """Generate search variations to broaden coverage."""
    queries = [topic]
    words = topic.lower().split()

    # Add quoted exact phrase
    if len(words) > 1:
        queries.append(f'"{topic}"')

    # Split long queries into sub-concepts
    if len(words) > 4:
        mid = len(words) // 2
        queries.append(" ".join(words[:mid]))
        queries.append(" ".join(words[mid:]))

    return queries[:4]  # Cap at 4 queries


def gather_papers(topic, target_count=20, year_range=None):
    """Search multiple query variations and deduplicate."""
    queries = _generate_query_variations(topic)
    all_papers = {}
    per_query = max(target_count // len(queries) + 5, 15)

    for q in queries:
        print(f"  Searching: {q}", file=sys.stderr)
        params = {"search": q, "per_page": min(per_query, 50)}
        if year_range:
            params["filter"] = f"publication_year:{year_range}"

        data = _get(f"{BASE}/works", params)
        if not data:
            continue

        for w in data.get("results", []):
            paper = _parse_work(w)
            key = paper.get("doi") or paper.get("openalex_id") or paper["title"]
            if key not in all_papers:
                all_papers[key] = paper

    # Sort by citations and take top N
    papers = sorted(all_papers.values(), key=lambda p: p.get("citations", 0), reverse=True)
    return papers[:target_count]


def identify_themes(papers):
    """Cluster papers by concept/keyword overlap."""
    concept_counts = Counter()
    paper_concepts = {}

    for p in papers:
        concepts = p.get("concepts", [])
        if not concepts and p.get("abstract"):
            # Fallback: extract key noun phrases from abstract
            concepts = _extract_keywords(p["abstract"])
        paper_concepts[p["title"]] = concepts
        for c in concepts:
            concept_counts[c] += 1

    # Top themes = concepts appearing in 3+ papers (or top 5)
    min_count = min(3, max(1, len(papers) // 5))
    themes = [c for c, n in concept_counts.most_common(10) if n >= min_count]
    if not themes:
        themes = [c for c, _ in concept_counts.most_common(5)]

    # Assign papers to themes
    theme_papers = defaultdict(list)
    for p in papers:
        concepts = paper_concepts.get(p["title"], [])
        assigned = False
        for t in themes:
            if t in concepts:
                theme_papers[t].append(p)
                assigned = True
        if not assigned:
            theme_papers["Other"].append(p)

    return dict(theme_papers)


def _extract_keywords(text, n=5):
    """Simple keyword extraction from abstract."""
    stop = {"the", "a", "an", "in", "of", "to", "and", "for", "is", "are", "was",
            "were", "on", "at", "by", "with", "from", "or", "that", "this", "it",
            "be", "as", "has", "have", "had", "not", "but", "can", "do", "will",
            "which", "their", "its", "our", "we", "they", "been", "more", "than",
            "also", "these", "those", "may", "such", "between", "through", "both",
            "into", "each", "other", "about", "using", "used", "based", "study",
            "results", "research", "paper", "however", "data", "analysis", "method"}
    words = re.findall(r'\b[a-z]{4,}\b', text.lower())
    counts = Counter(w for w in words if w not in stop)
    return [w for w, _ in counts.most_common(n)]


def generate_synthesis_md(topic, papers, themes, year_range=None):
    """Generate a markdown literature review."""
    lines = []
    lines.append(f"# Literature Review: {topic}\n")
    lines.append(f"*Generated by academic-research skill | "
                 f"Built by [Topanga](https://topanga.ludwitt.com)*\n")

    yr = f" ({year_range})" if year_range else ""
    lines.append(f"**Scope:** {len(papers)} papers{yr} | "
                 f"**Themes identified:** {len(themes)}\n")

    # Overview
    total_cites = sum(p.get("citations", 0) for p in papers)
    years = [p["year"] for p in papers if p.get("year")]
    oa_count = sum(1 for p in papers if p.get("open_access"))

    lines.append("## Overview\n")
    lines.append(f"- **Papers analyzed:** {len(papers)}")
    if years:
        lines.append(f"- **Year range:** {min(years)}–{max(years)}")
    lines.append(f"- **Total citations:** {total_cites:,}")
    lines.append(f"- **Open access:** {oa_count}/{len(papers)} ({100*oa_count//max(len(papers),1)}%)")

    # Most cited
    top = sorted(papers, key=lambda p: p.get("citations", 0), reverse=True)[:5]
    lines.append("\n### Most Cited Works\n")
    for i, p in enumerate(top, 1):
        authors = ", ".join(p.get("authors", [])[:2])
        if len(p.get("authors", [])) > 2:
            authors += " et al."
        yr = f" ({p['year']})" if p.get("year") else ""
        doi = f" — DOI: {p['doi']}" if p.get("doi") else ""
        lines.append(f"{i}. **{p['title']}** — {authors}{yr} [{p.get('citations', 0)} citations]{doi}")

    # Themes
    lines.append("\n## Thematic Analysis\n")
    for theme, tpapers in themes.items():
        lines.append(f"### {theme.title()} ({len(tpapers)} papers)\n")
        for p in tpapers[:5]:
            authors = ", ".join(p.get("authors", [])[:2])
            if len(p.get("authors", [])) > 2:
                authors += " et al."
            yr = f" ({p['year']})" if p.get("year") else ""
            oa = "🔓" if p.get("open_access") else "🔒"
            lines.append(f"- {oa} **{p['title']}** — {authors}{yr}")
            if p.get("abstract"):
                # First sentence of abstract
                first = p["abstract"].split(". ")[0] + "."
                if len(first) < 300:
                    lines.append(f"  > {first}")
        lines.append("")

    # Bibliography
    lines.append("## Full Bibliography\n")
    for i, p in enumerate(sorted(papers, key=lambda x: x.get("year") or 0, reverse=True), 1):
        authors = ", ".join(p.get("authors", [])[:3])
        if len(p.get("authors", [])) > 3:
            authors += " et al."
        yr = f" ({p['year']})" if p.get("year") else ""
        doi = f" https://doi.org/{p['doi']}" if p.get("doi") else ""
        lines.append(f"{i}. {authors}{yr}. *{p['title']}*.{doi}")

    lines.append(f"\n---\n*{len(papers)} papers reviewed.*")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Automated literature review")
    parser.add_argument("topic", help="Research topic")
    parser.add_argument("--papers", "-n", type=int, default=20, help="Target paper count")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    parser.add_argument("--years", help="Year range, e.g. 2020-2025")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    print(f"📚 Literature review: {args.topic}", file=sys.stderr)
    print(f"   Target: {args.papers} papers", file=sys.stderr)

    # Step 1: Gather
    print("\n1️⃣  Gathering papers...", file=sys.stderr)
    papers = gather_papers(args.topic, args.papers, args.years)
    print(f"   Found {len(papers)} unique papers", file=sys.stderr)

    if not papers:
        print("❌ No papers found", file=sys.stderr)
        sys.exit(1)

    # Step 2: Theme identification
    print("2️⃣  Identifying themes...", file=sys.stderr)
    themes = identify_themes(papers)
    print(f"   {len(themes)} themes identified", file=sys.stderr)

    # Step 3: Synthesis
    print("3️⃣  Generating synthesis...", file=sys.stderr)

    if args.json:
        output = json.dumps({
            "topic": args.topic,
            "paper_count": len(papers),
            "themes": {t: [p["title"] for p in ps] for t, ps in themes.items()},
            "papers": papers,
        }, indent=2)
    else:
        output = generate_synthesis_md(args.topic, papers, themes, args.years)

    if args.output:
        Path(args.output).write_text(output)
        print(f"\n✅ Review written to {args.output}", file=sys.stderr)
    else:
        print(output)

    print(f"\n📊 Summary: {len(papers)} papers, {len(themes)} themes", file=sys.stderr)


if __name__ == "__main__":
    main()
