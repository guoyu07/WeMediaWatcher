from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy import log
from WeMediaWatcher.items import QiongyouUserItem, QiongyouNoteItem
import time
from scrapy.http import FormRequest
import json
import pymongo
import time


class Qiongyou_Spider(Spider):
    name = "qiongyou"
    allowed_domains = ["qyer.cn"]
    start_urls = [
        "http://www.qyer.com/u/1267796"
    ]

    def parse(self, response):
        # time.sleep(t)
        sel = Selector(response)
        item = QiongyouUserItem()
        item['user_name'] = sel.xpath('//div[contains(@class,"infos")]/h3/strong/text()').extract()
        item['user_location'] = \
            sel.xpath('//div[contains(@class,"infos")]/div[contains(@class,"fontSong")]/span/text()').extract()[0]
        item['user_level'] = sel.xpath(
            '//div[contains(@class,"infos")]/div[contains(@class,"fontSong")]/a/text()').extract()
        item['follow'] = sel.xpath('//div[contains(@class,"attent")]//em/text()').extract()[0]
        item['fans'] = sel.xpath('//div[contains(@class,"attent")]//em/text()').extract()[1]
        return item


class QiongyouNote_Spider(Spider):
    name = "qiongyou_note"
    allowed_domains = ["qyer.cn", "qyer.com"]

    @staticmethod
    def load_user_dict():
        user_name_iuid = {"aero4400": "1267796"}
        return user_name_iuid

    @staticmethod
    def user_name_uid(request_body):
        params = request_body.decode("utf-8").split("&")
        user_info = {}
        for kv in params:
            if kv.split("=")[0] == "useruid":
                user_info["useruid"] = kv.split("=")[1]
            if kv.split("=")[0] == "username":
                user_info["username"] = kv.split("=")[1]
        return user_info

    def start_requests(self):
        url = "http://www.qyer.com/ajax.php"
        requests = []
        user_name_iuid = self.load_user_dict()
        for user_name, user_iuid in user_name_iuid.items():
            for i in range(1, 4):
                form_data = {
                    "action": "getuserhomethreadlist",
                    "page": str(i),
                    "useruid": user_iuid,
                    "type": "userhometravellist",
                    "username": user_name
                }
                request = FormRequest(url, callback=self.parse_model, formdata=form_data)
                requests.append(request)
        return requests

    def parse_model(self, response):
        user_info = self.user_name_uid(response.request.body)
        sel = Selector(response)
        note_item_list = sel.xpath("//div[contains(@class,'item')]")
        model_items = []
        for note_item in note_item_list:
            note_title = note_item.xpath("a//div//h3/text()").extract()[0]
            create_date = note_item.xpath("a//div//span[contains(@class,'fr')]/text()").extract()[0]
            note_pv = note_item.xpath("a//div//span[contains(@class,'poi')]/text()").extract()[0]
            note_common = note_item.xpath("a//div//span[contains(@class,'common')]/text()").extract()[0]
            note_like = note_item.xpath("a//div//span[contains(@class,'like')]/text()").extract()[0]
            item = QiongyouNoteItem()
            item["note_id"] = note_item.xpath("a/@href").extract()[0].split("-")[1]
            item["user_name"] = user_info["username"]
            item["user_id"] = user_info["useruid"]
            item["note_title"] = note_title
            item["note_type"] = note_item.xpath("a//div[contains(@class,'tips')]/text()").extract()[0]
            # note_item.xpath("a/div[contains(@class,'img')]//div[contains(@class,'tips')]")
            item["note_href"] = note_item.xpath("a/@href").extract()[0].replace("//", "")
            item["pv"] = note_pv
            item["comment"] = note_common
            # item["collect"]
            item["favour"] = note_like
            item["create_time"] = create_date
            item["crawl_time"] = time.time()
            model_items.append(item)
        return model_items
