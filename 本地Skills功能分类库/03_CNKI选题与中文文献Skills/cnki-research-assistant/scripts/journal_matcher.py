#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
期刊匹配模块
基于 CSSCI 期刊数据进行选题 - 期刊匹配
"""

import pandas as pd
import re
import os
from typing import List, Dict, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class JournalMatcher:
    """期刊匹配器"""
    
    def __init__(self, cssci_data_path: str = None):
        """
        初始化匹配器
        
        Args:
            cssci_data_path: CSSCI 数据文件路径（CSV 或 Excel，可选，默认使用相对路径）
        """
        if cssci_data_path is None:
            # 使用相对路径：相对于脚本目录的 ../data/
            script_dir = os.path.dirname(os.path.abspath(__file__))
            data_dir = os.path.join(script_dir, '../data')
            
            # 优先查找 Excel 文件，其次查找 CSV 文件
            cssci_data_path = None
            for filename in os.listdir(data_dir):
                if filename.endswith('.xlsx') and 'CSSCI' in filename:
                    cssci_data_path = os.path.join(data_dir, filename)
                    break
                elif filename.endswith('.csv'):
                    cssci_data_path = os.path.join(data_dir, filename)
                    break
            
            if not cssci_data_path:
                raise FileNotFoundError("CSSCI 数据文件不存在，请将数据文件放入 data/ 目录")
        
        self.data_path = cssci_data_path
        self.df = None
        self.total_journals = 0
        self._load_data()
    
    def _load_data(self):
        """加载并预处理数据"""
        # 根据文件扩展名选择读取方式
        if self.data_path.endswith('.xlsx'):
            # Excel 文件，跳过第一行标题
            self.df = pd.read_excel(self.data_path, skiprows=1)
        elif self.data_path.endswith('.csv'):
            # CSV 文件
            self.df = pd.read_csv(self.data_path)
        else:
            raise ValueError(f"不支持的文件格式：{self.data_path}")
        
        self.total_journals = len(self.df)
        
        # 数据清洗
        # 1. 处理"0"值（替换为空字符串）
        # 注意：列名可能是 '2026重点选题' 或 '2026 重点选题'，需要兼容
        topic_col = '2026重点选题' if '2026重点选题' in self.df.columns else '2026 重点选题'
        intro_col = '期刊简介' if '期刊简介' in self.df.columns else '期刊简介'
        level_col = '级别' if '级别' in self.df.columns else '级别'
        
        self.df[topic_col] = self.df[topic_col].fillna('').apply(
            lambda x: '' if x == '0' or x == 0 else str(x)
        )
        self.df[intro_col] = self.df[intro_col].fillna('').apply(
            lambda x: '' if x == '0' or x == 0 else str(x)
        )
        
        # 2. 标准化级别字段
        self.df['级别标准化'] = self.df[level_col].apply(self._normalize_level)
        
        # 3. 预处理选题文本（用于匹配）
        self.df['选题关键词'] = self.df[topic_col].apply(self._extract_keywords)
    
    def _normalize_level(self, level: str) -> str:
        """标准化期刊级别"""
        if '核心' in str(level):
            return 'core'
        elif '扩展' in str(level):
            return 'extended'
        return 'other'
    
    def _extract_keywords(self, topics: str) -> str:
        """从选题中提取关键词"""
        if not topics:
            return ''
        
        # 清理编号（如"1."、"2."等）
        cleaned = re.sub(r'^\d+\.', '', topics, flags=re.MULTILINE)
        cleaned = re.sub(r'\n\d+\.', '\n', cleaned)
        
        # 清理特殊字符
        cleaned = re.sub(r'[^\w\s\u4e00-\u9fff+]', ' ', cleaned)
        
        return cleaned.strip()
    
    def _tokenize_chinese(self, text: str) -> List[str]:
        """
        简单中文分词（按字符和常用词）
        实际生产环境可使用 jieba
        """
        # 简单处理：按字符分割，但保留常见双字词
        # 这里使用简化版本，实际可集成 jieba
        return list(text.replace(' ', ''))
    
    def match(self, keyword: str, top_n: int = 10, level: str = 'all') -> List[Dict[str, Any]]:
        """
        匹配期刊
        
        Args:
            keyword: 用户选题关键词
            top_n: 返回 Top N 个期刊
            level: 级别筛选 ('all', 'core', 'extended')
        
        Returns:
            匹配的期刊列表（按匹配度降序）
        """
        # 1. 级别筛选
        df_filtered = self.df.copy()
        if level != 'all':
            df_filtered = df_filtered[df_filtered['级别标准化'] == level]
        
        if len(df_filtered) == 0:
            return []
        
        # 2. 计算匹配分数
        scores = []
        for idx, row in df_filtered.iterrows():
            score = self._calculate_match_score(keyword, row)
            scores.append(score)
        
        df_filtered['match_score'] = scores
        
        # 3. 排序并返回 Top N
        df_sorted = df_filtered.sort_values('match_score', ascending=False)
        top_journals = df_sorted.head(top_n)
        
        # 4. 格式化输出
        # 动态获取列名（兼容不同版本的 CSSCI 数据）
        topic_col = '2026重点选题' if '2026重点选题' in df_filtered.columns else '2026 重点选题'
        
        results = []
        for _, row in top_journals.iterrows():
            matching_topics = self._find_matching_topics(keyword, row[topic_col])
            
            result = {
                '期刊名称': row['期刊名称'],
                '学科名称': row['学科名称'],
                '级别': row['级别'],
                'match_score': row['match_score'],
                'matching_topics': matching_topics[:5],  # 最多显示 5 个契合点
                '期刊网址': row.get('期刊网址', ''),
                '青年友好': '是' if row.get('期刊青年友好动作') and row.get('期刊青年友好动作') != '' else '否'
            }
            results.append(result)
        
        return results
    
    def _calculate_match_score(self, keyword: str, journal_row: pd.Series) -> float:
        """
        计算匹配度分数
        
        匹配度 = 0.4 × 学科匹配 + 0.4 × 选题相似度 + 0.2 × 级别系数
        """
        # 1. 学科匹配（0-1 分）
        discipline_score = self._match_discipline(keyword, journal_row['学科名称'])
        
        # 2. 选题相似度（0-1 分）
        # 动态获取列名
        topic_col = '2026重点选题' if '2026重点选题' in journal_row.index else '2026 重点选题'
        topic_score = self._match_topics(keyword, journal_row[topic_col])
        
        # 3. 级别系数
        level_score = 1.0 if journal_row['级别标准化'] == 'core' else 0.8
        
        # 加权总分
        total_score = 0.4 * discipline_score + 0.4 * topic_score + 0.2 * level_score
        
        return total_score * 100  # 转换为百分比
    
    def _match_discipline(self, keyword: str, discipline: str) -> float:
        """
        学科匹配度
        简单规则：关键词是否包含学科名称或相关词汇
        """
        if not discipline or discipline == '0':
            return 0.5  # 未知学科给中等分数
        
        # 学科关键词映射
        discipline_keywords = {
            '经济学': ['经济', '金融', '财政', '贸易', '产业', '市场', '投资', '消费'],
            '政治学': ['政治', '政府', '治理', '政策', '制度', '党建', '外交'],
            '教育学': ['教育', '教学', '学校', '课程', '学生', '教师', '学习'],
            '管理学': ['管理', '组织', '企业', '战略', '人力资源', '运营'],
            '法学': ['法律', '法治', '司法', '立法', '权利', '义务', '合同'],
            '社会学': ['社会', '社区', '人口', '家庭', '文化', '民俗'],
            '马克思主义': ['马克思主义', '社会主义', '共产党', '唯物', '辩证'],
            '综合性社会科学': ['综合', '社科', '社会'],
            '高校学报': ['学报', '大学', '高校'],
        }
        
        # 检查学科名称是否匹配
        if discipline in keyword or keyword in discipline:
            return 1.0
        
        # 检查学科相关关键词
        keywords_list = discipline_keywords.get(discipline, [discipline])
        for kw in keywords_list:
            if kw in keyword:
                return 0.9
        
        return 0.3  # 默认较低分数
    
    def _match_topics(self, keyword: str, topics: str) -> float:
        """
        选题相似度
        使用 TF-IDF + 余弦相似度
        """
        if not topics or topics == '0' or topics.strip() == '':
            return 0.0
        
        # 构建文档集合
        documents = [keyword, topics]
        
        try:
            # 简单字符级 TF-IDF
            vectorizer = TfidfVectorizer(
                analyzer='char',
                ngram_range=(1, 2),
                max_features=100
            )
            tfidf_matrix = vectorizer.fit_transform(documents)
            
            # 计算余弦相似度
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return float(similarity)
        except Exception:
            # 降级：简单关键词匹配
            keyword_chars = set(keyword)
            topic_chars = set(topics.replace(' ', ''))
            intersection = len(keyword_chars & topic_chars)
            union = len(keyword_chars | topic_chars)
            return intersection / union if union > 0 else 0.0
    
    def _find_matching_topics(self, keyword: str, topics: str) -> List[str]:
        """找出具体匹配的选题条目"""
        if not topics or topics == '0':
            return []
        
        matching = []
        keyword_lower = keyword.lower()
        
        # 按行分割选题
        topic_lines = topics.split('\n')
        for line in topic_lines:
            line = line.strip()
            if not line or line == '0':
                continue
            
            # 清理编号
            line_clean = re.sub(r'^\d+\.', '', line).strip()
            
            # 检查是否包含关键词
            if any(kw in line_clean for kw in [keyword, keyword_lower]):
                matching.append(line_clean)
        
        return matching


def test_matcher():
    """测试匹配器"""
    matcher = JournalMatcher('/root/.openclaw/workspace-hotspot/cssci_2025_2026_cleaned.csv')
    
    test_keywords = [
        "新质生产力",
        "金融发展",
        "人工智能",
        "乡村振兴",
        "数字经济"
    ]
    
    for kw in test_keywords:
        print(f"\n{'='*60}")
        print(f"选题：{kw}")
        print('='*60)
        
        results = matcher.match(kw, top_n=5)
        for i, r in enumerate(results, 1):
            print(f"{i}. 《{r['期刊名称']}》- {r['级别']} - 匹配度 {r['match_score']:.0f}%")
            if r['matching_topics']:
                print(f"   契合点：{', '.join(r['matching_topics'][:3])}")


if __name__ == '__main__':
    test_matcher()
