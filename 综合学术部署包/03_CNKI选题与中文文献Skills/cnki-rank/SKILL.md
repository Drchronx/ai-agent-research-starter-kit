# CNKI-Rank Skill - 知网学术热榜追踪

## 📖 技能说明

本技能用于抓取 CNKI（中国知网）学术热点榜单数据，包括：
- **下载热榜**（周榜/月榜）- 论文下载量排名
- **热词榜**（周榜/月榜）- 搜索关键词热度排名

支持数据持久化、趋势追踪、在榜天数统计，并生成包含网络搜索分析的周报/月报。

## 🚀 快速开始

### 1. 首次使用 - 初始化

```bash
openclaw exec --skill cnki-rank init
```

初始化流程会：
1. 交互式询问数据库配置信息
2. 创建 PostgreSQL 数据库和表结构
3. 生成配置文件 `config/config.json`

### 2. 抓取数据

```bash
# 抓取全部榜单（周榜 + 月榜）
openclaw exec --skill cnki-rank fetch

# 只抓取周榜
openclaw exec --skill cnki-rank fetch --scope week

# 只抓取月榜
openclaw exec --skill cnki-rank fetch --scope month
```

### 3. 生成报告

```bash
# 生成周报
openclaw exec --skill cnki-rank report --period week

# 生成月报
openclaw exec --skill cnki-rank report --period month

# 保存到文件
openclaw exec --skill cnki-rank report --period week --output ~/hotspot_report.md

# 创建飞书文档
openclaw exec --skill cnki-rank report --period week --feishu --title "学术热点周报"
```

### 4. 查询数据

```bash
# 查看当前热榜
openclaw exec --skill cnki-rank list --type article --scope week --top 10

# 查看霸榜文章
openclaw exec --skill cnki-rank list --type article --dominating

# 查看新上榜
openclaw exec --skill cnki-rank list --type article --newcomers

# 查看卷土重来
openclaw exec --skill cnki-rank list --type article --returning
```

## 📁 目录结构

```
~/.openclaw/skills/cnki-rank/
├── SKILL.md                      # 技能说明（本文件）
├── scripts/
│   ├── fetch_cnki.py             # 核心抓取脚本
│   ├── parse_cnki.py             # 数据解析模块
│   ├── db_manager.py             # 数据库操作模块
│   └── report_generator.py       # 报告生成模块
├── references/
│   └── schema.sql                # 数据库表结构
├── config/
│   ├── config.example.json       # 配置模板
│   └── config.json               # 实际配置（初始化后生成）
└── README.md                     # 详细使用说明
```

## ⚙️ 配置说明

### 数据库配置

初始化时会询问以下信息：

```json
{
  "database": {
    "host": "localhost",
    "port": 5432,
    "dbname": "academic_hotspot",
    "user": "your_username",
    "password": "your_password"
  }
}
```

### 报告配置

```json
{
  "report": {
    "output_format": "markdown",
    "feishu_doc_enabled": true,
    "search_top_n": 2,           // 对 TOP N 文章进行网络搜索分析
    "enable_web_search": true,    // 是否启用网络搜索
    "search_threshold": {
      "new_ranking": true,        // 是否搜索新上榜文章
      "returning": true,          // 是否搜索卷土重来文章
      "top_n": 2                  // 对新上榜/卷土重来搜索 TOP N
    }
  }
}
```

## 📊 数据表结构

### 主表（当前状态）

| 表名 | 说明 |
|------|------|
| `cnki_article_hotspot` | 论文热榜主表 |
| `cnki_keyword_hotspot` | 热词榜主表 |

### 历史表（趋势分析）

| 表名 | 说明 |
|------|------|
| `cnki_article_history` | 论文历史快照 |
| `cnki_keyword_history` | 热词历史快照 |

### 日志表

| 表名 | 说明 |
|------|------|
| `cnki_crawl_log` | 抓取任务日志 |
| `cnki_search_analysis` | 网络搜索分析缓存 |

## 🔍 状态说明

### 论文/热词状态

| 状态 | 说明 |
|------|------|
| `new` | 新上榜 |
| `continuing` | 持续在榜 |
| `returning` | 卷土重来（曾下榜后重新上榜） |
| `dropped` | 已下榜 |

### 在榜天数计算

- **周榜**：每次上榜 +7 天
- **月榜**：每次上榜 +30 天
- **连续周数**：连续上榜次数

## ⏰ 定时任务示例

用户可自行配置 cron 定时任务：

```cron
# 每周一 9:00 抓取周榜 + 月榜，生成周报
0 9 * * 1 cd ~/.openclaw/skills/cnki-rank && python3 scripts/fetch_cnki.py --scope all && python3 scripts/report_generator.py --period week --feishu

# 每月 1 号 10:00 生成月报
0 10 1 * * cd ~/.openclaw/skills/cnki-rank && python3 scripts/report_generator.py --period month --feishu --title "CNKI 学术热点月报"
```

## 🛠️ 依赖

- Python 3.8+
- PostgreSQL 12+
- Python 库：
  - `psycopg2-binary`
  - `requests`

安装依赖：
```bash
pip install psycopg2-binary requests
```

## 📝 注意事项

1. **数据库初始化**：首次使用前必须运行 `init` 命令
2. **网络访问**：需要能访问 CNKI 接口（`https://piccache.cnki.net`）
3. **数据累积**：历史数据需要时间累积，初期报告可能不完整
4. **SSL 证书**：CNKI 接口使用 HTTPS，已配置忽略证书验证
5. **搜索限制**：网络搜索功能使用 DuckDuckGo API，可能需要代理

## ⚠️ 已知问题

### 1. 排名不连续

**现象**：报告中排名显示为 6,11,12... 而非 1,2,3...

**原因**：CNKI 接口返回的排名本身就是不连续的（可能过滤了某些学科）

**解决**：正常现象，反映真实榜单排名

### 2. 网络搜索失败

**现象**：报告中显示"搜索失败"或"暂无分析数据"

**原因**：
- DuckDuckGo API 访问受限
- 需要配置 HTTP 代理

**解决**：
```bash
export HTTP_PROXY=http://proxy:port
export HTTPS_PROXY=http://proxy:port
```

### 3. 抓取频率限制

**现象**：418 错误（I'm a teapot）

**原因**：请求过于频繁被 CNKI 限流

**解决**：等待 5-10 分钟后重试，或降低抓取频率

## 🔧 故障排查

### 配置文件丢失

重新运行初始化：
```bash
openclaw exec --skill cnki-rank init --force
```

### 数据库连接失败

检查配置文件中数据库信息是否正确：
```bash
cat ~/.openclaw/skills/cnki-rank/config/config.json
```

测试连接：
```bash
PGPASSWORD=密码 psql -h localhost -U cnki_user -d academic_hotspot -c "SELECT 1;"
```

### 数据抓取失败

检查网络连接：
```bash
curl -I https://piccache.cnki.net/kdn/index/kns8s/nvsmscripts/min/nranking.min.js?v=4.2
```

### 查看抓取日志

```bash
PGPASSWORD=密码 psql -h localhost -U cnki_user -d academic_hotspot -c \
  "SELECT crawl_time, scope, status, article_count, error_message FROM cnki_crawl_log ORDER BY crawl_time DESC LIMIT 10;"
```

## 🔧 故障排查

### 配置文件丢失

重新运行初始化：
```bash
openclaw exec --skill cnki-rank init --force
```

### 数据库连接失败

检查配置文件中数据库信息是否正确，确保 PostgreSQL 服务运行正常。

### 数据抓取失败

检查网络连接，确认能访问 `https://piccache.cnki.net`

## 📈 视图查询

数据库预置了以下视图方便查询：

```sql
-- 霸榜文章
SELECT * FROM v_article_dominating;

-- 新上榜文章
SELECT * FROM v_article_newcomers;

-- 卷土重来文章
SELECT * FROM v_article_returning;

-- 热词霸榜
SELECT * FROM v_keyword_dominating;
```

## 📞 维护

如需重置数据库：
```bash
psql -U your_user -d academic_hotspot -c "DROP TABLE IF EXISTS cnki_article_hotspot, cnki_keyword_hotspot, cnki_article_history, cnki_keyword_history, cnki_crawl_log, cnki_search_analysis CASCADE;"
```

然后重新运行初始化。
