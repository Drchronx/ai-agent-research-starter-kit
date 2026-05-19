#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
初始化脚本
检查依赖、创建配置、加载数据、测试所有模块
"""

import sys
import os
import json
import shutil
import subprocess
from pathlib import Path

# 脚本目录（相对路径基准）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
CONFIG_DIR = os.path.join(SKILL_ROOT, 'config')
DATA_DIR = os.path.join(SKILL_ROOT, 'data')
REPORTS_DIR = os.path.join(SKILL_ROOT, 'reports')
CONFIG_PATH = os.path.join(CONFIG_DIR, 'config.json')

# CSSCI 数据源路径
CSSCI_SOURCE = os.path.expanduser('/root/.openclaw/workspace-hotspot/cssci_2025_2026_cleaned.csv')
CSSCI_TARGET = os.path.join(DATA_DIR, 'cssci_2025_2026.csv')

# cnki-crawler 配置路径
CNKI_CRAWLER_CONFIG = os.path.expanduser('/root/.openclaw/workspace-hotspot/skills/cnki-crawler/.env')


def check_dependencies():
    """检查并安装依赖"""
    print("🔍 检查依赖...")
    
    required_packages = [
        ('requests', 'requests'),
        ('pandas', 'pandas'),
        ('openpyxl', 'openpyxl'),
        ('matplotlib', 'matplotlib'),
        ('psycopg2', 'psycopg2-binary'),
        ('sklearn', 'scikit-learn'),
    ]
    
    missing = []
    for import_name, pkg_name in required_packages:
        try:
            __import__(import_name)
            print(f"  ✅ {pkg_name}")
        except ImportError:
            print(f"  ❌ {pkg_name}")
            missing.append(pkg_name)
    
    if missing:
        print(f"\n📦 安装缺失依赖：{', '.join(missing)}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing, '-q'])
            print("✅ 依赖安装完成")
        except subprocess.CalledProcessError as e:
            print(f"❌ 依赖安装失败：{e}")
            return False
    
    return True


def load_cnki_crawler_config():
    """从 cnki-crawler 加载配置"""
    print("\n📋 加载 cnki-crawler 配置...")
    
    if not os.path.exists(CNKI_CRAWLER_CONFIG):
        print(f"  ⚠️ 配置文件不存在：{CNKI_CRAWLER_CONFIG}")
        print(f"  💡 提示：cnki-crawler 应在 {os.path.dirname(CNKI_CRAWLER_CONFIG)}")
        return None
    
    config = {}
    with open(CNKI_CRAWLER_CONFIG, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    
    # 解析数据库配置
    db_config = {}
    if 'CNKI_DB_DSN' in config:
        dsn = config['CNKI_DB_DSN']
        if '://' in dsn:
            parts = dsn.replace('postgresql://', '').split('@')
            if len(parts) == 2:
                user_pass, host_db = parts
                user_pass_parts = user_pass.split(':')
                if len(user_pass_parts) == 2:
                    user, passw = user_pass_parts
                    host_port_db = host_db.split('/')
                    if len(host_port_db) == 2:
                        host_port = host_port_db[0].split(':')
                        if len(host_port) == 2:
                            host, port = host_port
                            db = host_port_db[1]
                            db_config = {
                                'host': host,
                                'port': int(port),
                                'dbname': db,
                                'user': user,
                                'password': passw
                            }
    
    # 解析代理配置
    proxy_config = {}
    if 'CNKI_PROXY_HTTP' in config and 'CNKI_PROXY_HTTPS' in config:
        proxy_config = {
            'http': config['CNKI_PROXY_HTTP'],
            'https': config['CNKI_PROXY_HTTPS']
        }
    
    if db_config:
        print(f"  ✅ 数据库配置：{db_config.get('host')}:{db_config.get('port')}/{db_config.get('dbname')}")
    if proxy_config:
        print(f"  ✅ 代理配置：已配置")
    
    return {
        'database': db_config,
        'proxy': proxy_config
    }


def create_config():
    """创建配置文件"""
    print("\n⚙️ 创建配置...")
    
    os.makedirs(CONFIG_DIR, exist_ok=True)
    
    if os.path.exists(CONFIG_PATH):
        print(f"  ⚠️ 配置文件已存在：{CONFIG_PATH}")
        response = input("  是否覆盖？(y/N): ")
        if response.lower() != 'y':
            print("  跳过配置创建")
            return True
    
    base_config = load_cnki_crawler_config()
    if not base_config:
        print("  ⚠️ 无法加载 cnki-crawler 配置，使用默认值")
        base_config = {
            'database': {
                'host': 'localhost',
                'port': 5432,
                'dbname': 'cnki_db',
                'user': 'cnki_user',
                'password': '123456'
            },
            'proxy': {}
        }
    
    config = {
        'version': '1.0.0',
        'database': base_config['database'],
        'proxy': base_config['proxy'],
        'cssci_data': {
            'path': 'data/cssci_2025_2026.csv',  # 相对路径
            'last_updated': '2026-04-10'
        },
        'output': {
            'report_dir': 'reports',
            'chart_dir': 'reports/charts'
        },
        'external_skills': {
            'cnki_trend': '../cnki-trend/scripts/cnki_keyword_trend_report.py',
            'cnki_crawler': '../cnki-crawler/scripts/main.py',
            'cnki_rank_db': 'academic_hotspot'
        }
    }
    
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print(f"  ✅ 配置已保存：{CONFIG_PATH}")
    return True


def copy_cssci_data():
    """复制 CSSCI 数据到技能目录"""
    print("\n📊 配置 CSSCI 数据...")
    
    os.makedirs(DATA_DIR, exist_ok=True)
    
    if not os.path.exists(CSSCI_SOURCE):
        print(f"  ❌ 源文件不存在：{CSSCI_SOURCE}")
        return False
    
    # 检查目标文件
    if os.path.exists(CSSCI_TARGET):
        print(f"  ⚠️ 目标文件已存在：{CSSCI_TARGET}")
        response = input("  是否覆盖？(y/N): ")
        if response.lower() != 'y':
            print("  跳过数据复制")
            return True
    
    # 复制文件
    try:
        shutil.copy2(CSSCI_SOURCE, CSSCI_TARGET)
        file_size = os.path.getsize(CSSCI_TARGET) / 1024 / 1024
        print(f"  ✅ 数据已复制：{CSSCI_TARGET} ({file_size:.2f} MB)")
        return True
    except Exception as e:
        print(f"  ❌ 复制失败：{e}")
        return False


def test_database_connection():
    """测试数据库连接"""
    print("\n🧪 测试数据库连接...")
    
    config_path = CONFIG_PATH
    if not os.path.exists(config_path):
        print(f"  ⚠️ 配置文件不存在")
        return False
    
    try:
        import psycopg2
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        db_config = config.get('database', {})
        conn = psycopg2.connect(
            host=db_config.get('host', 'localhost'),
            port=db_config.get('port', 5432),
            dbname=db_config.get('dbname', 'cnki_db'),
            user=db_config.get('user'),
            password=db_config.get('password')
        )
        conn.close()
        print(f"  ✅ 数据库连接成功：{db_config.get('host')}:{db_config.get('port')}/{db_config.get('dbname')}")
        return True
    except Exception as e:
        print(f"  ⚠️ 数据库连接失败：{e}")
        print(f"  💡 提示：确保 PostgreSQL 运行且配置正确")
        return True  # 不阻塞后续流程


def test_journal_matcher():
    """测试期刊匹配器"""
    print("\n🧪 测试期刊匹配器...")
    
    try:
        sys.path.insert(0, SCRIPT_DIR)
        from journal_matcher import JournalMatcher
        
        # 使用相对路径
        matcher = JournalMatcher()  # 默认使用 data/cssci_2025_2026.csv
        results = matcher.match("新质生产力", top_n=3)
        
        if results:
            print(f"  ✅ 测试成功，匹配到 {len(results)} 个期刊")
            for r in results:
                print(f"     - 《{r['期刊名称']}》 ({r['match_score']:.0f}%)")
            return True
        else:
            print(f"  ⚠️ 未匹配到期刊（可能数据问题）")
            return True
            
    except Exception as e:
        print(f"  ❌ 测试失败：{e}")
        import traceback
        traceback.print_exc()
        return False


def test_research_gap_analyzer():
    """测试研究空白分析器"""
    print("\n🧪 测试研究空白分析器...")
    
    try:
        sys.path.insert(0, SCRIPT_DIR)
        from research_gap_analyzer import ResearchGapAnalyzer
        
        analyzer = ResearchGapAnalyzer()
        trend_data = {
            'metrics': {
                'yearly': {'recent_3y_ratio': 0.994, 'peak_year': '2025'},
                'subject': {'total_disciplines': 20, 'top_discipline_ratio': 0.224},
                'journal': {'total_journals': 190, 'concentration': 'low'}
            }
        }
        
        gaps = analyzer.analyze_from_trend_data(trend_data)
        
        if gaps:
            print(f"  ✅ 测试成功，识别到 {len(gaps)} 个研究空白")
            for g in gaps[:2]:
                print(f"     - {g['type']} (推荐指数：{g.get('gap_score', 0):.1f})")
            return True
        else:
            print(f"  ⚠️ 未识别到研究空白")
            return True
            
    except Exception as e:
        print(f"  ❌ 测试失败：{e}")
        import traceback
        traceback.print_exc()
        return False


def create_reports_dir():
    """创建报告输出目录"""
    print("\n📁 创建报告目录...")
    
    os.makedirs(REPORTS_DIR, exist_ok=True)
    os.makedirs(os.path.join(REPORTS_DIR, 'charts'), exist_ok=True)
    os.makedirs(os.path.join(REPORTS_DIR, '.gitkeep'), exist_ok=True)
    print(f"  ✅ 报告目录：{REPORTS_DIR}")
    print(f"  💡 提示：每次运行会自动创建关键词专属子目录，确保数据隔离")
    return True


def main():
    print("=" * 60)
    print("CNKI Research Assistant - 初始化")
    print("=" * 60)
    print(f"技能目录：{SKILL_ROOT}")
    print()
    
    # 1. 检查依赖
    if not check_dependencies():
        print("\n❌ 初始化失败：依赖安装问题")
        sys.exit(1)
    
    # 2. 创建配置
    if not create_config():
        print("\n❌ 初始化失败：配置创建问题")
        sys.exit(1)
    
    # 3. 复制 CSSCI 数据
    if not copy_cssci_data():
        print("\n❌ 初始化失败：CSSCI 数据复制问题")
        sys.exit(1)
    
    # 4. 创建报告目录
    create_reports_dir()
    
    # 5. 测试数据库连接
    test_database_connection()
    
    # 6. 测试期刊匹配器
    if not test_journal_matcher():
        print("\n⚠️ 警告：期刊匹配器测试失败")
    
    # 7. 测试研究空白分析器
    if not test_research_gap_analyzer():
        print("\n⚠️ 警告：研究空白分析器测试失败")
    
    print("\n" + "=" * 60)
    print("✅ 初始化完成！")
    print("=" * 60)
    print("\n使用示例:")
    print(f"  cd {SKILL_ROOT}")
    print(f"  python scripts/analyzer.py \"新质生产力\" --quick")
    print(f"  python scripts/analyzer.py \"数字经济\" --full-report --output reports/report.md")
    print()
    print("故障排查:")
    print(f"  cat {CONFIG_PATH}")
    print(f"  python scripts/init.py  # 重新初始化")
    print()


if __name__ == '__main__':
    main()
