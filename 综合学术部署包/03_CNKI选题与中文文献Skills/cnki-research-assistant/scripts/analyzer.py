#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNKI Research Assistant - 主分析引擎
整合 cnki-rank, cnki-trend, cnki-crawler, CSSCI 期刊数据
"""

import sys
import os
import json
import argparse
import subprocess
import psycopg2
from psycopg2 import extras
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# 添加脚本目录到路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from journal_matcher import JournalMatcher
from report_generator import ReportGenerator
from research_gap_analyzer import ResearchGapAnalyzer
from isolation_manager import IsolationManager


# 相对路径配置（基于技能目录）
SKILL_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
CONFIG_PATH = os.path.join(SKILL_ROOT, 'config/config.json')
CSSCI_DATA_PATH = os.path.join(SKILL_ROOT, 'data/cssci_2025_2026.csv')
REPORTS_DIR = os.path.join(SKILL_ROOT, 'reports')

# 外部技能路径（可配置）
CNKI_TREND_SCRIPT = os.path.expanduser('/root/.openclaw/workspace-hotspot/skills/cnki-trend/scripts/cnki_keyword_trend_report.py')
CNKI_CRAWLER_SCRIPT = os.path.expanduser('/root/.openclaw/workspace-hotspot/skills/cnki-crawler/scripts/main.py')
CNKI_RANK_DB = 'academic_hotspot'  # cnki-rank 使用的数据库


def load_config() -> Optional[Dict[str, Any]]:
    """加载配置文件"""
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def get_db_connection(dbname: str = None):
    """获取数据库连接"""
    config = load_config()
    if not config:
        return None
    
    db_config = config.get('database', {})
    if not db_config:
        return None
    
    try:
        conn = psycopg2.connect(
            host=db_config.get('host', 'localhost'),
            port=db_config.get('port', 5432),
            dbname=dbname or db_config.get('dbname', 'cnki_db'),
            user=db_config.get('user'),
            password=db_config.get('password')
        )
        return conn
    except Exception as e:
        print(f"数据库连接失败：{e}")
        return None


def check_rank(keyword: str) -> Dict[str, Any]:
    """
    检查关键词在热榜中的排名
    查询 cnki-rank (academic_hotspot) 数据库
    """
    result = {
        'success': False,
        'keyword': keyword,
        'week_rank': None,
        'month_rank': None,
        'days_on_list': 0,
        'status': 'unknown',
        'note': '未在热榜中找到匹配'
    }
    
    conn = get_db_connection(CNKI_RANK_DB)
    if not conn:
        result['note'] = '数据库连接失败'
        return result
    
    try:
        with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
            # 查询热词榜（周榜）（使用 LOWER + LIKE 替代 ILIKE）
            cur.execute("""
                SELECT keyword_id, keyword, week_rank, month_rank, 
                       week_status, week_consecutive, week_total_days
                FROM cnki_keyword_hotspot
                WHERE LOWER(keyword) LIKE LOWER(%s)
                ORDER BY COALESCE(week_rank, month_rank, 9999)
                LIMIT 1
            """, (f'%{keyword}%',))
            
            row = cur.fetchone()
            if row:
                result['success'] = True
                result['week_rank'] = row['week_rank']
                result['month_rank'] = row['month_rank']
                result['days_on_list'] = row['week_total_days'] or 0
                result['status'] = row['week_status'] or 'unknown'
                result['note'] = '热榜数据获取成功'
            else:
                # 尝试论文标题匹配（使用 LOWER + LIKE 替代 ILIKE）
                cur.execute("""
                    SELECT file_id, title, week_rank, week_status, week_total_days
                    FROM cnki_article_hotspot
                    WHERE LOWER(title) LIKE LOWER(%s)
                    ORDER BY COALESCE(week_rank, 9999)
                    LIMIT 1
                """, (f'%{keyword}%',))
                
                row = cur.fetchone()
                if row:
                    result['success'] = True
                    result['week_rank'] = row['week_rank']
                    result['status'] = row['week_status'] or 'unknown'
                    result['days_on_list'] = row['week_total_days'] or 0
                    result['note'] = '通过论文标题匹配到热榜数据'
    
    except Exception as e:
        result['note'] = f'数据库查询失败：{e}'
    finally:
        conn.close()
    
    return result


def analyze_trend(keyword: str, output_dir: str = None, font_path: str = None) -> Dict[str, Any]:
    """
    分析关键词趋势
    调用 cnki-trend 脚本
    
    Args:
        keyword: 分析关键词
        output_dir: 输出目录
        font_path: 中文字体文件路径（可选）
    """
    if output_dir is None:
        output_dir = REPORTS_DIR
    
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'charts'), exist_ok=True)
    
    # 调用 cnki-trend 脚本
    cmd = [
        sys.executable,
        CNKI_TREND_SCRIPT,
        keyword,
        '--output-dir', output_dir
    ]
    
    # 添加字体路径参数
    if font_path and os.path.exists(font_path):
        cmd.extend(['--font-path', font_path])
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=os.path.dirname(CNKI_TREND_SCRIPT)
        )
        
        if result.returncode == 0:
            report_path = os.path.join(output_dir, f'{keyword}_trend_report.md')
            json_path = os.path.join(output_dir, f'{keyword}_valid_groups.json')
            
            trend_data = {
                'success': True,
                'keyword': keyword,
                'report_path': report_path,
                'json_path': json_path,
                'charts_dir': os.path.join(output_dir, 'charts'),
            }
            
            if os.path.exists(json_path):
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    trend_data['metrics'] = extract_trend_metrics(data)
            
            return trend_data
        else:
            return {
                'success': False,
                'error': result.stderr or f'脚本返回错误码：{result.returncode}'
            }
            
    except subprocess.TimeoutExpired:
        return {'success': False, 'error': '趋势分析超时（>120 秒）'}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def extract_trend_metrics(data: Dict) -> Dict[str, Any]:
    """从趋势分析 JSON 中提取关键指标"""
    metrics = {}
    groups = data.get('valid_groups', [])
    
    # 年度趋势
    year_group = next((g for g in groups if g['group_name'] == 'YE-年度'), None)
    if year_group:
        items = sorted(year_group['items'], key=lambda x: int(x['c_fieldValue']))
        total = sum(item['y'] for item in items)
        peak = max(items, key=lambda x: x['y'])
        current_year = datetime.now().year
        recent_3y = sum(item['y'] for item in items if int(item['c_fieldValue']) >= current_year - 2)
        
        metrics['yearly'] = {
            'total_papers': total,
            'peak_year': peak['name'],
            'peak_count': peak['y'],
            'recent_3y_ratio': recent_3y / total if total else 0
        }
    
    # 学科分布
    subject_group = next((g for g in groups if g['group_name'] == 'CCL-学科'), None)
    if subject_group:
        items = subject_group['items']
        total = sum(item['y'] for item in items)
        top_subject = items[0] if items else None
        
        metrics['subject'] = {
            'total_disciplines': len(items),
            'top_discipline': top_subject['name'] if top_subject else None,
            'top_discipline_ratio': top_subject['y'] / total if top_subject and total else 0
        }
    
    # 期刊分布
    journal_group = next((g for g in groups if g['group_name'] == 'QK-期刊'), None)
    if journal_group:
        items = journal_group['items']
        metrics['journal'] = {
            'total_journals': len(items),
            'concentration': 'high' if len(items) < 20 else ('medium' if len(items) < 50 else 'low')
        }
    
    return metrics


def crawl_papers(keyword: str, limit: int = 100, multi_sort: bool = True) -> Dict[str, Any]:
    """
    抓取相关论文
    
    Args:
        keyword: 检索关键词
        limit: 每种排序的文献数量上限
        multi_sort: 是否启用多排序抓取（DFR/CF/PT/ZH）
    """
    result = {
        'success': False,
        'keyword': keyword,
        'papers_count': 0,
        'papers': [],
        'sort_stats': {}  # 记录每种排序抓取的数量
    }
    
    conn = get_db_connection()  # 使用 cnki_db
    if not conn:
        result['note'] = '数据库连接失败'
        return result
    
    try:
        with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
            if multi_sort:
                # 多排序抓取：DFR(热点) + CF(权威) + PT(最新) + ZH(综合)
                sort_fields = ['DFR', 'CF', 'PT', 'ZH']
                all_papers = []
                seen_titles = set()  # 用于去重
                
                for sort_field in sort_fields:
                    # 按不同排序字段查询
                    order_by = {
                        'DFR': 'download_count DESC NULLS LAST',
                        'CF': 'cited_count DESC NULLS LAST',
                        'PT': 'year DESC, publish_date DESC NULLS LAST',
                        'ZH': 'cited_count DESC NULLS LAST'  # ZH 综合排序用被引近似
                    }.get(sort_field, 'cited_count DESC NULLS LAST')
                    
                    cur.execute(f"""
                        SELECT title, authors, journal, year, cited_count, download_count,
                               keywords, abstract, detail_url, publish_date
                        FROM cnki_papers
                        WHERE (LOWER(title) LIKE LOWER(%s) 
                               OR keywords::text ILIKE %s)
                        ORDER BY {order_by}
                        LIMIT %s
                    """, (f'%{keyword}%', f'%{keyword}%', limit))
                    
                    papers = [dict(row) for row in cur.fetchall()]
                    
                    # 去重（基于标题）
                    new_papers = []
                    for p in papers:
                        title_key = p['title'].strip().lower()
                        if title_key not in seen_titles:
                            seen_titles.add(title_key)
                            new_papers.append(p)
                    
                    all_papers.extend(new_papers)
                    result['sort_stats'][sort_field] = {
                        'total': len(papers),
                        'new': len(new_papers)
                    }
                
                papers = all_papers
            else:
                # 单排序：按被引频次
                cur.execute("""
                    SELECT title, authors, journal, year, cited_count, download_count,
                           keywords, abstract, detail_url
                    FROM cnki_papers
                    WHERE LOWER(title) LIKE LOWER(%s) 
                       OR keywords::text ILIKE %s
                    ORDER BY cited_count DESC NULLS LAST
                    LIMIT %s
                """, (f'%{keyword}%', f'%{keyword}%', limit))
                
                papers = [dict(row) for row in cur.fetchall()]
            
            if papers:
                result['success'] = True
                result['papers_count'] = len(papers)
                result['papers'] = papers
                result['note'] = f'从数据库获取到 {len(papers)} 篇相关论文'
                
                # 额外统计信息
                result['stats'] = {
                    'unique_papers': len(papers),
                    'avg_cited_count': sum(int(p.get('cited_count') or 0) for p in papers) / len(papers),
                    'avg_download_count': sum(int(p.get('download_count') or 0) for p in papers) / len(papers),
                    'year_range': f"{min(p.get('year', '9999') or '9999' for p in papers)}-{max(p.get('year', '0') or '0' for p in papers)}"
                }
            else:
                result['note'] = '数据库中暂无相关论文，可能需要先运行 cnki-crawler 抓取'
    
    except Exception as e:
        result['note'] = f'数据库查询失败：{e}'
    finally:
        conn.close()
    
    return result


def match_journals(keyword: str, top_n: int = 10, level: str = 'all') -> Dict[str, Any]:
    """
    匹配推荐期刊
    使用 CSSCI 期刊数据（相对路径）
    """
    try:
        # JournalMatcher 会自动查找 data 目录中的 CSSCI 文件（支持 CSV 和 Excel）
        matcher = JournalMatcher()
        results = matcher.match(keyword, top_n=top_n, level=level)
        
        return {
            'success': True,
            'keyword': keyword,
            'matched_journals': results,
            'total_available': matcher.total_journals
        }
    except FileNotFoundError as e:
        return {
            'success': False,
            'error': f'CSSCI 数据文件不存在：{str(e)}'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'期刊匹配失败：{str(e)}'
        }


def generate_report(
    keyword: str,
    rank_data: Dict,
    trend_data: Dict,
    paper_data: Dict,
    journal_data: Dict,
    gap_data: Dict = None,
    output_path: str = None
) -> str:
    """生成综合分析报告"""
    generator = ReportGenerator()
    
    report = generator.build_report(
        keyword=keyword,
        rank_data=rank_data,
        trend_data=trend_data,
        paper_data=paper_data,
        journal_data=journal_data,
        gap_data=gap_data
    )
    
    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
    
    return report


def print_summary(keyword: str, results: Dict[str, Any]):
    """打印分析摘要"""
    print("=" * 80)
    print(f"📊 CNKI 选题分析报告：{keyword}")
    print("=" * 80)
    print(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 热点扫描
    rank = results.get('rank', {})
    print("🔥【热点扫描】")
    if rank.get('success'):
        if rank.get('week_rank'):
            print(f"   周榜排名：{rank['week_rank']}")
        if rank.get('month_rank'):
            print(f"   月榜排名：{rank['month_rank']}")
        print(f"   在榜天数：{rank.get('days_on_list', 0)}")
        print(f"   状态：{rank.get('status', 'unknown')}")
    else:
        print(f"   ⚠️ {rank.get('note', '数据获取失败')}")
    print()
    
    # 趋势评估
    trend = results.get('trend', {})
    print("📈【趋势评估】")
    if trend.get('success') and 'metrics' in trend:
        metrics = trend['metrics']
        if 'yearly' in metrics:
            y = metrics['yearly']
            print(f"   峰值年份：{y['peak_year']} ({y['peak_count']} 篇)")
            print(f"   近三年占比：{y['recent_3y_ratio']:.1%}")
        if 'subject' in metrics:
            s = metrics['subject']
            print(f"   主导学科：{s['top_discipline']} ({s['top_discipline_ratio']:.1%})")
        if 'journal' in metrics:
            j = metrics['journal']
            print(f"   期刊分布：{j['total_journals']} 种 ({j['concentration']} 集中度)")
    else:
        print(f"   ⚠️ {trend.get('error', '趋势分析失败')}")
    print()
    
    # 文献调研
    papers = results.get('papers', {})
    print("📄【文献调研】")
    if papers.get('success'):
        print(f"   相关论文：{papers['papers_count']} 篇")
        if papers['papers'][:3]:
            print("   高被引 Top 3:")
            for p in papers['papers'][:3]:
                print(f"     - {p['title']} ({p['cited_count']} 次)")
    else:
        print(f"   ⚠️ {papers.get('note', '文献抓取失败')}")
    print()
    
    # 期刊推荐
    journals = results.get('journals', {})
    print("📚【期刊推荐 Top 5】")
    if journals.get('success'):
        for i, j in enumerate(journals['matched_journals'][:5], 1):
            print(f"   {i}. 《{j['期刊名称']}》- 匹配度 {j['match_score']:.0f}% ({j['级别']})")
            if j.get('matching_topics'):
                topics = ', '.join(j['matching_topics'][:2])
                print(f"      契合点：{topics}")
    else:
        print(f"   ⚠️ {journals.get('error', '期刊匹配失败')}")
    print()
    
    # 研究空白
    gaps = results.get('gaps', {})
    print("💡【研究空白 Top 3】")
    if gaps.get('success') and gaps.get('gaps'):
        sorted_gaps = sorted(gaps['gaps'], key=lambda x: x.get('gap_score', 0), reverse=True)
        for i, gap in enumerate(sorted_gaps[:3], 1):
            stars = '⭐' * round(gap.get('gap_score', 0))
            print(f"   {i}. {gap['type']} ({stars})")
            print(f"      {gap['description'][:60]}...")
    else:
        print(f"   ⚠️ 暂无足够数据进行分析")
    print()
    
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(description='CNKI 选题分析助手')
    parser.add_argument('keyword', help='要分析的选题关键词')
    parser.add_argument('--full-report', action='store_true', help='执行完整分析（含文献抓取）')
    parser.add_argument('--quick', action='store_true', help='快速分析（仅热榜 + 趋势 + 期刊）')
    parser.add_argument('--check-rank', action='store_true', help='只检查热榜排名')
    parser.add_argument('--check-trend', action='store_true', help='只分析趋势')
    parser.add_argument('--match-journals', action='store_true', help='只匹配期刊')
    parser.add_argument('--crawl-papers', action='store_true', help='只抓取文献')
    parser.add_argument('--top', type=int, default=10, help='期刊推荐数量（默认 10）')
    parser.add_argument('--level', choices=['all', 'core', 'extended'], default='all', help='期刊级别筛选')
    parser.add_argument('--limit', type=int, default=100, help='文献抓取数量限制')
    parser.add_argument('--output', type=str, help='输出报告路径（默认保存到关键词专属目录）')
    parser.add_argument('--isolation', action='store_true', help='启用任务隔离（默认启用）')
    parser.add_argument('--cleanup', action='store_true', help='清理旧数据')
    
    args = parser.parse_args()
    
    # 加载配置
    config = load_config()
    if not config:
        print("⚠️ 配置文件不存在，请先运行：python scripts/init.py")
        sys.exit(1)
    
    # 初始化隔离管理器
    isolation = IsolationManager(SKILL_ROOT)
    
    # 清理旧数据（如果请求）
    if args.cleanup:
        print("🧹 清理旧数据...")
        isolation.cleanup_all_temp()
        print()
    
    results = {}
    
    # 准备隔离环境
    if args.isolation:
        keyword_dir = isolation.prepare_run(args.keyword)
        print(f"📁 使用隔离目录：{keyword_dir}")
        trend_output_dir = os.path.join(keyword_dir, 'charts')
    else:
        trend_output_dir = REPORTS_DIR
    
    # 根据参数决定执行哪些模块
    if args.check_rank or args.quick or args.full_report:
        print("🔍 正在检查热榜排名...")
        results['rank'] = check_rank(args.keyword)
    
    if args.check_trend or args.quick or args.full_report:
        print("📈 正在分析趋势...")
        # 配置中文字体路径
        font_path = os.path.join(SKILL_ROOT, 'data/STSONG.TTF')
        if not os.path.exists(font_path):
            font_path = None
        results['trend'] = analyze_trend(args.keyword, output_dir=trend_output_dir, font_path=font_path)
    
    if args.crawl_papers or args.full_report:
        print("📄 正在抓取文献...")
        results['papers'] = crawl_papers(args.keyword, limit=args.limit)
    
    if args.match_journals or args.quick or args.full_report:
        print("📚 正在匹配期刊...")
        results['journals'] = match_journals(args.keyword, top_n=args.top, level=args.level)
    
    # 研究空白分析（自动执行，基于已有数据）
    print("💡 正在分析研究空白...")
    gap_analyzer = ResearchGapAnalyzer()
    gap_results = []
    
    if results.get('papers', {}).get('success') and results['papers'].get('papers'):
        paper_gaps = gap_analyzer.analyze_from_papers(results['papers']['papers'])
        gap_results.extend(paper_gaps)
    
    if results.get('trend', {}).get('success') and 'metrics' in results['trend']:
        trend_gaps = gap_analyzer.analyze_from_trend_data(results['trend'])
        gap_results.extend(trend_gaps)
    
    if results.get('journals', {}).get('success') and results['journals'].get('matched_journals'):
        journal_gaps = gap_analyzer.analyze_from_cssci(results['journals']['matched_journals'])
        gap_results.extend(journal_gaps)
    
    results['gaps'] = {
        'success': len(gap_results) > 0,
        'gaps': gap_results,
        'report': gap_analyzer.generate_gap_report(gap_results)
    }
    
    # 打印摘要
    print_summary(args.keyword, results)
    
    # 生成完整报告
    if args.output:
        # 用户指定了输出路径
        print(f"\n📝 生成报告：{args.output}")
        report = generate_report(
            keyword=args.keyword,
            rank_data=results.get('rank', {}),
            trend_data=results.get('trend', {}),
            paper_data=results.get('papers', {}),
            journal_data=results.get('journals', {}),
            gap_data=results.get('gaps', {}),
            output_path=args.output
        )
        print("✅ 报告已保存")
    else:
        # 使用隔离目录
        if args.isolation:
            report_filename = f"{args.keyword}_分析报告.md"
            report_path = isolation.get_output_path(args.keyword, report_filename)
            print(f"\n📝 生成报告：{report_path}")
            report = generate_report(
                keyword=args.keyword,
                rank_data=results.get('rank', {}),
                trend_data=results.get('trend', {}),
                paper_data=results.get('papers', {}),
                journal_data=results.get('journals', {}),
                gap_data=results.get('gaps', {}),
                output_path=report_path
            )
            print("✅ 报告已保存到隔离目录")
            
            # 打印隔离状态
            print("\n" + isolation.generate_isolation_report(args.keyword))
    
    # 返回成功/失败状态
    success_count = sum(1 for r in results.values() if r.get('success'))
    total_count = len(results)
    
    if success_count == total_count:
        print("\n✅ 分析完成！")
        sys.exit(0)
    else:
        print(f"\n⚠️ 分析完成，{total_count - success_count} 个模块失败")
        sys.exit(0 if success_count > 0 else 1)


if __name__ == '__main__':
    main()
