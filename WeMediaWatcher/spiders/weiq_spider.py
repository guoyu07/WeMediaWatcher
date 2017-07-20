from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http.request import Request
from scrapy import log
from WeMediaWatcher.items import WeiqUser
import time
from scrapy.http import FormRequest
import json
import pymongo
import time
import random


class WeiQUser_Spider(Spider):
    name = "weiq"
    allowed_domains = ["weiq.cn"]
    start_urls = [
        "http://www.weiq.com/Owner/Newweibo/mediauser/class/11/p/%.html"
    ]

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
        "Connection": "keep-alive",
        "Host": "www.weiq.com",
        "Upgrade-Insecure-Requests": 1,
        "Content-Type": " application/x-www-form-urlencoded; charset=UTF-8",
        "Referer": "http://www.weiq.com/Owner/Newweibo/mediauser/class/11/p/5.html",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
    }

    cookie = {
        "PHPSESSID": "pihb874v8plodojjfc9g26bei0",
        "UM_distinctid": "15d5ea9619f7b6-01a30db3e9f502-8383667-1fa400-15d5ea961a0aef",
        "wadmincode": "pihb874v8plodojjfc9g26bei0",
        "_getmc": "AAVeVwczUWZSbl0wVWtUaAo2AmwMOFNjV2I%3D",
        "weiq_uuid": "05EADB7F-0BF3-4D6A-9D42-19A4142362BA",
        "CNZZDATA1260733938": "261154917-1500529172-%7C1500529172",
        "Hm_lvt_93deba7872e0b27eee3d1e5a437ceafe": "1500531745",
        "Hm_lpvt_93deba7872e0b27eee3d1e5a437ceafe": "1500533043"
    }

    def start_requests(self):
        for i in range(1, 194):
            url = "http://www.weiq.com/Owner/Newweibo/mediauser/class/11/p/{}.html".format(str(i))
            sleeptime = random.randint(1, 5)
            time.sleep(sleeptime)
            print(url)
            yield Request(url, headers=self.headers, cookies=self.cookie)

    def parse(self, response):
        sel = Selector(response)
        wei_item_list = sel.xpath("//tbody//tr")
        items = []
        for idx, item, in enumerate(wei_item_list):
            if idx != 0:
                name = item.xpath("td")[1].xpath("p/a/text()").extract()[0]
                type = item.xpath("td")[2].xpath("text()").extract()[0].strip()
                level = len(item.xpath("td")[3].xpath("div//img"))
                price_t = item.xpath("td")[4].xpath("p//span")[0].xpath("text()").extract()[0]
                price_r = item.xpath("td")[4].xpath("p//span")[1].xpath("text()").extract()[0]
                fans = item.xpath("td")[5].xpath("span/text()").extract()[0]
                weiq_item = WeiqUser()
                weiq_item["user_name"] = name
                weiq_item["account_type"] = type
                weiq_item["impact_level"] = level
                weiq_item["price_tweet"] = price_t
                weiq_item["price_retweet"] = price_r
                weiq_item["fans"] = fans
                items.append(weiq_item)
        return items
