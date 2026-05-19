#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNKI 热点快速测试报告（不依赖数据库）
"""

import sys
import os
import requests
import urllib3
from datetime import datetime, date

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from parse_cnki import parse_cnki_response


def web_search(query, count=3):
    """网络搜索"""
    try:
        from web_search import web_search as search_func
        return search_func(query=query, count=count)
    except:
        return []


def generate_quick_report():
    """生成快速测试报告"""
    
    # 抓取数据
    print("正在抓取 CNKI 数据...")
    url = "https://piccache.cnki.net/kdn/index/kns8s/nvsmscripts/min/nranking.min.js"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    response = requests.get(url, headers=headers, params={"v": "4.2"}, verify=False, timeout=30)
    
    if response.status_code != 200:
        print(f"抓取失败：{response.status_code}")
        return
    
    parsed = parse_cnki_response(response.text)
    
    # 生成报告
    today = date.today()
    week_num = today.isocalendar()[1]
    
    report = []
    report.append(f"# 📈 CNKI 学术热点测试报告 (2026-W{week_num})")
    report.append(f"\n*生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    report.append("\n---\n")
    
    # 论文周榜
    report.append("## 🔝 下载热榜 TOP10（周榜）\n")
    report.append("| 排名 | 标题 | 期刊 | PDSI |")
    report.append("|------|------|------|------|")
    
    for article in parsed['article_week'][:10]:
        title = article['title'][:40] + '...' if len(article['title']) > 40 else article['title']
        source = article['source'][:20]
        pdsi = article['pdsi_score']
        report.append(f"| {article['rank']} | {title} | {source} | {pdsi} |")
    
    report.append("\n")
    
    # 热词周榜
    report.append("## 🔥 热词榜 TOP10（周榜）\n")
    report.append("| 排名 | 关键词 | 热度 |")
    report.append("|------|--------|------|")
    
    for kw in parsed['keyword_week'][:10]:
        report.append(f"| {int(kw['keyword_id'])+1} | {kw['keyword']} | {kw['hot']} |")
    
    report.append("\n---\n")
    
    # 热点分析
    report.append("## 🔍 热点分析（网络搜索）\n")
    
    # 分析 TOP2 热词
    for kw in parsed['keyword_week'][:2]:
        keyword = kw['keyword']
        print(f"正在搜索 \"{keyword}\" 相关背景...")
        
        results = web_search(f"{keyword} 研究热点 2026", count=2)
        
        if results:
            report.append(f"### {keyword}\n")
            for r in results:
                title = r.get('title', '')
                snippet = r.get('snippet', '')
                if title or snippet:
                    report.append(f"- **{title}**: {snippet}\n")
            report.append("\n")
    
    report.append("\n---\n")
    report.append("\n*测试报告生成完毕 | 数据来源：CNKI 中国知网*")
    
    return "\n".join(report)


if __name__ == '__main__':
    report = generate_quick_report()
    
    # 输出到文件
    output_path = '/tmp/cnki_test_report.md'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ 测试报告已生成：{output_path}")
    print("\n" + "=" * 60)
    print("报告预览（前 50 行）:")
    print("=" * 60)
    
    for line in report.split('\n')[:50]:
        print(line)
