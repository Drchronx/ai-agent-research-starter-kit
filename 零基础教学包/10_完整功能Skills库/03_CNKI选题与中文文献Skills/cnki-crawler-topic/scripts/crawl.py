import requests
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from lxml import etree
from loguru import logger

from cnki_db import CNKIPaperRepository
from proxy_check import assert_proxy_available
import settings


class CNKISpider:
    DEFAULT_RETRY_TIMES = settings.DEFAULT_RETRY_TIMES
    ESTIMATED_SECONDS_PER_PAGE = settings.ESTIMATED_SECONDS_PER_PAGE

    def __init__(self,
                 query_pattern,
                 start_year=None,
                 end_year=None,
                 sort_field=settings.DEFAULT_SORT_FIELD,
                 sort_type=settings.DEFAULT_SORT_TYPE,
                 output_estimated_time=settings.DEFAULT_OUTPUT_ESTIMATED_TIME,
                 save_to_db=settings.DEFAULT_SAVE_TO_DB,
                 db_dsn=None,
                 ensure_db_table=settings.DEFAULT_ENSURE_DB_TABLE,
                 limit_pages=None,
                 print_result=False
                 ):

        self.headers = dict(settings.DEFAULT_HEADERS)

        self.page_size = settings.PAGE_SIZE
        self.session = requests.Session()
        self.query_pattern = query_pattern
        self.start_year = start_year
        self.end_year = end_year
        self.sort_field = sort_field
        self.sort_type = sort_type
        self.output_estimated_time = output_estimated_time
        self.save_to_db = save_to_db
        self.limit_pages = limit_pages
        self.print_result = print_result
        self.query_json = self.build_query_json()
        self.recsys_api = settings.CNKI_RECSYS_API
        self.cookies = {}
        self.proxies = dict(settings.DEFAULT_PROXIES)
        assert_proxy_available(self.proxies)
        self.update_cookies()
        self.turn_page_pattern = re.compile(r'<input id="hidTurnPage" type="hidden" value="(.*?)">')
        self.total_page_pattern = re.compile(r'<input id="totalCnt" type="hidden" value="(\d+)">')
        self.paper_repository = (
            CNKIPaperRepository(dsn=db_dsn, ensure_table=ensure_db_table)
            if self.save_to_db else None
        )

    def _request(self, method, url, retry_times=DEFAULT_RETRY_TIMES, session=None, **kwargs):
        """
        统一网络请求入口，默认重试 10 次。
        """
        kwargs.setdefault("timeout", settings.REQUEST_TIMEOUT)

        for attempt in range(1, retry_times + 1):
            try:
                request_session = session or self.session
                response = request_session.request(method, url, **kwargs)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                if attempt >= retry_times:
                    logger.error(f"请求失败，已重试 {retry_times} 次: {method.upper()} {url}，错误: {e}")
                    raise

                sleep_seconds = min(2 ** (attempt - 1), 30)
                logger.warning(
                    f"请求失败，准备第 {attempt + 1}/{retry_times} 次重试: "
                    f"{method.upper()} {url}，错误: {e}"
                )
                time.sleep(sleep_seconds)

    def build_query_json(self):
        """
        用于构建请求用的QueryJson参数
        :return:
        """
        if self.start_year or self.end_year:
            year_param = {
                "Key": ".tit-startend-yearbox",
                "Title": "",
                "Logic": 0,
                "Items": [
                    {
                        "Key": ".tit-startend-yearbox",
                        "Title": "出版年度",
                        "Logic": 0,
                        "Field": "YE",
                        "Operator": 7,
                        "Value": f"{self.start_year}",
                        "Value2": f"{self.end_year}"
                    }
                ],
                "ChildItems": []
            }
        else:
            year_param = None
        return {
            "Platform": "",
            "Resource": settings.CNKI_QUERY_RESOURCE,
            "Classid": settings.CNKI_QUERY_CLASS_ID,
            "Products": settings.CNKI_QUERY_PRODUCTS,
            "QNode": {
                "QGroup": [
                    {
                        "Key": "Subject",
                        "Title": "",
                        "Logic": 0,
                        "Items": [
                            {
                                "Key": "Expert",
                                "Title": "",
                                "Logic": 0,
                                "Field": "EXPERT",
                                "Operator": 0,
                                "Value": self.query_pattern,
                                "Value2": ""
                            }
                        ],
                        "ChildItems": []
                    },
                    {
                        "Key": "ControlGroup",
                        "Title": "",
                        "Logic": 0,
                        "Items": [],
                        "ChildItems": [year_param] if year_param else []
                    }
                ]
            },
            "ExScope": "1",
            "SearchType": 4,
            "Rlang": "CHINESE",
            "KuaKuCode": "",
            "Expands": {},
            "View": "changeDBOnlyFT",
            "SearchFrom": 4
        }

    def update_cookies(self):
        """
        获取 clientId
        :return:
        """
        try:
            logger.info("开始获取更新cookies……")

            response = self._request(
                "get",
                f"{self.recsys_api}/UtilityOpenApi/GenerateClientID",
                headers=self.headers
            )

            data = response.json()
            client_id = data.get("Data")
            logger.debug(client_id)

            self.cookies = {
                'Ecp_ClientId': f"{client_id}"
            }
            logger.success(f"cookies更新成功:{self.cookies}")

        except Exception as e:
            message = "获取 clientId 失败，请检查网络、代理或 CNKI 接口状态。"
            logger.error(f"{message}错误: {e}")
            raise RuntimeError(message) from e

    def get_first_page(self) -> tuple[str, str, int]:
        """
        采集第一页数据
        :return: turn_page参数, 网页源代码, 总页数
        """
        params = {
            "boolSearch": "true",
            "QueryJson": json.dumps(self.query_json),
            "pageNum": 1,
            "pageSize": self.page_size,
            "dstyle": "listmode",
            "boolSortSearch": "false",
            "sortField": self.sort_field,
            "sortType": self.sort_type,
            "aside": f"{self.query_pattern}",
            "subject": "",
            "language": "",
            "uniplatform": "",
            "CurPage": 1
        }
        response = self._request(
            "post",
            settings.CNKI_GRID_URL,
            cookies=self.cookies,
            headers=self.headers,
            proxies=self.proxies,
            data=params)
        turn_page = self.get_turn_page(response.text)
        # print(response.text)
        total_items = re.search(self.total_page_pattern, response.text)
        if total_items:
            # 计算总页数
            total = int(total_items.group(1))
            total_page = (total + self.page_size - 1) // self.page_size
        else:
            total_page = 0

        return turn_page, response.text, total_page

    def get_turn_page(self, page_source):
        """
        从网页源代码中获取turn_page参数
        :param page_source:
        :return:
        """
        turn_page = re.search(self.turn_page_pattern, page_source)
        if turn_page:
            return turn_page.group(1)
        return None

    def get_other_page(self, page, turn_page) -> tuple[str, str]:
        """
        采集其他页面数据
        :param page:
        :param turn_page:
        :return:turn_page参数, 网页源代码
        """
        params = {
            "boolSearch": "false",
            "QueryJson": json.dumps(self.query_json),
            "pageNum": f"{page}",
            "pageSize": f"{self.page_size}",
            "sortField": self.sort_field,
            "sortType": self.sort_type,
            "dstyle": "listmode",
            "boolSortSearch": "false",
            "aside": "",
            "subject": "",
            "turnpage": f"{turn_page}",
            "language": "",
            "uniplatform": ""
        }
        response = self._request(
            "post",
            settings.CNKI_GRID_URL,
            cookies=self.cookies,
            headers=self.headers,
            proxies=self.proxies,
            data=params)
        turn_page = self.get_turn_page(response.text)
        return turn_page, response.text

    @staticmethod
    def get_element(list_input):
        if list_input:
            return ''.join([element.strip() for element in list_input if element.strip()])
        return ""

    @staticmethod
    def format_duration(total_seconds):
        """
        将秒数格式化为更自然的中文时间单位。
        """
        if total_seconds <= 0:
            return "0秒"

        units = [
            ("天", 24 * 60 * 60),
            ("小时", 60 * 60),
            ("分钟", 60),
            ("秒", 1),
        ]
        parts = []
        remaining_seconds = total_seconds
        for unit_name, unit_seconds in units:
            value, remaining_seconds = divmod(remaining_seconds, unit_seconds)
            if value:
                parts.append(f"{value}{unit_name}")
        return ''.join(parts)

    def get_page_data(self, text):
        """
        Parse one result page and fetch detail pages concurrently.
        """
        tree = etree.HTML(text)
        result = []
        tr_list = tree.xpath("//table[@class='result-table-list']//tr")
        for tr in tr_list[1:]:
            result.append({
                '篇名': self.get_element(tr.xpath("./td[@class='name']//text()")),
                '刊名': self.get_element(tr.xpath("./td[@class='source']//text()")),
                '发表时间': self.get_element(tr.xpath("./td[@class='date']//text()")),
                '下载数': self.get_element(tr.xpath("./td[@class='download']//text()")),
                '被引数': self.get_element(tr.xpath("./td[@class='quote']//text()")),
                '详情页链接': self.get_element(tr.xpath("./td[@class='name']/a/@href")),
            })

        detail_workers = max(1, int(settings.DETAIL_PAGE_WORKERS))
        if detail_workers == 1 or len(result) <= 1:
            return [self.get_detail_page(item) for item in tqdm(result, total=len(result))]

        with ThreadPoolExecutor(max_workers=detail_workers) as executor:
            return list(tqdm(
                executor.map(lambda item: self.get_detail_page(item, session=requests), result),
                total=len(result),
            ))

    def get_source_categories(self):
        products = self.query_json.get("Products", "")
        return [product.strip() for product in products.split(",") if product.strip()]

    def save_page_to_db(self, page, items):
        if not self.paper_repository:
            return

        saved_count = self.paper_repository.save_papers(
            items,
            query_pattern=self.query_pattern,
            source_categories=self.get_source_categories()
        )
        logger.success(f"第 {page} 页已保存 {saved_count} 条数据到数据库")

    def get_detail_page(self, temp_dic, session=None):
        # print(temp_dic)
        link = temp_dic.get('详情页链接')
        response = self._request(
            "get",
            link,
            headers=self.headers,
            proxies=self.proxies,
            cookies=self.cookies,
            session=session
        )

        text = response.text
        # print(text)
        tree = etree.HTML(text)
        # 作者信息
        author_list = tree.xpath("//h3[@class='author'][1]/span")
        author_str = ""
        email_author_pattern = r"通讯作者地址\s+var cau = \"(.*?)\";"
        email_author_match = re.findall(email_author_pattern, text)
        email_author = email_author_match[0][:-1] if email_author_match else ""
        # print(email_author)
        for author in author_list:
            author_name = self.get_element(author.xpath("./a/text()"))
            sup = self.get_element(author.xpath("./a/sup/text()"))
            sup = f"【{sup}】" if sup else ""
            # print(author_name, sup)

            # 判断是否为通讯作者
            email_flag = "*" if author_name == email_author else ""

            if author_name:
                author_str += f"{sup}{author_name}{email_flag};"
            else:
                author_name = self.get_element(author.xpath("./text()"))
                sup = self.get_element(author.xpath("./sup/text()"))
                sup = f"【{sup}】" if sup else ""
                author_str += f"{sup}{author_name}{email_flag};"

        # print(author_str)
        # 院校信息
        organization_list = tree.xpath("//h3[@class='author'][2]/span")
        organization_str = ""
        for organization in organization_list:
            organization_name = self.get_element(organization.xpath("./a/text()"))
            if organization_name:
                organization_str += f"{organization_name};"
            else:
                organization_name = self.get_element(organization.xpath(".//text()"))
                organization_str += f"{organization_name};"

        # print(organization_str)
        # 摘要
        abstract = self.get_element(tree.xpath("//span[@class='abstract-text']//text()"))

        # 关键词
        keywords = self.get_element(tree.xpath("//p[@class='keywords']//text()"))

        # 基金资助
        funds = self.get_element(tree.xpath("//p[@class='funds']//text()"))

        # other_info
        other_info_list = tree.xpath("//li[@class='top-space']")
        for other_info in other_info_list:
            name = self.get_element(other_info.xpath("./span/text()"))
            value = self.get_element(other_info.xpath("./p/text()"))
            temp_dic.update({name: value})
        temp_dic.update({
            "作者": author_str,
            "组织": organization_str,
            "摘要": abstract,
            "关键词": keywords,
            "基金资助": funds,
        })
        return temp_dic

    def run(self):
        try:
            turn_page, first_page_source, total_page = self.get_first_page()
            logger.info(f"共有 {total_page} 页")
            if self.output_estimated_time:
                estimated_seconds = total_page * self.ESTIMATED_SECONDS_PER_PAGE
                logger.info(f"预计耗时: {self.format_duration(estimated_seconds)}")
            if self.limit_pages:
                total_page = min(total_page, self.limit_pages)
                logger.info(f"本次最多爬取 {total_page} 页")
            result = []
            items = self.get_page_data(first_page_source)
            result.extend(items)
            logger.info(f"第 1 页获取到 {len(items)} 条数据！")
            self.save_page_to_db(1, items)

            for page in range(2, total_page + 1):
                turn_page, page_source = self.get_other_page(page, turn_page)
                items = self.get_page_data(page_source)
                logger.info(f"第 {page} 页获取到 {len(items)} 条数据！")
                result.extend(items)
                self.save_page_to_db(page, items)
            if self.print_result:
                print(result)
            else:
                logger.info(f"本次共获取 {len(result)} 条数据")
        finally:
            if self.paper_repository:
                self.paper_repository.close()


