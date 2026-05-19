#!/bin/bash
# CNKI-Hotspot 一键抓取并生成报告脚本
# 用于定时任务

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="/tmp/cnki_reports"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 日期格式
DATE=$(date +%Y%m%d)
WEEK=$(date +%G-W%V)

echo "=========================================="
echo "CNKI-Hotspot 自动抓取 $(date)"
echo "=========================================="

# 抓取数据
echo "[1/3] 正在抓取 CNKI 数据..."
python3 "$SCRIPT_DIR/fetch_cnki.py" --scope all

if [ $? -ne 0 ]; then
    echo "❌ 数据抓取失败"
    exit 1
fi

echo "✅ 数据抓取成功"

# 生成周报
echo "[2/3] 正在生成周报..."
python3 "$SCRIPT_DIR/report_generator.py" --period week \
    --output "$OUTPUT_DIR/weekly_${DATE}.md"

if [ $? -ne 0 ]; then
    echo "❌ 周报生成失败"
    exit 1
fi

echo "✅ 周报生成成功：$OUTPUT_DIR/weekly_${DATE}.md"

# 如果是周一，同时生成月报
DAY_OF_WEEK=$(date +%u)
if [ "$DAY_OF_WEEK" -eq 1 ]; then
    echo "[3/3] 正在生成月报..."
    python3 "$SCRIPT_DIR/report_generator.py" --period month \
        --output "$OUTPUT_DIR/monthly_${DATE}.md"
    
    if [ $? -ne 0 ]; then
        echo "⚠️  月报生成失败（跳过）"
    else
        echo "✅ 月报生成成功：$OUTPUT_DIR/monthly_${DATE}.md"
    fi
fi

# 清理旧报告（保留最近 4 周）
echo "清理旧报告..."
cd "$OUTPUT_DIR"
ls -t weekly_*.md 2>/dev/null | tail -n +5 | xargs -r rm
ls -t monthly_*.md 2>/dev/null | tail -n +13 | xargs -r rm

echo "=========================================="
echo "✅ 任务完成"
echo "最新周报：$OUTPUT_DIR/weekly_${DATE}.md"
echo "=========================================="
