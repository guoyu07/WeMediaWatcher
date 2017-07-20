from scrapy.spider import Spider
from scrapy.selector import Selector
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

    def parse(self, response):
        sel = Selector(response)
        pass
