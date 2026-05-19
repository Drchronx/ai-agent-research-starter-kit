# Literature Reviewer - Multi-Backend Integration

## 📊 整合架构

本技能现已整合三个检索后端，形成完整的文献检索与综述工作流：

```
┌─────────────────────────────────────────────────────────────┐
│                    Literature Reviewer Skill                 │
│                     (总协调器 / 8 阶段工作流)                   │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐   ┌─────────────────┐   ┌───────────────────┐
│  cnki-crawler │   │academic-research│   │academic-research- │
│   (CNKI 知网)   │   │  (OpenAlex)     │   │   hub (Google     │
│   中文文献     │   │   英文文献 (主)   │   │     Scholar)      │
│               │   │                 │   │   英文文献 (补充)   │
└───────────────┘   └─────────────────┘   └───────────────────┘
```

## 🚀 快速开始

### 方式一：使用统一协调器（推荐）

```bash
cd /root/.openclaw/skills/Literature-Reviewer-Skill/scripts

python retrieval_coordinator.py \
  --cnki-query "SU='耐心资本'" \
  --english-query "patient capital" \
  --start-year 2020 \
  --end-year 2025 \
  --output-dir ./sessions/20240408_patient_capital
```

### 方式二：单独调用各后端

#### 1. CNKI 检索
```bash
cd /root/.openclaw/skills/cnki-crawler

# 首次使用需配置 .env
cp .env.example .env
# 编辑 .env 设置 CNKI_DB_DSN, CNKI_PROXY_HTTP, CNKI_PROXY_HTTPS

python scripts/main.py "SU='耐心资本'" \
  --start-year 2020 \
  --end-year 2025 \
  --limit-pages 10
```

#### 2. OpenAlex 检索
```bash
cd /root/.openclaw/skills/academic-research

python3 scripts/scholar-search.py search "patient capital" \
  --limit 50 \
  --from-year 2020 \
  --to-year 2025 \
  --json > openalex_results.json
```

#### 3. Google Scholar 检索
```bash
cd /root/.openclaw/skills/academic-research-hub

python scripts/research.py "patient capital" \
  --max-results 30 \
  --start-year 2020 \
  --end-year 2025 \
  --format json \
  --output scholar_results.json
```

## 📁 输出结构

```
sessions/{YYYYMMDD}_{topic}/
├── session_log.md              # 会话日志（含后端状态）
├── metadata.json               # 元数据
├── papers_raw.json             # 原始检索结果（合并三个后端）
├── papers_deduplicated.json    # 去重后结果
├── papers_analysis.json        # 文献分析结果
└── output/
    ├── references.md           # 参考文献列表
    ├── papers_analysis.md      # 文献分析报告
    ├── outline.md              # 综述大纲
    ├── draft.md                # 综述初稿
    ├── review_report.md        # 评审报告
    └── literature_review.md    # 最终综述文档
```

## 🔄 完整工作流

```
Phase 0: Session Log       → 创建会话文件夹和检查点
    ↓
Phase 1: Query Analysis    → 生成中英文关键词 + 后端查询
    ↓
Phase 2: Backend Retrieval → 并行调用三个检索后端
    ├── cnki-crawler (中文)
    ├── academic-research (英文 - 主)
    └── academic-research-hub (英文 - 补充)
    ↓
Phase 3: Deduplication     → DOI + 标题相似度去重
    ↓
Phase 4: Verification      → 元数据质量验证
    ↓
Phase 5: Data Export       → 导出参考文献
    ↓
Phase 6: Paper Analysis    → 单篇文献深度分析
    ↓
Phase 7: Citation Format   → GB/T 7714-2015 格式化
    ↓
Phase 8: Synthesis         → 大纲 → 初稿 → 评审 → 终稿
```

## 📋 后端对比

| 特性 | CNKI | OpenAlex | Google Scholar |
|------|------|----------|----------------|
| **数据源** | 知网期刊 | 2.5 亿 + 论文 | 学术网页 |
| **语言** | 中文 | 英文 | 多语言 |
| **API Key** | 需配置代理 | 免费无 key | 免费无 key |
| **检索速度** | 慢（爬虫） | 快（API） | 中（爬虫） |
| **元数据质量** | 高 | 高 | 中 |
| **全文链接** | 需订阅 | 部分开放获取 | 部分开放获取 |
| **引用数** | ✅ | ✅ | ✅ |
| **超时时间** | 5 分钟 | 5 分钟 | 5 分钟 |
| **重试次数** | 3 次 | 3 次 | 3 次 |

## ⚠️ 注意事项

### CNKI
- 必须配置代理（`CNKI_PROXY_HTTP`, `CNKI_PROXY_HTTPS`）
- 专业检索语法需参考 `../cnki-crawler/reference/专业检索语法.md`
- 年份通过 `--start-year/--end-year` 参数传递，**不要**嵌入检索式

### OpenAlex
- 免费 API 有速率限制，建议单次不超过 100 条
- 支持 DOI、作者、引用链检索
- 适合深度挖掘和高被引论文检索

### Google Scholar
- 有反爬虫机制，"Unusual traffic detected" 时需等待 10-15 分钟
- 建议每小时不超过 50 次检索
- 适合补充最新会议论文和预印本

## 🔧 故障排除

### 某个后端失败怎么办？

1. 检查 `session_log.md` 中的错误信息
2. 如其他后端成功且论文总数 ≥20，可继续工作流
3. 如论文不足，考虑：
   - 调整检索词（扩大范围）
   - 延长年份范围
   - 稍后重试失败的后端

### 去重后论文太少？

- 降低标题相似度阈值（默认 0.85 → 0.80）
- 检查是否有大量论文因 DOI 重复被移除
- 考虑保留不同语言版本（中文 + 英文）

## 📖 相关文档

- **后端配置详情**: `references/search-backends.md`
- **CNKI 检索语法**: `../cnki-crawler/reference/专业检索语法.md`
- **引用格式规范**: `references/gb-t-7714-2015.md`
- **主技能文档**: `SKILL.md`

## 🧪 测试建议

等待老师提供测试需求后，建议测试以下场景：

1. **基础测试**: 单一主题，中英文文献均有
2. **压力测试**: 大检索量（100+ 论文），测试去重和性能
3. **边界测试**: 某个后端失败时的容错能力
4. **质量测试**: 综述文档的学术质量和引用准确性
