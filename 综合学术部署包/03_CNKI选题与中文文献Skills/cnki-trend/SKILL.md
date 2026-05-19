---
name: cnki-trend
description: Crawl CNKI `getGroupData` for a specific keyword, keep only non-empty group results, and generate a trend-analysis report with charts focused on the current year, recent yearly momentum, topic concentration, subject and journal concentration, author and institution distribution, and fund signals. Use when the user asks for a CNKI keyword trend report, a 知网关键词趋势分析, a 年度趋势汇报, or wants CNKI data fetched first and then interpreted.
---

# CNKI Keyword Trend Report

Use this skill from `/root/.openclaw/workspace-hotspot/skills/cnki-trend`.

## Workflow

1. Install the local dependencies if needed:

```powershell
python -m pip install -r scripts/requirements.txt
```

2. Run the report script:

```powershell
python scripts/cnki_keyword_trend_report.py "耐心资本" --print-report
```

**Cookie 自动获取**：脚本默认会自动调用 `generate_client_id()` 动态获取 `Ecp_ClientId`，无需手动配置。

3. Read the generated files in `reports/`:
- `<keyword>_valid_groups.json`
- `<keyword>_trend_report.md`
- `charts/*.png`

4. Use only the valid groups in follow-up analysis. Ignore groups with empty responses.

## Behavior

- **Cookie 管理**（v2.0 新增）：
  - 默认自动调用 `generate_client_id()` 动态获取 `Ecp_ClientId`（与 cnki-crawler 一致的方法）
  - 支持通过 `--ecp-client-id` 参数或 `CNKI_ECP_CLIENT_ID` 环境变量手动指定
  - 自动获取失败时回退到内置默认值

- The script hits CNKI `kvisual8/article/getGroupData`.
- It tests the known candidate groups, drops empty responses, and keeps unique `(groupName, groupCode)` pairs only.
- It writes raw valid-group data to JSON for traceability.
- It writes a Markdown report that interprets:
  - yearly distribution, peak year, recent-three-year share, and current-year YTD caveat
  - major and secondary topic concentration
  - subject concentration
  - journal concentration
  - author and institution dispersion
  - fund support signals
- It renders chart images in `reports/charts/` and prefers Chinese-capable fonts such as `Microsoft YaHei` or `SimHei`.

## Parameters

- **Cookie 自动获取**（默认行为）：
  ```powershell
  # 不传 --ecp-client-id 时，脚本自动调用 generate_client_id() 获取
  python scripts/cnki_keyword_trend_report.py "耐心资本" --print-report
  ```

- **手动指定 Cookie**（可选）：
  ```powershell
  # 方式 1：命令行参数
  python scripts/cnki_keyword_trend_report.py "耐心资本" --ecp-client-id "<your-client-id>"
  
  # 方式 2：环境变量（优先级高于自动获取）
  $env:CNKI_ECP_CLIENT_ID="<your-client-id>"
  python scripts/cnki_keyword_trend_report.py "耐心资本"
  ```

- **Change output directory**:
  ```powershell
  python scripts/cnki_keyword_trend_report.py "耐心资本" --output-dir "reports/cnki"
  ```

## Interpretation Rules

- Treat current-year counts as year-to-date values unless the year is complete.
- Do not assume `sum(y)` equals unique paper count for topic, subject, author, institution, or fund groups. One paper can contribute to multiple buckets.
- If the journal group collapses to a single source, call out that the sample may be too narrow for whole-CNKI conclusions.
- Prefer trend wording such as “集中”“扩散”“头部明显”“分散” over hard causal claims.
