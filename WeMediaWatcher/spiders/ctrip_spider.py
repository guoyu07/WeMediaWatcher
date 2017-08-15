from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy import log
from WeMediaWatcher.items import CtripUser, CtripNoteItem
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


class Ctrip_Note_Spider(Spider):
    name = "ctrip_note"
    allowed_domains = ["http://you.ctrip.com"]

    user_list = [
        "http://you.ctrip.com/members/CE0D0FC0D0644A01B26C8BD2F2B43400/journals,29102663,用户29102663,张大枪",
        "http://you.ctrip.com/members/7E4EBF9E6E404AD8AE5276C689FAA194/journals,31769470,陆建华摄影,陆建华摄影",
        "http://you.ctrip.com/members/kdimage/journals,17678071,凯德印象,凯德印象",
        "http://you.ctrip.com/members/D4C0AAB152B34F91AE102BE3A763850E/journals,2619356,蘑菇张-NKU,蘑菇张-NKU",
        "http://you.ctrip.com/members/liluo20/journals,2817514,鱼鱼众生,鱼鱼众生liluo",
        "http://you.ctrip.com/members/bbbf3929482843b88a07908864ce26cf/journals,10584384,北石同学,北石同学",
        "http://you.ctrip.com/members/7B2022CA7A1B4ED689CE4ACD1D9D8448/journals,3836546,任紫玉ziyu,任紫玉ziyu",
        "http://you.ctrip.com/members/abby5/journals,2361425,Abby妞,Abby45",
        "http://you.ctrip.com/members/1C79F0A63B03460AB0B87438AF5AC7F2/journals,53205661,我就是吹风,我就是吹风",
        "http://you.ctrip.com/members/E221E7C0ED364362A4D93DEF1C654303/journals,6612378,杨舒涵-YOUNG,杨舒涵-YOUNG",
        "http://you.ctrip.com/members/linaimemory/journals,93762,林爱念念,林晶莹Lily",
        "http://you.ctrip.com/members/tuanzi/journals,23506033,团子E菲,团子E菲",
        "http://you.ctrip.com/members/manyouren/journals,19315293,慢游人吴晖,吴晖",
        "http://you.ctrip.com/members/zytxx/journals,14418317,志远天下行,志远天下行",
        "http://you.ctrip.com/members/E362841E3D454940ACE9602AAF3FF526/journals,52542763,爱幻想的sasa,爱幻想的sasa",
        "http://you.ctrip.com/members/xiaomanxing/journals,13447200,满星Min,摄影师满星",
        "http://you.ctrip.com/members/jqzys080119/journals,1989478,White小晴,White小晴",
        "http://you.ctrip.com/members/rickycai870/journals,1459496,菜尾蝗在路上,菜尾蝗-旅行摄影",
        "http://you.ctrip.com/members/6D4A49C0849C4D75BD97A2E3E7D920BC/journals,1967998,je****nui,jennynui",
        "http://you.ctrip.com/members/10EF2C3999DE4F81BC0AC902B451C435/journals,538265,行者老湖,行者老湖",
        "http://you.ctrip.com/members/41CCD9979148431D975ADDFFF9B75C6D/journals,21586764,狐狸猫amei,狐狸猫amei",
        "http://you.ctrip.com/members/4F0F666B978644F28BC2CAD7F03E8ECB/journals,11534189,青春河边巢,青春河边巢",
        "http://you.ctrip.com/members/shaolonglingdu/journals,36350098,龙先生旅行日记,劭龙零度",
        "http://you.ctrip.com/members/B0645CDD58174F7F999BD6B149C88B0B/journals,61415216,幻想家japaul,幻想家japaul",
        "http://you.ctrip.com/members/youxiaotian/journals,50058201,游遍天下笑问苍天,游笑天",
        "http://you.ctrip.com/members/xu900/journals,2638453,草原900,草原900",
        "http://you.ctrip.com/members/C36F44D3D4E84D24A80A0B09BF52056A/journals,4927858,游向蓝天的鱼,游向蓝天的鱼"
    ]

    def start_requests(self):
        url = "http://you.ctrip.com/membersite/TravelTag/TravelNotesNextPage?"
        requests = []
        user_name_iuid = ""
        for user_info in self.user_list:
            userid = user_info.split(",")[1]
            for i in range(1, 10):
                page_url = url + "pageIndex=" + str(i) + "&userid=" + userid + "&isOwner=0"
                request = Request(page_url, callback=self.parse_model)
                requests.append(request)
        return requests

    def parse_model(self, response):
        sel = Selector(response)
        item_list = []
        note_list = sel.xpath("//dd")
        for note in note_list:
            userid = ""
            user_name = ""
            user_raw_name = ""
            for params in response.url.split("&"):
                if params.startswith("userid="):
                    userid = params.replace("userid=", "")
            for user_info in self.user_list:
                id = user_info.split(",")[1]
                if id == userid:
                    user_raw_name = user_info.split(",")[3]
                    user_name = user_info.split(",")[2]
            note_name = note.xpath("strong//a/text()").extract()[0]
            note_location = note.xpath("q//a/text()").extract()[0]
            pv = note.xpath("em/text()").extract()[0]
            comment = note.xpath("em/text()").extract()[1]
            item = CtripNoteItem()
            item["create_time"] = note.xpath("span/text()").extract()[0]
            item["user_name"] = user_name
            item["user_raw_name"] = user_raw_name
            item["user_id"] = userid
            item["title"] = note_name
            item["note_location"] = note_location
            item["pv"] = pv
            item["comment"] = comment
            item_list.append(item)
        return item_list
