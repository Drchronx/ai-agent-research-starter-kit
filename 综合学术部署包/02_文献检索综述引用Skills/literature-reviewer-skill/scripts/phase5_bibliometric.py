#!/usr/bin/env python3
"""
v5.0 文献计量分析模块

输出：
- 年度发文趋势
- 期刊分布 Top 10
- 高被引文献 Top 20
- 关键词分布
"""

import json
import sys
from pathlib import Path
from collections import Counter
from datetime import datetime


def analyze_bibliometrics(papers):
    """文献计量分析"""
    
    # 1. 年度发文趋势
    year_dist = Counter()
    for p in papers:
        year = str(p.get('year', '未知'))
        # 清理年份格式
        if year and year.isdigit() and len(year) == 4:
            year_dist[year] += 1
        else:
            year_dist['未知'] += 1
    
    # 2. 期刊分布
    journal_dist = Counter()
    for p in papers:
        journal = p.get('journal', '未知') or '未知'
        journal_dist[journal] += 1
    
    # 3. 高被引文献
    cited_papers = [p for p in papers if p.get('cited_count', 0) > 0]
    top_cited = sorted(cited_papers, key=lambda x: x.get('cited_count', 0), reverse=True)[:20]
    
    # 4. 关键词分布
    keyword_dist = Counter()
    for p in papers:
        keywords = p.get('keywords', [])
        if isinstance(keywords, list):
            for kw in keywords:
                if kw and kw.strip():
                    keyword_dist[kw.strip()] += 1
    
    # 5. 作者分布（简化版）
    author_dist = Counter()
    for p in papers:
        authors = p.get('authors', [])
        if isinstance(authors, list):
            for author in authors[:3]:  # 只统计前 3 作者
                if author and author.strip():
                    # 清理作者名（去除 [1], [2] 等标记）
                    author_clean = author.replace('[1]', '').replace('[2]', '').replace('[3]', '').strip()
                    if author_clean:
                        author_dist[author_clean] += 1
    
    return {
        'year_distribution': dict(sorted(year_dist.items())),
        'journal_distribution': dict(journal_dist.most_common(10)),
        'top_cited_papers': top_cited,
        'keyword_distribution': dict(keyword_dist.most_common(20)),
        'author_distribution': dict(author_dist.most_common(10))
    }


def generate_markdown_report(analysis, total_papers, output_path):
    """生成 Markdown 格式报告"""
    
    lines = [
        "# 文献计量分析报告",
        "",
        f"**生成时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**文献总数:** {total_papers} 篇",
        "",
        "---",
        "",
        "## 1. 年度发文趋势",
        "",
        "| 年份 | 发文量 | 累计 | 占比 |",
        "|------|--------|------|------|",
    ]
    
    # 年度趋势
    cumulative = 0
    year_dist = analysis['year_distribution']
    for year in sorted([y for y in year_dist.keys() if y != '未知'] or ['2020']):
        count = year_dist.get(year, 0)
        cumulative += count
        pct = round(count / total_papers * 100, 1)
        lines.append(f"| {year} | {count} | {cumulative} | {pct}% |")
    
    if '未知' in year_dist:
        lines.append(f"| 未知 | {year_dist['未知']} | {cumulative + year_dist['未知']} | - |")
    
    lines.extend([
        "",
        "## 2. 期刊分布 Top 10",
        "",
        "| 排名 | 期刊 | 发文量 | 占比 |",
        "|------|------|--------|------|",
    ])
    
    for i, (journal, count) in enumerate(analysis['journal_distribution'].items(), 1):
        pct = round(count / total_papers * 100, 1)
        lines.append(f"| {i} | {journal} | {count} | {pct}% |")
    
    lines.extend([
        "",
        "## 3. 高被引文献 Top 20",
        "",
        "| 排名 | 文献 | 被引 | 年份 | 期刊 |",
        "|------|------|------|------|------|",
    ])
    
    for i, p in enumerate(analysis['top_cited_papers'][:20], 1):
        authors = ', '.join([str(a) for a in p.get('authors', [])[:2]])
        year = p.get('year', 'n.d.')
        title = p.get('title', '无标题')[:40] + '...' if len(p.get('title', '')) > 40 else p.get('title', '无标题')
        journal = p.get('journal', '无期刊')
        cited = p.get('cited_count', 0)
        lines.append(f"| {i} | {authors}. {title} | {cited} | {year} | {journal} |")
    
    if not analysis['top_cited_papers']:
        lines.append("| - | 暂无被引数据 | - | - | - |")
    
    lines.extend([
        "",
        "## 4. 关键词分布 Top 20",
        "",
        "| 排名 | 关键词 | 出现次数 |",
        "|------|--------|---------|",
    ])
    
    for i, (kw, count) in enumerate(analysis['keyword_distribution'].items(), 1):
        lines.append(f"| {i} | {kw} | {count} |")
    
    lines.extend([
        "",
        "## 5. 核心作者 Top 10",
        "",
        "| 排名 | 作者 | 发文量 |",
        "|------|------|--------|",
    ])
    
    for i, (author, count) in enumerate(analysis['author_distribution'].items(), 1):
        lines.append(f"| {i} | {author} | {count} |")
    
    lines.extend([
        "",
        "---",
        "",
        "*报告由 Literature Reviewer Skill v5.0 自动生成*"
    ])
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"✓ 文献计量报告已保存到：{output_path}")
    print(f"  总行数：{len(lines)}")


def main():
    if len(sys.argv) < 2:
        print("用法：python phase5_bibliometric.py <session_dir>")
        sys.exit(1)
    
    session_dir = Path(sys.argv[1])
    
    print("=" * 60)
    print("Phase 5: 文献计量分析")
    print("=" * 60)
    
    # 加载文献
    print("\n[1] 加载文献数据...")
    papers_path = session_dir / "papers_verified.json"
    with open(papers_path, 'r', encoding='utf-8') as f:
        papers = json.load(f)
    print(f"  加载 {len(papers)} 篇文献")
    
    # 分析
    print("\n[2] 执行文献计量分析...")
    analysis = analyze_bibliometrics(papers)
    
    print(f"  年度跨度：{min(analysis['year_distribution'].keys())} - {max(analysis['year_distribution'].keys())}")
    print(f"  期刊数量：{len(analysis['journal_distribution'])}")
    print(f"  高被引文献：{len(analysis['top_cited_papers'])} 篇")
    print(f"  关键词数量：{len(analysis['keyword_distribution'])} 个")
    
    # 生成报告
    print("\n[3] 生成 Markdown 报告...")
    output_path = session_dir / "output" / "bibliometric_report.md"
    generate_markdown_report(analysis, len(papers), output_path)
    
    # 保存 JSON 结果（供后续模块使用）
    json_path = session_dir / "phase5_bibliometric.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    print(f"✓ JSON 结果已保存到：{json_path}")
    
    print("\n" + "=" * 60)
    print("✓ Phase 5 完成!")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
