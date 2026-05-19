#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
研究空白分析模块
识别尚未充分研究的方向和潜在切入点
"""

import os
import json
from typing import Dict, List, Any, Optional
from collections import Counter, defaultdict
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ResearchGapAnalyzer:
    """研究空白分析器"""
    
    def __init__(self):
        self.gaps = []
    
    def analyze_from_papers(self, papers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        从论文数据中识别研究空白
        
        Args:
            papers: 论文列表，包含 title, keywords, abstract, authors, organizations, funds 等字段
        
        Returns:
            研究空白列表
        """
        gaps = []
        
        # 1. 关键词共现分析 - 识别未充分研究的关键词组合
        keyword_gaps = self._analyze_keyword_cooccurrence(papers)
        gaps.extend(keyword_gaps)
        
        # 2. 主题聚类分析 - 识别研究主题分布
        cluster_gaps = self._analyze_topic_clusters(papers)
        gaps.extend(cluster_gaps)
        
        # 3. 方法分析 - 识别研究方法多样性（新增）
        method_gaps = self._analyze_research_methods(papers)
        gaps.extend(method_gaps)
        
        # 4. 机构分析 - 识别研究力量分布（新增）
        org_gaps = self._analyze_organizations(papers)
        gaps.extend(org_gaps)
        
        # 5. 基金分析 - 识别资助方向（新增）
        fund_gaps = self._analyze_funds(papers)
        gaps.extend(fund_gaps)
        
        # 6. 时间趋势分析 - 识别新兴方向（新增）
        trend_gaps = self._analyze_yearly_trends(papers)
        gaps.extend(trend_gaps)
        
        return gaps
    
    def _analyze_keyword_cooccurrence(self, papers: List[Dict]) -> List[Dict]:
        """分析关键词共现，识别未充分研究的组合"""
        # 提取所有关键词
        all_keywords = []
        paper_keywords = []
        
        for paper in papers:
            kws = paper.get('keywords', [])
            if isinstance(kws, str):
                kws = [k.strip() for k in kws.split(';') if k.strip()]
            if kws:
                all_keywords.extend(kws)
                paper_keywords.append(kws)
        
        # 统计关键词频次
        keyword_freq = Counter(all_keywords)
        top_keywords = [kw for kw, _ in keyword_freq.most_common(30)]
        
        # 分析共现矩阵
        cooccurrence = defaultdict(int)
        for kws in paper_keywords:
            for i, kw1 in enumerate(kws):
                for kw2 in kws[i+1:]:
                    pair = tuple(sorted([kw1, kw2]))
                    cooccurrence[pair] += 1
        
        # 识别低频但有潜力的组合
        gaps = []
        potential_pairs = []
        
        for kw1 in top_keywords[:10]:
            for kw2 in top_keywords[10:20]:
                pair = tuple(sorted([kw1, kw2]))
                count = cooccurrence.get(pair, 0)
                
                # 如果两个关键词都高频，但共现频次低，可能是研究空白
                if keyword_freq[kw1] > 5 and keyword_freq[kw2] > 5 and count < 3:
                    potential_pairs.append({
                        'keywords': [kw1, kw2],
                        'cooccurrence_count': count,
                        'kw1_freq': keyword_freq[kw1],
                        'kw2_freq': keyword_freq[kw2],
                        'gap_score': (keyword_freq[kw1] + keyword_freq[kw2]) / (count + 1)
                    })
        
        # 按空白评分排序
        potential_pairs.sort(key=lambda x: x['gap_score'], reverse=True)
        
        for i, pair in enumerate(potential_pairs[:5]):
            gaps.append({
                'type': '关键词组合空白',
                'description': f"{pair['keywords'][0]} + {pair['keywords'][1]} 的交叉研究较少",
                'evidence': f"共现仅 {pair['cooccurrence_count']} 次，但两个关键词分别出现 {pair['kw1_freq']} 次和 {pair['kw2_freq']} 次",
                'gap_score': pair['gap_score'],
                'suggested_direction': f"建议探索{pair['keywords'][0]}与{pair['keywords'][1]}的交叉研究"
            })
        
        return gaps
    
    def _analyze_topic_clusters(self, papers: List[Dict]) -> List[Dict]:
        """分析主题聚类，识别研究不足的子方向"""
        # 提取标题和摘要
        texts = []
        for paper in papers:
            text_parts = []
            if paper.get('title'):
                text_parts.append(paper['title'])
            if paper.get('abstract'):
                text_parts.append(paper['abstract'])
            if text_parts:
                texts.append(' '.join(text_parts))
        
        if len(texts) < 10:
            return []
        
        # TF-IDF 聚类
        try:
            vectorizer = TfidfVectorizer(max_features=100, ngram_range=(1, 2))
            tfidf_matrix = vectorizer.fit_transform(texts)
            
            # 计算文档相似度
            similarity_matrix = cosine_similarity(tfidf_matrix)
            
            # 识别低相似度文档（可能是研究空白）
            avg_similarities = similarity_matrix.mean(axis=1)
            outlier_indices = [i for i, sim in enumerate(avg_similarities) if sim < avg_similarities.mean() - avg_similarities.std()]
            
            gaps = []
            for idx in outlier_indices[:3]:
                gaps.append({
                    'type': '边缘研究方向',
                    'description': f"论文 '{texts[idx][:50]}...' 与主流研究差异较大",
                    'evidence': '该研究与平均相似度低于 1 个标准差',
                    'gap_score': 2.0,
                    'suggested_direction': '可能代表新兴交叉方向，值得深入探索'
                })
            
            return gaps
            
        except Exception as e:
            return []
    
    def analyze_from_trend_data(self, trend_data: Dict) -> List[Dict]:
        """
        从趋势数据中识别研究空白
        
        Args:
            trend_data: cnki-trend 的趋势分析数据
        
        Returns:
            研究空白列表
        """
        gaps = []
        
        if not trend_data or 'metrics' not in trend_data:
            return gaps
        
        metrics = trend_data['metrics']
        
        # 1. 学科分布分析 - 识别研究不足的学科
        if 'subject' in metrics:
            subject_data = metrics['subject']
            total_disciplines = subject_data.get('total_disciplines', 0)
            top_discipline_ratio = subject_data.get('top_discipline_ratio', 0)
            
            if total_disciplines > 15 and top_discipline_ratio < 0.3:
                gaps.append({
                    'type': '学科交叉空白',
                    'description': f"学科分布分散（{total_disciplines}个学科），首位学科占比仅{top_discipline_ratio:.1%}",
                    'evidence': '说明该主题处于跨学科扩散阶段，尚未形成稳定的学科落点',
                    'gap_score': 3.5,
                    'suggested_direction': '可选择任一学科视角切入，竞争相对较小'
                })
        
        # 2. 期刊分布分析 - 识别发表空间
        if 'journal' in metrics:
            journal_data = metrics['journal']
            total_journals = journal_data.get('total_journals', 0)
            concentration = journal_data.get('concentration', 'unknown')
            
            if total_journals > 100 and concentration == 'low':
                gaps.append({
                    'type': '期刊发表空白',
                    'description': f"期刊覆盖广泛（{total_journals}种），集中度低",
                    'evidence': '说明该主题已突破单一期刊圈层，多期刊欢迎相关投稿',
                    'gap_score': 4.0,
                    'suggested_direction': '可根据研究内容精准匹配期刊，发表空间充足'
                })
        
        # 3. 年度趋势分析 - 识别新兴方向
        if 'yearly' in metrics:
            yearly_data = metrics['yearly']
            recent_3y_ratio = yearly_data.get('recent_3y_ratio', 0)
            peak_year = yearly_data.get('peak_year', '')
            
            if recent_3y_ratio > 0.9:
                gaps.append({
                    'type': '新兴热点空白',
                    'description': f"近三年研究占比{recent_3y_ratio:.1%}，峰值出现在{peak_year}",
                    'evidence': '说明该主题是近期新兴热点，研究范式尚未固化',
                    'gap_score': 4.5,
                    'suggested_direction': '建议尽快切入，抢占研究先机'
                })
        
        return gaps
    
    def analyze_from_cssci(self, journal_matches: List[Dict]) -> List[Dict]:
        """
        从期刊匹配数据中识别选题缺口
        
        Args:
            journal_matches: 期刊匹配结果列表
        
        Returns:
            研究空白列表
        """
        gaps = []
        
        if not journal_matches:
            return gaps
        
        # 分析期刊契合点
        all_topics = []
        for journal in journal_matches:
            matching_topics = journal.get('matching_topics', [])
            all_topics.extend(matching_topics)
        
        # 统计选题方向频次
        topic_freq = Counter(all_topics)
        
        # 识别低频但重要的方向
        if topic_freq:
            low_freq_topics = [topic for topic, count in topic_freq.items() if count == 1]
            
            if low_freq_topics:
                gaps.append({
                    'type': '期刊选题空白',
                    'description': f"部分期刊征稿方向研究较少：{', '.join(low_freq_topics[:3])}",
                    'evidence': '这些方向在 CSSCI 期刊明确征稿，但现有研究相对较少',
                    'gap_score': 3.8,
                    'suggested_direction': f"建议关注{low_freq_topics[0] if low_freq_topics else '期刊征稿方向'}，契合期刊需求"
                })
        
        # 分析匹配度分布
        match_scores = [j['match_score'] for j in journal_matches]
        avg_score = sum(match_scores) / len(match_scores) if match_scores else 0
        
        if avg_score < 45:
            gaps.append({
                'type': '匹配度提升空间',
                'description': f"期刊平均匹配度{avg_score:.0f}%，有提升空间",
                'evidence': '说明当前选题与期刊征稿方向的契合度可以进一步优化',
                'gap_score': 2.5,
                'suggested_direction': '建议细化选题方向，更精准对接期刊征稿重点'
            })
        
        return gaps
    
    def generate_gap_report(self, gaps: List[Dict]) -> str:
        """生成研究空白报告"""
        if not gaps:
            return "## 🔍 研究空白分析\n\n暂无足够数据进行分析。\n"
        
        # 按空白评分排序
        gaps_sorted = sorted(gaps, key=lambda x: x.get('gap_score', 0), reverse=True)
        
        report = "## 💡 研究空白分析\n\n"
        report += "基于论文数据、趋势分析和期刊匹配，识别以下研究空白：\n\n"
        
        # Top 空白
        report += "### 优先研究方向\n\n"
        for i, gap in enumerate(gaps_sorted[:5], 1):
            gap_score = gap.get('gap_score', 0)
            stars = '⭐' * min(5, round(gap_score))
            report += f"#### {i}. {gap['type']}（推荐指数：{stars}）\n\n"
            report += f"**发现**: {gap['description']}\n\n"
            report += f"**证据**: {gap['evidence']}\n\n"
            report += f"**建议**: {gap['suggested_direction']}\n\n"
            report += "---\n\n"
        
        # 空白类型统计
        gap_types = Counter(g['type'] for g in gaps)
        report += "### 空白类型分布\n\n"
        for gap_type, count in gap_types.most_common():
            report += f"- {gap_type}: {count} 个\n"
        
        report += "\n**说明**: 推荐指数基于空白程度、研究潜力和发表空间综合评估（1-5 星）\n"
        
        return report
    
    def _analyze_research_methods(self, papers: List[Dict]) -> List[Dict]:
        """
        分析研究方法多样性，识别方法空白
        
        从摘要中提取方法关键词：实证/理论/案例/仿真/综述等
        """
        gaps = []
        
        # 方法关键词库
        method_keywords = {
            '实证研究': ['实证', '回归', '计量', 'DID', 'IV', 'RDD', 'PSM', '面板数据'],
            '理论研究': ['理论', '模型', '框架', '机理', '机制', '假设'],
            '案例研究': ['案例', '质性', '访谈', '扎根', '民族志'],
            '综述研究': ['综述', '回顾', '进展', '展望', 'meta 分析'],
            '仿真模拟': ['仿真', '模拟', 'ABM', '系统动力学', '演化博弈'],
            '实验研究': ['实验', 'RCT', '随机对照', '问卷', '调查']
        }
        
        method_counts = defaultdict(int)
        
        for paper in papers:
            abstract = (paper.get('abstract') or '').lower()
            title = (paper.get('title') or '').lower()
            text = abstract + ' ' + title
            
            for method, keywords in method_keywords.items():
                if any(kw.lower() in text for kw in keywords):
                    method_counts[method] += 1
        
        total = sum(method_counts.values())
        if total == 0:
            return gaps
        
        # 识别方法单一性
        method_ratios = {m: c/total for m, c in method_counts.items()}
        
        # 如果某种方法占比过高，建议引入其他方法
        dominant_method = max(method_ratios.items(), key=lambda x: x[1], default=None)
        if dominant_method and dominant_method[1] > 0.6:
            gaps.append({
                'type': '方法空白',
                'description': f'现有研究以{dominant_method[0]}为主（占比{dominant_method[1]:.1%}），方法多样性不足',
                'evidence': f'{len(papers)}篇文献中，{method_counts[dominant_method[0]]}篇采用{dominant_method[0]}方法',
                'suggested_direction': f'建议引入{[m for m in method_ratios.keys() if m != dominant_method[0]][:2]}方法',
                'gap_score': 4.0 if dominant_method[1] > 0.8 else 3.5
            })
        
        # 如果缺少某些重要方法
        important_methods = ['实证研究', '理论研究']
        missing_methods = [m for m in important_methods if method_counts.get(m, 0) == 0]
        if missing_methods:
            gaps.append({
                'type': '方法空白',
                'description': f'缺乏{missing_methods[0]}，研究方法不够全面',
                'evidence': f'{len(papers)}篇文献中未发现{missing_methods[0]}',
                'suggested_direction': f'建议采用{missing_methods[0]}方法深化研究',
                'gap_score': 3.5
            })
        
        return gaps
    
    def _analyze_organizations(self, papers: List[Dict]) -> List[Dict]:
        """
        分析研究机构分布，识别机构合作空白
        """
        gaps = []
        
        # 统计机构频次
        org_counter = Counter()
        for paper in papers:
            orgs = paper.get('organizations', [])
            if isinstance(orgs, str):
                orgs = [orgs]
            for org in orgs:
                if org and org.strip():
                    org_counter[org.strip()] += 1
        
        if len(org_counter) == 0:
            return gaps
        
        # 识别头部机构
        top_orgs = org_counter.most_common(5)
        top_concentration = sum(c for _, c in top_orgs) / sum(org_counter.values())
        
        # 如果头部集中度过高，建议寻找差异化机构
        if top_concentration > 0.5:
            gaps.append({
                'type': '机构合作空白',
                'description': f'研究力量集中于头部机构（Top5 占比{top_concentration:.1%}），跨机构合作空间大',
                'evidence': f'头部机构：{[org for org, _ in top_orgs]}',
                'suggested_direction': '建议与非头部机构合作，或开展跨机构联合研究',
                'gap_score': 3.0
            })
        
        return gaps
    
    def _analyze_funds(self, papers: List[Dict]) -> List[Dict]:
        """
        分析基金资助分布，识别资助方向空白
        """
        gaps = []
        
        # 统计基金频次
        fund_counter = Counter()
        funded_count = 0
        
        for paper in papers:
            funds = paper.get('funds', [])
            if isinstance(funds, str):
                funds = [funds]
            if funds and funds[0]:
                funded_count += 1
                for fund in funds:
                    if fund and fund.strip():
                        fund_counter[fund.strip()] += 1
        
        # 基金支持率
        fund_rate = funded_count / len(papers) if papers else 0
        
        # 识别主要资助方向
        top_funds = fund_counter.most_common(5)
        
        if top_funds:
            gaps.append({
                'type': '基金导向',
                'description': f'主要资助方向：{[fund for fund, _ in top_funds]}',
                'evidence': f'{funded_count}/{len(papers)} ({fund_rate:.1%}) 文献获得基金支持',
                'suggested_direction': '建议关注国家社科基金、自然科学基金等主要资助方向',
                'gap_score': 2.5  # 信息性建议，评分较低
            })
        
        return gaps
    
    def _analyze_yearly_trends(self, papers: List[Dict]) -> List[Dict]:
        """
        分析年度趋势，识别新兴研究方向
        """
        gaps = []
        
        # 按年份统计
        year_papers = defaultdict(list)
        for paper in papers:
            year = paper.get('year', '')
            if year and year.isdigit():
                year_papers[year].append(paper)
        
        if len(year_papers) < 3:
            return gaps
        
        # 识别增长趋势
        years = sorted(year_papers.keys())
        recent_2y = [y for y in years if int(y) >= int(years[-1]) - 1]
        older_years = [y for y in years if y not in recent_2y]
        
        recent_count = sum(len(year_papers[y]) for y in recent_2y)
        older_count = sum(len(year_papers[y]) for y in older_years)
        
        # 如果近期文献激增，说明是新兴热点
        if recent_count > older_count * 2:
            gaps.append({
                'type': '新兴热点',
                'description': f'近两年文献量激增（{recent_count}篇 vs 历史{older_count}篇），处于研究爆发期',
                'evidence': f'年度分布：{dict((y, len(year_papers[y])) for y in years)}',
                'suggested_direction': '建议尽快切入，抢占研究先机',
                'gap_score': 4.5
            })
        
        return gaps


def test_gap_analyzer():
    """测试研究空白分析器"""
    analyzer = ResearchGapAnalyzer()
    
    # 测试趋势数据分析
    trend_data = {
        'metrics': {
            'yearly': {'recent_3y_ratio': 0.994, 'peak_year': '2025'},
            'subject': {'total_disciplines': 20, 'top_discipline_ratio': 0.224},
            'journal': {'total_journals': 190, 'concentration': 'low'}
        }
    }
    
    gaps = analyzer.analyze_from_trend_data(trend_data)
    print(analyzer.generate_gap_report(gaps))


if __name__ == '__main__':
    test_gap_analyzer()
