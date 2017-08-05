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
        "http://www.weiq.com/Owner/Newweibo/mediauser/p/{}.html"
    ]

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
        "Connection": "keep-alive",
        "Host": "www.weiq.com",
        "Upgrade-Insecure-Requests": 1,
        "Content-Type": " application/x-www-form-urlencoded; charset=UTF-8",
        "Referer": "http://www.weiq.com/owner/newweibo/mediauser.html",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
    }

    cookie = {
        "UM_distinctid": "15d315a82d2741-0b16c507de293b-8383667-1fa400-15d315a82d3272",
        "PHPSESSID": "vgk1t6knc9efqv9dodk9o9i3r1",
        "wadmincode": "vgk1t6knc9efqv9dodk9o9i3r1",
        "_getmc": "AGhePAc7UWVSYF1eVQxUYAo2Am0MMVNrV2lUYFI6DW1bMVA0",
        "weiq_uuid": "E97DEDE6-C032-40BC-98C0-5E821D9CD738",
        "CNZZDATA1260733938": "562659707-1499771446-http%253A%252F%252Fwww.baidu.com%252F%7C1501847347",
        "Hm_lvt_93deba7872e0b27eee3d1e5a437ceafe": "1500636483,1501064137,1501147478,1501851226",
        "Hm_lpvt_93deba7872e0b27eee3d1e5a437ceafe": "1501851493"
    }

    def start_requests(self):
        for i in range(1, 1327):
            url = "http://www.weiq.com/Owner/Newweibo/mediauser/p/{}.html".format(str(i))
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
                weibo_id = item.xpath("td")[1].xpath("p/a/@href").extract()[0].replace("/showdetailweibo/", "").replace(
                    ".html", "")
                weiq_item = WeiqUser()
                weiq_item["user_name"] = name
                weiq_item["account_type"] = type
                weiq_item["impact_level"] = level
                weiq_item["price_tweet"] = float(price_t.replace("￥", ""))
                weiq_item["price_retweet"] = float(price_r.replace("￥", ""))
                weiq_item["fans"] = fans
                weiq_item["weibo_id"] = weibo_id
                items.append(weiq_item)
        return items
