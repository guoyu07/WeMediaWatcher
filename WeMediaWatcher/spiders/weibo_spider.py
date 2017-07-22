from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http.request import Request
from scrapy import log
from WeMediaWatcher.items import MafengwoUserItem, MafengwoNoteItem
import time
from scrapy.http import FormRequest
import json
import pymongo
import time


class WeiboUser_Spider(Spider):
    name = "weibo"
    allowed_domains = ["weibo.cn"]
    start_urls = [
        "http://weibo.com/p/1005051918611551/info"
    ]

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "weibo.com",
        "Upgrade-Insecure-Requests": 1,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
    }

    cookie = {
        "YF-Page-G0": "d52660735d1ea4ed313e0beb68c05fc5",
        "SUB": "_2AkMuLMrYf8NxqwJRmPkdyW_gaYl_ygnEieKYcDsDJRMxHRl-yT83qmxetRB1495xcfJcIPGEBB5GYe3aIgPo_g..",
        "SUBP": "0033WrSXqPxfM72-Ws9jqgMF55529P9D9WWb_MfQH4rn1bLchOVUc0Yr",
        "_s_tentry": "-",
        "Apache": "2607444537988.215.1500530166356",
        "SINAGLOBAL": "2607444537988.215.1500530166356",
        "ULV": "1500530166384:1:1:1:2607444537988.215.1500530166356:",
        "YF-Ugrow-G0": "5b31332af1361e117ff29bb32e4d8439",
        "WBtopGlobal_register_version": "3fd0ccee5c381362"
    }

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, headers=self.headers, cookies=self.cookie)

    def parse(self, response):
        sel = Selector(text=response.body.decode('utf-8'))
        for i in range(0, 15):
            script_str = sel.xpath("script")[i].extract()
            if script_str.startswith("<script>FM.view(") and script_str.endswith(")</script>"):
                script_content_str = script_str.replace("<script>FM.view(", "").replace(")</script>", "")
                script_content_html = eval(script_content_str).get("html")
                if script_content_html is not None:
                    content_sel = Selector(text=script_content_html)
                    # desc_list = content_sel.xpath("//li[contains(@class,'li_1')]")
                    # if len(desc_list) > 0:
                    #     for desc_item in desc_list:
                    #         desc_item
                    cotent_l = content_sel.xpath("//li[contains(@class,'li_1')]//span//text()").extract()
                    content_sel.xpath("//li[contains(@class,'li_1')]//span//text()").extract()
                    desc_dict = {}
                    for idx, c in cotent_l:
                        if c.strip("") == "":
                            print(c.strip())
