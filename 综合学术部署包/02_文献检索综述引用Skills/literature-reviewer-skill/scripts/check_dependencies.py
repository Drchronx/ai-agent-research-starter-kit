#!/usr/bin/env python3
"""
依赖检查脚本

检查项目：
1. 外部技能依赖（cnki-crawler, academic-research, academic-research-hub）
2. 数据库依赖（PostgreSQL + cnki_db）
3. Python 依赖（psycopg2, requests 等）
4. 配置文件（.env）

用法:
    python scripts/check_dependencies.py
"""

import sys
import os
from pathlib import Path

class DependencyChecker:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.passed = []
        
    def check_skill_dependencies(self):
        """检查外部技能依赖"""
        skill_deps = [
            ('../cnki-crawler', 'CNKI 爬虫技能'),
            ('../academic-research', 'OpenAlex 检索技能'),
            ('../academic-research-hub', 'Google Scholar 检索技能'),
        ]
        
        base_dir = Path(__file__).parent.parent
        
        for dep_path, dep_name in skill_deps:
            dep_full_path = (base_dir / dep_path).resolve()
            if dep_full_path.exists():
                self.passed.append(f"✅ {dep_name}: {dep_path}")
            else:
                self.errors.append(f"❌ {dep_name} 缺失：{dep_path}")
    
    def check_database(self):
        """检查数据库依赖"""
        try:
            import psycopg2
            self.passed.append("✅ psycopg2 已安装")
            
            # 尝试连接数据库
            dsn = os.getenv('CNKI_DB_DSN', 'postgresql://cnki_user:123456@localhost/cnki_db')
            conn = psycopg2.connect(dsn)
            conn.close()
            self.passed.append(f"✅ 数据库连接成功")
            
        except ImportError:
            self.errors.append("❌ psycopg2 未安装：pip install psycopg2-binary")
        except Exception as e:
            self.errors.append(f"❌ 数据库连接失败：{e}")
    
    def check_python_dependencies(self):
        """检查 Python 依赖"""
        python_deps = [
            ('requests', 'HTTP 请求库'),
            ('lxml', 'XML/HTML 解析库'),
            ('loguru', '日志库'),
        ]
        
        for dep_name, dep_desc in python_deps:
            try:
                __import__(dep_name)
                self.passed.append(f"✅ {dep_desc}: {dep_name}")
            except ImportError:
                self.errors.append(f"❌ {dep_desc} 缺失：pip install {dep_name}")
    
    def check_env_file(self):
        """检查配置文件"""
        env_path = Path(__file__).parent.parent / '.env'
        if env_path.exists():
            self.passed.append(f"✅ 配置文件存在")
        else:
            self.warnings.append(f"⚠️ 配置文件缺失（可从 .env.example 复制）")
    
    def run(self):
        """运行所有检查"""
        print("=" * 60)
        print("文献综述技能 - 依赖检查")
        print("=" * 60)
        print()
        
        self.check_skill_dependencies()
        self.check_python_dependencies()
        self.check_database()
        self.check_env_file()
        
        # 输出结果
        if self.passed:
            print("✅ 通过检查:")
            for item in self.passed:
                print(f"  {item}")
            print()
        
        if self.warnings:
            print("⚠️ 警告:")
            for item in self.warnings:
                print(f"  {item}")
            print()
        
        if self.errors:
            print("❌ 错误:")
            for item in self.errors:
                print(f"  {item}")
            print()
            print("=" * 60)
            print("❌ 依赖检查未通过，请先解决上述问题！")
            print("=" * 60)
            return False
        else:
            print("=" * 60)
            print("✅ 所有依赖检查通过！可以开始使用文献综述技能。")
            print("=" * 60)
            return True


if __name__ == '__main__':
    checker = DependencyChecker()
    success = checker.run()
    sys.exit(0 if success else 1)
