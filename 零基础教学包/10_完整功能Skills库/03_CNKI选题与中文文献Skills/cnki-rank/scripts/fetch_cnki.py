#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNKI 热点数据抓取脚本
负责请求 CNKI 接口、解析数据、入库更新
"""

import sys
import os
import json
import time
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional

# 添加脚本目录到路径
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from parse_cnki import parse_cnki_response, validate_parsed_data
from db_manager import CNKIDatabase


# 请求配置
CNKI_URL = "https://piccache.cnki.net/kdn/index/kns8s/nvsmscripts/min/nranking.min.js"
HEADERS = {
    "sec-ch-ua-platform": '"Windows"',
    "Referer": "https://www.cnki.net/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0",
    "sec-ch-ua": '"Chromium";v="146", "Not-A.Brand";v="24", "Microsoft Edge";v="146"',
    "sec-ch-ua-mobile": "?0"
}

# 禁用 SSL 警告
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


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


def fetch_cnki_data(scope: str = 'all', max_retries: int = 3) -> Optional[str]:
    """
    抓取 CNKI 热点数据（带重试机制）
    
    Args:
        scope: 'week', 'month', or 'all'
        max_retries: 最大重试次数，默认 3 次
    
    Returns:
        JavaScript 响应文本，失败返回 None
    """
    for attempt in range(1, max_retries + 1):
        try:
            print(f"正在请求 CNKI 接口（第 {attempt}/{max_retries} 次尝试）...")
            response = requests.get(CNKI_URL, headers=HEADERS, params={"v": "4.2"}, timeout=30, verify=False)
            response.raise_for_status()
            print(f"请求成功！")
            return response.text
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response else 'unknown'
            print(f"HTTP 错误 {status_code}：{e}")
            if status_code == 418:
                print(f"  → 检测到限流（418），等待 5 秒后重试...")
            elif status_code >= 500:
                print(f"  → 服务器错误，等待 3 秒后重试...")
            else:
                print(f"  → 其他 HTTP 错误，等待 2 秒后重试...")
            if attempt < max_retries:
                wait_time = 5 if status_code == 418 else (3 if status_code >= 500 else 2)
                time.sleep(wait_time)
        except requests.exceptions.Timeout:
            print(f"请求超时（第 {attempt} 次），等待 3 秒后重试...")
            if attempt < max_retries:
                time.sleep(3)
        except requests.exceptions.ConnectionError as e:
            print(f"连接错误：{e}（第 {attempt} 次），等待 3 秒后重试...")
            if attempt < max_retries:
                time.sleep(3)
        except requests.RequestException as e:
            print(f"请求失败：{e}")
            break
    
    print(f"所有 {max_retries} 次尝试均失败，放弃抓取")
    return None


def process_articles(db: CNKIDatabase, articles: List[Dict[str, Any]], scope: str) -> Dict[str, int]:
    """处理论文数据"""
    stats = {'new': 0, 'returning': 0, 'continuing': 0, 'dropped': 0}
    current_file_ids = []
    
    for article in articles:
        try:
            current_file_ids.append(article['file_id'])
            
            # 获取当前状态
            existing = db.get_article_status(article['file_id'])
            
            if existing:
                rank_field = f'{scope}_rank'
                if existing.get(rank_field) is not None:
                    stats['continuing'] += 1
                else:
                    stats['returning'] += 1
            else:
                stats['new'] += 1
            
            # 更新数据库
            db.update_article_hotspot(article, scope)
        except Exception as e:
            print(f"处理论文 {article.get('title', 'unknown')} 失败：{e}")
            import traceback
            traceback.print_exc()
    
    # 标记下榜论文
    db.mark_dropped_articles(current_file_ids, scope)
    
    # 记录历史快照
    db.record_article_history(articles, scope)
    
    return stats


def process_keywords(db: CNKIDatabase, keywords: List[Dict[str, Any]], scope: str) -> Dict[str, int]:
    """处理热词数据"""
    stats = {'new': 0, 'returning': 0, 'continuing': 0, 'dropped': 0}
    current_keyword_ids = []
    
    for keyword in keywords:
        current_keyword_ids.append(keyword['keyword_id'])
        
        # 获取当前状态
        existing = db.get_keyword_status(keyword['keyword_id'])
        
        if existing:
            rank_field = f'{scope}_rank'
            if existing.get(rank_field) is not None:
                stats['continuing'] += 1
            else:
                stats['returning'] += 1
        else:
            stats['new'] += 1
        
        # 更新数据库
        db.update_keyword_hotspot(keyword, scope)
    
    # 标记下榜热词
    db.mark_dropped_keywords(current_keyword_ids, scope)
    
    # 记录历史快照
    db.record_keyword_history(keywords, scope)
    
    return stats


def fetch_and_store(scope: str = 'all') -> Dict[str, Any]:
    """
    主函数：抓取并存储数据
    
    Returns:
        抓取结果摘要
    """
    result = {
        'success': False,
        'scope': scope,
        'timestamp': datetime.now().isoformat(),
        'article_stats': {},
        'keyword_stats': {},
        'error': None
    }
    
    # 加载配置
    config = load_config()
    if not config:
        result['error'] = '配置文件不存在，请先运行初始化'
        return result
    
    # 抓取数据
    js_text = fetch_cnki_data(scope)
    if not js_text:
        result['error'] = '数据抓取失败'
        return result
    
    # 解析数据
    parsed_data = parse_cnki_response(js_text)
    if not validate_parsed_data(parsed_data):
        result['error'] = '数据解析失败'
        return result
    
    # 连接数据库
    db = CNKIDatabase(config)
    if not db.connect():
        result['error'] = '数据库连接失败'
        return result
    
    try:
        # 处理周榜
        if scope in ['week', 'all']:
            article_stats = process_articles(db, parsed_data['article_week'], 'week')
            keyword_stats = process_keywords(db, parsed_data['keyword_week'], 'week')
            
            result['article_stats']['week'] = article_stats
            result['keyword_stats']['week'] = keyword_stats
        
        # 处理月榜
        if scope in ['month', 'all']:
            article_stats = process_articles(db, parsed_data['article_month'], 'month')
            keyword_stats = process_keywords(db, parsed_data['keyword_month'], 'month')
            
            result['article_stats']['month'] = article_stats
            result['keyword_stats']['month'] = keyword_stats
        
        # 提交事务
        db.commit()
        
        # 记录抓取日志
        total_stats = {
            'article_count': sum(len(parsed_data.get(f'article_{s}', [])) for s in ['week', 'month'] if scope in [s, 'all']),
            'keyword_count': sum(len(parsed_data.get(f'keyword_{s}', [])) for s in ['week', 'month'] if scope in [s, 'all']),
        }
        
        for period_stats in result['article_stats'].values():
            total_stats['new_articles'] = total_stats.get('new_articles', 0) + period_stats.get('new', 0)
            total_stats['returning_articles'] = total_stats.get('returning_articles', 0) + period_stats.get('returning', 0)
        
        for period_stats in result['keyword_stats'].values():
            total_stats['new_keywords'] = total_stats.get('new_keywords', 0) + period_stats.get('new', 0)
            total_stats['returning_keywords'] = total_stats.get('returning_keywords', 0) + period_stats.get('returning', 0)
        
        db.record_crawl_log(scope, total_stats)
        db.commit()
        
        result['success'] = True
        
    except Exception as e:
        db.rollback()
        result['error'] = str(e)
        db.record_crawl_log(scope, {}, 'failed', str(e))
        db.commit()
    
    finally:
        db.close()
    
    return result


def print_summary(result: Dict[str, Any]):
    """打印抓取摘要"""
    print("=" * 60)
    print("CNKI 热点数据抓取完成")
    print("=" * 60)
    print(f"时间：{result['timestamp']}")
    print(f"范围：{result['scope']}")
    print(f"状态：{'✅ 成功' if result['success'] else '❌ 失败'}")
    
    if result['error']:
        print(f"错误：{result['error']}")
        return
    
    for period, stats in result.get('article_stats', {}).items():
        print(f"\n📄 论文{period}榜:")
        print(f"  新增：{stats.get('new', 0)}")
        print(f"  持续：{stats.get('continuing', 0)}")
        print(f"  回归：{stats.get('returning', 0)}")
    
    for period, stats in result.get('keyword_stats', {}).items():
        print(f"\n🔥 热词{period}榜:")
        print(f"  新增：{stats.get('new', 0)}")
        print(f"  持续：{stats.get('continuing', 0)}")
        print(f"  回归：{stats.get('returning', 0)}")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='CNKI 热点数据抓取')
    parser.add_argument('--scope', choices=['week', 'month', 'all'], default='all',
                        help='抓取范围：week(周榜), month(月榜), all(全部)')
    parser.add_argument('--json', action='store_true', help='以 JSON 格式输出结果')
    
    args = parser.parse_args()
    
    result = fetch_and_store(args.scope)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_summary(result)
        sys.exit(0 if result['success'] else 1)
