import argparse
import json
import os
import re
import urllib3
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from typing import Any

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import requests


URL = "https://kns.cnki.net/kvisual8/article/getGroupData"
RECSYS_API = "https://recsys.cnki.net"
DEFAULT_ECP_CLIENT_ID = "__Mv7VRS__3lz5QgRkptIUl515QQaMxY0VCiwCvk75"

# Proxy configuration (same as cnki-crawler)
# 从环境变量读取，如果没有则使用默认值
PROXIES = {
    "http": os.getenv("CNKI_PROXY_HTTP", "http://t17252328275921:ji53ky6z@u640.kdltps.com:15818/"),
    "https": os.getenv("CNKI_PROXY_HTTPS", "http://t17252328275921:ji53ky6z@u640.kdltps.com:15818/"),
}

HEADERS_BASE = {
    "Origin": "https://kns.cnki.net",
    "Referer": "https://kns.cnki.net/kvisual8/article/center?language=CHS&uniplatform=NZKPT",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0"
    ),
}

HEADERS = HEADERS_BASE


def generate_client_id() -> str | None:
    """
    动态生成 CNKI Ecp_ClientId cookie（与 cnki-crawler 一致的方法）。
    返回 client_id 字符串，失败时返回 None。
    """
    try:
        response = requests.post(
            f"{RECSYS_API}/UtilityOpenApi/GenerateClientID",
            headers=HEADERS_BASE,
            timeout=10,
            verify=False,
        )
        response.raise_for_status()
        data = response.json()
        client_id = data.get("Data")
        if client_id:
            return client_id
    except Exception:
        pass
    return None


CANDIDATE_GROUPS = [
    ("YE-年度", "YEAR", "年度分布"),
    ("ZYZT-主要主题", "KEYWORD", "主要主题"),
    ("CYZT-次要主题", "KEYWORD", "次要主题"),
    ("CCL-学科", "SUBJECT", "学科"),
    ("YJCC-研究层次", "OTHER", "研究层次"),
    ("QK-期刊", "JOURNAL", "期刊"),
    ("LYBSM-来源类别", "OTHER", "来源类别"),
    ("AUC-中国作者", "OTHER", "中国作者"),
    ("AFC-机构", "ORG", "机构"),
    ("FUC-基金", "FUND", "基金"),
    ("OA-OA出版", "OTHER", "OA出版"),
]



def sanitize_filename(value: str) -> str:
    cleaned = re.sub(r'[<>:"/\\\\|?*]+', "_", value.strip())
    cleaned = re.sub(r"\s+", "_", cleaned)
    return cleaned or "cnki-keyword"


def configure_chinese_font(font_path: str = None) -> str | None:
    """
    配置中文字体。
    
    Args:
        font_path: 可选的自定义字体文件路径（如 STSONG.TTF）
    
    Returns:
        字体名称，如果失败则返回 None
    """
    # 优先使用自定义字体文件
    if font_path and os.path.exists(font_path):
        try:
            # 注册自定义字体到 matplotlib 字体管理器
            font_manager.fontManager.addfont(font_path)
            font_prop = font_manager.FontProperties(fname=font_path)
            font_name = font_prop.get_name()
            
            # 设置全局字体
            plt.rcParams["font.sans-serif"] = [font_name, 'DejaVu Sans']
            plt.rcParams["axes.unicode_minus"] = False
            
            print(f"✅ 中文字体已加载：{font_name}")
            return font_name
        except Exception as e:
            print(f"⚠️ 自定义字体加载失败：{e}，尝试使用系统字体...")
    
    # 回退到系统字体
    candidates = [
        "Microsoft YaHei",
        "SimHei",
        "Noto Sans CJK SC",
        "Source Han Sans SC",
        "PingFang SC",
        "WenQuanYi Zen Hei",
    ]
    available = {font.name for font in font_manager.fontManager.ttflist}
    for name in candidates:
        if name in available:
            plt.rcParams["font.sans-serif"] = [name, 'DejaVu Sans']
            plt.rcParams["axes.unicode_minus"] = False
            print(f"✅ 使用系统字体：{name}")
            return name
    
    # 最后回退方案
    plt.rcParams["font.sans-serif"] = ['DejaVu Sans']
    plt.rcParams["axes.unicode_minus"] = False
    print("⚠️ 未找到中文字体，使用 DejaVu Sans（中文可能显示为方框）")
    return None


def build_query_json(keyword: str) -> dict[str, Any]:
    return {
        "Platform": "",
        "Resource": "JOURNAL",
        "Classid": "YSTT4HG0",
        "Products": "CJFQ,CAPJ,CJTL",
        "QNode": {
            "QGroup": [
                {
                    "Key": "Subject",
                    "Title": "",
                    "Logic": 0,
                    "Items": [],
                    "ChildItems": [
                        {
                            "Key": "input[data-tipid=gradetxt-1]",
                            "Title": "主题",
                            "Logic": 0,
                            "Items": [
                                {
                                    "Key": "input[data-tipid=gradetxt-1]",
                                    "Title": "主题",
                                    "Logic": 0,
                                    "Field": "SU",
                                    "Operator": "TOPRANK",
                                    "Value": keyword,
                                    "Value2": "",
                                }
                            ],
                            "ChildItems": [],
                        }
                    ],
                },
                {
                    "Key": "ControlGroup",
                    "Title": "",
                    "Logic": 0,
                    "Items": [],
                    "ChildItems": [],
                },
            ]
        },
        "ExScope": "1",
        "SearchType": 1,
        "Rlang": "CHINESE",
        "KuaKuCode": "",
        "Expands": {},
        "View": "changeDBOnlyFT",
        "SearchFrom": 99,
    }


def build_payload(keyword: str, group_name: str, group_code: str) -> dict[str, str]:
    return {
        "dbCode": "JOURNAL",
        "queryJson": json.dumps(build_query_json(keyword), ensure_ascii=False),
        "q": "",
        "groupName": group_name,
        "groupCode": group_code,
        "valueType": "3",
        "manageId": "",
        "language": "CHS",
        "uniplatform": "NZKPT",
        "subject": "",
        "random": "0.6479158936825272",
    }


def fetch_group(
    session: requests.Session,
    keyword: str,
    group_name: str,
    group_code: str,
    label: str,
    max_retries: int = 10,
) -> dict[str, Any] | None:
    """
    抓取单个分组数据（带重试机制）。
    
    Args:
        max_retries: 最大重试次数，默认 10 次
    """
    import random
    import time
    
    for attempt in range(1, max_retries + 1):
        try:
            # 随机延迟，避免被识别为自动化请求
            if attempt > 1:
                wait_time = random.uniform(2, 5) * (attempt ** 1.5)  # 指数退避
                print(f"  第 {attempt} 次请求，等待 {wait_time:.1f} 秒...")
                time.sleep(wait_time)
            
            # 随机化 User-Agent
            headers_with_random_ua = dict(HEADERS)
            chrome_versions = [
                "120.0.0.0",
                "121.0.0.0",
                "122.0.0.0",
                "123.0.0.0",
            ]
            headers_with_random_ua["User-Agent"] = (
                f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                f"(KHTML, like Gecko) Chrome/{random.choice(chrome_versions)} Safari/537.36"
            )
            
            response = session.post(
                URL,
                headers=headers_with_random_ua,
                data=build_payload(keyword, group_name, group_code),
                timeout=30,
                proxies=PROXIES,
                verify=False,
            )
            
            # 检查是否触发反爬
            if response.status_code == 418:
                print(f"  ⚠️ 第 {attempt} 次请求触发反爬 (418)，准备重试...")
                if attempt < max_retries:
                    continue
                else:
                    print(f"  ❌ 已达到最大重试次数 {max_retries}，放弃")
                    return None
            
            response.raise_for_status()
            raw_text = response.text.strip()
            if not raw_text:
                return None

            parsed = json.loads(raw_text)
            if not isinstance(parsed, list) or not parsed:
                return None

            if attempt > 1:
                print(f"  ✅ 第 {attempt} 次请求成功！")
            
            return {
                "group_name": group_name,
                "group_code": group_code,
                "label": label,
                "items": parsed,
            }
            
        except requests.RequestException as e:
            print(f"  ⚠️ 第 {attempt} 次请求失败：{e}")
            if attempt >= max_retries:
                print(f"  ❌ 已达到最大重试次数 {max_retries}，放弃")
                return None
    
    return None


def collect_groups(keyword: str, ecp_client_id: str | None = None) -> list[dict[str, Any]]:
    """
    采集 CNKI 分组数据（带重试机制）。
    
    Args:
        keyword: 关键词
        ecp_client_id: 可选的 Ecp_ClientId。如果不传或为 None，会自动调用 generate_client_id() 获取。
    """
    groups = OrderedDict()
    
    # 如果没有提供 ecp_client_id，尝试动态生成
    if not ecp_client_id:
        generated_id = generate_client_id()
        if generated_id:
            ecp_client_id = generated_id
        else:
            ecp_client_id = DEFAULT_ECP_CLIENT_ID
    
    print(f"开始采集 CNKI 分组数据，关键词：{keyword}")
    print(f"使用代理：{PROXIES}")
    print(f"Cookie: Ecp_ClientId={ecp_client_id[:20]}...")
    
    with requests.Session() as session:
        session.cookies.set("Ecp_ClientId", ecp_client_id)
        session.proxies.update(PROXIES)
        
        for i, (group_name, group_code, label) in enumerate(CANDIDATE_GROUPS, 1):
            key = (group_name, group_code)
            if key in groups:
                continue
            
            print(f"\n[{i}/{len(CANDIDATE_GROUPS)}] 正在获取：{group_name} ({label})...")
            result = fetch_group(session, keyword, group_name, group_code, label, max_retries=10)
            if result is not None:
                print(f"  ✅ 成功获取 {len(result['items'])} 条数据")
                groups[key] = result
            else:
                print(f"  ❌ 获取失败，跳过")
    
    return list(groups.values())


def find_group(groups: list[dict[str, Any]], group_name: str) -> dict[str, Any] | None:
    for group in groups:
        if group["group_name"] == group_name:
            return group
    return None


def format_top_items(items: list[dict[str, Any]], limit: int = 5) -> str:
    if not items:
        return "无"
    return "；".join(f"{item['name']}({item['y']})" for item in items[:limit])


def describe_year_trend(group: dict[str, Any] | None, current_year: int) -> list[str]:
    if not group:
        return ["未获取到年度分布，无法做年度趋势判断。"]

    items = sorted(group["items"], key=lambda row: int(row["c_fieldValue"]))
    total = sum(item["y"] for item in items)
    peak = max(items, key=lambda item: item["y"])
    recent_items = [item for item in items if int(item["c_fieldValue"]) >= current_year - 2]
    recent_total = sum(item["y"] for item in recent_items)
    current = next((item for item in items if int(item["c_fieldValue"]) == current_year), None)
    previous = next((item for item in items if int(item["c_fieldValue"]) == current_year - 1), None)

    lines = [
        f"年度记录共 {len(items)} 个年份节点，累计计数 {total}，峰值出现在 {peak['name']}，计 {peak['y']} 篇。",
        f"近三年合计 {recent_total} 篇，占全部年度计数的 {recent_total / total:.1%}，说明热度主要集中在最近阶段。"
        if total
        else "年度计数为 0，无法判断近三年占比。",
    ]
    if current:
        current_line = f"{current['name']}目前记录 {current['y']} 篇"
        if previous:
            delta = current["y"] - previous["y"]
            direction = "高于" if delta > 0 else "低于" if delta < 0 else "持平于"
            current_line += f"，相对 {previous['name']} {direction} {abs(delta)} 篇。"
        else:
            current_line += "，但缺少直接可比的上一年节点。"
        current_line += " 当前年份通常是年内累计值，解读时不要直接当成全年终值。"
        lines.append(current_line)
    return lines


def describe_keyword_group(group: dict[str, Any] | None, title: str) -> list[str]:
    if not group:
        return [f"未获取到{title}数据。"]

    items = group["items"]
    total = sum(item["y"] for item in items)
    top = items[0]
    top5 = sum(item["y"] for item in items[:5])
    lines = [
        f"{title}返回 {len(items)} 个条目，累计计数 {total}；最高频项为 {top['name']}({top['y']})。",
        f"前 5 项为 {format_top_items(items)}，前 5 项累计占比 {top5 / total:.1%}。"
        if total
        else f"{title}计数为 0。",
    ]
    if total:
        if top["y"] / total >= 0.3:
            lines.append(f"{title}集中度较高，说明关键词关联议题已经出现相对明确的主轴。")
        else:
            lines.append(f"{title}集中度偏低，说明关键词关联议题较分散，跨主题扩散明显。")
    return lines


def describe_subject_group(group: dict[str, Any] | None) -> list[str]:
    if not group:
        return ["未获取到学科分布。"]

    items = group["items"]
    total = sum(item["y"] for item in items)
    top = items[0]
    return [
        f"学科共覆盖 {len(items)} 个方向，累计计数 {total}。",
        f"首位学科是 {top['name']}({top['y']})，占学科计数的 {top['y'] / total:.1%}；前 5 项为 {format_top_items(items)}。"
        if total
        else "学科计数为 0。",
        "如果首位学科占比明显偏高，说明该关键词在知网期刊样本中已经形成较稳定的学科落点。"
        if total and top["y"] / total >= 0.5
        else "学科分布较分散，说明该关键词可能处于跨学科扩散阶段。",
    ]


def describe_journal_group(group: dict[str, Any] | None) -> list[str]:
    if not group:
        return ["未获取到期刊分布。"]

    items = group["items"]
    total = sum(item["y"] for item in items)
    if len(items) == 1:
        return [
            f"期刊仅识别到 {items[0]['name']} 一种来源，计 {items[0]['y']} 篇。",
            "样本高度集中在单一期刊，说明当前检索结果更像垂直刊物内的专题聚合，不适合直接外推到全学术生态。",
        ]

    top = items[0]
    return [
        f"期刊共覆盖 {len(items)} 种来源，累计计数 {total}。",
        f"头部期刊为 {top['name']}({top['y']})；前 5 项为 {format_top_items(items)}。",
        "期刊分布越分散，越能说明该关键词已经突破单一期刊圈层。"
        if total and top["y"] / total < 0.5
        else "头部期刊占比偏高，说明传播仍集中在有限刊源中。",
    ]


def describe_people_group(group: dict[str, Any] | None, label: str) -> list[str]:
    if not group:
        return [f"未获取到{label}分布。"]

    items = group["items"]
    total = sum(item["y"] for item in items)
    max_count = max(item["y"] for item in items)
    lines = [
        f"{label}共识别到 {len(items)} 个条目，累计计数 {total}；前 5 项为 {format_top_items(items)}。"
    ]
    if max_count == 1:
        lines.append(f"{label}分布高度分散，尚未出现明显的核心主体。")
    else:
        lines.append(f"{label}中已有头部主体出现，但整体仍需结合总样本判断是否形成稳定研究共同体。")
    return lines


def describe_fund_group(group: dict[str, Any] | None) -> list[str]:
    if not group:
        return ["未识别到基金分组，说明样本中基金标注较少，或该关键词在当前期刊样本中的项目化程度不高。"]

    items = group["items"]
    total = sum(item["y"] for item in items)
    return [
        f"基金共返回 {len(items)} 条记录，累计计数 {total}；前几项为 {format_top_items(items)}。",
        "基金条目较少时，通常说明该关键词更多处于跟进讨论或实践写作阶段，而不是高强度项目驱动阶段。",
    ]


def build_markdown_report(keyword: str, groups: list[dict[str, Any]]) -> str:
    now = datetime.now()
    current_year = now.year
    lines = [
        f"# 知网关键词趋势分析报告：{keyword}",
        "",
        f"- 生成时间：{now.strftime('%Y-%m-%d %H:%M:%S')}",
        "- 数据来源：CNKI `getGroupData` 分组接口",
        "- 检索范围：期刊资源 `JOURNAL`，主题字段 `SU`，操作符 `TOPRANK`",
        f"- 保留的有效分组数：{len(groups)}",
        "",
        "## 有效分组",
    ]
    for group in groups:
        lines.append(f"- {group['group_name']} / {group['group_code']}：{len(group['items'])} 条")

    lines.extend(["", "## 趋势解读", "", "### 年度趋势"])
    lines.extend(f"- {line}" for line in describe_year_trend(find_group(groups, "YE-年度"), current_year))

    lines.extend(["", "### 主题趋势"])
    lines.extend(f"- {line}" for line in describe_keyword_group(find_group(groups, "ZYZT-主要主题"), "主要主题"))
    lines.extend(f"- {line}" for line in describe_keyword_group(find_group(groups, "CYZT-次要主题"), "次要主题"))

    lines.extend(["", "### 学科与刊物格局"])
    lines.extend(f"- {line}" for line in describe_subject_group(find_group(groups, "CCL-学科")))
    lines.extend(f"- {line}" for line in describe_journal_group(find_group(groups, "QK-期刊")))

    lines.extend(["", "### 作者与机构"])
    lines.extend(f"- {line}" for line in describe_people_group(find_group(groups, "AUC-中国作者"), "作者"))
    lines.extend(f"- {line}" for line in describe_people_group(find_group(groups, "AFC-机构"), "机构"))

    lines.extend(["", "### 基金支持"])
    lines.extend(f"- {line}" for line in describe_fund_group(find_group(groups, "FUC-基金")))

    lines.extend(["", "## 综合结论"])
    year_group = find_group(groups, "YE-年度")
    journal_group = find_group(groups, "QK-期刊")
    subject_group = find_group(groups, "CCL-学科")
    if year_group:
        peak = max(year_group["items"], key=lambda item: item["y"])
        lines.append(f"- 年度热度峰值出现在 {peak['name']}，说明该关键词的关注度高点较清晰。")
    if journal_group:
        if len(journal_group["items"]) == 1:
            lines.append("- 当前样本完全集中于单一期刊，先检查检索条件是否过窄，再决定是否将其当作全局趋势。")
        else:
            top_journal = journal_group["items"][0]
            lines.append(f"- 期刊分布中 {top_journal['name']} 处于头部位置，但仍需结合其余刊源判断扩散广度。")
    if subject_group:
        top_subject = subject_group["items"][0]
        lines.append(f"- 学科落点以 {top_subject['name']} 为主，可据此判断该关键词当前最强的学术承载场域。")
    lines.append("- 当年数据默认按年内累计口径理解；如果需要严格同比，应在年底或统一时间窗口内重复抓取。")
    return "\n".join(lines) + "\n"


def save_bar_chart(
    items: list[dict[str, Any]],
    title: str,
    path: Path,
    *,
    top_n: int = 10,
    horizontal: bool = True,
) -> Path | None:
    if not items:
        return None

    # 获取当前字体设置
    font_name = plt.rcParams.get("font.sans-serif", ["DejaVu Sans"])[0]
    font_prop = font_manager.FontProperties(family=font_name)
    
    data = items[:top_n]
    labels = [item["name"] for item in data]
    values = [item["y"] for item in data]
    fig, ax = plt.subplots(figsize=(12, 7))

    if horizontal:
        labels = labels[::-1]
        values = values[::-1]
        ax.barh(range(len(labels)), values, color="#2f6fed")
        for index, value in enumerate(values):
            ax.text(value, index, f" {value}", va="center", fontsize=10, fontproperties=font_prop)
        ax.grid(axis="x", linestyle="--", alpha=0.25)
        ax.set_xlabel("计数", fontsize=12, fontproperties=font_prop)
        ax.set_yticks(range(len(labels)))
        ax.set_yticklabels(labels, fontproperties=font_prop)
    else:
        ax.bar(range(len(labels)), values, color="#2f6fed")
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, fontproperties=font_prop, rotation=30)
        for index, value in enumerate(values):
            ax.text(index, value, str(value), ha="center", va="bottom", fontsize=10, fontproperties=font_prop)
        ax.grid(axis="y", linestyle="--", alpha=0.25)
        ax.set_ylabel("计数", fontsize=12, fontproperties=font_prop)

    ax.set_title(title, fontsize=16, pad=14, fontproperties=font_prop)
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_charts(output_dir: Path, keyword: str, groups: list[dict[str, Any]]) -> list[Path]:
    chart_dir = output_dir / "charts"
    chart_dir.mkdir(parents=True, exist_ok=True)
    base_name = sanitize_filename(keyword)
    generated: list[Path] = []

    year_group = find_group(groups, "YE-年度")
    if year_group:
        items = sorted(year_group["items"], key=lambda row: int(row["c_fieldValue"]))
        path = chart_dir / f"{base_name}_年度趋势.png"
        result = save_bar_chart(items, f"{keyword} 年度趋势", path, top_n=len(items), horizontal=False)
        if result:
            generated.append(result)

    chart_specs = [
        ("ZYZT-主要主题", "主要主题 Top 10"),
        ("CCL-学科", "学科分布 Top 10"),
        ("QK-期刊", "期刊分布 Top 10"),
        ("AFC-机构", "机构分布 Top 10"),
        ("FUC-基金", "基金分布 Top 10"),
    ]
    for group_name, chart_title in chart_specs:
        group = find_group(groups, group_name)
        if not group:
            continue
        path = chart_dir / f"{base_name}_{group['label']}.png"
        result = save_bar_chart(group["items"], f"{keyword} {chart_title}", path)
        if result:
            generated.append(result)

    return generated


def append_chart_section(report: str, chart_paths: list[Path], font_name: str | None) -> str:
    if not chart_paths:
        return report

    chart_map = {path.stem.split("_", 1)[-1]: path for path in chart_paths}
    lines = report.rstrip().splitlines()
    output: list[str] = []

    section_images = {
        "### 年度趋势": [chart_map.get("年度趋势")],
        "### 主题趋势": [chart_map.get("主要主题")],
        "### 学科与刊物格局": [chart_map.get("学科"), chart_map.get("期刊")],
        "### 作者与机构": [chart_map.get("机构")],
        "### 基金支持": [chart_map.get("基金")],
    }

    for line in lines:
        output.append(line)
        if line in section_images:
            output.append("")
            for image_path in section_images[line]:
                if image_path:
                    output.append(f"![{image_path.stem}]({image_path})")
                    output.append("")

    output.extend(
        [
            "",
            "## 图表说明",
            f"- 中文字体：{font_name}" if font_name else "- 中文字体：未命中预设字体，若图片存在乱码请安装或切换到微软雅黑/黑体",
            "- 图表已插入对应章节，可直接在支持 Markdown 图片预览的环境中查看。",
        ]
    )
    return "\n".join(output) + "\n"


def write_outputs(output_dir: Path, keyword: str, groups: list[dict[str, Any]], report: str) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    base_name = sanitize_filename(keyword)
    json_path = output_dir / f"{base_name}_valid_groups.json"
    report_path = output_dir / f"{base_name}_trend_report.md"
    json_path.write_text(
        json.dumps(
            {
                "keyword": keyword,
                "generated_at": datetime.now().isoformat(timespec="seconds"),
                "valid_groups": groups,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    report_path.write_text(report, encoding="utf-8")
    return json_path, report_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="抓取知网关键词分组数据，过滤空分组，并生成趋势解读报告和统计图。")
    parser.add_argument("keyword", help="要分析的知网关键词")
    parser.add_argument("--output-dir", default="reports", help="输出目录，默认写入 ./reports")
    parser.add_argument(
        "--ecp-client-id",
        default=os.getenv("CNKI_ECP_CLIENT_ID", ""),
        help="CNKI 的 Ecp_ClientId；默认优先读取 CNKI_ECP_CLIENT_ID 环境变量，如果不传则自动调用 generate_client_id() 动态生成",
    )
    parser.add_argument("--print-report", action="store_true", help="在终端打印生成的 Markdown 报告")
    parser.add_argument(
        "--font-path",
        type=str,
        default=None,
        help="自定义中文字体文件路径（如 STSONG.TTF）"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    
    # 确定字体路径：优先使用 --font-path，其次使用默认的 STSONG.TTF
    font_path = args.font_path
    if not font_path:
        # 默认字体路径（相对于脚本目录）
        script_dir = Path(__file__).parent
        default_font = script_dir.parent.parent / "data" / "STSONG.TTF"
        if default_font.exists():
            font_path = str(default_font)
    
    font_name = configure_chinese_font(font_path)
    
    # 如果 --ecp-client-id 传了空字符串（默认值），则传 None 让 collect_groups 自动获取
    ecp_client_id = args.ecp_client_id if args.ecp_client_id else None
    groups = collect_groups(args.keyword, ecp_client_id)
    if not groups:
        raise SystemExit("未获取到任何有效分组，请检查关键词、Cookie 或接口状态。")

    output_dir = Path(args.output_dir)
    chart_paths = generate_charts(output_dir, args.keyword, groups)
    report = append_chart_section(build_markdown_report(args.keyword, groups), chart_paths, font_name)
    json_path, report_path = write_outputs(output_dir, args.keyword, groups, report)

    print(f"有效分组数: {len(groups)}")
    print(f"JSON 输出: {json_path}")
    print(f"报告输出: {report_path}")
    if chart_paths:
        print("图表输出:")
        for chart_path in chart_paths:
            print(f"- {chart_path}")
    if args.print_report:
        print("")
        print(report)


if __name__ == "__main__":
    main()
