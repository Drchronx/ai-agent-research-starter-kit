#!/usr/bin/env python3
"""
生成完整的参考文献列表
"""

import json
import sys
from pathlib import Path
from datetime import datetime

def generate_references(session_dir: Path, output_path: Path):
    """生成完整的参考文献列表"""
    
    # 加载验证后的论文
    papers_path = session_dir / "papers_verified.json"
    with open(papers_path, 'r', encoding='utf-8') as f:
        papers = json.load(f)
    
    # 分离中英文
    zh_papers = [p for p in papers if p.get('language') == 'zh']
    en_papers = [p for p in papers if p.get('language') == 'en']
    
    print(f"生成参考文献：中文 {len(zh_papers)} 篇，英文 {len(en_papers)} 篇")
    
    # 生成 GB/T 7714-2015 格式
    lines = [
        "# 参考文献 (References)",
        "",
        f"**生成时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**文献总数:** {len(papers)} 篇",
        f"**中文文献:** {len(zh_papers)} 篇",
        f"**英文文献:** {len(en_papers)} 篇",
        "",
        "---",
        "",
        "## 中文文献 (Chinese Literature)",
        "",
    ]
    
    # 中文文献
    for i, p in enumerate(zh_papers, 1):
        authors = p.get('authors', [])
        if isinstance(authors, list):
            # 清理作者格式（去除 [1], [2] 等标记）
            authors = [a.replace('[1]', '').replace('[2]', '').replace('[3]', '').strip() for a in authors]
            authors_str = ', '.join(authors[:3])
            if len(authors) > 3:
                authors_str += ', 等'
        else:
            authors_str = str(authors)
        
        year = p.get('year', 'n.d.')
        title = p.get('title', '无标题').replace('免费', '').strip()
        journal = p.get('journal', '无期刊')
        url = p.get('source_url', '')
        
        lines.append(f"**[C{i}]** {authors_str} ({year}). {title}. {journal}." + (f" URL: {url}" if url else "") + "\n")
    
    lines.extend([
        "---",
        "",
        "## English Literature",
        "",
    ])
    
    # 英文文献
    for i, p in enumerate(en_papers, 1):
        authors = p.get('authors', [])
        if isinstance(authors, list):
            authors_str = ', '.join([str(a) for a in authors[:3]])
            if len(authors) > 3:
                authors_str += ', et al.'
        else:
            authors_str = str(authors)
        
        year = p.get('year', 'n.d.')
        title = p.get('title', 'No Title').strip()
        journal = p.get('journal', 'No Journal')
        doi = p.get('doi', '')
        url = p.get('source_url', '')
        
        citation = f"**[E{i}]** {authors_str} ({year}). {title}. {journal}."
        if doi:
            citation += f" DOI: {doi}."
        if url:
            citation += f" URL: {url}."
        
        lines.append(citation + "\n")
    
    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"✓ 参考文献已保存到：{output_path}")
    print(f"  总行数：{len(lines)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python generate_references.py <session_dir>")
        sys.exit(1)
    
    session_dir = Path(sys.argv[1])
    output_path = session_dir / "output" / "references_full.md"
    generate_references(session_dir, output_path)
