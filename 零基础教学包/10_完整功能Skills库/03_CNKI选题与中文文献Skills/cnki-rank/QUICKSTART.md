# CNKI-Hotspot 快速启动指南

## 🚀 5 分钟快速开始

### 前置条件

1. Python 3.8+
2. PostgreSQL 12+
3. 能访问 CNKI 接口

### 步骤 1：安装依赖

```bash
pip install -r ~/.openclaw/skills/cnki-hotspot/scripts/requirements.txt
```

### 步骤 2：初始化数据库

**方式 A：使用已有数据库**

如果已有 `cnki_user` 用户和 `academic_hotspot` 数据库：

```bash
openclaw exec --skill cnki-hotspot init
```

按提示输入数据库密码即可。

**方式 B：手动创建数据库**

```bash
# 创建数据库
sudo -u postgres psql -c "CREATE DATABASE academic_hotspot OWNER cnki_user;"

# 创建配置文件
cat > ~/.openclaw/skills/cnki-hotspot/config/config.json << 'EOF'
{
  "database": {
    "host": "localhost",
    "port": 5432,
    "dbname": "academic_hotspot",
    "user": "cnki_user",
    "password": "你的密码"
  },
  "report": {
    "output_format": "markdown",
    "feishu_doc_enabled": true,
    "search_top_n": 2,
    "enable_web_search": true
  },
  "_meta": {
    "initialized": true,
    "version": "1.0"
  }
}
EOF

# 初始化表结构
PGPASSWORD=你的密码 psql -h localhost -U cnki_user -d academic_hotspot \
  -f ~/.openclaw/skills/cnki-hotspot/references/schema.sql
```

### 步骤 3：抓取数据

```bash
# 抓取全部榜单（周榜 + 月榜）
openclaw exec --skill cnki-hotspot fetch --scope all
```

### 步骤 4：生成报告

```bash
# 生成周报
openclaw exec --skill cnki-hotspot report --period week

# 保存到文件
openclaw exec --skill cnki-hotspot report --period week --output ~/hotspot_report.md
```

---

## 📋 常用命令

### 数据抓取

```bash
# 抓取周榜
openclaw exec --skill cnki-hotspot fetch --scope week

# 抓取月榜
openclaw exec --skill cnki-hotspot fetch --scope month

# 抓取全部
openclaw exec --skill cnki-hotspot fetch --scope all
```

### 报告生成

```bash
# 周报
openclaw exec --skill cnki-hotspot report --period week

# 月报
openclaw exec --skill cnki-hotspot report --period month

# 创建飞书文档
openclaw exec --skill cnki-hotspot report --period week --feishu
```

### 数据查询

```bash
# 查看当前热榜 TOP10
PGPASSWORD=密码 psql -h localhost -U cnki_user -d academic_hotspot -c \
  "SELECT week_rank, title, pdsi_score FROM cnki_article_hotspot WHERE week_rank IS NOT NULL ORDER BY week_rank LIMIT 10;"

# 查看抓取日志
PGPASSWORD=密码 psql -h localhost -U cnki_user -d academic_hotspot -c \
  "SELECT crawl_time, scope, status, article_count FROM cnki_crawl_log ORDER BY crawl_time DESC LIMIT 5;"

# 查看霸榜文章
PGPASSWORD=密码 psql -h localhost -U cnki_user -d academic_hotspot -c \
  "SELECT title, week_consecutive, week_total_days FROM v_article_dominating ORDER BY week_consecutive DESC;"
```

---

## ⏰ 定时任务配置

### Crontab 示例

```bash
crontab -e
```

添加以下内容：

```cron
# 每周一 9:00 抓取数据并生成周报
0 9 * * 1 openclaw exec --skill cnki-hotspot fetch --scope all && openclaw exec --skill cnki-hotspot report --period week --output /tmp/cnki_weekly.md

# 每月 1 号 10:00 生成月报
0 10 1 * * openclaw exec --skill cnki-hotspot report --period month --output /tmp/cnki_monthly.md
```

### Systemd Timer（可选）

创建服务文件 `/etc/systemd/system/cnki-hotspot.service`：

```ini
[Unit]
Description=CNKI Hotspot Weekly Report
After=network.target postgresql.service

[Service]
Type=oneshot
User=your_user
ExecStart=/root/.openclaw/skills/cnki-hotspot/scripts/fetch_and_report.sh
```

创建定时器 `/etc/systemd/system/cnki-hotspot.timer`：

```ini
[Unit]
Description=Run CNKI Hotspot Weekly
Requires=cnki-hotspot.service

[Timer]
OnCalendar=Mon *-*-* 09:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

启用：

```bash
sudo systemctl enable cnki-hotspot.timer
sudo systemctl start cnki-hotspot.timer
```

---

## 🔧 故障排查

### 问题 1：数据库连接失败

```bash
# 测试连接
PGPASSWORD=密码 psql -h localhost -U cnki_user -d academic_hotspot -c "SELECT 1;"
```

如果失败，检查：
- PostgreSQL 服务是否运行：`pg_isready`
- 密码是否正确
- 用户权限：`sudo -u postgres psql -c "\du cnki_user"`

### 问题 2：CNKI 接口访问失败

```bash
# 测试连接
curl -I https://piccache.cnki.net/kdn/index/kns8s/nvsmscripts/min/nranking.min.js?v=4.2
```

如果返回 418 或其他错误：
- 等待 5-10 分钟后重试（可能触发限流）
- 检查网络连接

### 问题 3：报告为空

```bash
# 检查数据库是否有数据
PGPASSWORD=密码 psql -h localhost -U cnki_user -d academic_hotspot -c \
  "SELECT COUNT(*) FROM cnki_article_hotspot;"
```

如果为 0，先运行抓取：
```bash
openclaw exec --skill cnki-hotspot fetch
```

### 问题 4：网络搜索失败

检查是否能访问 DuckDuckGo：
```bash
curl -I https://api.duckduckgo.com/
```

如果需要代理：
```bash
export HTTP_PROXY=http://proxy:port
export HTTPS_PROXY=http://proxy:port
```

---

## 📞 获取帮助

查看技能文档：
```bash
cat ~/.openclaw/skills/cnki-hotspot/SKILL.md
```

查看日志：
```bash
# 抓取日志
PGPASSWORD=密码 psql -h localhost -U cnki_user -d academic_hotspot -c \
  "SELECT * FROM cnki_crawl_log ORDER BY crawl_time DESC LIMIT 10;"
```

---

## 📊 数据库结构速查

### 主表

| 表名 | 说明 |
|------|------|
| `cnki_article_hotspot` | 论文热榜（当前状态） |
| `cnki_keyword_hotspot` | 热词榜（当前状态） |

### 历史表

| 表名 | 说明 |
|------|------|
| `cnki_article_history` | 论文历史快照 |
| `cnki_keyword_history` | 热词历史快照 |

### 视图

| 视图名 | 说明 |
|--------|------|
| `v_article_dominating` | 霸榜文章（≥3 周） |
| `v_article_newcomers` | 新上榜文章 |
| `v_article_returning` | 卷土重来文章 |
| `v_keyword_dominating` | 霸榜热词 |

---

*最后更新：2026-04-10*
