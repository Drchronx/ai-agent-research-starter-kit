#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据分析可视化脚本

功能：
1. 读取CSV/Excel数据文件
2. 生成描述性统计报告
3. 计算特征相关性
4. 生成分布可视化图表
5. 生成相关性热力图
6. 生成HTML分析报告
"""

import argparse
import os
import sys
import base64
from pathlib import Path
from io import BytesIO
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # 非交互式后端
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager
import matplotlib

# 配置中文字体支持
plt.rcParams['axes.unicode_minus'] = False

def setup_chinese_font():
    """设置中文字体，优先使用系统中可用的中文支持字体"""
    # 尝试多个字体列表，按优先级排序
    font_lists = [
        # Linux 中文字体
        ['WenQuanYi Zen Hei', 'WenQuanYi Micro Hei', 'Noto Sans CJK SC', 'Droid Sans Fallback'],
        # macOS 字体
        ['PingFang SC', 'Hiragino Sans GB', 'STHeiti'],
        # Windows 字体
        ['Microsoft YaHei', 'SimHei', 'SimSun'],
        # 通用
        ['sans-serif']
    ]
    
    available_fonts = {f.name for f in font_manager.fontManager.ttflist}
    
    for font_list in font_lists:
        for font_name in font_list:
            if font_name in available_fonts:
                plt.rcParams['font.sans-serif'] = [font_name]
                print(f"✓ 已设置中文字体: {font_name}")
                return font_name
    
    # 如果没有找到合适字体，使用 fallback
    plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei']
    print("⚠ 未找到专用中文字体，使用默认字体（可能部分中文无法显示）")
    return None

# 初始化字体设置
setup_chinese_font()


def load_data(file_path):
    """加载CSV或Excel数据"""
    file_ext = Path(file_path).suffix.lower()
    
    if file_ext == '.csv':
        # 尝试多种编码
        encodings = ['utf-8', 'gbk', 'gb2312', 'utf-8-sig']
        for encoding in encodings:
            try:
                df = pd.read_csv(file_path, encoding=encoding)
                print(f"✓ 成功读取CSV文件，编码: {encoding}")
                return df
            except UnicodeDecodeError:
                # 编码不匹配，继续尝试下一个
                print(f"  编码 {encoding} 不匹配，继续尝试...")
                continue
            except FileNotFoundError:
                raise FileNotFoundError(f"文件不存在: {file_path}")
            except pd.errors.EmptyDataError:
                raise ValueError(f"文件为空: {file_path}")
            except pd.errors.ParserError as e:
                raise ValueError(f"CSV格式错误: {e}")
        raise ValueError(f"无法识别文件编码，请手动转换文件为UTF-8格式")
    
    elif file_ext in ['.xlsx', '.xls']:
        df = pd.read_excel(file_path)
        print(f"成功读取Excel文件: {file_path}")
        return df
    
    else:
        raise ValueError(f"不支持的文件格式: {file_ext}，仅支持 .csv, .xlsx, .xls")


def fig_to_base64(fig):
    """将matplotlib图表转换为base64编码"""
    buffer = BytesIO()
    fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close(fig)
    return img_base64


def generate_statistics(df):
    """生成描述性统计报告"""
    print("\n=== 生成描述性统计报告 ===")
    
    # 数值型特征统计
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) == 0:
        print("警告：数据中没有数值型特征")
        return None, numeric_cols
    
    stats_df = df[numeric_cols].describe().T
    
    # 添加额外统计量
    stats_df['median'] = df[numeric_cols].median()
    stats_df['variance'] = df[numeric_cols].var()
    stats_df['skewness'] = df[numeric_cols].skew()
    stats_df['kurtosis'] = df[numeric_cols].kurtosis()
    stats_df['missing_count'] = df[numeric_cols].isnull().sum()
    stats_df['missing_ratio'] = (df[numeric_cols].isnull().sum() / len(df) * 100).round(2)
    
    print(f"已计算 {len(stats_df)} 个数值型特征的统计指标")
    
    return stats_df, numeric_cols


def generate_correlation_matrix(df):
    """生成相关性矩阵"""
    print("\n=== 计算相关性矩阵 ===")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) < 2:
        print("警告：数值型特征少于2个，无法计算相关性")
        return None
    
    # 计算相关系数矩阵
    corr_matrix = df[numeric_cols].corr()
    print(f"已计算 {len(corr_matrix)} 个特征的相关性矩阵")
    
    return corr_matrix


def generate_distribution_plot(df, col):
    """为单个特征生成分布图"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    data = df[col].dropna()
    
    # 直方图
    axes[0].hist(data, bins=30, color='steelblue', edgecolor='black', alpha=0.7)
    axes[0].set_xlabel(col, fontsize=12)
    axes[0].set_ylabel('频数 (Frequency)', fontsize=12)
    axes[0].set_title(f'{col} 的分布 (Distribution)', fontsize=14, fontweight='bold')
    axes[0].grid(True, alpha=0.3)
    
    # 箱线图
    box_data = axes[1].boxplot(data, patch_artist=True)
    box_data['boxes'][0].set_facecolor('lightblue')
    axes[1].set_ylabel(col, fontsize=12)
    axes[1].set_title(f'{col} 的箱线图 (Boxplot)', fontsize=14, fontweight='bold')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    return fig


def generate_correlation_heatmap(corr_matrix):
    """生成相关性热力图"""
    if corr_matrix is None or corr_matrix.empty:
        return None
    
    # 图表大小根据特征数量动态调整
    n_features = len(corr_matrix)
    fig_size = max(10, n_features * 0.8)
    
    fig, ax = plt.subplots(figsize=(fig_size, fig_size))
    
    # 绘制热力图
    sns.heatmap(corr_matrix, 
                annot=True, 
                fmt='.2f', 
                cmap='RdBu_r',
                center=0,
                square=True,
                linewidths=0.5,
                cbar_kws={'shrink': 0.8},
                ax=ax)
    
    ax.set_title('特征相关性热力图 (Feature Correlation Heatmap)', 
                 fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    
    return fig


def generate_scatter_plot(df, col, target_column):
    """生成散点图"""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # 大数据集采样
    sample_size = min(len(df), 5000)
    sample_df = df.sample(n=sample_size, random_state=42) if len(df) > sample_size else df
    
    ax.scatter(sample_df[col], sample_df[target_column], 
              alpha=0.5, s=20, color='steelblue', edgecolors='black', linewidth=0.3)
    ax.set_xlabel(col, fontsize=12)
    ax.set_ylabel(target_column, fontsize=12)
    ax.set_title(f'{col} vs {target_column}', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    return fig


def generate_html_report(df, stats_df, corr_matrix, numeric_cols, output_dir, target_column=None):
    """生成HTML分析报告"""
    print("\n=== 生成HTML分析报告 ===")
    
    # 收集强相关特征对
    strong_corr_pairs = []
    if corr_matrix is not None and len(corr_matrix) > 0:
        threshold = 0.7
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) >= threshold:
                    col1 = corr_matrix.columns[i]
                    col2 = corr_matrix.columns[j]
                    strong_corr_pairs.append((col1, col2, corr_value))
        strong_corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)
    
    # 收集缺失值信息
    missing_stats = df.isnull().sum()
    missing_cols = missing_stats[missing_stats > 0]
    
    # 生成HTML内容
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>数据分析报告</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Microsoft YaHei', '微软雅黑', 'SimHei', '黑体', 
                         'Noto Sans SC', 'PingFang SC', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 36px;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .header p {{
            font-size: 16px;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 50px;
        }}
        
        .section-title {{
            font-size: 28px;
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
            font-weight: 700;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        }}
        
        .stat-card h3 {{
            font-size: 14px;
            color: #666;
            margin-bottom: 8px;
            text-transform: uppercase;
        }}
        
        .stat-card .value {{
            font-size: 32px;
            font-weight: 700;
            color: #667eea;
        }}
        
        .info-box {{
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 15px 20px;
            margin: 20px 0;
            border-radius: 4px;
        }}
        
        .info-box.warning {{
            border-left-color: #ffc107;
            background: #fff3cd;
        }}
        
        .info-box.success {{
            border-left-color: #28a745;
            background: #d4edda;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            border-radius: 8px;
            overflow: hidden;
        }}
        
        th {{
            background: #667eea;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            font-size: 14px;
        }}
        
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #e9ecef;
        }}
        
        tr:hover {{
            background: #f8f9fa;
        }}
        
        .chart-container {{
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin: 30px 0;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        }}
        
        .chart-title {{
            font-size: 20px;
            color: #333;
            margin-bottom: 15px;
            font-weight: 600;
        }}
        
        .chart-image {{
            width: 100%;
            height: auto;
            border-radius: 4px;
        }}
        
        .distribution-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
            gap: 30px;
        }}
        
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            margin: 0 5px;
        }}
        
        .badge.strong {{
            background: #dc3545;
            color: white;
        }}
        
        .badge.moderate {{
            background: #ffc107;
            color: #333;
        }}
        
        .badge.weak {{
            background: #28a745;
            color: white;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 14px;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 28px;
            }}
            
            .content {{
                padding: 20px;
            }}
            
            .distribution-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 数据分析报告</h1>
            <p>全面的数据统计与可视化分析</p>
        </div>
        
        <div class="content">
            <!-- 数据概览 -->
            <div class="section">
                <h2 class="section-title">📈 数据概览</h2>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <h3>数据维度</h3>
                        <div class="value">{df.shape[0]} × {df.shape[1]}</div>
                        <p style="color: #666; margin-top: 5px;">行数 × 列数</p>
                    </div>
                    <div class="stat-card">
                        <h3>数值型特征</h3>
                        <div class="value">{len(numeric_cols)}</div>
                        <p style="color: #666; margin-top: 5px;">个特征</p>
                    </div>
                    <div class="stat-card">
                        <h3>非数值型特征</h3>
                        <div class="value">{len(df.select_dtypes(exclude=[np.number]).columns)}</div>
                        <p style="color: #666; margin-top: 5px;">个特征</p>
                    </div>
                    <div class="stat-card">
                        <h3>缺失值总数</h3>
                        <div class="value">{missing_stats.sum()}</div>
                        <p style="color: #666; margin-top: 5px;">个缺失值</p>
                    </div>
                </div>
"""
    
    # 添加缺失值信息
    if len(missing_cols) > 0:
        html_content += """
                <div class="info-box warning">
                    <strong>⚠️ 缺失值提醒：</strong><br>
"""
        for col, count in missing_cols.items():
            ratio = count / len(df) * 100
            html_content += f"                    • {col}: {count} 个缺失 ({ratio:.2f}%)<br>\n"
        html_content += """                </div>
"""
    else:
        html_content += """
                <div class="info-box success">
                    <strong>✓ 数据完整：</strong> 无缺失值
                </div>
"""
    
    html_content += """
            </div>
            
            <!-- 描述性统计 -->
            <div class="section">
                <h2 class="section-title">📋 描述性统计</h2>
                <div class="info-box">
                    <strong>说明：</strong>以下表格展示了每个数值型特征的统计指标，包括均值、标准差、最小值、最大值、中位数、偏度和峰度等。
                </div>
"""
    
    if stats_df is not None:
        html_content += """
                <table>
                    <thead>
                        <tr>
                            <th>特征名称</th>
                            <th>计数</th>
                            <th>均值</th>
                            <th>标准差</th>
                            <th>最小值</th>
                            <th>中位数</th>
                            <th>最大值</th>
                            <th>偏度</th>
                            <th>峰度</th>
                            <th>缺失率(%)</th>
                        </tr>
                    </thead>
                    <tbody>
"""
        for idx, row in stats_df.iterrows():
            html_content += f"""
                        <tr>
                            <td><strong>{idx}</strong></td>
                            <td>{int(row['count'])}</td>
                            <td>{row['mean']:.2f}</td>
                            <td>{row['std']:.2f}</td>
                            <td>{row['min']:.2f}</td>
                            <td>{row['median']:.2f}</td>
                            <td>{row['max']:.2f}</td>
                            <td>{row['skewness']:.2f}</td>
                            <td>{row['kurtosis']:.2f}</td>
                            <td>{row['missing_ratio']:.2f}</td>
                        </tr>
"""
        html_content += """
                    </tbody>
                </table>
"""
    
    html_content += """
            </div>
            
            <!-- 相关性分析 -->
            <div class="section">
                <h2 class="section-title">🔗 相关性分析</h2>
"""
    
    # 生成相关性热力图
    if corr_matrix is not None and len(corr_matrix) > 0:
        heatmap_fig = generate_correlation_heatmap(corr_matrix)
        heatmap_base64 = fig_to_base64(heatmap_fig)
        
        html_content += f"""
                <div class="chart-container">
                    <div class="chart-title">相关性热力图</div>
                    <img src="data:image/png;base64,{heatmap_base64}" class="chart-image" alt="相关性热力图">
                </div>
"""
        
        # 显示强相关特征对
        if strong_corr_pairs:
            html_content += """
                <div class="info-box">
                    <strong>🔍 强相关特征对 (|r| ≥ 0.7)：</strong><br>
"""
            for col1, col2, corr_val in strong_corr_pairs[:10]:  # 只显示前10对
                strength = "strong" if abs(corr_val) >= 0.9 else "moderate" if abs(corr_val) >= 0.8 else "strong"
                html_content += f"                    • {col1} ↔ {col2}: r = <span class='badge {strength}'>{corr_val:.3f}</span><br>\n"
            html_content += """                </div>
"""
    
    html_content += """
            </div>
            
            <!-- 特征分布 -->
            <div class="section">
                <h2 class="section-title">📊 特征分布</h2>
                <div class="info-box">
                    <strong>说明：</strong>以下图表展示了每个数值型特征的分布情况。左侧为直方图，右侧为箱线图。
                </div>
                
                <div class="distribution-grid">
"""
    
    # 生成每个特征的分布图
    for col in numeric_cols:
        dist_fig = generate_distribution_plot(df, col)
        dist_base64 = fig_to_base64(dist_fig)
        
        html_content += f"""
                    <div class="chart-container">
                        <div class="chart-title">{col}</div>
                        <img src="data:image/png;base64,{dist_base64}" class="chart-image" alt="{col}分布图">
                    </div>
"""
    
    html_content += """
                </div>
            </div>
"""
    
    # 如果指定了目标变量，生成散点图
    if target_column and target_column in df.columns and pd.api.types.is_numeric_dtype(df[target_column]):
        html_content += f"""
            <!-- 目标变量相关性 -->
            <div class="section">
                <h2 class="section-title">🎯 目标变量分析: {target_column}</h2>
                <div class="info-box">
                    <strong>说明：</strong>以下散点图展示了目标变量与其他特征的关系。
                </div>
                
                <div class="distribution-grid">
"""
        
        other_numeric_cols = [col for col in numeric_cols if col != target_column][:10]
        for col in other_numeric_cols:
            scatter_fig = generate_scatter_plot(df, col, target_column)
            scatter_base64 = fig_to_base64(scatter_fig)
            
            html_content += f"""
                    <div class="chart-container">
                        <div class="chart-title">{col} vs {target_column}</div>
                        <img src="data:image/png;base64,{scatter_base64}" class="chart-image" alt="{col} vs {target_column}">
                    </div>
"""
        
        html_content += """
                </div>
            </div>
"""
    
    html_content += """
        </div>
        
        <div class="footer">
            <p>数据分析报告 | 由 Data Visualization Analysis Skill 生成</p>
        </div>
    </div>
</body>
</html>
"""
    
    # 保存HTML文件
    html_path = os.path.join(output_dir, 'analysis_report.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML报告已保存: {html_path}")
    return html_path


def main():
    parser = argparse.ArgumentParser(description='数据分析可视化工具')
    parser.add_argument('--input_file', required=True, help='输入数据文件路径 (CSV/Excel)')
    parser.add_argument('--output_dir', default='./analysis_output', help='输出目录路径')
    parser.add_argument('--target_column', default=None, help='目标变量列名（可选）')
    
    args = parser.parse_args()
    
    # 验证输入文件
    if not os.path.exists(args.input_file):
        print(f"错误：输入文件不存在: {args.input_file}")
        sys.exit(1)
    
    # 创建输出目录
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 配置中文字体
    setup_chinese_font()
    
    print("\n" + "=" * 60)
    print("数据分析可视化工具")
    print("=" * 60)
    print(f"输入文件: {args.input_file}")
    print(f"输出目录: {args.output_dir}")
    
    # 加载数据
    print("\n>>> 加载数据...")
    df = load_data(args.input_file)
    print(f"数据加载成功: {df.shape[0]} 行 × {df.shape[1]} 列")
    
    # 执行分析
    stats_df, numeric_cols = generate_statistics(df)
    corr_matrix = generate_correlation_matrix(df)
    
    # 生成HTML报告
    html_path = generate_html_report(df, stats_df, corr_matrix, numeric_cols, 
                                     args.output_dir, args.target_column)
    
    print("\n" + "=" * 60)
    print("✓ 分析完成！")
    print("=" * 60)
    print(f"\n请打开HTML报告查看分析结果: {html_path}")


if __name__ == '__main__':
    main()
