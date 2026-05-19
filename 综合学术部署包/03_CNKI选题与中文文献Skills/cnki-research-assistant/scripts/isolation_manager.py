#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务隔离管理器
确保不同选题的分析数据完全隔离，避免数据污染
"""

import os
import shutil
import hashlib
from datetime import datetime
from typing import Optional, List
from pathlib import Path


class IsolationManager:
    """任务隔离管理器"""
    
    def __init__(self, skill_root: str):
        self.skill_root = skill_root
        self.reports_dir = os.path.join(skill_root, 'reports')
        self.data_dir = os.path.join(skill_root, 'data')
        self.temp_dir = os.path.join(skill_root, 'temp')
    
    def get_keyword_hash(self, keyword: str) -> str:
        """生成关键词的唯一哈希"""
        return hashlib.md5(keyword.encode('utf-8')).hexdigest()[:8]
    
    def get_keyword_dir(self, keyword: str) -> str:
        """获取关键词的专属目录"""
        keyword_hash = self.get_keyword_hash(keyword)
        keyword_dir = os.path.join(self.reports_dir, keyword_hash)
        return keyword_dir
    
    def prepare_run(self, keyword: str) -> str:
        """
        准备运行环境
        
        Args:
            keyword: 选题关键词
        
        Returns:
            专属输出目录路径
        """
        # 创建关键词专属目录
        keyword_dir = self.get_keyword_dir(keyword)
        os.makedirs(keyword_dir, exist_ok=True)
        os.makedirs(os.path.join(keyword_dir, 'charts'), exist_ok=True)
        
        # 清理旧的临时文件（超过 7 天）
        self._cleanup_old_runs(keyword_dir, days=7)
        
        return keyword_dir
    
    def _cleanup_old_runs(self, keyword_dir: str, days: int = 7):
        """清理旧的运行结果"""
        if not os.path.exists(keyword_dir):
            return
        
        cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)
        
        for filename in os.listdir(keyword_dir):
            if filename == '.gitkeep':
                continue
            
            file_path = os.path.join(keyword_dir, filename)
            try:
                file_mtime = os.path.getmtime(file_path)
                if file_mtime < cutoff_time:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
            except Exception as e:
                print(f"  ⚠️ 清理文件失败 {filename}: {e}")
    
    def get_output_path(self, keyword: str, filename: str) -> str:
        """
        获取输出文件路径
        
        Args:
            keyword: 选题关键词
            filename: 文件名
        
        Returns:
            完整文件路径
        """
        keyword_dir = self.get_keyword_dir(keyword)
        return os.path.join(keyword_dir, filename)
    
    def move_results_to_keyword_dir(self, keyword: str, source_files: List[str]):
        """
        将结果文件移动到关键词专属目录
        
        Args:
            keyword: 选题关键词
            source_files: 源文件路径列表
        """
        keyword_dir = self.get_keyword_dir(keyword)
        
        for source_path in source_files:
            if not os.path.exists(source_path):
                continue
            
            filename = os.path.basename(source_path)
            target_path = os.path.join(keyword_dir, filename)
            
            try:
                shutil.move(source_path, target_path)
                print(f"  ✅ 已移动：{filename}")
            except Exception as e:
                print(f"  ⚠️ 移动文件失败 {filename}: {e}")
    
    def list_keyword_runs(self, keyword: str) -> List[str]:
        """列出关键词的所有历史运行结果"""
        keyword_dir = self.get_keyword_dir(keyword)
        
        if not os.path.exists(keyword_dir):
            return []
        
        files = []
        for filename in sorted(os.listdir(keyword_dir)):
            if filename.startswith('.'):
                continue
            files.append(os.path.join(keyword_dir, filename))
        
        return files
    
    def get_latest_run(self, keyword: str) -> Optional[str]:
        """获取最近一次运行结果"""
        files = self.list_keyword_runs(keyword)
        
        if not files:
            return None
        
        # 返回最新的报告文件
        for f in reversed(files):
            if f.endswith('.md'):
                return f
        
        return None
    
    def cleanup_all_temp(self, days: int = 1):
        """清理所有临时文件"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        os.makedirs(self.temp_dir, exist_ok=True)
        print(f"✅ 临时目录已清理：{self.temp_dir}")
    
    def export_report(self, keyword: str, output_path: str) -> Optional[str]:
        """
        导出报告到用户指定路径
        
        Args:
            keyword: 选题关键词
            output_path: 用户指定的输出路径
        
        Returns:
            实际保存路径
        """
        latest = self.get_latest_run(keyword)
        if not latest:
            return None
        
        # 如果用户指定了路径，复制过去
        if output_path:
            output_dir = os.path.dirname(os.path.abspath(output_path))
            os.makedirs(output_dir, exist_ok=True)
            shutil.copy2(latest, output_path)
            return output_path
        
        return latest
    
    def generate_isolation_report(self, keyword: str) -> str:
        """生成隔离状态报告"""
        keyword_dir = self.get_keyword_dir(keyword)
        
        report = f"## 任务隔离状态：{keyword}\n\n"
        report += f"**专属目录**: `{keyword_dir}`\n\n"
        
        if os.path.exists(keyword_dir):
            files = self.list_keyword_runs(keyword)
            report += f"**历史运行**: {len(files)} 个文件\n\n"
            
            if files:
                report += "### 文件列表\n\n"
                for f in files:
                    size = os.path.getsize(f) / 1024
                    mtime = datetime.fromtimestamp(os.path.getmtime(f)).strftime('%Y-%m-%d %H:%M')
                    report += f"- `{os.path.basename(f)}` ({size:.1f} KB, {mtime})\n"
        else:
            report += "**历史运行**: 无\n\n"
        
        return report


def test_isolation():
    """测试隔离管理器"""
    manager = IsolationManager('/root/.openclaw/workspace-hotspot/skills/cnki-research-assistant')
    
    # 测试关键词哈希
    print("关键词哈希测试:")
    for kw in ["新质生产力", "耐心资本", "数字经济"]:
        print(f"  {kw}: {manager.get_keyword_hash(kw)}")
    
    # 测试目录生成
    print("\n专属目录测试:")
    for kw in ["新质生产力", "耐心资本"]:
        dir_path = manager.get_keyword_dir(kw)
        print(f"  {kw}: {dir_path}")
    
    # 生成隔离报告
    print("\n隔离状态报告:")
    print(manager.generate_isolation_report("新质生产力"))


if __name__ == '__main__':
    test_isolation()
