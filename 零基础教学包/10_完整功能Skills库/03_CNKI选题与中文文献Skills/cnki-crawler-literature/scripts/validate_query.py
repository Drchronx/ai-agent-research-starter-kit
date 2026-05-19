#!/usr/bin/env python3
"""
CNKI 专业检索式验证器

基于 reference/专业检索语法.md 第 7 节检查清单实现。
支持 CLI 独立调用，验证检索式语法是否正确。

用法:
    python validate_query.py "SU=('耐心资本'+'长期资本')"
"""

import re
import sys
from typing import Tuple, List


# 官方字段代码表（来自专业检索语法.md 第 2 节）
VALID_FIELD_CODES = {
    'SU', 'TKA', 'TI', 'KY', 'AB', 'CO', 'FT', 'AU', 'FI', 'RP',
    'AF', 'LY', 'RF', 'FU', 'CLC', 'SN', 'CN', 'DOI', 'QKLM', 'FAF', 'CF'
}

# 常见字段代码拼写错误映射
COMMON_TYPOS = {
    'SUB': 'SU',      # SUB → SU
    'TIT': 'TI',      # TIT → TI
    'KEY': 'KY',      # KEY → KY
    'ABS': 'AB',      # ABS → AB
    'AUT': 'AU',      # AUT → AU
    'AUTHOR': 'AU',   # AUTHOR → AU
    'JOU': 'LY',      # JOU → LY
    'JOURNAL': 'LY',  # JOURNAL → LY
    'FUN': 'FU',      # FUN → FU
    'FUND': 'FU',     # FUND → FU
    'ORG': 'AF',      # ORG → AF
    'ORGANIZATION': 'AF',  # ORGANIZATION → AF
}

# 字段内运算符
FIELD_OPERATORS = {'*', '+', '-'}

# 逻辑运算符
LOGIC_OPERATORS = {'and', 'or', 'not'}


def validate_cnki_query(query: str) -> Tuple[bool, List[str]]:
    """
    验证 CNKI 专业检索式语法
    
    Args:
        query: 检索式字符串
        
    Returns:
        (是否通过，错误列表)
    """
    errors = []
    
    # 1. 空查询检查
    if not query or not query.strip():
        errors.append("❌ 检索式为空")
        return False, errors
    
    query = query.strip()
    
    # 2. 中文引号检测（必须使用英文半角单引号）
    # Unicode: ""=201C/201D, ''=300A/300B, ''=300C/300D, ''=300E/300F
    chinese_quotes = ['\u201c', '\u201d', '\u300a', '\u300b', '\u300c', '\u300d', '\u300e', '\u300f']
    has_chinese_quote = any(q in query for q in chinese_quotes)
    if has_chinese_quote:
        errors.append("❌ 检测到中文引号，必须使用英文半角单引号 '...'")
    
    # 检查英文单引号是否成对
    single_quotes = query.count("'")
    if single_quotes % 2 != 0:
        errors.append("❌ 单引号未成对出现，请检查检索值是否都用 '...' 包裹")
    
    # 3. 年份参数检测（不应出现在检索式中）
    year_pattern = r"(?:YE|PY|YEAR)\s*=\s*['\"]?\d{4}"
    if re.search(year_pattern, query, re.IGNORECASE):
        errors.append("❌ 年份不应写入检索式，请使用 --start-year 和 --end-year 参数")
    
    # 4. 提取所有字段代码并验证
    field_pattern = r'([A-Za-z]+)\s*[%=<>!]'
    found_fields = re.findall(field_pattern, query)
    
    for field in found_fields:
        field_upper = field.upper()
        if field_upper not in VALID_FIELD_CODES:
            # 检查是否是常见拼写错误
            if field_upper in COMMON_TYPOS:
                correct = COMMON_TYPOS[field_upper]
                errors.append(f"❌ 字段代码 '{field}' 拼写错误，应为 '{correct}'")
            else:
                errors.append(f"❌ 未知字段代码 '{field}'，请参考官方字段表")
    
    # 5. 逻辑运算符格式检查（and/or/not 前后必须有空格）
    for op in ['and', 'or', 'not']:
        # 检查运算符前是否有空格（或位于开头）
        # 检查运算符后是否有空格（或位于结尾）
        pattern_before = r'(?<!\s)' + op + r'(?i)'
        pattern_after = r'(?i)' + op + r'(?!\s)'
        
        # 查找所有运算符位置
        op_matches = list(re.finditer(r'\b' + op + r'\b', query, re.IGNORECASE))
        for match in op_matches:
            start = match.start()
            end = match.end()
            
            # 检查前面是否有空格（或位于开头）
            if start > 0 and query[start-1] != ' ':
                errors.append(f"❌ 逻辑运算符 '{op}' 前面缺少空格")
                break
            
            # 检查后面是否有空格（或位于结尾）
            if end < len(query) and query[end] != ' ':
                errors.append(f"❌ 逻辑运算符 '{op}' 后面缺少空格")
                break
    
    # 6. 括号匹配检查
    paren_count = 0
    for char in query:
        if char == '(':
            paren_count += 1
        elif char == ')':
            paren_count -= 1
        if paren_count < 0:
            errors.append("❌ 括号不匹配：右括号 ')' 多于左括号 '('")
            break
    if paren_count > 0:
        errors.append(f"❌ 括号不匹配：缺少 {paren_count} 个右括号 ')'")
    
    # 7. 逗号分隔错误检测（应使用 + 号）
    # 检测引号内的逗号（常见错误：'词 1，词 2' 或 'A,B'）
    comma_in_quotes_pattern_zh = r"'[^']*，[^']*'"
    comma_in_quotes_pattern_en = r"'[^']*,[^']*'"
    if re.search(comma_in_quotes_pattern_zh, query) or re.search(comma_in_quotes_pattern_en, query):
        errors.append("❌ 检索值内使用逗号分隔，应使用 + 号连接（如 '词 1'+'词 2'）")
    
    # 8. 字段内运算符使用检查
    # 检测是否在中文字符串中使用逻辑运算符而非字段内运算符
    chinese_in_quotes = re.findall(r"'([\u4e00-\u9fa5]+)'", query)
    for text in chinese_in_quotes:
        if 'and' in text.lower() or 'or' in text.lower() or 'not' in text.lower():
            errors.append("❌ 检索值中包含英文单词，应使用 * + - 进行字段内组合")
    
    # 9. 数值字段比较运算符检查（CF>=1 而非 CF='100'）
    numeric_field_pattern = r"CF\s*=\s*['\"]\d+['\"]"
    if re.search(numeric_field_pattern, query):
        errors.append("❌ 被引频次 CF 应使用比较运算符（如 CF>=1），而非等号加引号")
    
    # 10. 空检索值检查
    empty_value_pattern = r"=\s*['\"]['\"]"
    if re.search(empty_value_pattern, query):
        errors.append("❌ 检测到空检索值，请为字段指定检索词")
    
    # 11. 检查是否有非法字符
    illegal_chars = []
    if '""' in query:
        illegal_chars.append('双引号 ""')
    if '【' in query or '】' in query:
        illegal_chars.append('中文括号【】')
    if '，' in query and not re.search(comma_in_quotes_pattern_zh, query):
        # 检查是否是字段间的逗号（也是错误）
        illegal_chars.append('中文逗号，')
    
    if illegal_chars:
        errors.append(f"❌ 检测到非法字符：{', '.join(illegal_chars)}")
    
    # 12. 检查字段代码是否使用小写（建议但不强制报错）
    lowercase_fields = [f for f in found_fields if f.islower() and len(f) <= 4]
    if lowercase_fields:
        # 这只是警告，不是错误
        pass
    
    is_valid = len(errors) == 0
    return is_valid, errors


def main():
    """CLI 入口"""
    if len(sys.argv) < 2:
        print("用法：python validate_query.py <检索式>")
        print("示例：python validate_query.py \"SU=('耐心资本'+'长期资本')\"")
        sys.exit(1)
    
    query = sys.argv[1]
    print(f"正在验证检索式：{query}\n")
    
    is_valid, errors = validate_cnki_query(query)
    
    if is_valid:
        print("✅ 检索式验证通过")
        sys.exit(0)
    else:
        print("❌ 检索式验证失败，发现以下问题：")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")
        print("\n请参考：reference/专业检索语法.md")
        sys.exit(1)


if __name__ == "__main__":
    main()
