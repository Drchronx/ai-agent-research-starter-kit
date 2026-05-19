# 文献综述技能 - 安装指南

## 📦 系统要求

- Python 3.8+
- PostgreSQL 12+
- 网络连接（用于文献检索）

## 🔗 依赖技能

本技能依赖以下外部技能，请确保已安装：

1. **cnki-crawler** - CNKI 爬虫技能
   - 路径：`../cnki-crawler`
   - 功能：爬取 CNKI 期刊论文元数据

2. **academic-research** - OpenAlex 检索技能
   - 路径：`../academic-research`
   - 功能：检索 OpenAlex 英文文献

3. **academic-research-hub** - Google Scholar 检索技能
   - 路径：`../academic-research-hub`
   - 功能：检索 Google Scholar 英文文献

## 📋 安装步骤

### 1. 检查依赖

```bash
cd literature-reviewer-skill-package
python scripts/check_dependencies.py
```

### 2. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

### 3. 配置数据库

```bash
# 复制配置文件
cp .env.example .env

# 编辑 .env，设置数据库连接
CNKI_DB_DSN=postgresql://cnki_user:123456@localhost/cnki_db
```

### 4. 创建数据库（如未创建）

```bash
# 连接 PostgreSQL
psql -U postgres

# 创建数据库和用户
CREATE DATABASE cnki_db;
CREATE USER cnki_user WITH PASSWORD '123456';
GRANT ALL PRIVILEGES ON DATABASE cnki_db TO cnki_user;
\q
```

### 5. 再次检查

```bash
python scripts/check_dependencies.py
```

看到"✅ 所有依赖检查通过"即可开始使用。

## 🚀 快速开始

```bash
python scripts/orchestrator.py "耐心资本" \
  --cnki-keywords "耐心资本，长期资本，战略性投资" \
  --en-keywords "patient capital,long-term capital" \
  --start-year 2020 \
  --end-year 2026
```

## 📊 输出文件

执行完成后，在 `sessions/{timestamp}_{主题}/` 目录下生成：

```
sessions/20260408_220643_供应链韧性/
├── papers_verified.json          # 验证后文献数据
├── phase5_bibliometric.json      # 文献计量分析
├── phase6_methodology.json       # 方法论评价
├── phase7_evolution.json         # 演进分析
└── output/
    ├── bibliometric_report.md    # 文献计量报告
    ├── methodology_report.md     # 方法论评价报告
    ├── evolution_report.md       # 演进分析报告
    └── literature_review_v5.md   # 最终综述
```

## 🔧 故障排查

### 依赖技能找不到

确保技能目录结构正确：
```
skills/
├── Literature-Reviewer-Skill/  # 本技能
├── cnki-crawler/               # 依赖 1
├── academic-research/          # 依赖 2
└── academic-research-hub/      # 依赖 3
```

### 数据库连接失败

检查 PostgreSQL 服务是否运行：
```bash
systemctl status postgresql
```

检查数据库用户权限：
```bash
psql -U cnki_user -d cnki_db -c "SELECT 1"
```

### 检索式验证失败

检查检索式语法：
```bash
python ../cnki-crawler/scripts/validate_query.py "SU=('耐心资本'+'长期资本')"
```

## 📚 更多信息

- 详细使用说明：查看 `SKILL.md`
- 技能功能介绍：查看 `README.md`

## 📞 支持

如有问题，请查看 `SKILL.md` 中的故障排查章节。
