#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNKI 自动化选题分析助手 v2.1
一键式完成：文献抓取 → 深度分析 → 报告生成 → 数据清理

v2.1 更新 (2026-04-10):
- 每次任务都是 fresh run，直接抓取最新数据
- 任务完成后自动清理临时数据
- 不再依赖数据库历史文献（确保分析时效性）
"""

import sys
import os
import json
import argparse
import subprocess
import time
from datetime import datetime
from pathlib import Path

# 添加脚本目录到路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
CNKI_CRAWLER_SCRIPT = '/root/.openclaw/skills/cnki-crawler/scripts/main.py'
ANALYZER_SCRIPT = os.path.join(SCRIPT_DIR, 'analyzer.py')
TEMP_DB_SUFFIX = '_temp_'  # 临时表后缀


def print_header(text: str):
    """打印标题"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def crawl_papers_fresh(keyword: str, target_count: int = 250):
    """
    抓取最新文献 - Fresh Run 模式
    每次都直接抓取最新数据，确保分析时效性
    
    Args:
        keyword: 检索关键词
        target_count: 目标文献数量（默认 250 篇）
    
    Returns:
        tuple: (success, papers_count, temp_table_name)
    """
    print_header(f"📥 步骤 1: 抓取最新文献（目标：{target_count}篇）")
    print("ℹ️  Fresh Run 模式：每次都是最新数据，不依赖历史文献")
    
    # 构建检索式
    query = f"SU=('{keyword}')"
    print(f"检索式：{query}")
    
    # 生成临时表名（避免污染主表）
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    temp_table = f"cnki_papers_temp_{timestamp}"
    
    print(f"\n正在抓取最新文献...")
    print(f"临时表：{temp_table}")
    
    cmd = [
        sys.executable,
        CNKI_CRAWLER_SCRIPT,
        query,
        '--sort-field', 'CF',  # 按被引频次（权威文献）
        '--limit-pages', '5',  # 抓取 5 页（约 250 篇）
        '--output-table', temp_table  # 写入临时表
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600,
            cwd=os.path.dirname(CNKI_CRAWLER_SCRIPT)
        )
        
        if result.returncode == 0:
            print(f"  ✅ 文献抓取完成")
        else:
            print(f"  ⚠️ 文献抓取失败：{result.stderr[:200]}")
            return False, 0, temp_table
    
    except subprocess.TimeoutExpired:
        print(f"  ⚠️ 文献抓取超时")
        return False, 0, temp_table
    except Exception as e:
        print(f"  ⚠️ 文献抓取异常：{e}")
        return False, 0, temp_table
    
    # 验证抓取结果
    papers_count = verify_papers_count(temp_table)
    print(f"\n抓取完成！共 {papers_count} 篇文献")
    
    if papers_count < 50:
        print(f"⚠️ 文献数量偏少（<{50}篇），可能影响分析质量")
    
    return True, papers_count, temp_table


def verify_papers_count(table_name: str) -> int:
    """验证临时表中文献数量"""
    try:
        import psycopg2
        
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            dbname='cnki_db',
            user='cnki_user',
            password='123456'
        )
        
        with conn.cursor() as cur:
            # 检查临时表是否存在
            cur.execute("""
                SELECT COUNT(*) FROM information_schema.tables 
                WHERE table_name = %s
            """, (table_name,))
            
            if cur.fetchone()[0] == 0:
                # 临时表不存在，尝试查询主表
                cur.execute(f"SELECT COUNT(*) FROM {table_name}")
                return cur.fetchone()[0]
        
        conn.close()
        return 0
    except Exception as e:
        print(f"⚠️ 验证失败：{e}")
        return 0


def cleanup_temp_data(temp_table: str):
    """清理临时数据"""
    print_header("🧹 步骤 4: 清理临时数据")
    
    try:
        import psycopg2
        
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            dbname='cnki_db',
            user='cnki_user',
            password='123456'
        )
        
        with conn.cursor() as cur:
            # 删除临时表
            cur.execute(f"DROP TABLE IF EXISTS {temp_table}")
            print(f"  ✅ 已删除临时表：{temp_table}")
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"⚠️ 清理失败：{e}")


def run_deep_analysis(keyword: str, output_path: str, temp_table: str = None):
    """
    运行深度分析
    
    Args:
        keyword: 关键词
        output_path: 报告输出路径
        temp_table: 临时表名（可选，用于指定数据源）
    """
    print_header("📊 步骤 2: 深度分析")
    
    cmd = [
        sys.executable,
        ANALYZER_SCRIPT,
        keyword,
        '--full-report',
        '--output', output_path
    ]
    
    if temp_table:
        cmd.extend(['--temp-table', temp_table])
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600,
            cwd=SKILL_ROOT
        )
        
        if result.returncode == 0:
            print(f"✅ 分析完成！报告已保存：{output_path}")
            return True
        else:
            print(f"⚠️ 分析失败：{result.stderr[:500]}")
            return False
    
    except subprocess.TimeoutExpired:
        print("⚠️ 分析超时")
        return False
    except Exception as e:
        print(f"⚠️ 分析异常：{e}")
        return False


def create_feishu_doc(keyword: str, report_path: str, charts_dir: str):
    """
    创建飞书文档并插入图表
    
    Args:
        keyword: 关键词
        report_path: 报告路径
        charts_dir: 图表目录
    """
    print_header("📄 步骤 3: 创建飞书文档")
    
    # 读取报告
    with open(report_path, 'r', encoding='utf-8') as f:
        report_content = f.read()
    
    # 简化报告（移除本地图片路径）
    simplified_report = []
    for line in report_content.split('\n'):
        if not line.startswith('!['):  # 跳过本地图片
            simplified_report.append(line)
    
    # 创建飞书文档（使用 subprocess 调用 feishu_create_doc）
    doc_title = f"{keyword} 选题分析报告（深度版）"
    doc_content = '\n'.join(simplified_report)
    
    print(f"文档标题：{doc_title}")
    print("⚠️ 飞书文档创建需要 API 调用，暂跳过...")
    print(f"📄 报告已保存到：{report_path}")
    
    # 返回报告路径，飞书文档可手动创建
    return report_path


def auto_analyze(keyword: str, output_dir: str = None, cleanup: bool = True):
    """
    一键自动化分析（v2.1 Fresh Run 模式）
    
    Args:
        keyword: 选题关键词
        output_dir: 输出目录（可选）
        cleanup: 是否清理临时数据（默认 True）
    
    Returns:
        dict: 包含报告路径、图表目录等
    """
    print_header(f"🚀 CNKI 自动化选题分析：{keyword}")
    print(f"开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("ℹ️  v2.1 Fresh Run 模式：每次都是最新数据")
    
    # 配置输出目录
    if output_dir is None:
        output_dir = os.path.join(SKILL_ROOT, 'reports/auto')
    
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'charts'), exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_path = os.path.join(output_dir, f"{keyword}_分析报告_{timestamp}.md")
    charts_dir = os.path.join(output_dir, 'charts')
    
    temp_table = None
    
    # 步骤 1: 抓取最新文献（Fresh Run）
    crawl_success, papers_count, temp_table = crawl_papers_fresh(keyword, target_count=250)
    
    if not crawl_success:
        print("\n⚠️ 文献抓取失败，但继续分析...")
    
    # 步骤 2: 深度分析
    analysis_success = run_deep_analysis(keyword, report_path, temp_table)
    
    if not analysis_success:
        print("\n⚠️ 分析失败")
        if cleanup and temp_table:
            cleanup_temp_data(temp_table)
        return {'success': False, 'error': '分析失败'}
    
    # 步骤 3: 输出结果
    print_header("✅ 分析完成")
    print(f"报告路径：{report_path}")
    print(f"图表目录：{charts_dir}")
    print(f"文献数量：{papers_count} 篇")
    print(f"\n完成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 步骤 4: 清理临时数据（可选）
    if cleanup and temp_table:
        cleanup_temp_data(temp_table)
    else:
        print(f"ℹ️  保留临时表：{temp_table}")
    
    return {
        'success': True,
        'report_path': report_path,
        'charts_dir': charts_dir,
        'papers_count': papers_count,
        'temp_table': temp_table if not cleanup else None
    }


def main():
    parser = argparse.ArgumentParser(description='CNKI 自动化选题分析助手')
    parser.add_argument('keyword', type=str, help='选题关键词')
    parser.add_argument('--output-dir', type=str, default=None, help='输出目录')
    parser.add_argument('--no-crawl', action='store_true', help='跳过文献抓取')
    
    args = parser.parse_args()
    
    if args.no_crawl:
        # 直接运行分析
        output_dir = args.output_dir or os.path.join(SKILL_ROOT, 'reports')
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = os.path.join(output_dir, f"{args.keyword}_分析报告_{timestamp}.md")
        
        print_header(f"🚀 CNKI 快速分析：{args.keyword}")
        run_deep_analysis(args.keyword, report_path)
    else:
        # 完整自动化流程
        auto_analyze(args.keyword, args.output_dir)


if __name__ == '__main__':
    main()
