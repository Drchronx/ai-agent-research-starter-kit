# CNKI Research Assistant - 快速指南

## 🚀 5 分钟快速开始

### 1. 初始化（首次使用）

```bash
cd /path/to/cnki-research-assistant
python scripts/init.py
```

### 2. 运行分析

```bash
# 快速分析（1-2 分钟）
python scripts/analyzer.py "新质生产力" --quick

# 完整分析（3-5 分钟）
python scripts/analyzer.py "新质生产力" --full-report --output reports/report.md
```

### 3. 查看报告

```bash
cat reports/report.md
```

---

## 📊 输出示例

### 命令行输出

```
================================================================================
📊 CNKI 选题分析报告：新质生产力
================================================================================
生成时间：2026-04-10 20:56:00

🔥【热点扫描】
   周榜排名：7
   月榜排名：7
   在榜天数：22
   状态：continuing

📈【趋势评估】
   峰值年份：2025 年 (18503 篇)
   近三年占比：99.4%
   主导学科：经济体制改革 (22.4%)
   期刊分布：190 种 (low 集中度)

📄【文献调研】
   相关论文：25 篇
   高被引 Top 1: 数字化转型赋能企业新质生产力 (84 次)

📚【期刊推荐 Top 5】
   1. 《经济经纬》- 匹配度 41% (核心)
   2. 《科技进步与对策》- 匹配度 40% (核心)
   3. 《科技与出版》- 匹配度 39% (核心)
   4. 《河南大学学报 (社会科学版)》- 匹配度 39% (核心)
   5. 《国际商务 (对外经济贸易大学报)》- 匹配度 38% (核心)

💡【研究空白 Top 3】
   1. 新兴热点空白 (⭐⭐⭐⭐)
      近三年研究占比 99.4%，峰值出现在 2025 年...
   2. 期刊发表空白 (⭐⭐⭐⭐)
      期刊覆盖广泛（190 种），集中度低...
   3. 期刊选题空白 (⭐⭐⭐⭐)
      部分期刊征稿方向研究较少...

================================================================================
✅ 分析完成！
```

### Markdown 报告

包含以下章节：
1. 执行摘要
2. 热点扫描
3. 趋势评估（含图表）
4. 文献调研
5. 期刊推荐
6. 研究空白分析
7. 综合评估与建议

---

## 🔧 常见问题

### Q1: 数据库连接失败

```bash
# 检查 PostgreSQL 服务
systemctl status postgresql

# 测试连接
psql -h localhost -U cnki_user -d cnki_db

# 重新初始化
python scripts/init.py
```

### Q2: CNKI 接口 418 错误

脚本会自动重试（最多 10 次），如持续失败：

```bash
# 检查代理配置
cat config/config.json | grep proxy

# 更新 cnki-crawler 的代理
vim /root/.openclaw/workspace-hotspot/skills/cnki-crawler/.env
```

### Q3: 图表中文乱码

```bash
# 安装中文字体
sudo apt install fonts-wqy-zenhei

# 或修改 matplotlib 配置
echo "plt.rcParams['font.sans-serif'] = ['Arial']" >> scripts/cnki_keyword_trend_report.py
```

### Q4: CSSCI 数据文件不存在

```bash
# 重新初始化
python scripts/init.py
```

---

## 📁 文件说明

| 文件 | 说明 |
|------|------|
| `scripts/analyzer.py` | 主分析引擎 |
| `scripts/journal_matcher.py` | 期刊匹配模块 |
| `scripts/research_gap_analyzer.py` | 研究空白分析模块 |
| `scripts/report_generator.py` | 报告生成模块 |
| `scripts/init.py` | 初始化脚本 |
| `config/config.json` | 配置文件 |
| `data/cssci_2025_2026.csv` | CSSCI 期刊数据 |
| `reports/` | 输出报告目录 |

---

## 🎯 使用技巧

### 1. 批量分析多个选题

```bash
for keyword in "新质生产力" "数字经济" "乡村振兴"; do
    python scripts/analyzer.py "$keyword" --quick
done
```

### 2. 仅分析特定模块

```bash
# 只检查热榜
python scripts/analyzer.py "选题" --check-rank

# 只匹配期刊
python scripts/analyzer.py "选题" --match-journals --top 20
```

### 3. 自定义输出路径

```bash
python scripts/analyzer.py "选题" --full-report --output /path/to/output.md
```

---

## 📞 技术支持

如遇问题，检查以下配置：

1. **Python 依赖**：`pip list | grep -E "requests|pandas|sklearn"`
2. **数据库连接**：`cat config/config.json`
3. **CSSCI 数据**：`ls -lh data/cssci_2025_2026.csv`
4. **代理配置**：`cat config/config.json | grep proxy`

---

*版本：1.0.0 | 最后更新：2026-04-10*
