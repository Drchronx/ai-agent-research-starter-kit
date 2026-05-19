#!/usr/bin/env python3
"""
Phase 4: 文献验证脚本

功能：
- 验证文献元数据质量
- 适配不同后端的字段差异
- 输出详细验证报告（通过/失败原因）
- 只丢弃真正无效的文献
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime


# 验证配置
VALIDATION_CONFIG = {
    # 必需字段（缺少则丢弃）
    'required_fields': ['title'],

    # 可选但重要的字段（缺少则扣分，不丢弃）
    'preferred_fields': ['authors', 'year', 'journal', 'abstract'],

    # 质量评分权重
    'quality_weights': {
        'doi': 10,
        'abstract': 5,
        'keywords': 3,
        'volume_issue': 2,
        'pages': 2,
        'cited_count_high': 5,  # >100
        'cited_count_medium': 3,  # >50
        'cited_count_low': 1,  # >10
    },

    # 最小质量分数（低于此分数标记为低质量，但不丢弃）
    'min_quality_score': 5,
}


def validate_paper(paper: Dict, paper_index: int) -> Tuple[bool, List[str], int]:
    """
    验证单篇文献

    Returns:
        (是否通过验证，警告/错误列表，质量分数)
    """
    errors = []
    warnings = []
    score = 0

    # 检查必需字段
    for field in VALIDATION_CONFIG['required_fields']:
        value = paper.get(field)
        if not value or (isinstance(value, str) and not value.strip()):
            errors.append(f"缺少必需字段：{field}")

    # 检查可选字段并评分
    if paper.get('doi'):
        score += VALIDATION_CONFIG['quality_weights']['doi']

    abstract = paper.get('abstract', '')
    if abstract and len(abstract) > 50:
        score += VALIDATION_CONFIG['quality_weights']['abstract']
    elif abstract:
        warnings.append(f"摘要过短 ({len(abstract)} 字符)")

    keywords = paper.get('keywords', [])
    if keywords and len(keywords) > 0:
        score += VALIDATION_CONFIG['quality_weights']['keywords']

    if paper.get('volume') and paper.get('issue'):
        score += VALIDATION_CONFIG['quality_weights']['volume_issue']

    if paper.get('pages'):
        score += VALIDATION_CONFIG['quality_weights']['pages']

    cited_count = paper.get('cited_count', 0)
    if cited_count > 100:
        score += VALIDATION_CONFIG['quality_weights']['cited_count_high']
    elif cited_count > 50:
        score += VALIDATION_CONFIG['quality_weights']['cited_count_medium']
    elif cited_count > 10:
        score += VALIDATION_CONFIG['quality_weights']['cited_count_low']

    # 检查年份合理性
    year = paper.get('year')
    if year:
        try:
            year_int = int(year)
            if year_int < 1900 or year_int > datetime.now().year + 1:
                warnings.append(f"异常年份：{year}")
        except (ValueError, TypeError):
            warnings.append(f"年份格式错误：{year}")

    # 检查作者
    authors = paper.get('authors', [])
    if not authors or len(authors) == 0:
        warnings.append("缺少作者信息")

    # 检查期刊/来源
    journal = paper.get('journal', '')
    if not journal:
        # 对于某些后端，使用 source 或 venue
        journal = paper.get('source', '') or paper.get('venue', '')
        if journal:
            paper['journal'] = journal  # 回填
        else:
            warnings.append("缺少期刊/来源信息")

    # 决定验证结果
    # 有必需字段缺失则失败
    is_valid = len(errors) == 0

    return is_valid, errors + warnings, score


def verify_papers(
    papers: List[Dict],
    min_quality_score: int = 0  # 0 = 不丢弃低质量文献，只标记
) -> Tuple[List[Dict], List[Dict], Dict]:
    """
    验证文献列表

    Args:
        papers: 文献列表
        min_quality_score: 最小质量分数（0 = 保留所有，只标记）

    Returns:
        (验证通过的文献，被丢弃的文献，统计信息)
    """
    verified = []
    rejected = []
    stats = {
        'total': len(papers),
        'verified': 0,
        'rejected': 0,
        'by_language': {
            'zh': {'verified': 0, 'rejected': 0, 'low_quality': 0},
            'en': {'verified': 0, 'rejected': 0, 'low_quality': 0}
        },
        'rejection_reasons': {},
        'quality_distribution': {
            'high': 0,  # score >= 15
            'medium': 0,  # 10 <= score < 15
            'low': 0,  # score < 10
        }
    }

    for i, paper in enumerate(papers):
        is_valid, issues, score = validate_paper(paper, i)
        lang = paper.get('language', 'unknown')

        # 记录质量分布
        if score >= 15:
            stats['quality_distribution']['high'] += 1
        elif score >= 10:
            stats['quality_distribution']['medium'] += 1
        else:
            stats['quality_distribution']['low'] += 1

        paper['quality_score'] = score
        paper['validation_issues'] = issues

        if not is_valid:
            # 验证失败，丢弃
            rejected.append(paper)
            stats['rejected'] += 1
            if lang in stats['by_language']:
                stats['by_language'][lang]['rejected'] += 1

            # 统计拒绝原因
            for issue in issues:
                if issue.startswith('缺少必需字段'):
                    reason = 'missing_required_field'
                else:
                    reason = 'other'
                stats['rejection_reasons'][reason] = stats['rejection_reasons'].get(reason, 0) + 1
        else:
            # 验证通过
            verified.append(paper)
            stats['verified'] += 1
            if lang in stats['by_language']:
                stats['by_language'][lang]['verified'] += 1

            # 检查是否低质量（标记但不丢弃）
            if score < min_quality_score:
                if lang in stats['by_language']:
                    stats['by_language'][lang]['low_quality'] += 1

    return verified, rejected, stats


def generate_verification_report(
    stats: Dict,
    rejected_papers: List[Dict],
    output_path: Path
):
    """生成验证报告"""
    report_lines = [
        "# 文献验证报告 (Verification Report)",
        "",
        f"**生成时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## 汇总统计",
        "",
        f"- **验证总数:** {stats.get('total', 0)} 篇",
        f"- **验证通过:** {stats.get('verified', 0)} 篇",
        f"- **验证失败:** {stats.get('rejected', 0)} 篇",
        f"- **通过率:** {stats.get('verified', 0) / stats.get('total', 1) * 100:.1f}%",
        "",
        "## 质量分布",
        "",
        f"- **高质量 (≥15 分):** {stats.get('quality_distribution', {}).get('high', 0)} 篇",
        f"- **中质量 (10-14 分):** {stats.get('quality_distribution', {}).get('medium', 0)} 篇",
        f"- **低质量 (<10 分):** {stats.get('quality_distribution', {}).get('low', 0)} 篇",
        "",
        "## 按语言统计",
        "",
        "| 语言 | 验证通过 | 验证失败 | 低质量标记 |",
        "|------|---------|---------|-----------|",
    ]

    for lang, lang_stats in stats.get('by_language', {}).items():
        lang_name = {'zh': '中文', 'en': '英文'}.get(lang, lang)
        report_lines.append(
            f"| {lang_name} | {lang_stats.get('verified', 0)} | "
            f"{lang_stats.get('rejected', 0)} | {lang_stats.get('low_quality', 0)} |"
        )

    # 拒绝原因统计
    if stats.get('rejection_reasons'):
        report_lines.extend([
            "",
            "## 拒绝原因",
            "",
            "| 原因 | 数量 |",
            "|------|------|",
        ])
        for reason, count in stats['rejection_reasons'].items():
            reason_cn = {
                'missing_required_field': '缺少必需字段',
                'other': '其他'
            }.get(reason, reason)
            report_lines.append(f"| {reason_cn} | {count} |")

    # 列出被拒绝的文献（前 20 篇）
    if rejected_papers:
        report_lines.extend([
            "",
            "## 被拒绝的文献 (前 20 篇)",
            "",
        ])
        for i, paper in enumerate(rejected_papers[:20]):
            title = paper.get('title', '无标题')[:60]
            source = paper.get('source_db', 'unknown')
            issues = paper.get('validation_issues', [])[:3]
            report_lines.append(
                f"{i+1}. [{source}] {title}...\n"
                f"   问题：{', '.join(issues)}"
            )
        if len(rejected_papers) > 20:
            report_lines.append(f"\n... 还有 {len(rejected_papers) - 20} 篇")

    report_content = '\n'.join(report_lines)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_content)

    return report_content


def main():
    if len(sys.argv) < 2:
        print("用法：python phase4_verify.py <session_dir> [min_quality_score]")
        sys.exit(1)

    session_dir = Path(sys.argv[1])
    min_quality_score = int(sys.argv[2]) if len(sys.argv) > 2 else 0

    # 加载去重后的数据
    dedup_path = session_dir / "papers_deduplicated.json"
    if not dedup_path.exists():
        print(f"错误：去重文件不存在 - {dedup_path}")
        print("请先运行：python phase3_deduplicate.py <session_dir>")
        sys.exit(1)

    print("=" * 60)
    print("Phase 4: 文献验证")
    print("=" * 60)

    with open(dedup_path, 'r', encoding='utf-8') as f:
        papers = json.load(f)

    print(f"\n加载文献：{len(papers)} 篇")

    # 执行验证
    print(f"\n执行验证 (最低质量分数：{min_quality_score})...")
    verified_papers, rejected_papers, stats = verify_papers(papers, min_quality_score)

    print(f"\n验证完成:")
    print(f"  - 验证通过：{stats.get('verified', 0)} 篇")
    print(f"  - 验证失败：{stats.get('rejected', 0)} 篇")
    print(f"  - 低质量标记：{stats['quality_distribution']['low']} 篇")

    # 按语言统计
    print(f"\n按语言统计:")
    for lang, lang_stats in stats.get('by_language', {}).items():
        lang_name = {'zh': '中文', 'en': '英文'}.get(lang, lang)
        print(f"  - {lang_name}: 通过 {lang_stats['verified']}, 失败 {lang_stats['rejected']}")

    # 保存验证后的数据
    output_path = session_dir / "papers_verified.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(verified_papers, f, ensure_ascii=False, indent=2)
    print(f"\n✓ 已保存到：{output_path}")

    # 生成报告
    report_path = session_dir / "phase4_verification_report.md"
    report = generate_verification_report(stats, rejected_papers, report_path)
    print(f"✓ 验证报告：{report_path}")

    # 保存统计信息
    stats_path = session_dir / "phase4_stats.json"
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)

    # 返回验证后数量
    return len(verified_papers)


if __name__ == "__main__":
    result = main()
    sys.exit(0 if result > 0 else 1)
