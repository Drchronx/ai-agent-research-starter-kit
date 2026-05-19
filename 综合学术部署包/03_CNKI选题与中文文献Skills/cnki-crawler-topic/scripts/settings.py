import os

CNKI_BASE_URL = "https://kns.cnki.net"
CNKI_RECSYS_API = "https://recsys.cnki.net/RCDService/api"
CNKI_GRID_URL = f"{CNKI_BASE_URL}/kns8s/brief/grid"
PROXY_CHECK_URL = "https://dev.kdlapi.com/testproxy"

REQUEST_TIMEOUT = 10
PROXY_CHECK_TIMEOUT = 8
DEFAULT_RETRY_TIMES = 10
ESTIMATED_SECONDS_PER_PAGE = 10
DETAIL_PAGE_WORKERS = 5

PAGE_SIZE = 50
DEFAULT_SAVE_TO_DB = True
DEFAULT_OUTPUT_ESTIMATED_TIME = True
DEFAULT_ENSURE_DB_TABLE = True

# 默认排序配置
DEFAULT_SORT_FIELD = "PT"   # 默认按发表时间排序
DEFAULT_SORT_TYPE = "desc"  # 默认降序

DB_DSN_ENV = "CNKI_DB_DSN"
PROXY_HTTP_ENV = "CNKI_PROXY_HTTP"
PROXY_HTTPS_ENV = "CNKI_PROXY_HTTPS"

DEFAULT_HEADERS = {
    "Origin": CNKI_BASE_URL,
    "Referer": f"{CNKI_BASE_URL}/kns8s/AdvSearch?captchaId=3cd276d2-ad8b-4259-8897-a0e9272f67f7",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
}

PROXY_HTTP = os.getenv(PROXY_HTTP_ENV)
PROXY_HTTPS = os.getenv(PROXY_HTTPS_ENV)
DEFAULT_PROXIES = (
    {
        "http": PROXY_HTTP,
        "https": PROXY_HTTPS,
    }
    if PROXY_HTTP and PROXY_HTTPS else {}
)

CNKI_QUERY_RESOURCE = "JOURNAL"
CNKI_QUERY_CLASS_ID = "YSTT4HG0"
CNKI_QUERY_PRODUCTS = "CJFQ,CAPJ,CJTL"
