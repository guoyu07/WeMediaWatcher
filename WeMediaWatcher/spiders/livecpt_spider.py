from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http.request import Request
from scrapy import log
from WeMediaWatcher.items import LiveCptUser
import time
from scrapy.http import FormRequest
import json
import pymongo
import time
import random


# class LivecptUser_spider(Spider):
#     name = "livecpt"
#     allowed_domains = ["weiq.com"]
#     start_urls = [
#         "http://www.weiq.com/Livecpt/Invite/index/p/{}.html"
#     ]
#     headers = {
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#         "Accept-Encoding": "gzip, deflate",
#         "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
#         "Connection": "keep-alive",
#         "Host": "www.weiq.com",
#         "Upgrade-Insecure-Requests": 1,
#         "Content-Type": " application/x-www-form-urlencoded; charset=UTF-8",
#         "Referer": "http://www.weiq.com/livecpt/invite/index.html",
#         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
#     }
#
#     cookie = {
#         "UM_distinctid": "15d315a82d2741-0b16c507de293b-8383667-1fa400-15d315a82d3272",
#         "PHPSESSID": "ksa0kon8qgn7krs32khf5ifvh4",
#         "weiq_uuid": "69264C7E-0512-4812-BFE4-5CBD81314709",
#         "session_id": "ksa0kon8qgn7krs32khf5ifvh4",
#         "wadmincode": "ksa0kon8qgn7krs32khf5ifvh4",
#         "_getmc": "AGhePAc7UWVSYF1eVQxUYAo2Am0MMVNrV2lUYFI6DW1bMVA0",
#         "CNZZDATA1260733938": "562659707-1499771446-http%253A%252F%252Fwww.baidu.com%252F%7C1501233741",
#         "Hm_lvt_93deba7872e0b27eee3d1e5a437ceafe": "1500533027,1500636483,1501064137,1501147478",
#         "Hm_lpvt_93deba7872e0b27eee3d1e5a437ceafe": "1501235338"
#     }
#
#     def start_requests(self):
#         for i in range(1, 2):
#             url = LivecptUser_spider.start_urls[0].format(str(i))
#             sleeptime = random.randint(1, 5)
#             time.sleep(sleeptime)
#             print(url)
#             yield Request(url, headers=self.headers, cookies=self.cookie)
#
#     def parse(self, response):
#         sel = Selector(response)
#         livecpt_item_list = sel.xpath("//table//tr[contains(@class,'t_bodyList')]")
#         items = []
#         for idx, item, in enumerate(livecpt_item_list):
#             name = item.xpath("td//div//p//span/text()").extract()[0]
#             platform = item.xpath("td//div[contains(@class,'d_airBubble')]/text()").extract()[0].strip()
#             location = item.xpath("td//p[contains(@class,'po_word')]/text()").extract()[0]
#             fans = item.xpath("td[contains(@class,'c_fansNum')]/text()").extract()[0].strip()
#             avg = item.xpath("td[contains(@class,'c_readMax')]/text()").extract()[0].strip()
#             max = item.xpath("td[contains(@class,'c_readPers')]/text()").extract()[0].strip()
#             price_list = item.xpath(
#                 "td[contains(@class,'c_priceBox')]//span[contains(@class,'c_priceNum')]/text()").extract()
#             detail_url = "http://www.weiq.com" + item.xpath("td[contains(@class,'c_operate')]//a/@href")[0].extract()
#             livecpt_item = LiveCptUser()
#             livecpt_item["user_name"] = name
#             livecpt_item["platform"] = platform
#             livecpt_item["location"] = location
#             livecpt_item["fans"] = fans
#             livecpt_item["avg_audience_num"] = avg
#             livecpt_item["max_audience_num"] = max
#             livecpt_item["price_1"] = price_list[0]
#             livecpt_item["price_2"] = price_list[1]
#             livecpt_item["price_3"] = price_list[2]
#             livecpt_item["price_4"] = price_list[3]
#             livecpt_item["price_5"] = price_list[4]
#             livecpt_item["detail_url"] = detail_url
#             items.append(livecpt_item)
#         return items
