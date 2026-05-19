---
name: cnki-crawler
description: Crawl CNKI journal paper metadata with the local Python crawler and save to PostgreSQL. Supports multi-sort retrieval (DFR/CF/PT/ZH) and mandatory query validation. Use when the user asks to collect CNKI papers, run the CNKI crawler, or query by CNKI field patterns.
---

# CNKI Crawler (v2.0)

**核心改进:**
- ✅ 支持 4 种排序策略（DFR/CF/PT/ZH）
- ✅ 检索式强制验证（执行前拦截错误）
- ✅ 多排序抓取 + 去重（覆盖热点 + 权威 + 最新 + 高相关）

---

## 快速启动

### 1. 环境准备

```bash
cd /root/.openclaw/skills/cnki-crawler

# 安装依赖
python -m pip install -r requirements.txt

# 创建本地配置
cp .env.example .env
# 编辑 .env 设置 CNKI_DB_DSN, CNKI_PROXY_HTTP, CNKI_PROXY_HTTPS
```

### 2. 检索式验证（强制）

```bash
# 验证检索式语法
python scripts/validate_query.py "SU=('耐心资本'+'长期资本')"
# ✅ 验证通过才能执行爬取
```

### 3. 单排序抓取

```bash
# 按被引频次 Top 100
python scripts/main.py "SU=('耐心资本'+'长期资本')" --sort-field CF --limit-pages 2

# 按发表时间 Top 100
python scripts/main.py "SU=('耐心资本'+'长期资本')" --sort-field PT --limit-pages 2

# 按下载频次 Top 100
python scripts/main.py "SU=('耐心资本'+'长期资本')" --sort-field DFR --limit-pages 2

# 按综合排序 Top 100
python scripts/main.py "SU=('耐心资本'+'长期资本')" --sort-field ZH --limit-pages 2
```

### 4. 多排序抓取（推荐）

```bash
# 4 种排序各抓 Top 100，去重后约 200-300 篇高质量文献
python scripts/main.py "SU=('耐心资本'+'长期资本')" --sort-field DFR --limit-pages 2
python scripts/main.py "SU=('耐心资本'+'长期资本')" --sort-field CF --limit-pages 2
python scripts/main.py "SU=('耐心资本'+'长期资本')" --sort-field PT --limit-pages 2
python scripts/main.py "SU=('耐心资本'+'长期资本')" --sort-field ZH --limit-pages 2
```

### 5. 带年份范围

```bash
# 2020-2026 年，按被引频次
python scripts/main.py "SU=('耐心资本'+'长期资本')" --sort-field CF --limit-pages 2 --start-year 2020 --end-year 2026
```

---

## CLI 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `query_pattern` | CNKI 专业检索式（必填） | - |
| `--sort-field` | 排序字段：PT/CF/DFR/ZH | `PT` |
| `--sort-type` | 排序方式：asc/desc | `desc` |
| `--start-year` | 起始年份 | 无限制 |
| `--end-year` | 结束年份 | 无限制 |
| `--limit-pages` | 最多爬取页数 | 无限制 |
| `--validate-only` | 只验证检索式，不爬取 | `False` |
| `--no-db` | 不写入数据库 | `False` |
| `--print-result` | 打印结果（仅小数据集） | `False` |

---

## 排序字段说明

| 代码 | 含义 | 适用场景 |
|------|------|----------|
| `PT` | 发表时间 | 获取最新研究 |
| `CF` | 被引频次 | 获取权威文献 |
| `DFR` | 下载频次 | 获取热点文献 |
| `ZH` | 综合排序 | 获取相关度最高 |

---

## 检索式语法

### 基本规则

**必须遵守:**
1. 字段代码来自官方字段表（SU/TI/KY/AB/AU 等）
2. 检索值使用英文半角单引号 `'...'`
3. `and`/`or`/`not` 前后必须有空格
4. 年份范围使用 `--start-year/--end-year`，不写入检索式
5. 字段内多词使用 `+` 号连接，不是逗号

### 正确示例

```text
SU=('耐心资本'+'长期资本'+'战略性投资')
TI='生态' and KY='生态文明'
SU=('经济发展'+'可持续发展') * '转变' - '泡沫'
```

### 错误示例

```text
# ❌ 使用逗号分隔
SU=('耐心资本，长期资本，战略性投资')

# ❌ 年份写入检索式
SU='耐心资本' and YE='2025'

# ❌ 字段代码错误
SUB='耐心资本'  # 应为 SU

# ❌ 逻辑运算符缺少空格
SU='test'and KY='test2'
```

---

## 检索式验证器

### 使用方式

```bash
# CLI 独立调用
python scripts/validate_query.py "SU=('耐心资本'+'长期资本')"

# 程序调用
from validate_query import validate_cnki_query
valid, errors = validate_cnki_query("SU=('耐心资本'+'长期资本')")
if not valid:
    for err in errors:
        print(err)
```

### 验证规则

1. **字段代码验证** - 必须在官方字段表中
2. **年份检查** - 不能出现在检索式中
3. **引号检查** - 必须使用英文半角单引号
4. **逻辑运算符格式** - `and`/`or`/`not` 前后必须有空格
5. **括号匹配** - 左右括号数量必须相等
6. **常见错误检测** - 逗号分隔、字段代码拼写错误等

---

## 项目结构

```
cnki-crawler/
├── scripts/
│   ├── main.py              # CLI 入口
│   ├── crawl.py             # 爬虫核心逻辑
│   ├── validate_query.py    # 检索式验证器 (v2.0 新增)
│   ├── cnki_db.py           # PostgreSQL 持久化
│   ├── proxy_check.py       # 代理验证
│   └── settings.py          # 配置
├── reference/
│   └── 专业检索语法.md       # 检索式语法速查
├── .env                     # 本地配置
├── .env.example             # 配置模板
└── requirements.txt         # 依赖
```

---

## 数据库 Schema

```sql
CREATE TABLE cnki_papers (
    search_id TEXT PRIMARY KEY,  -- md5(title + journal + year)
    title TEXT,
    authors TEXT[],
    journal TEXT,
    year TEXT,
    issue TEXT,
    publish_date TEXT,
    abstract TEXT,
    keywords TEXT[],
    organizations TEXT[],
    funds TEXT[],
    cited_count TEXT,
    download_count TEXT,
    detail_url TEXT,
    query_pattern TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 多排序抓取策略

### 为什么需要多排序？

单一排序可能遗漏重要文献：
- 仅按时间：错过经典高被引文献
- 仅按被引：错过最新前沿研究
- 仅按下载：错过学术深度文献

### 推荐策略

```bash
# 4 种排序各抓 Top 100
DFR: 下载频次 → 热点文献
CF: 被引频次 → 权威文献
PT: 发表时间 → 最新研究
ZH: 综合排序 → 高相关文献

# 预期结果
原始数据：4 × 100 = 400 篇
去重后：约 200-300 篇高质量文献
```

### 去重逻辑

1. **DOI 精确去重**（优先）
2. **标题相似度去重**（阈值 0.85）
3. **保留质量更高版本**（被引 + 下载更多）

---

## 常见用法

### 快速测试

```bash
# 验证检索式
python scripts/main.py "SU='耐心资本'" --validate-only

# 爬取 1 页测试
python scripts/main.py "SU='耐心资本'" --limit-pages 1 --print-result
```

### 生产环境

```bash
# 多排序完整抓取
python scripts/main.py "SU=('耐心资本'+'长期资本')" --sort-field DFR --limit-pages 2
python scripts/main.py "SU=('耐心资本'+'长期资本')" --sort-field CF --limit-pages 2
python scripts/main.py "SU=('耐心资本'+'长期资本')" --sort-field PT --limit-pages 2
python scripts/main.py "SU=('耐心资本'+'长期资本')" --sort-field ZH --limit-pages 2
```

### 导出 JSON

```bash
# 导出数据库中所有文献
python scripts/export_to_json.py /output/path/papers.json 500

# 导出特定查询的文献
python scripts/export_to_json.py /output/path/papers.json 500
```

---

## 故障排查

### 检索式验证失败

```bash
# 错误：SU 字段内应使用 + 号连接关键词，不是逗号
# 解决：SU=('A'+'B') 而不是 SU=('A','B')

# 错误：字段代码 'SUB' 应为 'SU'
# 解决：使用官方字段代码

# 错误：年份过滤应使用 --start-year/--end-year 参数
# 解决：年份不写入检索式
```

### 爬取结果为 0

1. 检查检索式语法（使用 `validate_query.py`）
2. 确认关键词使用 `+` 号连接
3. 确认代理可用（`python scripts/proxy_check.py`）

### 数据库连接失败

1. 检查 `.env` 中的 `CNKI_DB_DSN`
2. 确认 PostgreSQL 服务运行
3. 确认用户权限

---

## 维护

- **检索式验证规则** - `scripts/validate_query.py`
- **爬虫核心逻辑** - `scripts/crawl.py`
- **数据库 Schema** - `scripts/cnki_db.py`
- **默认参数** - `scripts/settings.py`
- **检索语法参考** - `reference/专业检索语法.md`

---

*最后更新：2026-04-08 (v2.0)*
