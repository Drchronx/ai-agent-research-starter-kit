#!/usr/bin/env python3
"""
文献综述工作流 - 主协调器 (v5.2 重构版)

核心改进:
- 每个会话完全独立的数据存储
- CNKI 爬取后立即导出到会话目录
- 后续分析只使用本会话数据文件
- 数据库仅作为临时存储

用法:
    python orchestrator.py <topic> <chinese_keywords> <english_keywords>
    python orchestrator.py "耐心资本" "耐心资本，长期资本，长期投资" "patient capital,long-term investment"
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import psycopg2


class LiteratureReviewOrchestrator:
    """文献综述工作流协调器"""

    def __init__(
        self,
        topic: str,
        chinese_keywords: List[str],
        english_keywords: List[str],
        start_year: int = 2020,
        end_year: int = 2025,
        base_dir: Optional[Path] = None
    ):
        self.topic = topic
        self.chinese_keywords = chinese_keywords
        self.english_keywords = english_keywords
        self.start_year = start_year
        self.end_year = end_year
        # base_dir 默认为 scripts 的父目录（即 skill 根目录）
        self.base_dir = base_dir or Path(__file__).parent.parent

        # 生成唯一 session ID（包含时间戳，确保唯一性）
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        topic_short = topic.replace(' ', '_').replace('/', '_')[:30]
        self.session_id = f"{timestamp}_{topic_short}"
        self.session_dir = self.base_dir / "sessions" / self.session_id

        # 工作流状态
        self.workflow_status = {
            'session_id': self.session_id,
            'topic': topic,
            'created_at': datetime.now().isoformat(),
            'phases': {}
        }

        # 数据库配置
        self.db_dsn = "postgresql://cnki_user:123456@localhost/cnki_db"

    def log(self, message: str, level: str = "INFO"):
        """打印日志"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] [{level}] {message}")

    def setup_session(self) -> bool:
        """Phase 0: 创建会话目录"""
        self.log(f"创建会话目录：{self.session_dir}")
        self.session_dir.mkdir(parents=True, exist_ok=True)
        (self.session_dir / "output").mkdir(exist_ok=True)

        # 保存元数据
        metadata = {
            'session_id': self.session_id,
            'topic': self.topic,
            'topic_english': self.topic,
            'created_at': datetime.now().isoformat(),
            'chinese_keywords': self.chinese_keywords,
            'english_keywords': self.english_keywords,
            'year_range': {
                'start': self.start_year,
                'end': self.end_year
            },
            'backends': ['cnki-crawler', 'academic-research', 'academic-research-hub'],
            'workflow_status': self.workflow_status,
            'data_files': {}  # 记录数据文件路径
        }

        with open(self.session_dir / "metadata.json", 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        self.log("✓ Phase 0 完成：会话初始化")
        self.workflow_status['phases']['phase_0'] = 'completed'
        return True

    def run_phase_1_2_cnki_retrieval(self) -> bool:
        """Phase 1-2: CNKI 检索（v2.0 多排序策略）"""
        self.log("Phase 1-2: 执行 CNKI 检索...")

        # 构建 CNKI 查询
        cnki_query = "SU=(" + ' + '.join([f"'{kw}'" for kw in self.chinese_keywords]) + ")"
        
        self.log(f"CNKI 查询：{cnki_query}")
        self.log(f"年份范围：{self.start_year}-{self.end_year}")

        # 验证检索式
        self.log("验证检索式语法...")
        validate_result = subprocess.run(
            ['python', 'scripts/validate_query.py', cnki_query],
            cwd='/root/.openclaw/skills/cnki-crawler',
            capture_output=True,
            text=True
        )
        
        if validate_result.returncode != 0:
            self.log(f"检索式验证失败:\n{validate_result.stderr}", "ERROR")
            return False
        
        self.log("✓ 检索式验证通过")

        # 4 种排序策略
        sort_fields = [
            ('DFR', '下载频次'),
            ('CF', '被引频次'),
            ('PT', '发表时间'),
            ('ZH', '综合排序')
        ]

        cnki_crawler_dir = Path('/root/.openclaw/skills/cnki-crawler')
        
        for sort_field, sort_name in sort_fields:
            self.log(f"爬取 {sort_name} Top 100...")
            
            cmd = [
                'python', 'scripts/main.py',
                cnki_query,
                '--sort-field', sort_field,
                '--limit-pages', '2',
                '--start-year', str(self.start_year),
                '--end-year', str(self.end_year)
            ]
            
            result = subprocess.run(cmd, cwd=cnki_crawler_dir, capture_output=True, text=True)
            
            if result.returncode != 0:
                self.log(f"{sort_name} 爬取失败：{result.stderr}", "WARNING")
            else:
                self.log(f"✓ {sort_name} 爬取完成")

        # 导出 CNKI 数据到会话目录
        self.log("导出 CNKI 数据到会话目录...")
        cnki_output = self.session_dir / "papers_cnki_raw.json"
        
        # 不传 query-pattern（因为数据库 search_terms 字段存储的是实际检索词，不是完整检索式）
        # 只按年份过滤，导出最近爬取的所有文献
        export_cmd = [
            'python', 'scripts/export_to_json.py',
            str(cnki_output),
            '--start-year', str(self.start_year),
            '--end-year', str(self.end_year)
        ]
        
        export_result = subprocess.run(export_cmd, cwd=cnki_crawler_dir, capture_output=True, text=True)
        
        if export_result.returncode != 0:
            self.log(f"导出失败：{export_result.stderr}", "ERROR")
            return False
        
        # 统计导出数量
        with open(cnki_output, 'r', encoding='utf-8') as f:
            cnki_papers = json.load(f)
        
        self.log(f"✓ CNKI 数据已导出：{len(cnki_papers)} 篇")
        
        # 更新元数据
        metadata_path = self.session_dir / "metadata.json"
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        metadata['data_files']['papers_cnki_raw.json'] = str(cnki_output)
        metadata['cnki_count'] = len(cnki_papers)
        
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        self.workflow_status['phases']['phase_1_2'] = 'completed'
        return True

    def run_phase_3_english_retrieval(self) -> bool:
        """Phase 3: 英文文献检索"""
        self.log("Phase 3: 执行英文文献检索...")

        english_query = ' OR '.join([f'"{kw}"' for kw in self.english_keywords])
        
        # OpenAlex
        self.log("检索 OpenAlex...")
        openalex_output = self.session_dir / "papers_openalex_raw.json"
        
        oa_cmd = [
            'python3', '/root/.openclaw/skills/academic-research/scripts/scholar-search.py',
            'search', english_query,
            '--limit', '50',
            '--json',
            '--years', f'{self.start_year}-{self.end_year}'
        ]
        
        try:
            result = subprocess.run(oa_cmd, capture_output=True, text=True, timeout=120)
            with open(openalex_output, 'w', encoding='utf-8') as f:
                f.write(result.stdout)
            
            with open(openalex_output, 'r', encoding='utf-8') as f:
                oa_papers = json.load(f)
            
            self.log(f"✓ OpenAlex: {len(oa_papers)} 篇")
        except Exception as e:
            self.log(f"OpenAlex 检索失败：{e}", "WARNING")
            # 创建空文件
            with open(openalex_output, 'w', encoding='utf-8') as f:
                json.dump([], f)
            oa_papers = []

        # Google Scholar（可选）
        self.log("检索 Google Scholar...")
        scholar_output = self.session_dir / "papers_scholar_raw.json"
        
        try:
            gs_cmd = [
                'python', '/root/.openclaw/skills/academic-research-hub/scripts/research.py',
                english_query,
                '--max-results', '30',
                '--start-year', str(self.start_year),
                '--end-year', str(self.end_year),
                '--format', 'json'
            ]
            result = subprocess.run(gs_cmd, capture_output=True, text=True, timeout=120)
            
            with open(scholar_output, 'w', encoding='utf-8') as f:
                f.write(result.stdout)
            
            with open(scholar_output, 'r', encoding='utf-8') as f:
                scholar_papers = json.load(f)
            
            self.log(f"✓ Google Scholar: {len(scholar_papers)} 篇")
        except Exception as e:
            self.log(f"Google Scholar 检索失败：{e}", "WARNING")
            with open(scholar_output, 'w', encoding='utf-8') as f:
                json.dump([], f)
            scholar_papers = []

        # 合并英文文献
        en_papers = oa_papers + scholar_papers
        
        # 标准化并保存
        all_en_output = self.session_dir / "papers_en_raw.json"
        with open(all_en_output, 'w', encoding='utf-8') as f:
            json.dump(en_papers, f, ensure_ascii=False, indent=2)
        
        self.log(f"✓ 英文文献总计：{len(en_papers)} 篇")
        
        # 更新元数据
        metadata_path = self.session_dir / "metadata.json"
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        metadata['data_files']['papers_en_raw.json'] = str(all_en_output)
        metadata['en_count'] = len(en_papers)
        
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        self.workflow_status['phases']['phase_3'] = 'completed'
        return True

    def run_phase_4_deduplication(self) -> bool:
        """Phase 4: 去重"""
        self.log("Phase 4: 执行去重...")

        # 加载所有文献
        cnki_path = self.session_dir / "papers_cnki_raw.json"
        en_path = self.session_dir / "papers_en_raw.json"
        
        with open(cnki_path, 'r', encoding='utf-8') as f:
            cnki_papers = json.load(f)
        
        with open(en_path, 'r', encoding='utf-8') as f:
            en_papers = json.load(f)
        
        # 合并
        all_papers = cnki_papers + en_papers
        self.log(f"合并后文献总数：{len(all_papers)} 篇")

        # 去重逻辑
        seen_dois = set()
        seen_titles = set()
        unique_papers = []
        duplicates = 0

        for p in all_papers:
            doi = p.get('doi', '').strip()
            title = p.get('title', '').strip().lower()
            
            # DOI 去重
            if doi and doi in seen_dois:
                duplicates += 1
                continue
            
            # 标题去重
            if title and title in seen_titles:
                duplicates += 1
                continue
            
            seen_dois.add(doi)
            seen_titles.add(title)
            unique_papers.append(p)

        # 保存去重后的文献
        dedup_output = self.session_dir / "papers_deduplicated.json"
        with open(dedup_output, 'w', encoding='utf-8') as f:
            json.dump(unique_papers, f, ensure_ascii=False, indent=2)

        self.log(f"✓ 去重完成：删除 {duplicates} 篇重复，剩余 {len(unique_papers)} 篇")

        # 保存去重报告
        report_path = self.session_dir / "dedup_report.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"# 去重报告\n\n")
            f.write(f"- 原始文献：{len(all_papers)} 篇\n")
            f.write(f"- 删除重复：{duplicates} 篇\n")
            f.write(f"- 唯一文献：{len(unique_papers)} 篇\n")
            f.write(f"- CNKI: {len(cnki_papers)} 篇\n")
            f.write(f"- 英文：{len(en_papers)} 篇\n")

        # 更新元数据
        metadata_path = self.session_dir / "metadata.json"
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        metadata['data_files']['papers_deduplicated.json'] = str(dedup_output)
        metadata['dedup_count'] = len(unique_papers)
        
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        self.workflow_status['phases']['phase_4'] = 'completed'
        return True

    def run_phase_5_verification(self) -> bool:
        """Phase 5: 验证"""
        self.log("Phase 5: 执行验证...")

        dedup_path = self.session_dir / "papers_deduplicated.json"
        
        with open(dedup_path, 'r', encoding='utf-8') as f:
            papers = json.load(f)

        # 验证逻辑（只要求标题）
        verified_papers = []
        failed_papers = []

        for p in papers:
            title = p.get('title', '').strip()
            
            if title:
                verified_papers.append(p)
            else:
                failed_papers.append(p)

        # 保存验证后的文献
        verified_output = self.session_dir / "papers_verified.json"
        with open(verified_output, 'w', encoding='utf-8') as f:
            json.dump(verified_papers, f, ensure_ascii=False, indent=2)

        self.log(f"✓ 验证完成：通过 {len(verified_papers)} 篇，失败 {len(failed_papers)} 篇")

        # 保存验证报告
        report_path = self.session_dir / "verification_report.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"# 验证报告\n\n")
            f.write(f"- 验证总数：{len(papers)} 篇\n")
            f.write(f"- 验证通过：{len(verified_papers)} 篇\n")
            f.write(f"- 验证失败：{len(failed_papers)} 篇\n")
            f.write(f"- 验证标准：标题字段必填\n")

        # 更新元数据
        metadata_path = self.session_dir / "metadata.json"
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        metadata['data_files']['papers_verified.json'] = str(verified_output)
        metadata['verified_count'] = len(verified_papers)
        
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        self.workflow_status['phases']['phase_5'] = 'completed'
        return True

    def run_phase_6_bibliometrics(self) -> bool:
        """Phase 6: 文献计量分析"""
        self.log("Phase 6: 执行文献计量分析...")

        output_path = self.session_dir / "output" / "bibliometric_report.md"

        cmd = [
            'python', 'scripts/phase5_bibliometric.py',
            str(self.session_dir)
        ]

        result = subprocess.run(cmd, cwd=self.base_dir, capture_output=True, text=True)
        
        if result.returncode != 0:
            self.log(f"文献计量分析失败：{result.stderr}", "ERROR")
            return False

        self.log(f"✓ 文献计量分析完成：{output_path}")

        # 保存 JSON 结果
        json_path = self.session_dir / "phase6_bibliometric.json"
        if (self.session_dir / 'output' / 'phase5_bibliometric.json').exists():
            import shutil
            shutil.copy(self.session_dir / 'output' / 'phase5_bibliometric.json', json_path)

        self.workflow_status['phases']['phase_6'] = 'completed'
        return True

    def run_phase_7_methodology(self) -> bool:
        """Phase 7: 方法论评价"""
        self.log("Phase 7: 执行方法论评价...")

        output_path = self.session_dir / "output" / "methodology_report.md"

        cmd = [
            'python', 'scripts/phase6_methodology.py',
            str(self.session_dir)
        ]

        result = subprocess.run(cmd, cwd=self.base_dir, capture_output=True, text=True)
        
        if result.returncode != 0:
            self.log(f"方法论评价失败：{result.stderr}", "ERROR")
            return False

        self.log(f"✓ 方法论评价完成：{output_path}")

        # 保存 JSON 结果
        json_path = self.session_dir / "phase7_methodology.json"
        if (self.session_dir / 'output' / 'phase6_methodology.json').exists():
            import shutil
            shutil.copy(self.session_dir / 'output' / 'phase6_methodology.json', json_path)

        self.workflow_status['phases']['phase_7'] = 'completed'
        return True

    def run_phase_8_evolution(self) -> bool:
        """Phase 8: 演进分析（完全动态）"""
        self.log("Phase 8: 执行演进分析...")

        verified_path = self.session_dir / "papers_verified.json"
        output_path = self.session_dir / "output" / "evolution_report.md"

        cmd = [
            'python', 'phase7_evolution.py',
            str(verified_path),
            '--output', str(output_path)
        ]

        result = subprocess.run(cmd, cwd=self.base_dir / 'scripts', capture_output=True, text=True)
        
        if result.returncode != 0:
            self.log(f"演进分析失败：{result.stderr}", "ERROR")
            return False

        self.log(f"✓ 演进分析完成：{output_path}")

        # 保存 JSON 结果
        json_path = self.session_dir / "phase8_evolution.json"
        if (self.session_dir / 'output' / 'phase7_evolution.json').exists():
            import shutil
            shutil.copy(self.session_dir / 'output' / 'phase7_evolution.json', json_path)

        self.workflow_status['phases']['phase_8'] = 'completed'
        return True

    def run_phase_9_11_synthesis(self) -> bool:
        """Phase 9-11: 核心论文分析 + 引用格式化 + 综述撰写"""
        self.log("Phase 9-11: 执行综合撰写...")

        # 调用综合撰写脚本
        cmd = [
            'python', 'phase10_final_review_v5.py',
            str(self.session_dir),
            self.topic
        ]

        result = subprocess.run(cmd, cwd=self.base_dir / 'scripts', capture_output=True, text=True, timeout=600)
        
        if result.returncode != 0:
            self.log(f"综合撰写失败：{result.stderr}", "ERROR")
            return False

        self.log(f"✓ 综合撰写完成")

        self.workflow_status['phases']['phase_9_11'] = 'completed'
        return True

    def save_workflow_status(self):
        """保存工作流状态"""
        metadata_path = self.session_dir / "metadata.json"
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        metadata['workflow_status'] = self.workflow_status
        metadata['completed_at'] = datetime.now().isoformat()
        
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

    def run(self):
        """执行完整工作流"""
        self.log("=" * 60)
        self.log(f"文献综述工作流 v5.2 - {self.topic}")
        self.log("=" * 60)

        try:
            # Phase 0
            if not self.setup_session():
                return False

            # Phase 1-2
            if not self.run_phase_1_2_cnki_retrieval():
                return False

            # Phase 3
            if not self.run_phase_3_english_retrieval():
                return False

            # Phase 4
            if not self.run_phase_4_deduplication():
                return False

            # Phase 5
            if not self.run_phase_5_verification():
                return False

            # Phase 6
            if not self.run_phase_6_bibliometrics():
                return False

            # Phase 7
            if not self.run_phase_7_methodology():
                return False

            # Phase 8
            if not self.run_phase_8_evolution():
                return False

            # Phase 9-11
            if not self.run_phase_9_11_synthesis():
                return False

            # 保存状态
            self.save_workflow_status()

            self.log("=" * 60)
            self.log("✓ 文献综述工作流完成!")
            self.log(f"会话目录：{self.session_dir}")
            self.log("=" * 60)

            return True

        except Exception as e:
            self.log(f"工作流执行失败：{e}", "ERROR")
            self.save_workflow_status()
            return False


def main():
    parser = argparse.ArgumentParser(description='文献综述工作流协调器')
    parser.add_argument('topic', type=str, help='研究主题')
    parser.add_argument('--cnki-keywords', type=str, required=True, help='中文关键词（逗号分隔）')
    parser.add_argument('--en-keywords', type=str, required=True, help='英文关键词（逗号分隔）')
    parser.add_argument('--start-year', type=int, default=2020, help='起始年份')
    parser.add_argument('--end-year', type=int, default=2025, help='结束年份')
    parser.add_argument('--base-dir', type=str, default=None, help='基础目录')

    args = parser.parse_args()

    # 支持中文和英文逗号分隔
    cnki_keywords_str = args.cnki_keywords.replace('，', ',')
    en_keywords_str = args.en_keywords.replace('，', ',')
    
    orchestrator = LiteratureReviewOrchestrator(
        topic=args.topic,
        chinese_keywords=[k.strip() for k in cnki_keywords_str.split(',') if k.strip()],
        english_keywords=[k.strip() for k in en_keywords_str.split(',') if k.strip()],
        start_year=args.start_year,
        end_year=args.end_year,
        base_dir=Path(args.base_dir) if args.base_dir else None
    )

    success = orchestrator.run()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
