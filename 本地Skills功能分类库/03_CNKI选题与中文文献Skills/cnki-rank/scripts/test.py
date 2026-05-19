#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNKI 热点技能测试脚本
验证各模块功能是否正常
"""

import sys
import os

# 添加脚本目录到路径
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)


def test_parse_module():
    """测试解析模块"""
    print("=" * 60)
    print("测试 1: 解析模块")
    print("=" * 60)
    
    try:
        from parse_cnki import parse_cnki_response, validate_parsed_data
        import requests
        
        # 抓取数据
        url = "https://piccache.cnki.net/kdn/index/kns8s/nvsmscripts/min/nranking.min.js"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, params={"v": "4.2"}, timeout=10)
        
        if response.status_code != 200:
            print(f"❌ 请求失败：{response.status_code}")
            return False
        
        # 解析数据
        parsed = parse_cnki_response(response.text)
        
        # 验证
        if not validate_parsed_data(parsed):
            print("❌ 解析结果为空")
            return False
        
        # 输出统计
        print(f"✅ 解析成功")
        print(f"   论文周榜：{len(parsed['article_week'])} 条")
        print(f"   论文月榜：{len(parsed['article_month'])} 条")
        print(f"   热词周榜：{len(parsed['keyword_week'])} 条")
        print(f"   热词月榜：{len(parsed['keyword_month'])} 条")
        
        # 显示示例
        if parsed['article_week']:
            first = parsed['article_week'][0]
            print(f"\n   论文周榜 TOP1: {first['title'][:50]}...")
        
        if parsed['keyword_week']:
            first = parsed['keyword_week'][0]
            print(f"   热词周榜 TOP1: {first['keyword']} (热度：{first['hot']})")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败：{e}")
        return False


def test_config():
    """测试配置文件"""
    print("\n" + "=" * 60)
    print("测试 2: 配置文件")
    print("=" * 60)
    
    config_path = os.path.join(script_dir, '../config/config.json')
    
    if not os.path.exists(config_path):
        print(f"⚠️  配置文件不存在：{config_path}")
        print("   请先运行：openclaw exec --skill cnki-hotspot init")
        return False
    
    try:
        import json
        with open(config_path) as f:
            config = json.load(f)
        
        # 验证必要字段
        required = ['database', '_meta']
        for field in required:
            if field not in config:
                print(f"❌ 缺少必要字段：{field}")
                return False
        
        db_config = config['database']
        db_required = ['host', 'port', 'dbname', 'user', 'password']
        for field in db_required:
            if field not in db_config or not db_config[field]:
                print(f"❌ 数据库配置缺少：{field}")
                return False
        
        print(f"✅ 配置文件有效")
        print(f"   数据库：{db_config['dbname']}@{db_config['host']}:{db_config['port']}")
        print(f"   用户：{db_config['user']}")
        print(f"   已初始化：{config['_meta'].get('initialized', False)}")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置文件读取失败：{e}")
        return False


def test_database():
    """测试数据库连接"""
    print("\n" + "=" * 60)
    print("测试 3: 数据库连接")
    print("=" * 60)
    
    config_path = os.path.join(script_dir, '../config/config.json')
    if not os.path.exists(config_path):
        print("⚠️  配置文件不存在，跳过数据库测试")
        return None
    
    try:
        import json
        with open(config_path) as f:
            config = json.load(f)
        
        from db_manager import CNKIDatabase
        
        db = CNKIDatabase(config)
        if not db.connect():
            print("❌ 数据库连接失败")
            return False
        
        # 测试查询
        top_articles = db.get_top_articles('week', 5)
        print(f"✅ 数据库连接成功")
        print(f"   周榜论文数：{len(top_articles)}")
        
        if top_articles:
            print(f"   TOP1: {top_articles[0]['title'][:50]}...")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ 数据库测试失败：{e}")
        return False


def test_report_generation():
    """测试报告生成"""
    print("\n" + "=" * 60)
    print("测试 4: 报告生成")
    print("=" * 60)
    
    config_path = os.path.join(script_dir, '../config/config.json')
    if not os.path.exists(config_path):
        print("⚠️  配置文件不存在，跳过报告测试")
        return None
    
    try:
        import json
        with open(config_path) as f:
            config = json.load(f)
        
        from report_generator import generate_report
        
        report = generate_report('week', config)
        
        if not report or report.startswith('❌'):
            print(f"❌ 报告生成失败：{report}")
            return False
        
        # 检查报告内容
        sections = ['#', '##', '📈', '🔝', '🔥']
        found_sections = [s for s in sections if s in report]
        
        print(f"✅ 报告生成成功")
        print(f"   长度：{len(report)} 字符")
        print(f"   包含章节：{', '.join(found_sections)}")
        
        # 显示前 500 字符
        print(f"\n   报告预览:")
        for line in report.split('\n')[:10]:
            print(f"   {line}")
        
        return True
        
    except Exception as e:
        print(f"❌ 报告生成失败：{e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("CNKI-Hotspot 技能测试")
    print("=" * 60)
    
    results = {
        'parse': test_parse_module(),
        'config': test_config(),
        'database': test_database(),
        'report': test_report_generation()
    }
    
    # 汇总
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v is True)
    total = len([v for v in results.values() if v is not None])
    
    for test_name, result in results.items():
        if result is True:
            print(f"✅ {test_name}: 通过")
        elif result is False:
            print(f"❌ {test_name}: 失败")
        else:
            print(f"⚠️  {test_name}: 跳过")
    
    print(f"\n总计：{passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！")
        sys.exit(0)
    else:
        print("\n⚠️  部分测试失败，请检查配置")
        sys.exit(1)


if __name__ == '__main__':
    main()
