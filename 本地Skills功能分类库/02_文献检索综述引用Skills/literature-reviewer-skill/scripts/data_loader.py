#!/usr/bin/env python3
"""
统一数据加载器 - 加载并标准化多后端文献数据

功能：
- 加载 CNKI、OpenAlex、Google Scholar 的原始数据
- 标准化字段名到统一 schema
- 合并为单一 JSON 文件
- 输出加载报告
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class DataLoader:
    """统一数据加载器"""

    # 字段映射表：后端字段 -> 统一字段
    FIELD_MAPPINGS = {
        'cnki': {
            'title': 'title',
            'authors': 'authors',
            'journal': 'journal',
            'year': 'year',
            'abstract': 'abstract',
            'keywords': 'keywords',
            'doi': 'doi',
            'url': 'source_url',
            'cited_count': 'cited_count',  # CNKI 被引频次
            'download_count': 'download_count',  # CNKI 下载频次
        },
        'openalex': {
            'title': 'title',
            'authors': 'authors',
            'source': 'journal',  # 关键字段映射
            'publication_year': 'year',
            'abstract': 'abstract',
            'keywords': 'keywords',
            'doi': 'doi',
            'landing_url': 'source_url',
            'cited_by_count': 'cited_count',
        },
        'scholar': {
            'title': 'title',
            'authors': 'authors',
            'venue': 'journal',  # 关键字段映射
            'year': 'year',
            'snippet': 'abstract',  # 关键字段映射
            'url': 'source_url',
            'citations': 'cited_count',
        }
    }

    def __init__(self, session_dir: Path):
        self.session_dir = session_dir
        self.load_report = {
            'timestamp': datetime.now().isoformat(),
            'backends': {},
            'total_loaded': 0,
            'total_standardized': 0,
            'warnings': []
        }

    def load_cnki_papers(self) -> List[Dict]:
        """加载 CNKI 论文"""
        cnki_path = self.session_dir / "papers_raw_cnki.json"
        if not cnki_path.exists():
            self.load_report['warnings'].append("CNKI 数据文件不存在")
            return []

        with open(cnki_path, 'r', encoding='utf-8') as f:
            papers = json.load(f)

        self.load_report['backends']['cnki'] = {
            'raw_count': len(papers),
            'file': str(cnki_path)
        }

        standardized = []
        for i, paper in enumerate(papers):
            std = self._standardize_paper(paper, 'cnki')
            if std:
                standardized.append(std)
            else:
                self.load_report['warnings'].append(
                    f"CNKI 论文 {i+1}: 标准化失败 - 缺少标题"
                )

        return standardized

    def load_openalex_papers(self) -> List[Dict]:
        """加载 OpenAlex 论文"""
        path = self.session_dir / "papers_raw_openalex.json"
        if not path.exists():
            self.load_report['warnings'].append("OpenAlex 数据文件不存在")
            return []

        with open(path, 'r', encoding='utf-8') as f:
            papers = json.load(f)

        self.load_report['backends']['openalex'] = {
            'raw_count': len(papers),
            'file': str(path)
        }

        standardized = []
        for i, paper in enumerate(papers):
            std = self._standardize_paper(paper, 'openalex')
            if std:
                standardized.append(std)
            else:
                self.load_report['warnings'].append(
                    f"OpenAlex 论文 {i+1}: 标准化失败 - 缺少标题"
                )

        return standardized

    def load_scholar_papers(self) -> List[Dict]:
        """加载 Google Scholar 论文"""
        path = self.session_dir / "papers_raw_scholar.json"
        if not path.exists():
            self.load_report['warnings'].append("Google Scholar 数据文件不存在")
            return []

        with open(path, 'r', encoding='utf-8') as f:
            papers = json.load(f)

        self.load_report['backends']['google_scholar'] = {
            'raw_count': len(papers),
            'file': str(path)
        }

        standardized = []
        for i, paper in enumerate(papers):
            std = self._standardize_paper(paper, 'scholar')
            if std:
                standardized.append(std)
            else:
                self.load_report['warnings'].append(
                    f"Google Scholar 论文 {i+1}: 标准化失败 - 缺少标题"
                )

        return standardized

    def _standardize_paper(self, paper: Dict, backend: str) -> Optional[Dict]:
        """标准化单篇论文的字段"""
        mappings = self.FIELD_MAPPINGS.get(backend, {})

        # 提取标题（必需字段）
        title = paper.get('title', '').strip()
        if not title:
            return None

        # 构建标准化记录
        std = {
            'source_db': backend,
            'backend': {
                'cnki': 'cnki-crawler',
                'openalex': 'academic-research',
                'scholar': 'academic-research-hub'
            }[backend],
            'backend_query': '',  # 后续填充
            'language': 'zh' if backend == 'cnki' else 'en',
        }

        # 字段映射
        for source_field, target_field in mappings.items():
            value = paper.get(source_field)
            if value is not None:
                std[target_field] = value

        # 特殊处理：OpenAlex 的 abstract_inverted_index
        if backend == 'openalex' and not std.get('abstract'):
            abstract_idx = paper.get('abstract_inverted_index', {})
            if abstract_idx:
                # 重建 abstract
                words = sorted(
                    [(word, idx) for word, indices in abstract_idx.items() for idx in indices],
                    key=lambda x: x[1]
                )
                std['abstract'] = ' '.join([word for word, _ in words])

        # 特殊处理：authors 可能是对象列表
        authors = std.get('authors', [])
        if authors and isinstance(authors[0], dict):
            if 'display_name' in authors[0]:  # OpenAlex 格式
                std['authors'] = [a.get('display_name', '') for a in authors[:5]]
            elif 'name' in authors[0]:
                std['authors'] = [a.get('name', '') for a in authors[:5]]

        # 确保 authors 是字符串列表
        if not isinstance(std.get('authors', []), list):
            std['authors'] = []

        # 设置默认值
        std.setdefault('journal', std.get('source', ''))
        std.setdefault('year', paper.get('publication_year'))
        std.setdefault('abstract', std.get('snippet', ''))
        std.setdefault('doi', '')
        std.setdefault('source_url', std.get('landing_url', ''))
        # cited_count 默认值：优先使用已映射的值，其次尝试不同后端的字段名
        if 'cited_count' not in std:
            std['cited_count'] = paper.get('cited_count') or paper.get('citations') or 0
        std.setdefault('download_count', paper.get('download_count', 0))
        std.setdefault('keywords', [])

        return std

    def merge_and_save(self, output_file: str = "papers_raw_merged.json"):
        """合并所有后端数据并保存"""
        print("=" * 60)
        print("数据加载与标准化")
        print("=" * 60)

        # 优先使用 retrieval_coordinator.py 生成的 papers_raw.json
        papers_raw_path = self.session_dir / "papers_raw.json"
        if papers_raw_path.exists():
            print(f"\n检测到检索协调器输出：{papers_raw_path}")
            with open(papers_raw_path, 'r', encoding='utf-8') as f:
                all_papers = json.load(f)
            
            # 统计
            zh_count = sum(1 for p in all_papers if p.get('language') == 'zh')
            en_count = sum(1 for p in all_papers if p.get('language') == 'en')
            
            self.load_report['total_loaded'] = len(all_papers)
            self.load_report['total_standardized'] = len(all_papers)
            self.load_report['language_stats'] = {'zh': zh_count, 'en': en_count}
            
            # 保存合并后的数据
            output_path = self.session_dir / output_file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(all_papers, f, ensure_ascii=False, indent=2)
            
            print(f"\n✓ 已保存到：{output_path}")
            print(f"\n汇总:")
            print(f"  总文献数：{len(all_papers)}")
            print(f"  中文文献：{zh_count}")
            print(f"  英文文献：{en_count}")
            
            # 保存加载报告
            report_path = self.session_dir / "load_report.json"
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(self.load_report, f, ensure_ascii=False, indent=2)
            
            print("\n" + "=" * 60)
            return all_papers
        
        # 否则从独立文件加载
        all_papers = []

        print("\n[1/3] 加载 CNKI 数据...")
        cnki_papers = self.load_cnki_papers()
        all_papers.extend(cnki_papers)
        print(f"  ✓ CNKI: {len(cnki_papers)} 篇")

        print("\n[2/3] 加载 OpenAlex 数据...")
        openalex_papers = self.load_openalex_papers()
        all_papers.extend(openalex_papers)
        print(f"  ✓ OpenAlex: {len(openalex_papers)} 篇")

        print("\n[3/3] 加载 Google Scholar 数据...")
        scholar_papers = self.load_scholar_papers()
        all_papers.extend(scholar_papers)
        print(f"  ✓ Google Scholar: {len(scholar_papers)} 篇")

        # 统计
        self.load_report['total_loaded'] = len(cnki_papers) + len(openalex_papers) + len(scholar_papers)
        self.load_report['total_standardized'] = len(all_papers)

        # 按语言统计
        zh_count = sum(1 for p in all_papers if p.get('language') == 'zh')
        en_count = sum(1 for p in all_papers if p.get('language') == 'en')
        self.load_report['language_stats'] = {'zh': zh_count, 'en': en_count}

        # 保存合并后的数据
        output_path = self.session_dir / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(all_papers, f, ensure_ascii=False, indent=2)

        print(f"\n✓ 已保存到：{output_path}")
        print(f"\n汇总:")
        print(f"  总文献数：{len(all_papers)}")
        print(f"  中文文献：{zh_count}")
        print(f"  英文文献：{en_count}")

        # 保存加载报告
        report_path = self.session_dir / "load_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.load_report, f, ensure_ascii=False, indent=2)

        if self.load_report['warnings']:
            print(f"\n⚠️ 警告 ({len(self.load_report['warnings'])} 条):")
            for w in self.load_report['warnings'][:5]:
                print(f"  - {w}")
            if len(self.load_report['warnings']) > 5:
                print(f"  ... 还有 {len(self.load_report['warnings']) - 5} 条")

        print("\n" + "=" * 60)
        return all_papers


def main():
    if len(sys.argv) < 2:
        print("用法：python data_loader.py <session_dir>")
        sys.exit(1)

    session_dir = Path(sys.argv[1])
    if not session_dir.exists():
        print(f"错误：目录不存在 - {session_dir}")
        sys.exit(1)

    loader = DataLoader(session_dir)
    papers = loader.merge_and_save()

    if len(papers) == 0:
        print("错误：未加载到任何文献")
        sys.exit(1)


if __name__ == "__main__":
    main()
