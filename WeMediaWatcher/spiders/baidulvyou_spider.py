from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy import log
from WeMediaWatcher.items import BaiduUserItem, BaiduNoteItem
import time
from scrapy.http import FormRequest
import json
import pymongo
import time


class BaidulvyouUser_Spider(Spider):
    name = "baidulvyou"
    allowed_domains = ["lvyou.baidu.com"]
    start_urls = [
        "https://lvyou.baidu.com/user/notes/060519fe24de71cf701ca2a4"
    ]

    def parse(self, response):
        sel = Selector(response)
        item = BaiduUserItem()
        item["user_id"] = response.request.url.replace("https://lvyou.baidu.com/user/notes/", "")
        item["user_name"] = sel.xpath("//div[contains(@class,'master-info')]/h2/text()").extract()[0].replace("\n", "")
        item["user_info"] = sel.xpath("//div[contains(@class,'counselor-introduction')]/text()").extract()[0].strip()
        item["user_level"] = sel.xpath("//div[contains(@class,'personal-info')]/a/text()").extract()[0]
        item["user_location"] = sel.xpath("//div[contains(@class,'personal-info')]/span/text()").extract()[
            0].strip().replace("常住地 ", "")
        item["crawl_time"] = time.time()
        return item


class BaidulvNote_Spider(Spider):
    name = "baidulvyou_note"
    allowed_domains = ["lvyou.baidu.com"]

    @staticmethod
    def load_user_list():
        user_name_iuid = {"周杨fly": "060519fe24de71cf701ca2a4"}
        return user_name_iuid

    def start_requests(self):
        url = "http://www.mafengwo.cn/wo/ajax_post.php"
        requests = []
        user_name_iuid = self.load_user_list()
        for user_name, user_iuid in user_name_iuid.items():
            for i in range(1, 4):
                form_data = {
                    "pn": "10",
                    "rn": "10",
                    "pagelets[]": "pagelet_main",
                    "t": "769925"
                }
                pass
