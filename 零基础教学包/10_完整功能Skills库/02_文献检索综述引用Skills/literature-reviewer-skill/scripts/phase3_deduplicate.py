#!/usr/bin/env python3
"""
Phase 3: 文献去重脚本

功能：
- 基于 DOI 精确去重
- 基于标题相似度去重
- 保留信息更完整的版本
- 输出去重报告
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from difflib import SequenceMatcher
from datetime import datetime


def normalize_doi(doi: str) -> Optional[str]:
    """标准化 DOI"""
    if not doi:
        return None
    doi = str(doi).strip()
    # 移除常见前缀
    for prefix in ['https://doi.org/', 'http://doi.org/', 'doi.org/', 'DOI:', 'doi:']:
        if doi.lower().startswith(prefix):
            doi = doi[len(prefix):]
    return doi.lower().strip() if doi else None


def calculate_similarity(str1: str, str2: str) -> float:
    """计算两个字符串的相似度"""
    if not str1 or not str2:
        return 0.0
    s1 = str1.lower().strip()
    s2 = str2.lower().strip()
    return SequenceMatcher(None, s1, s2).ratio()


def calculate_quality_score(paper: Dict) -> float:
    """
    计算文献质量分数（用于决定保留哪个重复版本）
    """
    score = 0.0

    # 有 DOI 加分
    if paper.get('doi'):
        score += 10

    # 有完整元数据加分
    if paper.get('abstract') and len(paper['abstract']) > 50:
        score += 5
    if paper.get('volume') and paper.get('issue'):
        score += 3
    if paper.get('pages'):
        score += 2
    if paper.get('keywords') and len(paper['keywords']) > 0:
        score += 2

    # 引用数加分（归一化）
    cited = paper.get('cited_count', 0)
    if cited > 100:
        score += 5
    elif cited > 50:
        score += 3
    elif cited > 10:
        score += 1

    return score


def deduplicate_papers(
    papers: List[Dict],
    title_similarity_threshold: float = 0.85
) -> Tuple[List[Dict], List[Dict], Dict]:
    """
    文献去重主函数

    去重策略：
    1. DOI 精确匹配（优先）
    2. 标题相似度匹配（次优）
    3. 保留质量分数更高的版本

    Args:
        papers: 文献列表
        title_similarity_threshold: 标题相似度阈值（默认 0.85）

    Returns:
        (去重后的文献列表，被移除的重复文献列表，统计信息)
    """
    if not papers:
        return [], [], {}

    unique_papers = []
    removed_papers = []
    stats = {
        'doi_duplicates': 0,
        'title_duplicates': 0,
        'total_removed': 0,
        'by_language': {
            'zh': {'original': 0, 'unique': 0, 'removed': 0},
            'en': {'original': 0, 'unique': 0, 'removed': 0}
        }
    }

    # 统计原始数量
    for paper in papers:
        lang = paper.get('language', 'unknown')
        if lang in stats['by_language']:
            stats['by_language'][lang]['original'] += 1

    # DOI 映射：doi -> paper
    doi_map: Dict[str, Dict] = {}

    # 标题映射：用于相似度匹配 [(title, paper), ...]
    title_map: List[Tuple[str, Dict]] = []

    for paper in papers:
        doi = normalize_doi(paper.get('doi', ''))
        title = paper.get('title', '').strip()
        lang = paper.get('language', 'unknown')

        # 检查 DOI 匹配
        if doi and doi in doi_map:
            # DOI 重复，比较质量
            existing = doi_map[doi]
            existing_score = calculate_quality_score(existing)
            new_score = calculate_quality_score(paper)

            if new_score > existing_score:
                # 新版本质量更高，替换
                doi_map[doi] = paper
                # 从 unique_papers 中移除旧的
                if existing in unique_papers:
                    unique_papers.remove(existing)
                    removed_papers.append(existing)
                unique_papers.append(paper)
            else:
                # 保留旧版本
                removed_papers.append(paper)

            stats['doi_duplicates'] += 1
            stats['total_removed'] += 1
            if lang in stats['by_language']:
                stats['by_language'][lang]['removed'] += 1
            continue

        # 没有 DOI 或 DOI 不重复，检查标题相似度
        is_duplicate = False
        for existing_title, existing_paper in title_map:
            similarity = calculate_similarity(title, existing_title)

            if similarity >= title_similarity_threshold:
                # 标题相似，比较质量
                existing_score = calculate_quality_score(existing_paper)
                new_score = calculate_quality_score(paper)

                if new_score > existing_score:
                    # 新版本质量更高，替换
                    removed_papers.append(existing_paper)
                    unique_papers.remove(existing_paper)
                    title_map.remove((existing_title, existing_paper))

                    unique_papers.append(paper)
                    title_map.append((title, paper))
                    if doi:
                        doi_map[doi] = paper
                else:
                    # 保留旧版本
                    removed_papers.append(paper)

                stats['title_duplicates'] += 1
                stats['total_removed'] += 1
                if lang in stats['by_language']:
                    stats['by_language'][lang]['removed'] += 1

                is_duplicate = True
                break

        if not is_duplicate:
            unique_papers.append(paper)
            if doi:
                doi_map[doi] = paper
            title_map.append((title, paper))

    # 统计去重后数量
    for paper in unique_papers:
        lang = paper.get('language', 'unknown')
        if lang in stats['by_language']:
            stats['by_language'][lang]['unique'] += 1

    return unique_papers, removed_papers, stats


def generate_deduplication_report(
    stats: Dict,
    removed_papers: List[Dict],
    output_path: Path
):
    """生成去重报告"""
    report_lines = [
        "# 文献去重报告 (Deduplication Report)",
        "",
        f"**生成时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## 汇总统计",
        "",
        f"- **原始文献总数:** {stats.get('doi_duplicates', 0) + stats.get('title_duplicates', 0) + stats.get('by_language', {}).get('zh', {}).get('unique', 0) + stats.get('by_language', {}).get('en', {}).get('unique', 0)}",
        f"- **DOI 重复:** {stats.get('doi_duplicates', 0)} 篇",
        f"- **标题相似重复:** {stats.get('title_duplicates', 0)} 篇",
        f"- **移除重复:** {stats.get('total_removed', 0)} 篇",
        f"- **去重后唯一:** {stats.get('by_language', {}).get('zh', {}).get('unique', 0) + stats.get('by_language', {}).get('en', {}).get('unique', 0)} 篇",
        "",
        "## 按语言统计",
        "",
        "| 语言 | 原始数量 | 去重后 | 移除重复 | 去重率 |",
        "|------|---------|--------|---------|--------|",
    ]

    for lang, lang_stats in stats.get('by_language', {}).items():
        lang_name = {'zh': '中文', 'en': '英文'}.get(lang, lang)
        original = lang_stats.get('original', 0)
        unique = lang_stats.get('unique', 0)
        removed = lang_stats.get('removed', 0)
        rate = f"{removed / original * 100:.1f}%" if original > 0 else "0%"
        report_lines.append(
            f"| {lang_name} | {original} | {unique} | {removed} | {rate} |"
        )

    # 列出被移除的重复文献（前 20 篇）
    if removed_papers:
        report_lines.extend([
            "",
            "## 被移除的重复文献 (前 20 篇)",
            "",
        ])
        for i, paper in enumerate(removed_papers[:20]):
            title = paper.get('title', '无标题')[:80]
            authors = ', '.join(paper.get('authors', [])[:2])
            year = paper.get('year', 'n.d.')
            source = paper.get('source_db', 'unknown')
            doi = paper.get('doi', '')
            reason = "DOI 重复" if doi else "标题相似"
            report_lines.append(
                f"{i+1}. [{source}] {authors} ({year}). {title}... (移除原因：{reason})"
            )
        if len(removed_papers) > 20:
            report_lines.append(f"\n... 还有 {len(removed_papers) - 20} 篇")

    report_content = '\n'.join(report_lines)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_content)

    return report_content


def main():
    if len(sys.argv) < 2:
        print("用法：python phase3_deduplicate.py <session_dir>")
        sys.exit(1)

    session_dir = Path(sys.argv[1])
    if not session_dir.exists():
        print(f"错误：目录不存在 - {session_dir}")
        sys.exit(1)

    # 加载合并后的数据
    merged_path = session_dir / "papers_raw_merged.json"
    if not merged_path.exists():
        print(f"错误：合并文件不存在 - {merged_path}")
        print("请先运行：python data_loader.py <session_dir>")
        sys.exit(1)

    print("=" * 60)
    print("Phase 3: 文献去重")
    print("=" * 60)

    with open(merged_path, 'r', encoding='utf-8') as f:
        papers = json.load(f)

    print(f"\n加载文献：{len(papers)} 篇")

    # 执行去重
    print("\n执行去重...")
    unique_papers, removed_papers, stats = deduplicate_papers(papers)

    print(f"\n去重完成:")
    print(f"  - DOI 重复：{stats.get('doi_duplicates', 0)} 篇")
    print(f"  - 标题相似：{stats.get('title_duplicates', 0)} 篇")
    print(f"  - 移除重复：{stats.get('total_removed', 0)} 篇")
    print(f"  - 唯一文献：{len(unique_papers)} 篇")

    # 保存去重后的数据
    output_path = session_dir / "papers_deduplicated.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(unique_papers, f, ensure_ascii=False, indent=2)
    print(f"\n✓ 已保存到：{output_path}")

    # 生成报告
    report_path = session_dir / "phase3_deduplication_report.md"
    report = generate_deduplication_report(stats, removed_papers, report_path)
    print(f"✓ 去重报告：{report_path}")

    # 保存统计信息
    stats_path = session_dir / "phase3_stats.json"
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)

    # 返回去重后数量供后续脚本使用
    return len(unique_papers)


if __name__ == "__main__":
    result = main()
    sys.exit(0 if result > 0 else 1)
