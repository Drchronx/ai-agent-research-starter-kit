from pathlib import Path

import requests
from dotenv import load_dotenv
from loguru import logger

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

import settings


def get_configured_proxies():
    proxies = dict(settings.DEFAULT_PROXIES)
    if proxies.get("http") and proxies.get("https"):
        return proxies

    message = (
        "代理池未配置。请在 .env 中设置 "
        f"{settings.PROXY_HTTP_ENV} 和 {settings.PROXY_HTTPS_ENV} 后重新运行。"
    )
    raise RuntimeError(message)


def assert_proxy_available(proxies=None):
    proxies = proxies or get_configured_proxies()

    try:
        logger.info(f"正在验证代理池: {settings.PROXY_CHECK_URL}")
        response = requests.get(
            settings.PROXY_CHECK_URL,
            proxies=proxies,
            timeout=settings.PROXY_CHECK_TIMEOUT,
            headers={"Connection": "close"},
        )
        response.raise_for_status()
        logger.success(f"代理池可用: {response.text[:200]}")
        return True
    except requests.RequestException as exc:
        message = "代理池不可用，请更换代理后重新运行项目。"
        logger.error(f"{message} 错误: {exc}")
        raise RuntimeError(message) from exc


def main():
    try:
        assert_proxy_available()
    except RuntimeError as exc:
        logger.error(exc)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()