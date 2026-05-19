#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNKI 热点技能初始化脚本
交互式配置数据库并创建表结构
"""

import sys
import os
import json
import psycopg2
from datetime import datetime
from typing import Dict, Any

# 添加脚本目录到路径
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)


def ask_question(question: str, default: str = None, password: bool = False) -> str:
    """交互式提问"""
    if default:
        prompt = f"{question} [{default}]: "
    else:
        prompt = f"{question}: "
    
    if password:
        import getpass
        value = getpass.getpass(prompt)
    else:
        value = input(prompt)
    
    return value.strip() if value.strip() else (default or "")


def load_example_config() -> Dict[str, Any]:
    """加载配置模板"""
    example_path = os.path.join(script_dir, '../config/config.example.json')
    if os.path.exists(example_path):
        with open(example_path) as f:
            return json.load(f)
    return {}


def save_config(config: Dict[str, Any]):
    """保存配置文件"""
    config_dir = os.path.join(script_dir, '../config')
    os.makedirs(config_dir, exist_ok=True)
    
    config_path = os.path.join(config_dir, 'config.json')
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 配置文件已保存：{config_path}")


def test_db_connection(db_config: Dict[str, Any]) -> bool:
    """测试数据库连接"""
    try:
        # 先测试能否连接到服务器
        conn = psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            dbname='postgres',
            user=db_config['user'],
            password=db_config['password']
        )
        conn.close()
        
        # 再测试目标数据库是否存在
        try:
            conn = psycopg2.connect(
                host=db_config['host'],
                port=db_config['port'],
                dbname=db_config['dbname'],
                user=db_config['user'],
                password=db_config['password']
            )
            conn.close()
            print(f"✅ 数据库 {db_config['dbname']} 已存在")
        except psycopg2.OperationalError:
            print(f"ℹ️  数据库 {db_config['dbname']} 不存在，将自动创建")
        
        return True
    except Exception as e:
        print(f"❌ 数据库连接失败：{e}")
        return False


def create_database(db_config: Dict[str, Any]) -> bool:
    """创建数据库（如果不存在）"""
    try:
        # 先连接到默认数据库
        conn = psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            dbname='postgres',
            user=db_config['user'],
            password=db_config['password']
        )
        conn.autocommit = True
        cur = conn.cursor()
        
        # 检查数据库是否存在
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_config['dbname'],))
        if not cur.fetchone():
            cur.execute(f"CREATE DATABASE {db_config['dbname']}")
            print(f"✅ 数据库 {db_config['dbname']} 创建成功")
        else:
            print(f"ℹ️  数据库 {db_config['dbname']} 已存在")
        
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"⚠️  数据库创建失败（可能需要手动创建）: {e}")
        return False


def load_schema() -> str:
    """加载 SQL schema"""
    schema_path = os.path.join(script_dir, '../references/schema.sql')
    if os.path.exists(schema_path):
        with open(schema_path, encoding='utf-8') as f:
            return f.read()
    return ""


def create_tables(db_config: Dict[str, Any]) -> bool:
    """创建数据表"""
    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        
        schema_sql = load_schema()
        if schema_sql:
            cur.execute(schema_sql)
            conn.commit()
            print("✅ 数据表创建成功")
        else:
            print("❌ 未找到 schema.sql 文件")
            return False
        
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ 数据表创建失败：{e}")
        return False


def initialize():
    """主初始化流程"""
    print("=" * 60)
    print("CNKI 热点技能初始化")
    print("=" * 60)
    print()
    
    # 加载配置模板
    example_config = load_example_config()
    
    # 交互式配置
    print("请配置数据库连接信息：")
    print()
    
    db_config = {
        'host': ask_question("数据库主机", example_config.get('database', {}).get('host', 'localhost')),
        'port': int(ask_question("数据库端口", str(example_config.get('database', {}).get('port', 5432)))),
        'dbname': ask_question("数据库名称", example_config.get('database', {}).get('dbname', 'academic_hotspot')),
        'user': ask_question("数据库用户", example_config.get('database', {}).get('user', '')),
        'password': ask_question("数据库密码", password=True)
    }
    
    print()
    print("正在测试数据库连接...")
    if not test_db_connection(db_config):
        print()
        retry = ask_question("是否重试？(y/n)", "y")
        if retry.lower() == 'y':
            return initialize()
        else:
            print("❌ 初始化取消")
            sys.exit(1)
    
    print("✅ 数据库连接成功")
    print()
    
    # 询问是否创建数据库
    create_db = ask_question("是否需要创建数据库？(y/n)", "y")
    if create_db.lower() == 'y':
        create_database(db_config)
    
    # 创建表结构
    print()
    print("正在创建数据表...")
    if not create_tables(db_config):
        print("❌ 表结构创建失败")
        sys.exit(1)
    
    # 保存配置
    print()
    config = {
        'database': db_config,
        'report': example_config.get('report', {}),
        '_meta': {
            'initialized': True,
            'version': '1.0',
            'created_at': datetime.now().isoformat()
        }
    }
    
    save_config(config)
    
    # 完成
    print()
    print("=" * 60)
    print("✅ 初始化完成！")
    print("=" * 60)
    print()
    print("现在可以运行以下命令：")
    print()
    print("  1. 抓取数据:")
    print("     openclaw exec --skill cnki-hotspot fetch")
    print()
    print("  2. 生成周报:")
    print("     openclaw exec --skill cnki-hotspot report --period week")
    print()
    print("  3. 生成月报:")
    print("     openclaw exec --skill cnki-hotspot report --period month")
    print()


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='CNKI 热点技能初始化')
    parser.add_argument('--force', action='store_true', help='强制重新初始化（覆盖现有配置）')
    
    args = parser.parse_args()
    
    # 检查是否已初始化
    config_path = os.path.join(script_dir, '../config/config.json')
    if os.path.exists(config_path) and not args.force:
        print("⚠️  检测到已有配置文件")
        print(f"   路径：{config_path}")
        print()
        overwrite = ask_question("是否覆盖现有配置？(y/n)", "n")
        if overwrite.lower() != 'y':
            print("✅ 初始化取消，使用现有配置")
            sys.exit(0)
    
    initialize()
