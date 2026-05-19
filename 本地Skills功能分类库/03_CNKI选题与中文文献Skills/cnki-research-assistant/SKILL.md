---
name: cnki-research-assistant
description: CNKI 选题分析助手 - 整合热榜追踪、趋势分析、文献调研、期刊匹配和 6 维度研究空白分析，支持一键自动化分析，为学术选题提供数据驱动的决策支持。
---

# CNKI Research Assistant - 选题分析助手（v2.1）

## 📖 技能说明

本技能整合五个数据源，提供一站式选题分析服务：

| 数据源 | 功能 | 输出 |
|--------|------|------|
| **cnki-rank** | 热点发现 | 下载榜/热词榜排名、在榜天数、状态 |
| **cnki-trend** | 趋势评估 | 年度趋势、学科分布、期刊格局、机构/基金分析 |
| **cnki-crawler** | 文献调研 | 高质量论文元数据、高被引文献识别 |
| **CSSCI 期刊库** | 期刊匹配 | 933 种 C 刊选题方向、匹配度评分 |
| **研究空白分析** | 空白发现 | 关键词/方法/机构/基金/趋势 6 维度分析 |

---

## ⚡ v2.1 重要更新 (2026-04-10)

### Fresh Run 模式

**变更**：每次分析都是独立任务，直接抓取最新数据

| 版本 | 数据策略 | 适用场景 |
|------|---------|---------|
| v2.0 | 累积式（复用数据库历史文献） | ❌ 已废弃 |
| v2.1 | Fresh Run（每次都抓取最新数据） | ✅ 学术热点分析 |

**原因**：
- 学术热点具有时效性，几个月前的数据已过时
- 每次分析应基于最新发表的研究
- 旧任务数据完成后自动清理

**例外**：趋势分析（cnki-trend）需要历史数据，会保留聚合指标

## 🚀 快速开始

### 方式一：一键自动化分析（推荐）

```bash
# Fresh Run 模式：每次都抓取最新数据，完成后自动清理
python scripts/auto_analyzer.py "你的选题关键词"
```

**示例：**
```bash
python scripts/auto_analyzer.py "数字经济"
```

**自动完成：**
1. ✅ 抓取最新文献（约 250 篇，写入临时表）
2. ✅ 深度分析（热榜 + 趋势 + 文献 + 期刊 + 研究空白）
3. ✅ 生成 Markdown 报告 + 5 张可视化图表
4. ✅ 清理临时数据

**预计耗时**：8-15 分钟

**输出：**
- 本地报告：`reports/auto/关键词_分析报告_时间戳.md`
- 图表目录：`reports/auto/charts/` (5 张趋势图)

**数据策略**：
- 每次任务独立，不依赖历史数据
- 使用临时表存储抓取文献
- 分析完成后自动清理临时表

---

### 方式二：分步分析（灵活控制）

```bash
# 完整分析
python scripts/analyzer.py "新质生产力" --full-report --output reports/report.md

# 快速分析（仅热榜 + 趋势 + 期刊）
python scripts/analyzer.py "数字经济" --quick

# 只检查热榜排名
python scripts/analyzer.py "耐心资本" --check-rank

# 只分析趋势（含图表生成）
python scripts/analyzer.py "耐心资本" --check-trend

# 只匹配期刊
python scripts/analyzer.py "乡村振兴" --match-journals --top 10
```

---

### 方式三：保留临时数据（调试用）

```bash
# 分析完成后保留临时表
python scripts/auto_analyzer.py "数字经济" --no-cleanup
```

**适用场景**：调试、复查、二次分析

---

## 📁 目录结构

```
cnki-research-assistant/
├── SKILL.md                          # 本文件
├── README_自动化分析.md                # 自动化分析详细文档
├── QUICK_START.md                    # 快速开始指南
├── scripts/
│   ├── auto_analyzer.py              # 一键自动化分析（v2.1 Fresh Run）
│   ├── analyzer.py                   # 主分析引擎
│   ├── journal_matcher.py            # 期刊匹配模块（支持 Excel）
│   ├── research_gap_analyzer.py      # 研究空白分析模块（6 维度）
│   ├── report_generator.py           # 报告生成模块
│   ├── isolation_manager.py          # 任务隔离管理器
│   ├── init.py                       # 初始化脚本
│   └── requirements.txt              # 依赖列表
├── config/
│   └── config.json                   # 配置文件（初始化后生成）
├── data/
│   ├── STSONG.TTF                    # 中文字体文件
│   └── cssci_2025_2026.csv           # CSSCI 期刊数据
└── reports/
    └── auto/                         # 自动化分析报告输出
        ├── {关键词}_分析报告_{时间戳}.md
        └── charts/                   # 趋势图表
```

---

## ⚠️ 重要说明

### 数据时效性

**v2.1 变更**：
- 每次分析都是 Fresh Run，直接抓取最新数据
- 临时表在分析完成后自动清理
- 不依赖数据库历史文献

**原因**：
- 学术热点具有时效性
- 几个月前的数据已过时
- 确保每次分析基于最新发表的研究

### 趋势分析例外

趋势分析（cnki-trend）调用 CNKI getGroupData API，获取的是全网聚合数据：
- 年度趋势（1980-2026）
- 学科分布
- 期刊格局
- 机构/基金统计

这些数据来自 CNKI 实时计算，不依赖本地数据库。

---

## 📊 分析报告结构

### 1. 执行摘要
- 热度评估（⭐⭐⭐⭐ 4.0/5）
- 发表空间（⭐⭐⭐⭐ 4.5/5）
- 竞争程度评分
- 核心发现（峰值年份、主导学科、推荐期刊）

### 2. 热点扫描 (cnki-rank)
- 当前热榜排名（周榜/月榜）
- 在榜天数统计
- 状态识别（new/continuing/returning/dropped）

### 3. 趋势评估 (cnki-trend)
- 年度趋势图 + 峰值年份
- 近三年占比（判断热度持续性）
- 学科分布（判断学科承载能力）
- 期刊集中度（判断发表空间）
- 头部机构分布（判断研究共同体）
- 基金支持情况（判断项目化程度）
- **可视化图表（6 张 PNG，中文字体已适配）**

### 4. 文献调研 (cnki-crawler)
- 抓取文献数（230+ 篇）
- 高被引文献 Top 10
- 文献统计信息（平均被引、平均下载、年份范围）

### 5. 期刊推荐 (CSSCI 数据)
- 匹配度评分 Top 10 期刊
- 选题契合点说明
- 期刊级别（核心/扩展）
- 投稿策略建议

### 6. 研究空白分析（6 维度，v2.0 新增）💎

| 维度 | 分析内容 | 输出示例 |
|------|---------|---------|
| **关键词共现** | 识别未充分研究的关键词组合 | "高质量发展 + 供应链韧性 研究较少" |
| **主题聚类** | 研究主题分布 | 主题集中度分析 |
| **研究方法** | 实证/理论/案例/仿真等方法多样性 | "缺乏因果推断方法" |
| **机构合作** | 研究机构分布 | "头部机构集中度高" |
| **基金资助** | 资助方向分析 | "主要资助方向：国家社科基金" |
| **时间趋势** | 年度文献量变化 | "近两年文献激增，处于爆发期" |

### 7. 综合评估与建议
- 选题可行性评估（热度/发表空间/竞争程度）
- 潜在切入点（学科交叉/方法创新/视角创新）
- 投稿策略（首选期刊/备选期刊/投稿时机）

---

## ⚙️ 配置说明

### 数据库配置
初始化时自动从 cnki-crawler 继承：
```json
{
  "database": {
    "host": "localhost",
    "port": 5432,
    "dbname": "cnki_db",
    "user": "cnki_user",
    "password": "123456"
  }
}
```

### 代理配置
自动继承 cnki-crawler 的代理，用于 CNKI 接口访问：
```json
{
  "proxy": {
    "http": "http://user:pass@host:port/",
    "https": "http://user:pass@host:port/"
  }
}
```

### CSSCI 数据路径
使用相对路径，支持 Excel 和 CSV 格式（v2.0 新增）：
```json
{
  "cssci_data": {
    "path": "data/中文社会科学引文索引 (CSSCI) 来源期刊目录 (2025-2026).xlsx"
  }
}
```

### 中文字体配置（v2.0 新增）
图表生成使用 `data/STSONG.TTF` 字体文件，中文显示正常。

---

## 🔧 依赖

```bash
pip install -r scripts/requirements.txt
```

**依赖列表**：
- requests (HTTP 请求)
- pandas (数据处理)
- openpyxl (Excel 读取)
- matplotlib (图表生成，中文字体已适配)
- psycopg2-binary (PostgreSQL 连接)
- scikit-learn (文本分析)

---

## 📝 使用示例

### 示例 1：一键自动化分析（推荐）

```bash
python scripts/auto_analyzer.py "数字经济"
```

**输出**：
- 自动抓取 250 篇权威文献
- 完整分析报告（含 6 维度研究空白）
- 6 张可视化图表

### 示例 2：快速评估选题

```bash
python scripts/analyzer.py "人工智能 + 教育" --quick
```

输出摘要报告（不含文献抓取）：
- 热榜排名
- 趋势评分
- 期刊推荐 Top 5
- 研究空白 Top 3

### 示例 3：深度分析

```bash
python scripts/analyzer.py "数据要素市场化" --full-report --output reports/report.md
```

输出完整报告：
- 五大模块完整分析
- 趋势图表附件
- 研究空白识别
- 投稿建议

### 示例 4：仅期刊匹配

```bash
python scripts/analyzer.py "乡村振兴" --match-journals --top 20 --level core
```

只匹配核心期刊，输出 Top 20 推荐。

### 示例 5：指定输出目录

```bash
python scripts/auto_analyzer.py "数字经济" --output-dir /path/to/my/reports
```

---

## ⚠️ 注意事项

### 1. 运行时长

| 分析模式 | 预计时长 |
|---------|---------|
| 一键自动化（含抓取） | 8-15 分钟 |
| 快速分析 (--quick) | 1-2 分钟 |
| 完整分析 (--full-report) | 2-3 分钟 |
| 仅趋势分析 | 2-3 分钟 |

### 2. 代理依赖

CNKI 接口需要代理，请确保：
- cnki-crawler 的 `.env` 文件配置正确
- 代理服务器可用
- 如遇 418 错误，脚本会自动重试（最多 10 次）

### 3. 中文字体（v2.0 已解决）

图表生成使用 `data/STSONG.TTF` 字体文件，中文显示正常。

### 4. 数据库

需要 PostgreSQL 数据库：
- 复用 cnki-crawler 的 `cnki_db`
- cnki-rank 使用 `academic_hotspot`

### 5. 文献抓取策略（v2.1）

- **检索式**：`SU=('关键词')`（主题字段）
- **排序**：按被引频次（CF），确保权威文献
- **页数**：5 页（约 250 篇）
- **存储**：写入临时表（`cnki_papers_temp_{时间戳}`）
- **清理**：分析完成后自动删除临时表

---

## 🔍 匹配算法说明

### 期刊匹配度评分

```
匹配度 = 0.4 × 学科匹配 + 0.4 × 选题相似度 + 0.2 × 级别系数
```

- **学科匹配**：用户选题关键词 vs 期刊学科名称
- **选题相似度**：用户选题关键词 vs 期刊 2026 重点选题（TF-IDF + 余弦相似度）
- **级别系数**：核心来源=1.0，扩展版=0.8

### 研究空白评分（v2.0 新增）

```
空白评分 = 空白程度 + 研究潜力 + 发表空间
```

- **空白程度**：现有研究数量越少，评分越高
- **研究潜力**：热点程度、政策相关性
- **发表空间**：期刊征稿需求、匹配度

---

## 🔧 维护

### 重置配置
```bash
rm config/config.json
python scripts/init.py
```

### 更新 CSSCI 数据
```bash
cp /path/to/new_cssci.xlsx data/
```

### 迁移技能
```bash
# 整个技能目录可迁移到其他位置
cp -r /path/to/cnki-research-assistant /new/location/
cd /new/location/cnki-research-assistant
python scripts/init.py  # 重新初始化
```

### 查看配置
```bash
cat config/config.json
```

### 测试运行
```bash
# 测试期刊匹配器
python scripts/journal_matcher.py

# 测试研究空白分析（6 维度）
python scripts/research_gap_analyzer.py

# 测试自动化分析
python scripts/auto_analyzer.py "测试关键词" --no-crawl
```

---

## 📞 故障排查

### 问题 1：数据库连接失败

**症状**：热点扫描或文献调研模块失败

**解决**：
1. 检查 PostgreSQL 服务是否运行
2. 验证 `config/config.json` 中的数据库配置
3. 测试连接：`PGPASSWORD=123456 psql -h localhost -U cnki_user -d cnki_db`

### 问题 2：CNKI 接口 418 错误

**症状**：趋势分析模块失败

**解决**：
1. 检查代理配置是否正确
2. 脚本会自动重试（最多 10 次）
3. 如持续失败，更新代理配置

### 问题 3：图表中文乱码

**症状**：趋势图表中文字符显示为方框

**解决**：
1. 检查字体文件是否存在：`ls -la data/STSONG.TTF`
2. 字体文件已配置，如仍有问题请重新初始化

### 问题 4：CSSCI 数据文件不存在

**症状**：期刊匹配模块失败

**解决**：
```bash
python scripts/init.py  # 重新初始化
```

### 问题 5：文献抓取失败

**症状**：抓取结果为 0

**解决**：
1. 检查代理：`python /root/.openclaw/skills/cnki-crawler/scripts/proxy_check.py`
2. 验证检索式：`python /root/.openclaw/skills/cnki-crawler/scripts/validate_query.py "SU=('数字经济')"`

---

## 📚 相关文档

| 文档 | 说明 |
|------|------|
| `README_自动化分析.md` | 一键自动化分析详细文档 |
| `QUICK_START.md` | 快速开始指南 |
| `reports/auto/` | 自动化分析报告输出目录 |

---

## 📈 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| v2.1 | 2026-04-10 | **Fresh Run 模式**：每次独立任务、临时表存储、自动清理 |
| v2.0 | 2026-04-10 | 新增一键自动化分析、6 维度研究空白分析、中文字体适配、CSSCI Excel 支持 |
| v1.0 | 2026-04-08 | 初始版本 |

---

*最后更新：2026-04-10 | 版本：2.0.0*
