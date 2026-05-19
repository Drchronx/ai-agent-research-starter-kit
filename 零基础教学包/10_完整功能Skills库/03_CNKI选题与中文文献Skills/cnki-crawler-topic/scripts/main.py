import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

from crawl import CNKISpider
from settings import DB_DSN_ENV, DEFAULT_SORT_FIELD, DEFAULT_SORT_TYPE
from validate_query import validate_cnki_query


def parse_args():
    parser = argparse.ArgumentParser(description="Crawl CNKI papers and optionally save each page to PostgreSQL.")
    parser.add_argument("query_pattern", help="CNKI query pattern, for example: SU='耐心资本'")
    parser.add_argument("--start-year", help="Start publication year.")
    parser.add_argument("--end-year", help="End publication year.")
    parser.add_argument("--sort-field", type=str, default=DEFAULT_SORT_FIELD,
                        help="排序字段：PT=发表时间，CF=被引频次，DFR=下载频次，ZH=综合排序 (默认：PT)")
    parser.add_argument("--sort-type", type=str, default=DEFAULT_SORT_TYPE,
                        help="排序方式：asc/desc (默认：desc)")
    parser.add_argument("--db-dsn", help=f"PostgreSQL DSN. Defaults to {DB_DSN_ENV} environment variable.")
    parser.add_argument("--no-db", action="store_true", help="Disable database saving.")
    parser.add_argument("--no-estimated-time", action="store_true", help="Disable estimated time output.")
    parser.add_argument("--no-ensure-table", action="store_true", help="Do not create cnki_papers table automatically.")
    parser.add_argument("--limit-pages", type=int, help="Crawl at most this many pages.")
    parser.add_argument("--print-result", action="store_true", help="Print all crawled records after the run.")
    parser.add_argument("--validate-only", action="store_true",
                        help="只验证检索式，不执行爬取")
    return parser.parse_args()


def main():
    args = parse_args()
    
    # 验证检索式
    logger.info("正在验证检索式语法...")
    valid, errors = validate_cnki_query(args.query_pattern)
    if not valid:
        logger.error("❌ 检索式验证失败:")
        for err in errors:
            logger.error(f"  - {err}")
        logger.error("\n请参考：reference/专业检索语法.md")
        sys.exit(1)
    
    logger.info("✅ 检索式验证通过")
    
    # 只验证模式
    if args.validate_only:
        logger.info("验证模式：检索式语法正确，未执行爬取")
        sys.exit(0)
    
    spider = CNKISpider(
        query_pattern=args.query_pattern,
        start_year=args.start_year,
        end_year=args.end_year,
        sort_field=args.sort_field,
        sort_type=args.sort_type,
        output_estimated_time=not args.no_estimated_time,
        save_to_db=not args.no_db,
        db_dsn=args.db_dsn,
        ensure_db_table=not args.no_ensure_table,
        limit_pages=args.limit_pages,
        print_result=args.print_result,
    )
    spider.run()


if __name__ == "__main__":
    main()