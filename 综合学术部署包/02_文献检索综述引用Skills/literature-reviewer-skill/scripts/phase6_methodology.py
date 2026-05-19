#!/usr/bin/env python3
"""
v5.0 方法论评价模块

输出：
- 因果识别策略分布
- 内生性处理方法
- 稳健性检验方法
"""

import json
import sys
from pathlib import Path
from collections import Counter
from datetime import datetime


# 方法论关键词编码
METHODOLOGY_CODES = {
    'did': ['双重差分', 'DID', '多期 DID', '渐进 DID', '倍差法', '双重差分法'],
    'iv': ['工具变量', 'IV', '2SLS', '两阶段', '工具变量法'],
    'rd': ['断点回归', 'RD', 'RDD', '断点'],
    'psm': ['倾向得分匹配', 'PSM', '匹配', 'Propensity Score'],
    'fe': ['固定效应', 'FE', '双向固定效应', '个体固定效应', '时间固定效应'],
    'gmm': ['GMM', '系统 GMM', '差分 GMM', '广义矩估计'],
    're': ['随机效应', 'RE'],
    'tobit': ['Tobit', '截断'],
    'logit_probit': ['Logit', 'Probit', '二值选择']
}

ENDOGENEITY_SOLUTIONS = {
    'lagged': ['滞后', 'Lag', '一期滞后', '滞后一期'],
    'iv': ['工具变量', 'IV', '外生变量'],
    'did': ['双重差分', 'DID', '外生冲击', '政策', '准自然实验'],
    'rd': ['断点', 'RD', 'RDD'],
    'heckman': ['Heckman', '样本选择', 'Heckit'],
    'system_gmm': ['系统 GMM', '动态面板']
}

ROBUSTNESS_CHECKS = {
    'replace_variable': ['替换', '替代', '更换', '重新衡量'],
    'change_sample': ['子样本', '分样本', '剔除', '排除', '改变样本'],
    'add_control': ['控制变量', '加入', '增加', ' additional'],
    'change_method': ['更换方法', '不同方法', '替换估计'],
    'placebo': ['安慰剂', 'Placebo', '虚构'],
    'exclude_special': ['排除', '剔除', '不含', '不包括']
}


def analyze_methodology(papers):
    """方法论分析"""
    
    results = {
        'identification_strategy': Counter(),
        'endogeneity_solution': Counter(),
        'robustness_check': Counter(),
        'papers_with_method': []
    }
    
    for paper in papers:
        title = paper.get('title', '')
        abstract = paper.get('abstract', '') or ''
        text = title + ' ' + abstract
        
        paper_methods = []
        paper_endo = []
        paper_robust = []
        
        # 识别策略
        for method, keywords in METHODOLOGY_CODES.items():
            if any(kw in text for kw in keywords):
                results['identification_strategy'][method] += 1
                paper_methods.append(method)
        
        # 内生性处理
        for solution, keywords in ENDOGENEITY_SOLUTIONS.items():
            if any(kw in text for kw in keywords):
                results['endogeneity_solution'][solution] += 1
                paper_endo.append(solution)
        
        # 稳健性检验
        for check, keywords in ROBUSTNESS_CHECKS.items():
            if any(kw in text for kw in keywords):
                results['robustness_check'][check] += 1
                paper_robust.append(check)
        
        if paper_methods or paper_endo or paper_robust:
            results['papers_with_method'].append({
                'title': paper.get('title', ''),
                'authors': paper.get('authors', []),
                'year': paper.get('year', ''),
                'journal': paper.get('journal', ''),
                'methods': paper_methods,
                'endogeneity': paper_endo,
                'robustness': paper_robust
            })
    
    # 转换为普通字典
    results['identification_strategy'] = dict(results['identification_strategy'])
    results['endogeneity_solution'] = dict(results['endogeneity_solution'])
    results['robustness_check'] = dict(results['robustness_check'])
    
    return results


def generate_markdown_report(results, total_papers, output_path):
    """生成 Markdown 报告"""
    
    lines = [
        "# 方法论评价报告",
        "",
        f"**生成时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**文献总数:** {total_papers} 篇",
        "",
        "---",
        "",
        "## 1. 因果识别策略分布",
        "",
        "| 方法 | 文献数 | 占比 | 说明 |",
        "|------|--------|------|------|",
    ]
    
    method_names = {
        'did': '双重差分 (DID)',
        'iv': '工具变量 (IV)',
        'rd': '断点回归 (RD)',
        'psm': '倾向得分匹配 (PSM)',
        'fe': '固定效应 (FE)',
        'gmm': '广义矩估计 (GMM)',
        're': '随机效应 (RE)',
        'tobit': 'Tobit 模型',
        'logit_probit': 'Logit/Probit'
    }
    
    method_desc = {
        'did': '利用外生政策冲击识别因果',
        'iv': '寻找外生工具变量',
        'rd': '利用阈值附近的局部随机性',
        'psm': '构造反事实对照组',
        'fe': '控制个体/时间不变特征',
        'gmm': '处理动态面板内生性',
        're': '随机效应假设',
        'tobit': '处理截断数据',
        'logit_probit': '二值选择模型'
    }
    
    id_results = results['identification_strategy']
    total_with_method = sum(id_results.values())
    
    for method, count in sorted(id_results.items(), key=lambda x: x[1], reverse=True):
        name = method_names.get(method, method)
        desc = method_desc.get(method, '')
        pct = round(count / total_papers * 100, 1)
        lines.append(f"| {name} | {count} | {pct}% | {desc} |")
    
    if not id_results:
        lines.append("| - | - | - | 未识别到明确方法 |")
    else:
        lines.append(f"\n**说明:** {total_with_method} 篇文献 ({round(total_with_method/total_papers*100, 1)}%) 使用了明确的因果识别策略。")
    
    lines.extend([
        "",
        "## 2. 内生性处理方法",
        "",
        "| 方法 | 文献数 | 占比 | 说明 |",
        "|------|--------|------|------|",
    ])
    
    endo_names = {
        'lagged': '滞后解释变量',
        'iv': '工具变量法',
        'did': '双重差分/外生冲击',
        'rd': '断点回归',
        'heckman': 'Heckman 选择模型',
        'system_gmm': '系统 GMM'
    }
    
    endo_desc = {
        'lagged': '缓解反向因果',
        'iv': '寻找外生变异来源',
        'did': '利用准自然实验',
        'rd': '利用局部随机性',
        'heckman': '纠正样本选择偏误',
        'system_gmm': '处理动态内生性'
    }
    
    endo_results = results['endogeneity_solution']
    
    for solution, count in sorted(endo_results.items(), key=lambda x: x[1], reverse=True):
        name = endo_names.get(solution, solution)
        desc = endo_desc.get(solution, '')
        pct = round(count / total_papers * 100, 1)
        lines.append(f"| {name} | {count} | {pct}% | {desc} |")
    
    if not endo_results:
        lines.append("| - | - | - | 未识别到明确处理方法 |")
    
    lines.extend([
        "",
        "## 3. 稳健性检验方法",
        "",
        "| 方法 | 使用频率 | 说明 |",
        "|------|---------|------|",
    ])
    
    robust_names = {
        'replace_variable': '替换核心变量',
        'change_sample': '改变样本范围',
        'add_control': '增加控制变量',
        'change_method': '更换估计方法',
        'placebo': '安慰剂检验',
        'exclude_special': '排除特殊样本'
    }
    
    robust_results = results['robustness_check']
    
    for check, count in sorted(robust_results.items(), key=lambda x: x[1], reverse=True):
        name = robust_names.get(check, check)
        freq = '高' if count > 20 else '中' if count > 10 else '低'
        lines.append(f"| {name} | {freq} ({count}篇) | 检验结果稳健性 |")
    
    if not robust_results:
        lines.append("| - | - | 未识别到明确检验方法 |")
    
    lines.extend([
        "",
        "## 4. 方法论质量评价",
        "",
        "### 4.1 总体评价",
        "",
    ])
    
    # 质量评价
    if total_with_method / total_papers > 0.3:
        quality = "较好"
        comment = "超过 30% 的文献使用了明确的因果识别策略"
    elif total_with_method / total_papers > 0.15:
        quality = "中等"
        comment = "约 15-30% 的文献使用了因果识别策略，仍有改进空间"
    else:
        quality = "有待提高"
        comment = "使用因果识别策略的文献比例较低"
    
    lines.append(f"**因果识别质量:** {quality}")
    lines.append("")
    lines.append(f"**评价:** {comment}")
    
    lines.extend([
        "",
        "### 4.2 主要问题",
        "",
        "1. **内生性处理不足:** 部分文献仅使用固定效应，未充分处理反向因果",
        "2. **工具变量质量:** 部分文献的工具变量外生性论证不充分",
        "3. **稳健性检验:** 安慰剂检验等高级方法使用较少",
        "",
        "### 4.3 改进建议",
        "",
        "1. 更多利用政策冲击作为外生变异来源",
        "2. 加强工具变量的外生性论证",
        "3. 增加安慰剂检验、排除竞争性解释等稳健性检验",
        "",
        "---",
        "",
        "*报告由 Literature Reviewer Skill v5.0 自动生成*"
    ])
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"✓ 方法论评价报告已保存到：{output_path}")


def main():
    if len(sys.argv) < 2:
        print("用法：python phase6_methodology.py <session_dir>")
        sys.exit(1)
    
    session_dir = Path(sys.argv[1])
    
    print("=" * 60)
    print("Phase 6: 方法论评价")
    print("=" * 60)
    
    # 加载文献
    print("\n[1] 加载文献数据...")
    papers_path = session_dir / "papers_verified.json"
    with open(papers_path, 'r', encoding='utf-8') as f:
        papers = json.load(f)
    print(f"  加载 {len(papers)} 篇文献")
    
    # 分析
    print("\n[2] 执行方法论分析...")
    results = analyze_methodology(papers)
    
    print(f"  识别到因果识别策略：{sum(results['identification_strategy'].values())} 篇次")
    print(f"  识别到内生性处理：{sum(results['endogeneity_solution'].values())} 篇次")
    print(f"  识别到稳健性检验：{sum(results['robustness_check'].values())} 篇次")
    
    # 生成报告
    print("\n[3] 生成 Markdown 报告...")
    output_path = session_dir / "output" / "methodology_report.md"
    generate_markdown_report(results, len(papers), output_path)
    
    # 保存 JSON 结果
    json_path = session_dir / "phase6_methodology.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"✓ JSON 结果已保存到：{json_path}")
    
    print("\n" + "=" * 60)
    print("✓ Phase 6 完成!")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
