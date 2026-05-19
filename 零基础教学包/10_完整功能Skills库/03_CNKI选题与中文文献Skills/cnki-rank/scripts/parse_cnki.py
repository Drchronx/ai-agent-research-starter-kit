#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNKI 热点数据解析模块
解析 JavaScript 返回的数据，提取四个榜单
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Any, Optional


def js_to_json(js_str: str) -> str:
    """
    将 JavaScript 对象字符串转换为合法 JSON
    主要处理：无引号的键名
    """
    # 给键名添加双引号：key: -> "key":
    json_str = re.sub(r'([{,]\s*)([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1"\2":', js_str)
    return json_str


def extract_js_variable(js_text: str, var_name: str) -> Optional[str]:
    """从 JavaScript 代码中提取变量值"""
    # 尝试匹配数组类型变量 - 需要找到匹配的结束括号
    pattern = rf'{var_name}='
    match = re.search(pattern, js_text)
    if not match:
        return None
    
    start = match.end()
    # 找到数组的开始
    if js_text[start] != '[':
        return None
    
    # 计算括号匹配
    bracket_count = 0
    end = start
    for i in range(start, len(js_text)):
        if js_text[i] == '[':
            bracket_count += 1
        elif js_text[i] == ']':
            bracket_count -= 1
            if bracket_count == 0:
                end = i + 1
                break
    
    if bracket_count != 0:
        return None
    
    return js_text[start:end]


def parse_article_data(article_obj: Dict[str, Any], rank: int, scope: str) -> Dict[str, Any]:
    """解析单篇论文数据"""
    return {
        'file_id': article_obj.get('fileId', ''),
        'title': article_obj.get('title', ''),
        'source': article_obj.get('source', ''),
        'pub_date': article_obj.get('pubDateTime', ''),
        'pdsi_score': float(article_obj.get('pdsi', 0) or 0),
        'first_author': article_obj.get('firstAuthor', ''),
        'subject': article_obj.get('subject', ''),
        'title_link': article_obj.get('titleLink', ''),
        'author_link': article_obj.get('authorLink', ''),
        'navi_link': article_obj.get('naviLink', ''),
        'rank': rank,
        'scope': scope,
        'start_date': article_obj.get('startDateTime', ''),
        'end_date': article_obj.get('endDateTime', '')
    }


def parse_keyword_data(keyword_obj: Dict[str, Any], scope: str) -> Dict[str, Any]:
    """解析单个热词数据"""
    return {
        'keyword_id': str(keyword_obj.get('id', '')),
        'keyword': keyword_obj.get('keyword', ''),
        'hot': int(keyword_obj.get('hot', 0) or 0),
        'rate': int(keyword_obj.get('rate', 0) or 0),
        'scope': scope,
        'batch_id': keyword_obj.get('batch_id', ''),
        'link': keyword_obj.get('link', ''),
        'related_words': keyword_obj.get('relatedWords', ''),
        'similar_words': keyword_obj.get('similarWords', '')
    }


def parse_cnki_response(js_text: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    解析 CNKI 接口返回的 JavaScript 数据
    
    返回结构：
    {
        'article_week': [...],
        'article_month': [...],
        'keyword_week': [...],
        'keyword_month': [...]
    }
    """
    result = {
        'article_week': [],
        'article_month': [],
        'keyword_week': [],
        'keyword_month': []
    }
    
    # 解析论文周榜
    article_week_str = extract_js_variable(js_text, 'articleRecommendweek')
    if article_week_str:
        try:
            # 转换为合法 JSON
            article_week_str = js_to_json(article_week_str)
            article_week_list = json.loads(article_week_str)
            for idx, item in enumerate(article_week_list):
                result['article_week'].append(parse_article_data(item, idx + 1, 'week'))
        except json.JSONDecodeError as e:
            print(f"解析论文周榜失败：{e}")
    
    # 解析论文月榜
    article_month_str = extract_js_variable(js_text, 'articleRecommendmonth')
    if article_month_str:
        try:
            article_month_str = js_to_json(article_month_str)
            article_month_list = json.loads(article_month_str)
            for idx, item in enumerate(article_month_list):
                result['article_month'].append(parse_article_data(item, idx + 1, 'month'))
        except json.JSONDecodeError as e:
            print(f"解析论文月榜失败：{e}")
    
    # 解析热词周榜
    keyword_week_str = extract_js_variable(js_text, 'hotSearchweek')
    if keyword_week_str:
        try:
            keyword_week_str = js_to_json(keyword_week_str)
            keyword_week_list = json.loads(keyword_week_str)
            for item in keyword_week_list:
                result['keyword_week'].append(parse_keyword_data(item, 'week'))
        except json.JSONDecodeError as e:
            print(f"解析热词周榜失败：{e}")
    
    # 解析热词月榜
    keyword_month_str = extract_js_variable(js_text, 'hotSearchmonth')
    if keyword_month_str:
        try:
            keyword_month_str = js_to_json(keyword_month_str)
            keyword_month_list = json.loads(keyword_month_str)
            for item in keyword_month_list:
                result['keyword_month'].append(parse_keyword_data(item, 'month'))
        except json.JSONDecodeError as e:
            print(f"解析热词月榜失败：{e}")
    
    return result


def validate_parsed_data(parsed_data: Dict[str, List]) -> bool:
    """验证解析后的数据是否有效"""
    has_data = (
        len(parsed_data.get('article_week', [])) > 0 or
        len(parsed_data.get('article_month', [])) > 0 or
        len(parsed_data.get('keyword_week', [])) > 0 or
        len(parsed_data.get('keyword_month', [])) > 0
    )
    return has_data


if __name__ == '__main__':
    # 测试代码
    import requests
    from urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    
    headers = {
        "sec-ch-ua-platform": '"Windows"',
        "Referer": "https://www.cnki.net/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0",
        "sec-ch-ua": '"Chromium";v="146", "Not-A.Brand";v="24", "Microsoft Edge";v="146"',
        "sec-ch-ua-mobile": "?0"
    }
    url = "https://piccache.cnki.net/kdn/index/kns8s/nvsmscripts/min/nranking.min.js"
    params = {"v": "4.2"}
    
    response = requests.get(url, headers=headers, params=params, verify=False)
    
    if response.status_code == 200:
        parsed = parse_cnki_response(response.text)
        print(f"论文周榜：{len(parsed['article_week'])} 条")
        print(f"论文月榜：{len(parsed['article_month'])} 条")
        print(f"热词周榜：{len(parsed['keyword_week'])} 条")
        print(f"热词月榜：{len(parsed['keyword_month'])} 条")
        
        if parsed['article_week']:
            print("\n论文周榜 TOP3:")
            for item in parsed['article_week'][:3]:
                print(f"  {item['rank']}. {item['title']} (PDSI: {item['pdsi_score']})")
        
        if parsed['keyword_week']:
            print("\n热词周榜 TOP3:")
            for item in parsed['keyword_week'][:3]:
                print(f"  {item['keyword_id']}. {item['keyword']} (热度：{item['hot']})")
    else:
        print(f"请求失败：{response.status_code}")
