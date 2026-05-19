#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据可视化分析脚本

功能：
1. 数据统计描述性分析
2. 相关性分析
3. 特征分布可视化
4. 相关性热力图
5. 生成HTML格式的分析报告

使用方法：
python data_visualizer.py <input_file> --output <output_dir>

参数说明：
- input_file: 输入数据文件路径（支持 .csv, .xlsx, .xls）
- --output: 输出目录路径（默认为 ./output）
"""

import argparse
import os
import sys
import warnings
from pathlib import Path
from io import BytesIO
import base64
import subprocess

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
from jinja2 import Template

warnings.filterwarnings('ignore')


def setup_chinese_font():
    """
    智能检测并配置中文字体
    优先级：
    1. 系统已安装的中文字体（WenQuanYi、Noto Sans CJK等）
    2. DejaVu Sans（Linux默认）
    3. 其他备选字体
    """
    # 常见中文字体列表（按优先级排序）
    chinese_fonts = [
        'WenQuanYi Micro Hei',      # Linux常见开源中文字体
        'WenQuanYi Zen Hei',        # Linux常见开源中文字体
        'Noto Sans CJK SC',         # Google开源中文字体
        'Noto Sans CJK',            # Google开源中文字体
        'Source Han Sans CN',       # Adobe开源中文字体
        'Microsoft YaHei',          # Windows中文字体
        'SimHei',                    # Windows中文字体
        'PingFang SC',              # Mac中文字体
        'Hiragino Sans GB',         # Mac中文字体
        'STHeiti',                   # Mac中文字体
        'DejaVu Sans',              # Linux默认字体
    ]
    
    # 获取系统所有可用字体
    available_fonts = set([f.name for f in fm.fontManager.ttflist])
    
    # 查找第一个可用的中文字体
    selected_font = None
    for font in chinese_fonts:
        if font in available_fonts:
            selected_font = font
            print(f"检测到可用中文字体: {font}")
            break
    
    if selected_font:
        plt.rcParams['font.sans-serif'] = [selected_font, 'DejaVu Sans', 'sans-serif']
    else:
        # 如果没有找到中文字体，尝试使用系统默认的sans-serif
        print("警告: 未检测到中文字体，使用系统默认字体（中文可能显示为方块）")
        plt.rcParams['font.sans-serif'] = ['sans-serif', 'DejaVu Sans']
    
    # 解决负号显示问题
    plt.rcParams['axes.unicode_minus'] = False
    
    # 设置图形参数
    plt.rcParams['figure.figsize'] = (10, 6)
    plt.rcParams['figure.dpi'] = 100


# 初始化中文字体配置
setup_chinese_font()


class DataVisualizer:
    """数据可视化分析器"""
    
    def __init__(self, input_file, output_dir='./output'):
        """
        初始化分析器
        
        Args:
            input_file: 输入数据文件路径
            output_dir: 输出目录路径
        """
        self.input_file = Path(input_file)
        self.output_dir = Path(output_dir)
        self.df = None
        self.numeric_cols = []
        self.categorical_cols = []
        self.figures = {}
        
    def load_data(self):
        """加载数据文件"""
        if not self.input_file.exists():
            raise FileNotFoundError(f"数据文件不存在: {self.input_file}")
        
        suffix = self.input_file.suffix.lower()
        
        try:
            if suffix == '.csv':
                # 尝试不同编码
                for encoding in ['utf-8', 'gbk', 'gb2312', 'latin1']:
                    try:
                        self.df = pd.read_csv(self.input_file, encoding=encoding)
                        break
                    except UnicodeDecodeError:
                        continue
                if self.df is None:
                    raise ValueError("无法读取CSV文件，请检查文件编码")
                    
            elif suffix in ['.xlsx', '.xls']:
                self.df = pd.read_excel(self.input_file)
            else:
                raise ValueError(f"不支持的文件格式: {suffix}，仅支持 .csv, .xlsx, .xls")
                
            print(f"成功加载数据: {self.df.shape[0]} 行 × {self.df.shape[1]} 列")
            
        except Exception as e:
            raise ValueError(f"数据加载失败: {str(e)}")
        
        # 识别数值型和分类特征
        self.numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        print(f"数值型特征: {len(self.numeric_cols)} 个")
        print(f"分类特征: {len(self.categorical_cols)} 个")
        
    def create_output_dir(self):
        """创建输出目录"""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        figures_dir = self.output_dir / 'figures'
        figures_dir.mkdir(exist_ok=True)
        
    def descriptive_statistics(self):
        """描述性统计分析"""
        print("\n正在进行描述性统计分析...")
        
        stats = {}
        
        # 基础统计信息
        stats['shape'] = self.df.shape
        stats['dtypes'] = self.df.dtypes.value_counts().to_dict()
        stats['missing_values'] = self.df.isnull().sum().to_dict()
        stats['missing_ratio'] = (self.df.isnull().sum() / len(self.df) * 100).to_dict()
        
        # 数值型特征统计
        if self.numeric_cols:
            stats['numeric_stats'] = self.df[self.numeric_cols].describe().to_dict()
            
        # 分类特征统计
        if self.categorical_cols:
            stats['categorical_stats'] = {}
            for col in self.categorical_cols:
                stats['categorical_stats'][col] = {
                    'unique_count': self.df[col].nunique(),
                    'top_values': self.df[col].value_counts().head(10).to_dict()
                }
        
        return stats
    
    def correlation_analysis(self):
        """相关性分析"""
        print("\n正在进行相关性分析...")
        
        if len(self.numeric_cols) < 2:
            print("警告: 数值型特征少于2个，无法进行相关性分析")
            return None
        
        # 计算相关系数矩阵
        corr_matrix = self.df[self.numeric_cols].corr()
        
        return corr_matrix
    
    def plot_distribution(self):
        """绘制特征分布图"""
        print("\n正在生成特征分布图...")
        
        if not self.numeric_cols:
            print("警告: 没有数值型特征，无法生成分布图")
            return
        
        figures_data = []
        
        # 为每个数值型特征创建直方图和箱线图
        for i, col in enumerate(self.numeric_cols[:20]):  # 限制最多20个特征
            fig, axes = plt.subplots(1, 2, figsize=(14, 5))
            
            # 直方图
            axes[0].hist(self.df[col].dropna(), bins=30, color='steelblue', 
                        edgecolor='black', alpha=0.7)
            axes[0].set_title(f'{col} - 分布直方图', fontsize=12, fontweight='bold')
            axes[0].set_xlabel(col)
            axes[0].set_ylabel('频数')
            axes[0].grid(axis='y', alpha=0.3)
            
            # 箱线图
            axes[1].boxplot(self.df[col].dropna(), vert=True, patch_artist=True,
                           boxprops=dict(facecolor='lightblue', color='navy'),
                           medianprops=dict(color='red', linewidth=2),
                           whiskerprops=dict(color='navy'),
                           capprops=dict(color='navy'))
            axes[1].set_title(f'{col} - 箱线图', fontsize=12, fontweight='bold')
            axes[1].set_ylabel(col)
            axes[1].grid(axis='y', alpha=0.3)
            
            plt.tight_layout()
            
            # 转换为base64
            buffer = BytesIO()
            fig.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
            buffer.seek(0)
            img_base64 = base64.b64encode(buffer.getvalue()).decode()
            figures_data.append({
                'col': col,
                'img_base64': img_base64
            })
            
            plt.close(fig)
        
        self.figures['distribution'] = figures_data
        print(f"已生成 {len(figures_data)} 个特征的分布图")
    
    def plot_correlation_heatmap(self):
        """绘制相关性热力图"""
        print("\n正在生成相关性热力图...")
        
        if len(self.numeric_cols) < 2:
            print("警告: 数值型特征少于2个，无法生成热力图")
            return
        
        corr_matrix = self.df[self.numeric_cols].corr()
        
        # 调整图形大小
        n_cols = len(self.numeric_cols)
        fig_size = max(10, min(n_cols * 0.8, 20))
        
        fig, ax = plt.subplots(figsize=(fig_size, fig_size * 0.8))
        
        # 绘制热力图
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
        sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', 
                   cmap='coolwarm', center=0, square=True,
                   linewidths=0.5, cbar_kws={"shrink": 0.8},
                   vmin=-1, vmax=1, ax=ax)
        
        ax.set_title('特征相关性热力图', fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        # 转换为base64
        buffer = BytesIO()
        fig.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        self.figures['heatmap'] = img_base64
        
        plt.close(fig)
        print("相关性热力图生成完成")
    
    def plot_missing_values(self):
        """绘制缺失值可视化图"""
        print("\n正在生成缺失值可视化...")
        
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df) * 100).round(2)
        missing_df = pd.DataFrame({
            'Missing Count': missing,
            'Missing Percentage': missing_pct
        }).sort_values('Missing Count', ascending=False)
        
        missing_df = missing_df[missing_df['Missing Count'] > 0]
        
        if missing_df.empty:
            print("数据没有缺失值")
            return None
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x = range(len(missing_df))
        ax.bar(x, missing_df['Missing Percentage'], color='coral', alpha=0.8)
        ax.set_xticks(x)
        ax.set_xticklabels(missing_df.index, rotation=45, ha='right')
        ax.set_ylabel('缺失百分比 (%)', fontsize=11)
        ax.set_xlabel('特征名称', fontsize=11)
        ax.set_title('缺失值分布图', fontsize=13, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        # 添加数值标签
        for i, (idx, row) in enumerate(missing_df.iterrows()):
            ax.text(i, row['Missing Percentage'] + 0.5, 
                   f"{row['Missing Percentage']:.1f}%", 
                   ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        
        # 转换为base64
        buffer = BytesIO()
        fig.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        self.figures['missing'] = img_base64
        
        plt.close(fig)
        print("缺失值可视化完成")
    
    def generate_html_report(self, stats):
        """生成HTML分析报告"""
        print("\n正在生成HTML报告...")
        
        template_str = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>数据可视化分析报告</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Microsoft YaHei', 'SimHei', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .content {
            padding: 40px;
        }
        
        .section {
            margin-bottom: 50px;
        }
        
        .section-title {
            font-size: 1.8em;
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
        }
        
        .stat-card h3 {
            font-size: 1.1em;
            color: #667eea;
            margin-bottom: 10px;
        }
        
        .stat-card .value {
            font-size: 2em;
            font-weight: bold;
            color: #764ba2;
        }
        
        .table-container {
            overflow-x: auto;
            margin: 20px 0;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        th {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }
        
        td {
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }
        
        tr:hover {
            background-color: #f5f7fa;
        }
        
        .figure-container {
            margin: 30px 0;
            text-align: center;
        }
        
        .figure-container img {
            max-width: 100%;
            height: auto;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }
        
        .figure-container h3 {
            margin: 20px 0 15px;
            color: #667eea;
        }
        
        .distribution-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 30px;
            margin: 20px 0;
        }
        
        .distribution-item {
            background: #f9f9f9;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .distribution-item img {
            width: 100%;
            height: auto;
            border-radius: 8px;
        }
        
        .footer {
            background: #f5f7fa;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }
        
        .badge {
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            margin: 5px;
        }
        
        .badge-numeric {
            background: #e3f2fd;
            color: #1976d2;
        }
        
        .badge-categorical {
            background: #f3e5f5;
            color: #7b1fa2;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 数据可视化分析报告</h1>
            <p>基于您的数据生成的全面分析报告</p>
        </div>
        
        <div class="content">
            <!-- 数据概览 -->
            <div class="section">
                <h2 class="section-title">📈 数据概览</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <h3>数据行数</h3>
                        <div class="value">{{ stats.shape[0] }}</div>
                    </div>
                    <div class="stat-card">
                        <h3>特征数量</h3>
                        <div class="value">{{ stats.shape[1] }}</div>
                    </div>
                    <div class="stat-card">
                        <h3>数值型特征</h3>
                        <div class="value">{{ numeric_count }}</div>
                    </div>
                    <div class="stat-card">
                        <h3>分类特征</h3>
                        <div class="value">{{ categorical_count }}</div>
                    </div>
                </div>
                
                <div class="table-container">
                    <h3>特征类型分布</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>数据类型</th>
                                <th>数量</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for dtype, count in stats.dtypes.items() %}
                            <tr>
                                <td>{{ dtype }}</td>
                                <td>{{ count }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
            
            <!-- 缺失值分析 -->
            {% if figures.missing %}
            <div class="section">
                <h2 class="section-title">🔍 缺失值分析</h2>
                <div class="figure-container">
                    <img src="data:image/png;base64,{{ figures.missing }}" alt="缺失值分布图">
                </div>
                
                <div class="table-container">
                    <h3>缺失值统计</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>特征名称</th>
                                <th>缺失数量</th>
                                <th>缺失比例 (%)</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for col, count in stats.missing_values.items() %}
                            {% if count > 0 %}
                            <tr>
                                <td>{{ col }}</td>
                                <td>{{ count }}</td>
                                <td>{{ stats.missing_ratio[col] | round(2) }}%</td>
                            </tr>
                            {% endif %}
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
            {% endif %}
            
            <!-- 描述性统计 -->
            {% if stats.numeric_stats %}
            <div class="section">
                <h2 class="section-title">📊 描述性统计分析</h2>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>统计指标</th>
                                {% for col in stats.numeric_stats.keys() %}
                                <th>{{ col }}</th>
                                {% endfor %}
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>计数</strong></td>
                                {% for col in stats.numeric_stats.keys() %}
                                <td>{{ stats.numeric_stats[col].count | round(2) }}</td>
                                {% endfor %}
                            </tr>
                            <tr>
                                <td><strong>均值</strong></td>
                                {% for col in stats.numeric_stats.keys() %}
                                <td>{{ stats.numeric_stats[col].mean | round(2) }}</td>
                                {% endfor %}
                            </tr>
                            <tr>
                                <td><strong>标准差</strong></td>
                                {% for col in stats.numeric_stats.keys() %}
                                <td>{{ stats.numeric_stats[col].std | round(2) }}</td>
                                {% endfor %}
                            </tr>
                            <tr>
                                <td><strong>最小值</strong></td>
                                {% for col in stats.numeric_stats.keys() %}
                                <td>{{ stats.numeric_stats[col].min | round(2) }}</td>
                                {% endfor %}
                            </tr>
                            <tr>
                                <td><strong>25%分位</strong></td>
                                {% for col in stats.numeric_stats.keys() %}
                                <td>{{ stats.numeric_stats[col]['25%'] | round(2) }}</td>
                                {% endfor %}
                            </tr>
                            <tr>
                                <td><strong>中位数</strong></td>
                                {% for col in stats.numeric_stats.keys() %}
                                <td>{{ stats.numeric_stats[col]['50%'] | round(2) }}</td>
                                {% endfor %}
                            </tr>
                            <tr>
                                <td><strong>75%分位</strong></td>
                                {% for col in stats.numeric_stats.keys() %}
                                <td>{{ stats.numeric_stats[col]['75%'] | round(2) }}</td>
                                {% endfor %}
                            </tr>
                            <tr>
                                <td><strong>最大值</strong></td>
                                {% for col in stats.numeric_stats.keys() %}
                                <td>{{ stats.numeric_stats[col].max | round(2) }}</td>
                                {% endfor %}
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            {% endif %}
            
            <!-- 特征分布可视化 -->
            {% if figures.distribution %}
            <div class="section">
                <h2 class="section-title">📈 特征分布可视化</h2>
                <p>以下图表展示了每个数值型特征的分布情况（直方图和箱线图）：</p>
                <div class="distribution-grid">
                    {% for fig in figures.distribution %}
                    <div class="distribution-item">
                        <h3>{{ fig.col }}</h3>
                        <img src="data:image/png;base64,{{ fig.img_base64 }}" alt="{{ fig.col }}分布图">
                    </div>
                    {% endfor %}
                </div>
            </div>
            {% endif %}
            
            <!-- 相关性分析 -->
            {% if figures.heatmap %}
            <div class="section">
                <h2 class="section-title">🔥 相关性分析热力图</h2>
                <div class="figure-container">
                    <img src="data:image/png;base64,{{ figures.heatmap }}" alt="相关性热力图">
                </div>
                <p style="margin-top: 20px; color: #666;">
                    <strong>说明：</strong>颜色越深表示相关性越强。红色表示正相关，蓝色表示负相关。数值范围：-1（完全负相关）到 +1（完全正相关）。
                </p>
            </div>
            {% endif %}
            
            <!-- 分类特征统计 -->
            {% if stats.categorical_stats %}
            <div class="section">
                <h2 class="section-title">📋 分类特征统计</h2>
                {% for col, col_stats in stats.categorical_stats.items() %}
                <div class="table-container">
                    <h3>{{ col }} - 取值分布（Top 10）</h3>
                    <p>唯一值数量: {{ col_stats.unique_count }}</p>
                    <table>
                        <thead>
                            <tr>
                                <th>取值</th>
                                <th>数量</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for value, count in col_stats.top_values.items() %}
                            <tr>
                                <td>{{ value }}</td>
                                <td>{{ count }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                {% endfor %}
            </div>
            {% endif %}
        </div>
        
        <div class="footer">
            <p>📊 数据可视化分析报告 | 由 data-viz-analyzer 生成</p>
            <p>报告生成时间: {{ generation_time }}</p>
        </div>
    </div>
</body>
</html>
"""
        
        template = Template(template_str)
        
        html_content = template.render(
            stats=stats,
            numeric_count=len(self.numeric_cols),
            categorical_count=len(self.categorical_cols),
            figures=self.figures,
            generation_time=pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        # 保存HTML报告
        report_path = self.output_dir / 'data_analysis_report.html'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✓ HTML报告已生成: {report_path}")
        
    def run(self):
        """执行完整的分析流程"""
        print("="*60)
        print("开始数据可视化分析...")
        print("="*60)
        
        # 1. 加载数据
        self.load_data()
        
        # 2. 创建输出目录
        self.create_output_dir()
        
        # 3. 描述性统计
        stats = self.descriptive_statistics()
        
        # 4. 相关性分析
        correlation = self.correlation_analysis()
        
        # 5. 生成可视化图表
        self.plot_missing_values()
        self.plot_distribution()
        self.plot_correlation_heatmap()
        
        # 6. 生成HTML报告
        self.generate_html_report(stats)
        
        print("\n" + "="*60)
        print("✓ 数据分析完成！")
        print(f"✓ 报告位置: {self.output_dir / 'data_analysis_report.html'}")
        print("="*60)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='数据可视化分析工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python data_visualizer.py data.csv --output ./results
  python data_visualizer.py data.xlsx --output ./analysis
        """
    )
    
    parser.add_argument('input_file', help='输入数据文件路径（支持 .csv, .xlsx, .xls）')
    parser.add_argument('--output', '-o', default='./output', 
                       help='输出目录路径（默认: ./output）')
    
    args = parser.parse_args()
    
    # 执行分析
    visualizer = DataVisualizer(args.input_file, args.output)
    visualizer.run()


if __name__ == '__main__':
    main()
