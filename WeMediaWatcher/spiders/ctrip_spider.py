from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy import log
from WeMediaWatcher.items import CtripUser
import time
from scrapy.http import FormRequest
from scrapy.http.request import Request
import json
import pymongo
import time
import random


class Ctrip_Spider(Spider):
    name = "ctrip"
    allowed_domains = ["http://you.ctrip.com"]
    user_homepage_dict = {'凯德印象': 'http://you.ctrip.com/members/kdimage/journals',
                          '张大枪': 'http://you.ctrip.com/members/CE0D0FC0D0644A01B26C8BD2F2B43400/journals',
                          '鱼鱼众生liluo': 'http://you.ctrip.com/members/liluo20/journals',
                          '游向蓝天的鱼': 'http://you.ctrip.com/members/C36F44D3D4E84D24A80A0B09BF52056A/journals',
                          '任紫玉ziyu': 'http://you.ctrip.com/members/7B2022CA7A1B4ED689CE4ACD1D9D8448/journals',
                          '蘑菇张-NKU': 'http://you.ctrip.com/members/D4C0AAB152B34F91AE102BE3A763850E/journals',
                          '陆建华摄影': 'http://you.ctrip.com/members/7E4EBF9E6E404AD8AE5276C689FAA194/journals',
                          '北石同学': 'http://you.ctrip.com/members/bbbf3929482843b88a07908864ce26cf/journals',
                          'Abby45': 'http://you.ctrip.com/members/abby5/journals',
                          '林晶莹Lily': 'http://you.ctrip.com/members/linaimemory/journals',
                          '吴晖': 'http://you.ctrip.com/members/manyouren/journals',
                          '杨舒涵-YOUNG': 'http://you.ctrip.com/members/E221E7C0ED364362A4D93DEF1C654303/journals',
                          '我就是吹风': 'http://you.ctrip.com/members/1C79F0A63B03460AB0B87438AF5AC7F2/journals',
                          '团子E菲': 'http://you.ctrip.com/members/tuanzi/journals',
                          '菜尾蝗-旅行摄影': 'http://you.ctrip.com/members/rickycai870/journals',
                          '志远天下行': 'http://you.ctrip.com/members/zytxx/journals',
                          '摄影师满星': 'http://you.ctrip.com/members/xiaomanxing/journals',
                          '爱幻想的sasa': 'http://you.ctrip.com/members/E362841E3D454940ACE9602AAF3FF526/journals',
                          'White小晴': 'http://you.ctrip.com/members/jqzys080119/journals',
                          'jennynui': 'http://you.ctrip.com/members/6D4A49C0849C4D75BD97A2E3E7D920BC/journals',
                          '行者老湖': 'http://you.ctrip.com/members/10EF2C3999DE4F81BC0AC902B451C435/journals',
                          '狐狸猫amei': 'http://you.ctrip.com/members/41CCD9979148431D975ADDFFF9B75C6D/journals',
                          '青春河边巢': 'http://you.ctrip.com/members/4F0F666B978644F28BC2CAD7F03E8ECB/journals',
                          '劭龙零度': 'http://you.ctrip.com/members/shaolonglingdu/journals',
                          '草原900': 'http://you.ctrip.com/members/xu900/journals',
                          '幻想家japaul': 'http://you.ctrip.com/members/B0645CDD58174F7F999BD6B149C88B0B/journals',
                          '游笑天': 'http://you.ctrip.com/members/youxiaotian/journals'}

    def start_requests(self):
        requests = []
        for user_name, user_homepage in self.user_homepage_dict.items():
            request = Request(user_homepage)
            requests.append(request)
        return requests

    def parse(self, response):
        sel = Selector(response)
        user_id = sel.xpath("//input[contains(@name,'hdn_userid')]/@value").extract()[0]
        user_name = sel.xpath("//span[contains(@class,'info-name')]/text()")[0].extract()
        gender = sel.xpath("//span[contains(@class,'J_gender')]//i/@title")[0].extract()
        if sel.xpath("//div[contains(@class,'column_info')]//dd/text()").extract():
            desc = sel.xpath("//div[contains(@class,'column_info')]//dd/text()").extract()[0].strip()
        else:
            desc = ""
        follow = sel.xpath("//ul[contains(@class,'cf')]//li//strong//a/text()").extract()[0].strip()
        fans = sel.xpath("//ul[contains(@class,'cf')]//li//strong//a/text()").extract()[1].strip()
        item = CtripUser()
        item["user_id"] = user_id
        item["user_name"] = user_name
        item["user_raw_name"] = [k for k, v in self.user_homepage_dict.items() if v == response.url][0]
        item["user_homepage"] = response.url
        item["gender"] = gender
        item["user_desc"] = desc
        item["fans"] = fans
        item["follow"] = follow
        return item
