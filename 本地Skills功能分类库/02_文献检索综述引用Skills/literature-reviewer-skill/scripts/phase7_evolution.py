#!/usr/bin/env python3
"""
v5.1 研究演进分析模块（完全动态版）

改进：
- 阶段划分：按实际文献年份自动划分（累计占比法）
- 主题识别：直接使用作者关键词，不做预定义归类
- 热点变化：对比各阶段关键词词频变化
- 政策事件：改为空列表，由用户后续补充

泛用性：适用于任何研究主题（耐心资本、数字普惠金融、ESG 等）
"""

import json
import sys
from pathlib import Path
from collections import Counter
from datetime import datetime
from typing import Dict, List, Tuple, Any


def divide_phases_auto(papers: List[Dict]) -> Dict[str, List[str]]:
    """
    自动划分研究阶段（按累计占比法）
    
    规则：
    - 萌芽期：累计占比 < 10%
    - 发展期：累计占比 10% - 50%
    - 深化期：累计占比 > 50%
    
    Returns:
        {
            '萌芽期': ['2020', '2021', '2022'],
            '发展期': ['2023', '2024'],
            '深化期': ['2025', '2026']
        }
    """
    # 统计每年发文量
    year_counts = Counter()
    for p in papers:
        year = str(p.get('year', ''))
        if year and len(year) == 4 and year.isdigit():
            year_counts[year] += 1
    
    if not year_counts:
        return {'未知': []}
    
    total = sum(year_counts.values())
    cumulative = 0
    phases = {}
    current_phase = None
    
    for year in sorted(year_counts.keys()):
        cumulative += year_counts[year]
        ratio = cumulative / total
        
        # 确定阶段名称
        if ratio < 0.1:
            phase_name = '萌芽期'
        elif ratio < 0.5:
            phase_name = '发展期'
        else:
            phase_name = '深化期'
        
        # 如果阶段变化，创建新条目
        if phase_name != current_phase:
            current_phase = phase_name
            phases[phase_name] = []
        
        phases[phase_name].append(year)
    
    # 如果只有一个阶段，重新命名
    if len(phases) == 1:
        phase_name = list(phases.keys())[0]
        years = phases[phase_name]
        return {
            f'{phase_name} ({years[0]}-{years[-1]})': years
        }
    
    # 添加年份范围到阶段名称
    result = {}
    for phase_name, years in phases.items():
        if len(years) > 1:
            result[f'{phase_name} ({years[0]}-{years[-1]})'] = years
        else:
            result[f'{phase_name} ({years[0]})'] = years
    
    return result


def analyze_phase_keywords(papers: List[Dict], phases: Dict[str, List[str]]) -> Dict[str, List[Tuple[str, int]]]:
    """
    统计各阶段的关键词词频（直接使用作者关键词）
    
    Args:
        papers: 文献列表
        phases: 阶段划分结果
    
    Returns:
        {
            '萌芽期 (2020-2022)': [('耐心资本', 50), ('长期投资', 30), ...],
            '发展期 (2023-2024)': [('企业创新', 80), ('融资约束', 60), ...],
            '深化期 (2025-2026)': [('新质生产力', 120), ('数智化', 90), ...]
        }
    """
    phase_keywords = {}
    
    for phase_name, years in phases.items():
        all_keywords = []
        
        for p in papers:
            year = str(p.get('year', ''))
            if year in years:
                keywords = p.get('keywords', [])
                if isinstance(keywords, list):
                    all_keywords.extend([kw.strip() for kw in keywords if kw and kw.strip()])
        
        # 统计词频 Top 15
        keyword_counts = Counter(all_keywords)
        phase_keywords[phase_name] = keyword_counts.most_common(15)
    
    return phase_keywords


def analyze_hotspot_changes(phase_keywords: Dict[str, List[Tuple[str, int]]]) -> List[Dict[str, Any]]:
    """
    分析热点变化（对比相邻阶段）
    
    Returns:
        [
            {
                'from': '萌芽期 (2020-2022)',
                'to': '发展期 (2023-2024)',
                'emerging': ['企业创新', '融资约束'],  # 新兴热点
                'fading': ['概念界定', '理论探讨'],     # 消退热点
                'persistent': ['公司治理'],              # 持续热点
                'rising': [('耐心资本', 20, 80)]         # 上升最快的词（词频变化）
            },
            ...
        ]
    """
    changes = []
    phase_names = list(phase_keywords.keys())
    
    for i in range(1, len(phase_names)):
        prev_phase = phase_names[i - 1]
        curr_phase = phase_names[i]
        
        # 转换为集合便于计算
        prev_keywords = set([kw for kw, count in phase_keywords[prev_phase]])
        curr_keywords = set([kw for kw, count in phase_keywords[curr_phase]])
        
        # 转换为字典便于查找词频
        prev_counts = dict(phase_keywords[prev_phase])
        curr_counts = dict(phase_keywords[curr_phase])
        
        # 新兴热点（新增）
        emerging = list(curr_keywords - prev_keywords)[:10]
        
        # 消退热点（消失）
        fading = list(prev_keywords - curr_keywords)[:10]
        
        # 持续热点（保留）
        persistent = list(prev_keywords & curr_keywords)
        
        # 上升最快的词（计算词频变化）
        rising = []
        for kw in persistent:
            prev_count = prev_counts.get(kw, 0)
            curr_count = curr_counts.get(kw, 0)
            if prev_count > 0:
                change = curr_count - prev_count
                change_ratio = (curr_count - prev_count) / prev_count
                if change > 0:
                    rising.append((kw, prev_count, curr_count, change, change_ratio))
        
        # 按变化幅度排序
        rising.sort(key=lambda x: x[4], reverse=True)
        rising = [(kw, prev, curr) for kw, prev, curr, _, _ in rising[:10]]
        
        changes.append({
            'from': prev_phase,
            'to': curr_phase,
            'emerging': emerging,
            'fading': fading,
            'persistent': persistent[:10],
            'rising': rising
        })
    
    return changes


def analyze_evolution(papers: List[Dict]) -> Dict[str, Any]:
    """
    研究演进分析（主函数）
    
    Args:
        papers: 文献列表
    
    Returns:
        {
            'phases': {...},  # 阶段划分
            'phase_keywords': {...},  # 各阶段关键词
            'hotspot_changes': [...],  # 热点变化
            'year_distribution': {...},  # 年份分布
            'policy_events': []  # 政策事件（由用户补充）
        }
    """
    # 1. 自动阶段划分
    phases = divide_phases_auto(papers)
    
    # 2. 各阶段关键词统计
    phase_keywords = analyze_phase_keywords(papers, phases)
    
    # 3. 热点变化分析
    hotspot_changes = analyze_hotspot_changes(phase_keywords)
    
    # 4. 年份分布
    year_counts = Counter()
    for p in papers:
        year = str(p.get('year', ''))
        if year and len(year) == 4 and year.isdigit():
            year_counts[year] += 1
    
    return {
        'phases': phases,
        'phase_keywords': phase_keywords,
        'hotspot_changes': hotspot_changes,
        'year_distribution': dict(sorted(year_counts.items())),
        'policy_events': []  # 改为空列表，由用户后续补充
    }


def generate_markdown_report(results: Dict[str, Any], output_path: Path):
    """生成 Markdown 格式报告"""
    
    lines = [
        "# 研究演进分析报告",
        "",
        f"**生成时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "---",
        "",
        "## 1. 研究阶段划分",
        "",
        "基于文献累计占比自动划分：",
        "",
        "| 阶段 | 年份 | 说明 |",
        "|------|------|------|",
    ]
    
    phases = results.get('phases', {})
    for phase_name, years in phases.items():
        phase_type = phase_name.split(' ')[0]
        if phase_type == '萌芽期':
            description = "早期探索，发文量较少"
        elif phase_type == '发展期':
            description = "快速增长，实证研究增多"
        else:
            description = "成熟深化，主题多元化"
        
        year_range = '-'.join(years) if len(years) > 1 else years[0]
        lines.append(f"| {phase_name} | {year_range} | {description} |")
    
    lines.extend([
        "",
        "## 2. 各阶段研究热点",
        "",
    ])
    
    phase_keywords = results.get('phase_keywords', {})
    for phase_name, keywords in phase_keywords.items():
        lines.append(f"### {phase_name}")
        lines.append("")
        lines.append("| 排名 | 关键词 | 出现频次 |")
        lines.append("|------|--------|----------|")
        
        for i, (kw, count) in enumerate(keywords[:10], 1):
            lines.append(f"| {i} | {kw} | {count} |")
        
        lines.append("")
    
    # 热点变化
    hotspot_changes = results.get('hotspot_changes', [])
    if hotspot_changes:
        lines.extend([
            "## 3. 热点演变分析",
            "",
        ])
        
        for change in hotspot_changes:
            lines.append(f"### {change['from']} → {change['to']}")
            lines.append("")
            
            if change['emerging']:
                lines.append(f"**新兴热点:** {', '.join(change['emerging'][:5])}")
                lines.append("")
            
            if change['fading']:
                lines.append(f"**消退热点:** {', '.join(change['fading'][:5])}")
                lines.append("")
            
            if change['rising']:
                lines.append("**上升最快:**")
                for kw, prev, curr in change['rising'][:5]:
                    lines.append(f"- {kw}: {prev} → {curr} 篇")
                lines.append("")
            
            lines.append("---")
            lines.append("")
    
    # 年份分布
    year_dist = results.get('year_distribution', {})
    if year_dist:
        lines.extend([
            "## 4. 年度发文趋势",
            "",
            "| 年份 | 发文量 | 占比 |",
            "|------|--------|------|",
        ])
        
        total = sum(year_dist.values())
        for year, count in year_dist.items():
            ratio = count / total * 100 if total > 0 else 0
            lines.append(f"| {year} | {count} | {ratio:.1f}% |")
        
        lines.append("")
    
    # 政策事件（预留）
    lines.extend([
        "## 5. 政策事件（待补充）",
        "",
        "> 注：政策事件需要人工补充，建议格式：",
        "> - 20XX 年：政策名称/事件描述",
        "> - 影响：对研究主题的影响",
        "",
    ])
    
    if results.get('policy_events'):
        for event in results['policy_events']:
            lines.append(f"- **{event.get('year', '未知')}**: {event.get('event', '')}")
            if event.get('impact'):
                lines.append(f"  - 影响：{event['impact']}")
    else:
        lines.append("*暂无政策事件数据*")
    
    lines.append("")
    
    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    return output_path


def main():
    """CLI 入口"""
    if len(sys.argv) < 2:
        print("用法：python phase7_evolution.py <papers_verified.json> [--output <output_path>]")
        sys.exit(1)
    
    input_path = Path(sys.argv[1])
    output_dir = input_path.parent
    
    # 解析输出路径参数
    output_path = None
    if '--output' in sys.argv:
        idx = sys.argv.index('--output')
        if idx + 1 < len(sys.argv):
            output_path = Path(sys.argv[idx + 1])
    
    if not output_path:
        output_path = output_dir / "evolution_report.md"
    
    # 加载文献数据
    with open(input_path, 'r', encoding='utf-8') as f:
        papers = json.load(f)
    
    print(f"加载文献：{len(papers)} 篇")
    
    # 执行分析
    results = analyze_evolution(papers)
    
    # 保存 JSON 结果
    json_path = output_dir / "phase7_evolution.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"保存 JSON: {json_path}")
    
    # 生成 Markdown 报告
    generate_markdown_report(results, output_path)
    print(f"生成报告：{output_path}")
    
    # 输出摘要
    phases = results.get('phases', {})
    print(f"\n阶段划分：{len(phases)} 个")
    for phase_name, years in phases.items():
        print(f"  - {phase_name}: {len(years)} 年")
    
    hotspot_changes = results.get('hotspot_changes', [])
    print(f"\n热点变化分析：{len(hotspot_changes)} 次转变")


if __name__ == '__main__':
    main()
