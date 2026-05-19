# CNKI-Hotspot 技能

## 概述

本技能用于抓取和分析 CNKI（中国知网）学术热点榜单数据，支持：

- ✅ 下载热榜（周榜/月榜）
- ✅ 热词榜（周榜/月榜）
- ✅ 数据持久化（PostgreSQL）
- ✅ 趋势追踪（在榜天数、连续周数）
- ✅ 状态识别（新上榜/持续/回归/下榜）
- ✅ 网络搜索分析
- ✅ 周报/月报生成
- ✅ 飞书文档集成

## ⚡ 快速开始

```bash
# 1. 安装依赖
pip install -r scripts/requirements.txt

# 2. 初始化（交互式配置数据库）
openclaw exec --skill cnki-hotspot init

# 3. 抓取数据
openclaw exec --skill cnki-hotspot fetch

# 4. 生成周报
openclaw exec --skill cnki-hotspot report --period week
```

详细指南请参阅 [QUICKSTART.md](QUICKSTART.md)

## 快速开始

### 1. 安装依赖

```bash
pip install psycopg2-binary requests
```

### 2. 初始化

```bash
openclaw exec --skill cnki-hotspot init
```

### 3. 抓取数据

```bash
openclaw exec --skill cnki-hotspot fetch
```

### 4. 生成报告

```bash
openclaw exec --skill cnki-hotspot report --period week --feishu
```

## 详细文档

请参阅 [SKILL.md](SKILL.md) 获取完整使用说明。

## 数据流

```
CNKI 接口 → 抓取脚本 → 解析模块 → 数据库管理 → 报告生成
   ↓                                           ↓
JavaScript                                  Markdown
   ↓                                           ↓
parse_cnki.py                            report_generator.py
   ↓                                           ↓
db_manager.py                            飞书文档/文件
   ↓
PostgreSQL
```

## 核心功能

### 抓取 (fetch_cnki.py)

- 请求 CNKI 接口
- 解析 JavaScript 返回数据
- 识别新上榜/持续/回归/下榜
- 更新在榜天数和连续周数
- 记录历史快照

### 解析 (parse_cnki.py)

- 提取 4 个榜单数据：
  - `articleRecommendweek` - 论文周榜
  - `articleRecommendmonth` - 论文月榜
  - `hotSearchweek` - 热词周榜
  - `hotSearchmonth` - 热词月榜
- 标准化数据结构
- 错误处理

### 数据库 (db_manager.py)

- 连接管理
- CRUD 操作
- 状态对比
- 历史快照
- 视图查询

### 报告 (report_generator.py)

- 生成 Markdown 报告
- 网络搜索分析
- 飞书文档集成
- 自定义配置

## 数据库表

### 主表

| 表名 | 说明 | 更新频率 |
|------|------|----------|
| `cnki_article_hotspot` | 论文热榜 | 每周/月 |
| `cnki_keyword_hotspot` | 热词榜 | 每周/月 |

### 历史表

| 表名 | 说明 | 用途 |
|------|------|------|
| `cnki_article_history` | 论文历史 | 趋势分析 |
| `cnki_keyword_history` | 热词历史 | 趋势分析 |

### 辅助表

| 表名 | 说明 |
|------|------|
| `cnki_crawl_log` | 抓取日志 |
| `cnki_search_analysis` | 搜索缓存 |

## 配置

配置文件位于 `config/config.json`，包含：

```json
{
  "database": {...},
  "report": {
    "enable_web_search": true,
    "search_top_n": 2,
    ...
  }
}
```

## 定时任务

建议配置 cron 定时任务：

```cron
# 每周一抓取 + 生成周报
0 9 * * 1 openclaw exec --skill cnki-hotspot fetch && openclaw exec --skill cnki-hotspot report --period week --feishu
```

## 故障排查

### 常见问题

1. **配置文件不存在** → 运行 `init` 命令
2. **数据库连接失败** → 检查配置和网络
3. **抓取失败** → 检查 CNKI 接口可访问性
4. **报告为空** → 先运行 `fetch` 抓取数据

### 日志查看

```bash
psql -U user -d academic_hotspot -c "SELECT * FROM cnki_crawl_log ORDER BY crawl_time DESC LIMIT 10;"
```

## 扩展

### 添加新榜单

1. 在 `parse_cnki.py` 中添加解析逻辑
2. 在 `schema.sql` 中添加对应表结构
3. 在 `db_manager.py` 中添加处理方法

### 自定义报告

修改 `report_generator.py` 中的 `generate_report()` 函数。

## 维护

### 数据清理

```sql
-- 清理 1 年前的历史数据
DELETE FROM cnki_article_history WHERE snapshot_date < NOW() - INTERVAL '1 year';
DELETE FROM cnki_keyword_history WHERE snapshot_date < NOW() - INTERVAL '1 year';
```

### 重置技能

```bash
# 删除配置
rm config/config.json

# 删除数据库表
psql -U user -d academic_hotspot -c "DROP TABLE IF EXISTS ... CASCADE;"

# 重新初始化
openclaw exec --skill cnki-hotspot init
```

## 版本

- v1.0 - 初始版本 (2026-04-10)
  - 支持四个榜单抓取
  - 数据库持久化
  - 趋势追踪
  - 报告生成

## 踩坑记录

### 1. SSL 证书验证失败

**错误**：`SSL: CERTIFICATE_VERIFY_FAILED`

**解决**：在 requests 中禁用证书验证
```python
requests.get(url, verify=False)
urllib3.disable_warnings()
```

### 2. JavaScript 解析失败

**错误**：`Expecting property name enclosed in double quotes`

**原因**：CNKI 返回的是 JavaScript 对象，键名无双引号

**解决**：添加 `js_to_json()` 函数转换
```python
def js_to_json(js_str):
    return re.sub(r'([{,]\s*)([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1"\2":', js_str)
```

### 3. 数据库游标类型错误

**错误**：`tuple indices must be integers or slices, not str`

**原因**：`cursor.fetchone()` 返回 tuple 而非 dict

**解决**：使用 `RealDictCursor`
```python
with conn.cursor(cursor_factory=RealDictCursor) as cur:
    row = cur.fetchone()
    return dict(row) if row else None
```

### 4. 418 限流错误

**错误**：`418 Client Error: I'm a teapot`

**原因**：请求过于频繁被 CNKI 限流

**解决**：
- 等待 5-10 分钟后重试
- 降低抓取频率（建议每周 1 次）

### 5. 网络搜索模块导入

**错误**：`No module named 'web_search'`

**原因**：`web_search` 是 OpenClaw 工具，不是 Python 模块

**解决**：直接调用 DuckDuckGo API
```python
url = f"https://api.duckduckgo.com/?q={quote(query)}&format=json"
```

## 许可证

PolyForm Noncommercial License 1.0.0

