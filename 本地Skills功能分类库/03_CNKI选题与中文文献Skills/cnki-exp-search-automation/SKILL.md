---
name: cnki-exp-search-automation
description: CNKI（中国知网）高级搜索自动化技能。使用浏览器自动化技术搜索文献并获取结果列表及摘要信息。建议在有头浏览器环境下使用以便于处理反机器人验证。
author: OpenClaw
version: 0.0.3
date: 2026-03-16
tags:
  - cnki
  - 中国知网
  - 文献检索
  - 学术搜索
  - 浏览器自动化
  - 摘要提取
categories:
  - 学术研究
  - 数据采集
requires:
  - browser: 浏览器工具（建议使用有头浏览器以便处理验证）
  - network: 网络访问 CNKI
references:
  - cnki-fields.md: CNKI专业检索字段一览表
  - query-examples.md: CNKI专业检索查询案例
notes: |
  - 反机器人验证需要用户自行解决：当出现滑块验证、点选验证或验证码时，需要用户手动完成验证
  - 建议在有头浏览器（headful）环境下使用，无头模式可能触发验证
  - 请合理控制请求频率，遵守CNKI服务条款
  - 本技能通过 OpenClaw 的 browser 工具执行浏览器操作
  - 建议设置 profile="user" 使用用户浏览器以便处理验证码
permissions:
  - browser: 控制浏览器访问网页
  - storage: 读写文件保存数据
features:
  - CNKI高级搜索/专业检索
  - 批量获取搜索结果列表
  - 文章详情页摘要提取
  - 反机器人验证处理（需用户手动完成）
  - 多页结果翻页提取
usage: |
  ## 快速开始

  ### 示例命令
  
  **搜索文献：**
  在CNKI上搜索"结膜松弛的治疗"相关文献
  
  **获取摘要：**
  获取某篇CNKI文章的摘要信息
  
  ---
---

# CNKI 高级搜索自动化技能

## 技能描述

CNKI（中国知网）高级搜索自动化技能。利用 OpenClaw 浏览器工具自动化执行 CNKI 专业检索，获取文献列表和摘要信息。

**核心特点：**
- 使用浏览器自动化，无需额外依赖
- 支持专业检索语法
- 批量提取多页结果
- 提取文章完整元数据

## 使用场景

- 学术文献调研
- 批量获取 CNKI 文献元数据
- 提取文献摘要信息
- 系统性文献综述

## 前置要求

- OpenClaw 环境（已配置浏览器工具）
- 可访问 CNKI 网站（https://kns.cnki.net）
- **建议使用有头浏览器模式**以便处理验证码

---

## 功能1：搜索并获取结果列表

### 执行步骤

**Step 1: 打开CNKI搜索页面**

使用 browser 工具导航到CNKI搜索页面：

```
action: navigate
url: https://www.cnki.net/
```



**Step 2: 输入搜索关键词**

在搜索框中输入检索语句，如：
```
'结膜松弛'
```

使用 fill 操作输入：
```
kind: fill
ref: 搜索框
text: '结膜松弛'
```

**Step 3: 点击搜索按钮**

使用 click 操作：
```
kind: click
ref: 搜索按钮
```

**Step 4: 等待并提取结果**

等待结果加载后，使用 snapshot 或 evaluate 提取数据。

### 搜索结果提取（JavaScript）

在浏览器控制台执行以下代码提取当前页结果：

```javascript
// 提取搜索结果表格数据
function extractResults() {
  const results = [];
  
  // 尝试查找结果表格
  const table = document.querySelector('table.resulttable') || 
                document.querySelector('.result-table') ||
                document.querySelector('table');
  
  if (!table) {
    console.log('未找到结果表格');
    return results;
  }
  
  const rows = table.querySelectorAll('tr');
  
  rows.forEach(row => {
    const cells = row.querySelectorAll('td');
    if (cells.length >= 5) {
      const titleCell = cells[1];
      const titleLink = titleCell?.querySelector('a');
      
      if (titleLink) {
        results.push({
          title: titleLink.textContent?.trim() || '',
          link: titleLink.href || '',
          authors: cells[2]?.textContent?.trim() || '',
          source: cells[3]?.textContent?.trim() || '',
          date: cells[4]?.textContent?.trim() || '',
          cites: cells[6]?.textContent?.trim() || '0'
        });
      }
    }
  });
  
  return results;
}

extractResults();
```

**提取后数据示例：**
```json
[
  {
    "title": "射频微创治疗结膜松弛引起溢泪的临床观察",
    "link": "https://kns.cnki.net/kcms2/article/abstract/xxx",
    "authors": "郑璇;杨晓钊;杨华;张懿;王博",
    "source": "国际眼科杂志",
    "date": "2026-02-25",
    "cites": "0"
  }
]
```

### 翻页处理

翻到下一页（使用键盘更稳定）：
```
kind: press
key: ArrowRight
```

或点击下一页按钮：
```
kind: click
ref: 下一页按钮
```

翻页后等待2-3秒让页面加载：

```
timeMs: 3000
```

---

## 功能2：获取文章摘要信息

### 执行步骤

**Step 1: 导航到文章详情页**

直接打开文章URL：
```
action: navigate
url: https://kns.cnki.net/kcms2/article/abstract/xxxxx
```

**Step 2: 等待页面加载**

等待主要元素加载完成：
```
loadState: domcontentloaded
timeMs: 5000
```

**Step 3: 提取文章元数据**

在浏览器中执行以下代码：

```javascript
// 提取文章详情
function extractArticleDetails() {
  const details = {};
  
  // 标题
  const titleEl = document.querySelector('h1') || 
                  document.querySelector('.title') ||
                  document.querySelector('[class*="title"]');
  details.title = titleEl?.textContent?.trim() || '';
  
  // 作者列表
  const authorLinks = document.querySelectorAll('.author-list a, .author a, a.author, [class*="author"] a');
  details.authors = Array.from(authorLinks).map(a => a.textContent?.trim()).filter(Boolean);
  
  // 机构
  const orgEl = document.querySelector('[class*="org"]') || 
                document.querySelector('.institution') ||
                document.querySelector('[class*="institution"]');
  details.institution = orgEl?.textContent?.trim() || '';
  
  // 期刊
  const journalEl = document.querySelector('.journal-name') ||
                    document.querySelector('.source') ||
                    document.querySelector('[class*="journal"], [class*="source"]');
  details.journal = journalEl?.textContent?.trim() || '';
  
  // 发表日期
  const dateEl = document.querySelector('.publish-date') ||
                 document.querySelector('.date') ||
                 document.querySelector('[class*="date"]');
  details.publishDate = dateEl?.textContent?.trim() || '';
  
  // 摘要
  const abstractEl = document.querySelector('.abstract') ||
                     document.querySelector('.summary') ||
                     document.querySelector('[class*="abstract"]');
  details.abstract = abstractEl?.textContent?.trim() || '';
  
  // 关键词
  const keywordLinks = document.querySelectorAll('.keywords a, .keyword a, [class*="keyword"] a');
  details.keywords = Array.from(keywordLinks).map(k => k.textContent?.trim()).filter(Boolean);
  
  // DOI
  const doiEl = document.querySelector('.doi') || document.querySelector('[class*="doi"]');
  details.doi = doiEl?.textContent?.trim() || '';
  
  // 页码
  const pagesEl = document.querySelector('.pages');
  details.pages = pagesEl?.textContent?.trim() || '';
  
  // 卷期
  const volumeEl = document.querySelector('.volume');
  details.volume = volumeEl?.textContent?.trim() || '';
  
  // 引用次数
  const citeEl = document.querySelector('.cited') || document.querySelector('[class*="cite"]');
  details.cites = citeEl?.textContent?.trim() || '0';
  
  return details;
}

extractArticleDetails();
```

**提取后数据示例：**
```json
{
  "title": "新月形结膜切除联合结膜巩膜固定术治疗结膜松弛症",
  "authors": ["武耀红", "何敏"],
  "institution": "山西医科大学第二医院",
  "journal": "临床医药实践",
  "publishDate": "2006-04-25",
  "abstract": "目的: 探讨新月形结膜切除联合结膜巩膜固定术治疗结膜松弛症的疗效...",
  "keywords": ["结膜松弛症", "新月形切除", "巩膜固定术"],
  "doi": "",
  "pages": "293-294",
  "volume": "2006(04)",
  "cites": 0
}
```
**Step 4: 返回前一页，继续下一个论文数据提取**


---

## 常用查询示例

### 基础检索

| 检索内容 | 查询语句 |
|----------|----------|
| 结膜松弛主题 | `SU='结膜松弛'` |
| 结膜松弛治疗 | `SU='结膜松弛' and SU='治疗'` |
| 结膜松弛或手术 | `SU='结膜松弛' or SU='手术'` |

### 进阶检索

| 检索内容 | 查询语句 |
|----------|----------|
| 特定作者 | `AU='张兴儒' and SU='结膜松弛'` |
| 特定单位 | `AF='复旦大学' and SU='结膜松弛'` |
| 篇名检索 | `TI='结膜松弛症'` |
| 全文检索 | `FT='手术方法'` |
| 高被引文献 | `SU='结膜松弛' and CF>10` |
| 特定期刊 | `LY='中华眼科杂志' and SU='结膜松弛'` |

### 医学检索

| 检索内容 | 查询语句 |
|----------|----------|
| 眼科分类 | `SU='结膜松弛' and CLC=R779.6` |
| 基金资助 | `FU='国家自然科学基金' and SU='结膜松弛'` |
| 中英文扩展 | `SU='结膜松弛' or SU='conjunctivochalasis'` |

---

## 反机器人验证处理

CNKI 可能会出现验证，需要用户手动处理：

### 验证类型

1. **滑块验证** - 拖动滑块完成拼图
2. **点选验证** - 点击指定图片
3. **验证码输入** - 输入数字/字母

### 处理方法

**有头浏览器模式（推荐）：**

使用 `profile="user"` 让用户可以在浏览器中手动完成验证：

```
profile: user
action: navigate
url: https://kns.cnki.net/kns8s/AdvSearch?type=expert
```

出现验证时，告诉用户：
> "检测到CNKI验证，请手动完成验证后继续"

用户完成验证后，继续执行后续操作。

### 避免验证的建议

- 使用有头模式而非无头模式
- 降低操作频率，避免快速连续请求
- 每次操作间添加适当延迟（2-3秒）
- 保持会话，不要频繁新建浏览器实例

---

## 数据导出

### 导出为JSON

将提取的数据保存为JSON文件：

```
# 提取的数据格式
[
  {
    "title": "文献标题",
    "link": "https://...",
    "authors": "作者列表",
    "source": "期刊来源",
    "date": "发表日期",
    "cites": "引用数"
  }
]
```

使用 write 工具保存：

```
file_path: cnki_results.json
content: <提取的JSON数据>
```

### 导出为CSV

转换为CSV格式：

```
title,authors,source,date,cites
文献标题,作者,期刊,日期,引用数
...
```

---

## 完整工作流示例

### 搜索结膜松弛治疗文献

**1. 打开高级搜索页面**
```
action: navigate
url: https://kns.cnki.net/kns8s/AdvSearch?type=expert
```

**2. 等待页面加载**
```
loadState: networkidle
timeMs: 10000
```

**3. 输入搜索词**
```
kind: fill
ref: 搜索框
text: SU='结膜松弛' and SU='治疗'
```

**4. 点击搜索**
```
kind: click
ref: 搜索按钮
```

**5. 等待结果并提取**
```
loadState: networkidle
timeMs: 8000
```

**6. 翻页提取多页结果**

循环执行：提取当前页 → 翻页 → 等待 → 提取

**7. 保存结果**

将提取的数据保存到文件。

---

## 注意事项

1. **验证码处理**：有头模式下用户可手动处理
2. **请求频率**：每页操作间隔2-3秒
3. **数据完整性**：部分老文献可能无摘要
4. **登录状态**：需要登录才能查看部分文献详情

---

## 错误处理

| 错误情况 | 解决方法 |
|----------|----------|
| 页面加载超时 | 增加等待时间或刷新重试 |
| 找不到元素 | 使用备选选择器 |
| 验证码出现 | 等待用户手动完成 |
| 数据提取为空 | 检查页面结构是否变化 |

---

## 相关文件

- `references/cnki-fields.md` - CNKI专业检索字段一览表
- `references/query-examples.md` - CNKI专业检索查询案例

---

## 更新日志

### 2026-03-16 (v0.0.3)
- 新增时间范围筛选功能说明
- 添加发表时间（具体日期范围）设置方法
- 添加更新时间（相对时间下拉选项）设置方法
- 添加元素引用参考（ref=e124, e125, e129, e130, e131）

### 2026-03-15 (v0.0.2)
- 完善浏览器操作流程
- 添加详细的JavaScript提取代码
- 增加常用查询示例
- 完善反机器人验证处理说明

### 2026-03-05 (v0.0.1)
- 初始版本
---

## 时间范围设置（2026-03-16 更新）

### 发表时间（Publication Time）- 具体日期范围

高级搜索页面提供两种时间范围筛选方式。

#### 方式一：发表时间 - 具体日期范围

点击日期输入框会弹出日历选择器，可选择具体日期：

```
# 点击第一个日期输入框（开始日期）
kind: click
ref: e124  # 发表时间开始日期输入框

# 在弹出的日历中选择日期
# 日历显示当月所有天数，点击具体日期即可选中

# 点击第二个日期输入框（结束日期）
kind: click
ref: e125  # 发表时间结束日期输入框

# 在弹出的日历中选择结束日期
```

**元素参考：**
- 发表时间开始日期输入框: `ref=e124`
- 发表时间结束日期输入框: `ref=e125`
- 两个输入框之间显示为: `2026-03-01 -- 2026-03-31`

**日历选择器操作：**
1. 点击日期输入框，弹出日历
2. 日历默认显示当前月份
3. 点击具体日期数字即可选中
4. 选择后日历自动关闭，日期显示在输入框中
5. 日期格式为: YYYY-MM-DD (如: 2026-03-01)

#### 方式二：更新时间 - 相对时间下拉选项

点击下拉菜单可选择预设的时间范围：

```
# 点击更新时间下拉菜单
kind: click
ref: e129  # 更新时间下拉菜单
```

**元素参考：**
- 更新时间下拉区域: `ref=e129`
- 当前选中值: `ref=e130` (默认显示"不限")
- 下拉箭头: `ref=e131` (显示"∨")
- 下拉选项列表容器: `ref=e641`
- 各选项元素引用：
  - 不限: `ref=e642`
  - 最近一周: `ref=e644`
  - 最近一月: `ref=e646`
  - 最近半年: `ref=e648`
  - 最近一年: `ref=e650`
  - 今年迄今: `ref=e652`
  - 上一年度: `ref=e654`

**可选时间范围：**
- 不限（默认）
- 最近一周
- 最近一月
- 最近半年
- 最近一年
- 今年迄今
- 上一年度
（具体选项以实际页面为准）
