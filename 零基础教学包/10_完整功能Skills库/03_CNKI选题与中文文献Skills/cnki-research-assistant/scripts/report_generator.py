#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
报告生成模块
生成 Markdown 格式的综合分析报告
"""

from datetime import datetime
from typing import Dict, Any, List
import os


class ReportGenerator:
    """报告生成器"""
    
    def __init__(self):
        self.template_path = None
    
    def build_report(
        self,
        keyword: str,
        rank_data: Dict[str, Any],
        trend_data: Dict[str, Any],
        paper_data: Dict[str, Any],
        journal_data: Dict[str, Any],
        gap_data: Dict[str, Any] = None
    ) -> str:
        """
        构建综合分析报告
        
        Args:
            keyword: 选题关键词
            rank_data: 热榜数据
            trend_data: 趋势数据
            paper_data: 文献数据
            journal_data: 期刊匹配数据
        
        Returns:
            Markdown 格式报告
        """
        sections = []
        
        # 标题
        sections.append(self._build_header(keyword))
        
        # 执行摘要
        sections.append(self._build_executive_summary(keyword, rank_data, trend_data, journal_data))
        
        # 热点扫描
        sections.append(self._build_rank_section(rank_data))
        
        # 趋势评估
        sections.append(self._build_trend_section(trend_data))
        
        # 文献调研
        sections.append(self._build_paper_section(paper_data))
        
        # 期刊推荐
        sections.append(self._build_journal_section(journal_data))
        
        # 研究空白分析
        if gap_data:
            sections.append(self._build_gap_section(gap_data))
        
        # 综合评估与建议
        sections.append(self._build_recommendation_section(keyword, rank_data, trend_data, journal_data, gap_data))
        
        # 附录
        sections.append(self._build_appendix(trend_data))
        
        return '\n\n'.join(sections)
    
    def _build_header(self, keyword: str) -> str:
        """生成报告标题"""
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return f"""# 📊 CNKI 选题分析报告：{keyword}

**生成时间**: {now}  
**数据来源**: CNKI 热榜、CNKI getGroupData、CSSCI 期刊库 (2025-2026)

---
"""
    
    def _build_executive_summary(
        self,
        keyword: str,
        rank_data: Dict,
        trend_data: Dict,
        journal_data: Dict
    ) -> str:
        """生成执行摘要"""
        # 计算综合评分
        heat_score = self._calculate_heat_score(rank_data, trend_data)
        publish_score = self._calculate_publish_score(trend_data, journal_data)
        
        # 生成星级
        heat_stars = '⭐' * round(heat_score)
        publish_stars = '⭐' * round(publish_score)
        
        return f"""## 📋 执行摘要

| 评估维度 | 评分 | 说明 |
|---------|------|------|
| **热度评估** | {heat_stars} ({heat_score:.1f}/5) | 基于热榜排名 + 年度趋势 |
| **发表空间** | {publish_stars} ({publish_score:.1f}/5) | 基于期刊分布 + 匹配度 |
| **竞争程度** | {'中等' if 2.5 <= heat_score <= 3.5 else ('激烈' if heat_score > 3.5 else '较低')} | 基于头部机构集中度 |

### 核心发现

""" + self._generate_key_findings(keyword, trend_data, journal_data)
    
    def _calculate_heat_score(self, rank_data: Dict, trend_data: Dict) -> float:
        """计算热度评分（0-5 分）"""
        score = 2.5  # 基础分
        
        # 热榜加分
        if rank_data.get('success'):
            week_rank = rank_data.get('week_rank')
            if week_rank and week_rank <= 10:
                score += 1.5
            elif week_rank and week_rank <= 30:
                score += 1.0
            elif week_rank:
                score += 0.5
        
        # 趋势加分
        if trend_data.get('success') and 'metrics' in trend_data:
            metrics = trend_data['metrics']
            if 'yearly' in metrics:
                recent_ratio = metrics['yearly'].get('recent_3y_ratio', 0)
                if recent_ratio > 0.8:
                    score += 1.0
                elif recent_ratio > 0.5:
                    score += 0.5
        
        return min(5.0, max(0.0, score))
    
    def _calculate_publish_score(self, trend_data: Dict, journal_data: Dict) -> float:
        """计算发表空间评分（0-5 分）"""
        score = 2.5  # 基础分
        
        # 期刊分布加分
        if trend_data.get('success') and 'metrics' in trend_data:
            metrics = trend_data['metrics']
            if 'journal' in metrics:
                journal_count = metrics['journal'].get('total_journals', 0)
                if journal_count > 50:
                    score += 1.5
                elif journal_count > 20:
                    score += 1.0
                else:
                    score += 0.5
        
        # 匹配度加分
        if journal_data.get('success'):
            journals = journal_data.get('matched_journals', [])
            if journals:
                top_match = journals[0].get('match_score', 0)
                if top_match > 80:
                    score += 1.0
                elif top_match > 60:
                    score += 0.5
        
        return min(5.0, max(0.0, score))
    
    def _generate_key_findings(
        self,
        keyword: str,
        trend_data: Dict,
        journal_data: Dict
    ) -> str:
        """生成核心发现"""
        findings = []
        
        if trend_data.get('success') and 'metrics' in trend_data:
            metrics = trend_data['metrics']
            
            if 'yearly' in metrics:
                y = metrics['yearly']
                findings.append(f"- **热度峰值**: {y['peak_year']} 年 ({y['peak_count']} 篇)，近三年占比 {y['recent_3y_ratio']:.1%}")
            
            if 'subject' in metrics:
                s = metrics['subject']
                findings.append(f"- **主导学科**: {s['top_discipline']} (占比 {s['top_discipline_ratio']:.1%})")
        
        if journal_data.get('success'):
            journals = journal_data.get('matched_journals', [])
            if journals:
                top3 = journals[:3]
                journal_names = [f"《{j['期刊名称']}》" for j in top3]
                findings.append(f"- **推荐期刊**: {', '.join(journal_names)}")
        
        if not findings:
            findings.append("- 数据收集中，详细分析见下文各章节")
        
        return '\n'.join(findings)
    
    def _build_rank_section(self, rank_data: Dict) -> str:
        """热点扫描章节"""
        content = """## 🔥 一、热点扫描 (CNKI 热榜)

"""
        if rank_data.get('success'):
            if rank_data.get('week_rank'):
                content += f"- **周榜排名**: 第 {rank_data['week_rank']} 名\n"
            if rank_data.get('month_rank'):
                content += f"- **月榜排名**: 第 {rank_data['month_rank']} 名\n"
            content += f"- **在榜天数**: {rank_data.get('days_on_list', 0)} 天\n"
            content += f"- **状态**: {rank_data.get('status', 'unknown')}\n"
        else:
            content += f"> ⚠️ {rank_data.get('note', '热榜数据获取失败')}\n"
        
        return content
    
    def _build_trend_section(self, trend_data: Dict) -> str:
        """趋势评估章节"""
        content = """## 📈 二、趋势评估 (CNKI getGroupData)

"""
        if trend_data.get('success'):
            if 'metrics' in trend_data:
                metrics = trend_data['metrics']
                
                # 年度趋势
                if 'yearly' in metrics:
                    y = metrics['yearly']
                    content += f"""### 2.1 年度趋势

- **数据总量**: {y['total_papers']} 篇
- **峰值年份**: {y['peak_year']} ({y['peak_count']} 篇)
- **近三年占比**: {y['recent_3y_ratio']:.1%}
- **趋势判断**: {'上升期' if y['recent_3y_ratio'] > 0.7 else ('成熟期' if y['recent_3y_ratio'] > 0.4 else '衰退期')}

"""
                
                # 学科分布
                if 'subject' in metrics:
                    s = metrics['subject']
                    content += f"""### 2.2 学科分布

- **覆盖学科数**: {s['total_disciplines']} 个
- **首位学科**: {s['top_discipline']} ({s['top_discipline_ratio']:.1%})
- **学科集中度**: {'高' if s['top_discipline_ratio'] > 0.5 else ('中' if s['top_discipline_ratio'] > 0.3 else '低')}

"""
                
                # 期刊分布
                if 'journal' in metrics:
                    j = metrics['journal']
                    content += f"""### 2.3 期刊格局

- **覆盖期刊数**: {j['total_journals']} 种
- **集中度**: {j['concentration']}
- **发表空间**: {'充足' if j['concentration'] == 'low' else ('适中' if j['concentration'] == 'medium' else '有限')}

"""
            
            # 图表引用
            if 'charts_dir' in trend_data and os.path.exists(trend_data['charts_dir']):
                content += """### 2.4 趋势图表

"""
                chart_files = [f for f in os.listdir(trend_data['charts_dir']) if f.endswith('.png')]
                for chart in chart_files[:5]:
                    chart_name = chart.replace('.png', '').replace('_', ' ')
                    content += f"![{chart_name}]({os.path.join(trend_data['charts_dir'], chart)})\n\n"
        else:
            content += f"> ⚠️ {trend_data.get('error', '趋势分析失败')}\n"
        
        return content
    
    def _build_paper_section(self, paper_data: Dict) -> str:
        """文献调研章节"""
        content = """## 📄 三、文献调研 (CNKI 论文库)

"""
        if paper_data.get('success'):
            if paper_data.get('papers_count', 0) > 0:
                content += f"- **抓取文献数**: {paper_data['papers_count']} 篇\n"
                content += "- **高被引文献**: (待集成)\n"
                content += "- **核心作者**: (待集成)\n"
            else:
                content += "> ⚠️ 文献抓取模块集成中，当前跳过\n"
        else:
            content += f"> ⚠️ {paper_data.get('error', '文献抓取失败')}\n"
        
        return content
    
    def _build_gap_section(self, gap_data: Dict) -> str:
        """研究空白分析章节"""
        if not gap_data.get('success') or not gap_data.get('report'):
            return "## 💡 五、研究空白分析\n\n> ⚠️ 暂无足够数据进行分析\n\n"
        
        return "## 💡 五、研究空白分析\n\n" + gap_data['report'].replace('## 🔍 研究空白分析\n\n', '')
    
    def _build_journal_section(self, journal_data: Dict) -> str:
        """期刊推荐章节"""
        content = """## 📚 四、期刊推荐 (CSSCI 期刊库)

**匹配算法**: 0.4×学科匹配 + 0.4×选题相似度 + 0.2×级别系数

"""
        if journal_data.get('success'):
            journals = journal_data.get('matched_journals', [])
            if journals:
                content += "| 排名 | 期刊名称 | 学科 | 级别 | 匹配度 | 契合点 |\n"
                content += "|------|---------|------|------|--------|--------|\n"
                
                for i, j in enumerate(journals, 1):
                    matching_topics = ', '.join(j.get('matching_topics', [])[:2]) or '暂无'
                    content += f"| {i} | 《{j['期刊名称']}》 | {j['学科名称']} | {j['级别']} | {j['match_score']:.0f}% | {matching_topics} |\n"
            else:
                content += "> 未找到匹配期刊\n"
        else:
            content += f"> ⚠️ {journal_data.get('error', '期刊匹配失败')}\n"
        
        return content
    
    def _build_recommendation_section(
        self,
        keyword: str,
        rank_data: Dict,
        trend_data: Dict,
        journal_data: Dict,
        gap_data: Dict = None
    ) -> str:
        """综合评估与建议章节"""
        heat_score = self._calculate_heat_score(rank_data, trend_data)
        publish_score = self._calculate_publish_score(trend_data, journal_data)
        
        content = f"""## 💡 五、综合评估与建议

### 5.1 选题可行性

| 维度 | 评估 | 建议 |
|------|------|------|
| **研究热度** | {'🔥 高' if heat_score > 3.5 else ('⚡ 中' if heat_score > 2.5 else '❄️ 低')} | {'建议尽快切入' if heat_score > 3.5 else '可稳步跟进'} |
| **发表空间** | {'✅ 充足' if publish_score > 3.5 else ('⚠️ 适中' if publish_score > 2.5 else '🔒 有限')} | {'多期刊可选' if publish_score > 3.5 else '需精准匹配'} |
| **竞争程度** | {'激烈' if heat_score > 4 else ('中等' if heat_score > 2.5 else '较低')} | {'差异化切入' if heat_score > 4 else '正常推进'} |

### 5.2 潜在切入点

"""
        # 生成切入点建议
        content += self._generate_research_angles(keyword, trend_data)
        
        content += f"""
### 5.3 投稿策略

1. **首选期刊**: 匹配度 Top 3 期刊（见第四章）
2. **备选期刊**: 扩展版期刊或相关学科期刊
3. **投稿时机**: {'尽快（热点上升期）' if heat_score > 3.5 else '常规推进'}

"""
        return content
    
    def _generate_research_angles(self, keyword: str, trend_data: Dict) -> str:
        """生成潜在切入点建议"""
        angles = []
        
        if trend_data.get('success') and 'metrics' in trend_data:
            metrics = trend_data['metrics']
            
            if 'subject' in metrics:
                s = metrics['subject']
                angles.append(f"- **学科交叉**: 结合{s['top_discipline']}与其他学科视角")
            
            if 'journal' in metrics:
                j = metrics['journal']
                if j['concentration'] == 'low':
                    angles.append("- **期刊选择**: 期刊分布分散，可多选目标期刊")
                else:
                    angles.append("- **期刊选择**: 期刊集中，需精准匹配头部期刊偏好")
        
        angles.append(f"- **方法创新**: 结合新数据、新方法研究{keyword}")
        angles.append(f"- **视角创新**: 从微观/宏观/跨文化视角切入{keyword}")
        
        return '\n'.join(angles)
    
    def _build_appendix(self, trend_data: Dict) -> str:
        """附录章节"""
        content = """---

## 📎 附录

### 数据来源说明

1. **CNKI 热榜**: https://www.cnki.net/ (下载榜/热词榜)
2. **CNKI getGroupData**: 知网可视化分析接口
3. **CSSCI 期刊库**: 2025-2026 年 C 刊重点选题汇总（933 种期刊）

### 指标解释

- **近三年占比**: 2024-2026 年论文数 / 总论文数，反映热度持续性
- **学科集中度**: 首位学科占比，反映学科承载能力
- **期刊集中度**: 覆盖期刊数量，反映发表空间
- **匹配度**: 选题与期刊的契合程度（0-100%）

### 注意事项

1. 当年数据为年内累计值，非全年预测
2. 匹配度仅供参考，投稿前请查阅期刊最新征稿启事
3. 建议结合人工判断，不要完全依赖算法推荐

---

*报告由 CNKI Research Assistant 自动生成*
"""
        return content
