#!/usr/bin/env python3
"""
导出 CNKI 文献到 JSON 文件

支持按查询条件过滤，确保每个会话导出独立的数据文件
"""

import argparse
import json
import psycopg2
import sys
from pathlib import Path
from datetime import datetime


def export_to_json(output_path: str, query_pattern: str = None, start_year: str = None, end_year: str = None, dsn: str = None):
    """
    导出 CNKI 文献到 JSON 文件
    
    Args:
        output_path: 输出文件路径
        query_pattern: 查询模式（可选，用于过滤）
        start_year: 起始年份
        end_year: 结束年份
        dsn: 数据库连接字符串
    """
    # 默认数据库配置
    if dsn is None:
        dsn = "postgresql://cnki_user:123456@localhost/cnki_db"
    
    # 连接数据库
    conn = psycopg2.connect(dsn)
    cur = conn.cursor()
    
    # 构建查询
    conditions = []
    params = []
    
    if query_pattern:
        conditions.append("search_terms = %s")
        params.append(query_pattern)
    
    if start_year and end_year:
        conditions.append("year BETWEEN %s AND %s")
        params.extend([start_year, end_year])
    
    where_clause = ""
    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)
    
    query = f"""
        SELECT title, authors, journal, year, issue, publish_date, 
               abstract, keywords, organizations, funds, 
               cited_count, download_count, detail_url, search_terms
        FROM cnki_papers
        {where_clause}
        ORDER BY year DESC, cited_count DESC
    """
    
    cur.execute(query, params)
    
    papers = []
    for row in cur.fetchall():
        paper = {
            'source_db': 'cnki',
            'backend': 'cnki-crawler',
            'backend_query': row[12] or query_pattern or '',
            'title': row[0] or '',
            'authors': row[1] if row[1] else [],
            'organizations': row[8] if row[8] else [],
            'journal': row[2] or '',
            'year': row[3] or '',
            'publish_date': row[5] or '',
            'volume': '',
            'issue': row[4] or '',
            'pages': '',
            'doi': '',
            'abstract': row[6] or '',
            'keywords': row[7] if row[7] else [],
            'funds': row[9] if row[9] else [],
            'cited_count': int(row[10]) if row[10] and str(row[10]).isdigit() else 0,
            'download_count': int(row[11]) if row[11] and str(row[11]).isdigit() else 0,
            'source_url': row[12] or '',
            'language': 'zh'
        }
        papers.append(paper)
    
    cur.close()
    conn.close()
    
    # 确保输出目录存在
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # 保存到 JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(papers, f, ensure_ascii=False, indent=2)
    
    print(f"导出 {len(papers)} 篇文献到 {output_path}")
    return len(papers)


def main():
    parser = argparse.ArgumentParser(description='导出 CNKI 文献到 JSON')
    parser.add_argument('output_path', type=str, help='输出文件路径')
    parser.add_argument('--query-pattern', type=str, default=None, help='查询模式（用于过滤）')
    parser.add_argument('--start-year', type=str, default=None, help='起始年份')
    parser.add_argument('--end-year', type=str, default=None, help='结束年份')
    parser.add_argument('--dsn', type=str, default=None, help='数据库连接字符串')
    
    args = parser.parse_args()
    
    export_to_json(
        output_path=args.output_path,
        query_pattern=args.query_pattern,
        start_year=args.start_year,
        end_year=args.end_year,
        dsn=args.dsn
    )


if __name__ == '__main__':
    main()
