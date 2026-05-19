#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNKI 热点报告生成模块
生成周报/月报，包含网络搜索分析
"""

import sys
import os
import json
import requests
from datetime import datetime, date
from typing import Dict, List, Any, Optional

# 添加脚本目录到路径
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from db_manager import CNKIDatabase


def load_config() -> Optional[Dict[str, Any]]:
    """加载配置文件"""
    config_paths = [
        os.path.join(script_dir, '../config/config.json'),
        os.path.expanduser('~/.openclaw/skills/cnki-hotspot/config/config.json')
    ]
    
    for path in config_paths:
        if os.path.exists(path):
            with open(path) as f:
                return json.load(f)
    
    return None


def web_search(query: str, count: int = 5) -> List[Dict[str, str]]:
    """
    网络搜索（使用 DuckDuckGo）
    注意：此函数需要在 OpenClaw 环境中通过 skill 调用才能访问 web_search 工具
    
    Returns:
        搜索结果列表，每项包含 title, url, snippet
    """
    # 在 OpenClaw skill 环境中，直接调用外部 web_search 工具
    # 这里使用 HTTP 方式调用 DuckDuckGo
    try:
        import requests
        from urllib.parse import quote
        
        url = f"https://api.duckduckgo.com/?q={quote(query)}&format=json&no_redirect=1"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        results = []
        # 处理摘要
        if data.get('AbstractText'):
            results.append({
                'title': data.get('Heading', query),
                'url': data.get('AbstractURL', ''),
                'snippet': data.get('AbstractText', '')
            })
        
        # 处理相关结果
        for item in data.get('RelatedTopics', [])[:count]:
            if isinstance(item, dict) and 'Text' in item:
                results.append({
                    'title': item.get('Text', '')[:100],
                    'url': item.get('FirstURL', ''),
                    'snippet': item.get('Text', '')
                })
        
        return results[:count]
    except Exception as e:
        print(f"搜索失败 {query}: {e}")
        return []


def analyze_hotspot(keyword: str, context: str = "") -> Optional[str]:
    """
    分析热点背后的原因
    
    Args:
        keyword: 热点关键词
        context: 额外上下文（如论文标题）
    
    Returns:
        分析摘要，失败返回 None
    """
    query = f"{keyword} 研究热点 原因 2026"
    if context:
        query = f"{keyword} {context} 为什么热门"
    
    results = web_search(query, count=3)
    
    if not results:
        return None
    
    # 简单汇总搜索结果
    summary_parts = []
    for i, r in enumerate(results[:2], 1):
        title = r.get('title', '')
        snippet = r.get('snippet', '')
        if title or snippet:
            summary_parts.append(f"{title}. {snippet}" if title else snippet)
    
    return "\n".join(summary_parts) if summary_parts else None


def generate_report(period: str = 'week', config: Dict[str, Any] = None) -> str:
    """
    生成热点报告
    
    Args:
        period: 'week' 或 'month'
        config: 配置对象
    
    Returns:
        Markdown 格式报告
    """
    if not config:
        config = load_config()
    
    if not config:
        return "❌ 配置文件不存在，请先初始化"
    
    db = CNKIDatabase(config)
    if not db.connect():
        return "❌ 数据库连接失败"
    
    try:
        report = []
        today = date.today()
        week_num = today.isocalendar()[1]
        month = today.month
        
        # 报告标题
        if period == 'week':
            report.append(f"# 📈 CNKI 学术热点周报 (2026-W{week_num})")
            report.append(f"\n*生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*")
        else:
            report.append(f"# 📊 CNKI 学术热点月报 (2026 年{month}月)")
            report.append(f"\n*生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*")
        
        report.append("\n---\n")
        
        # ==================== 论文热榜 ====================
        report.append("## 🔝 下载热榜 TOP10\n")
        
        top_articles = db.get_top_articles(period, 10)
        if top_articles:
            report.append("| 排名 | 标题 | 期刊 | PDSI | 在榜天数 | 趋势 |")
            report.append("|------|------|------|------|----------|------|")
            
            for article in top_articles:
                rank = article.get(f'{period}_rank', '-')
                title = article.get('title', '')[:40] + '...' if len(article.get('title', '')) > 40 else article.get('title', '')
                source = article.get('source', '')[:20]
                pdsi = article.get(f'{period}_pdsi', '-')
                days = article.get(f'{period}_total_days', 0)
                status = article.get(f'{period}_status', '')
                
                trend_emoji = {'new': '🆕', 'continuing': '🔼', 'returning': '♻️'}.get(status, '')
                
                report.append(f"| {rank} | {title} | {source} | {pdsi} | {days} | {trend_emoji} |")
        else:
            report.append("*暂无数据*")
        
        report.append("\n")
        
        # ==================== 热词榜 ====================
        report.append("## 🔥 热词榜 TOP10\n")
        
        top_keywords = db.get_top_keywords(period, 10)
        if top_keywords:
            report.append("| 排名 | 关键词 | 热度 | 变化 | 在榜天数 |")
            report.append("|------|--------|------|------|----------|")
            
            for kw in top_keywords:
                rank = kw.get(f'{period}_rank', '-')
                keyword = kw.get('keyword', '')
                hot = kw.get(f'{period}_hot', '-')
                rate = kw.get(f'{period}_rate', 0)
                days = kw.get(f'{period}_total_days', 0)
                
                rate_emoji = '🔼' if rate > 0 else ('🔽' if rate < 0 else '➖')
                
                report.append(f"| {rank} | {keyword} | {hot} | {rate_emoji}{rate} | {days} |")
        else:
            report.append("*暂无数据*")
        
        report.append("\n---\n")
        
        # ==================== 霸榜文章 ====================
        report.append("## 👑 长期霸榜 (≥3 周)\n")
        
        dominating = db.get_dominating_articles(3)
        if dominating:
            for article in dominating[:5]:
                title = article.get('title', '')
                week_consecutive = article.get('week_consecutive', 0)
                month_consecutive = article.get('month_consecutive', 0)
                max_consecutive = max(week_consecutive, month_consecutive)
                report.append(f"- **{title}** (连续 {max_consecutive} 周)")
        else:
            report.append("*暂无长期霸榜文章*")
        
        report.append("\n")
        
        # ==================== 黑马新上榜 ====================
        report.append("## 🚀 黑马新上榜\n")
        
        newcomers = db.get_newcomer_articles()
        if newcomers:
            for article in newcomers[:5]:
                title = article.get('title', '')
                rank = article.get(f'{period}_rank', '')
                pdsi = article.get(f'{period}_pdsi', '-')
                report.append(f"- **{title}** (排名 {rank}, PDSI {pdsi})")
        else:
            report.append("*本期无新上榜文章*")
        
        report.append("\n")
        
        # ==================== 卷土重来 ====================
        report.append("## ♻️ 卷土重来\n")
        
        returning = db.get_returning_articles()
        if returning:
            for article in returning[:5]:
                title = article.get('title', '')
                rank = article.get(f'{period}_rank', '')
                days = article.get(f'{period}_total_days', 0)
                report.append(f"- **{title}** (排名 {rank}, 累计在榜 {days} 天)")
        else:
            report.append("*本期无卷土重来文章*")
        
        report.append("\n---\n")
        
        # ==================== 热点分析（网络搜索） ====================
        if config.get('report', {}).get('enable_web_search', True):
            report.append("## 🔍 热点背后原因分析\n")
            
            search_top_n = config.get('report', {}).get('search_top_n', 2)
            search_threshold = config.get('report', {}).get('search_threshold', {})
            
            analyzed_count = 0
            
            # 分析 TOP 文章
            for article in top_articles[:search_top_n]:
                title = article.get('title', '')
                keyword = title.split('：')[0].split('——')[0][:20]  # 提取关键词
                
                analysis = analyze_hotspot(keyword, title)
                if analysis:
                    report.append(f"### {title}\n")
                    report.append(f"{analysis}\n")
                    analyzed_count += 1
            
            # 分析新上榜
            if search_threshold.get('new_ranking', True):
                for article in newcomers[:2]:
                    title = article.get('title', '')
                    keyword = title.split('：')[0][:20]
                    
                    analysis = analyze_hotspot(keyword, f"新上榜 {title}")
                    if analysis:
                        report.append(f"### 🆕 {title}\n")
                        report.append(f"{analysis}\n")
                        analyzed_count += 1
            
            # 分析卷土重来
            if search_threshold.get('returning', True):
                for article in returning[:2]:
                    title = article.get('title', '')
                    keyword = title.split('：')[0][:20]
                    
                    analysis = analyze_hotspot(keyword, f"卷土重来 {title}")
                    if analysis:
                        report.append(f"### ♻️ {title}\n")
                        report.append(f"{analysis}\n")
                        analyzed_count += 1
            
            if analyzed_count == 0:
                report.append("*暂无分析数据*")
        
        report.append("\n---\n")
        report.append("\n*报告生成完毕 | 数据来源：CNKI 中国知网*")
        
        return "\n".join(report)
        
    finally:
        db.close()


def create_feishu_doc(report: str, title: str = None) -> Optional[str]:
    """
    创建飞书文档
    
    Returns:
        文档 ID，失败返回 None
    """
    try:
        from feishu_create_doc import feishu_create_doc
        
        if not title:
            today = date.today()
            title = f"CNKI 学术热点周报 (2026-W{today.isocalendar()[1]})"
        
        result = feishu_create_doc(title=title, markdown=report)
        return result.get('doc_id') or result.get('obj_token')
    except Exception as e:
        print(f"创建飞书文档失败：{e}")
        return None


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='CNKI 热点报告生成')
    parser.add_argument('--period', choices=['week', 'month'], default='week',
                        help='报告周期：week(周报), month(月报)')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--feishu', action='store_true', help='创建飞书文档')
    parser.add_argument('--title', help='飞书文档标题')
    
    args = parser.parse_args()
    
    config = load_config()
    if not config:
        print("❌ 配置文件不存在，请先初始化")
        sys.exit(1)
    
    # 生成报告
    report = generate_report(args.period, config)
    
    # 输出
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"✅ 报告已保存到：{args.output}")
    else:
        print(report)
    
    # 创建飞书文档
    if args.feishu:
        doc_id = create_feishu_doc(report, args.title)
        if doc_id:
            print(f"\n✅ 飞书文档已创建：https://bytedance.feishu.cn/docx/{doc_id}")
        else:
            print("\n❌ 飞书文档创建失败")


if __name__ == '__main__':
    main()
