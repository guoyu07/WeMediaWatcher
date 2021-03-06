from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy import log
from WeMediaWatcher.items import MafengwoUserItem, MafengwoNoteItem
import time
from scrapy.http import FormRequest
import json
import pymongo
import time
import random


class Mafengwo_Spider(Spider):
    name = "mafengwo"
    allowed_domains = ["mafengwo.cn"]
    start_urls = [
        "http://www.mafengwo.cn/u/5094364.html",
        "http://www.mafengwo.cn/u/biggun.html",
        "http://www.mafengwo.cn/u/sunjiahui.html",
        "http://www.mafengwo.cn/u/yannleec.html",
        "http://www.mafengwo.cn/u/sicilia.html"
    ]

    def parse(self, response):
        # time.sleep(t)
        sel = Selector(response)
        item = MafengwoUserItem()
        item['user_name'] = sel.xpath('//div[contains(@class,"MAvaName")]/text()').extract_first().replace("\n",
                                                                                                           "").strip()
        item['user_info'] = sel.xpath('//div[contains(@class,"MProfile")]/pre/text()').extract()
        item['user_location'] = sel.xpath('//span[contains(@class,"MAvaPlace")]/text()').extract()
        item['follow'] = sel.xpath('//div[contains(@class,"MAvaNums")]/strong/a/text()').extract()[0]
        item['fans'] = sel.xpath('//div[contains(@class,"MAvaNums")]/strong/a/text()').extract()[1]
        item['honey'] = sel.xpath('//div[contains(@class,"MAvaNums")]/strong/a/text()').extract()[2]
        item["crawl_time"] = time.time()
        return item


class MafengwoNote_Spider(Spider):
    name = "mafengwo_note"
    allowed_domains = ["mafengwo.cn"]

    @staticmethod
    def load_user_list():
        user_name_iuid = {'凯德印象': '773299', '张大枪': '9939790', '鱼鱼众生liluo': '5646072', '游向蓝天的鱼': '40894909',
                          '小小莎老师': '80825723', '蘑菇张-NKU': '5094364', '北石同学': '19156318', '呆呆strajectory': '78139115',
                          '方片7': '43132393', 'Thomas看看世界': '19382312', 'Abby45': '5017331', '林晶莹Lily': '50948302',
                          '吴晖': '48561087', '王超irwin': '1179698', '杨舒涵-YOUNG': '5400739', '我就是吹风': '62297660',
                          '团子E菲': '38551864', '湖北宋君': '77068946', '菜尾蝗-旅行摄影': '10519252', '志远天下行': '61009859',
                          '爱幻想的sasa': '5217865', '摄影师one': '5029534', '沙漠玫瑰_': '17341906', 'White小晴': '10344859',
                          'jennynui': '85324353', 'ayuyou': '5110334', '行者老湖': '326520', '青春河边巢': '40987395',
                          '劭龙零度': '71028018', '哈先生Ha': '89888129', '一路Y-Y': '5225694', '草原900': '19130841',
                          '幻想家japaul': '63760012', '游笑天': '668015','榛美去': '814051'}
        return user_name_iuid

    name_id_dict = {'凯德印象': '773299', '张大枪': '9939790', '鱼鱼众生liluo': '5646072', '游向蓝天的鱼': '40894909',
                    '小小莎老师': '80825723', '蘑菇张-NKU': '5094364', '北石同学': '19156318', '呆呆strajectory': '78139115',
                    '方片7': '43132393', 'Thomas看看世界': '19382312', 'Abby45': '5017331', '林晶莹Lily': '50948302',
                    '吴晖': '48561087', '王超irwin': '1179698', '杨舒涵-YOUNG': '5400739', '我就是吹风': '62297660',
                    '团子E菲': '38551864', '湖北宋君': '77068946', '菜尾蝗-旅行摄影': '10519252', '志远天下行': '61009859',
                    '爱幻想的sasa': '5217865', '摄影师one': '5029534', '沙漠玫瑰_': '17341906', 'White小晴': '10344859',
                    'jennynui': '85324353', 'ayuyou': '5110334', '行者老湖': '326520', '青春河边巢': '40987395',
                    '劭龙零度': '71028018', '哈先生Ha': '89888129', '一路Y-Y': '5225694', '草原900': '19130841',
                    '幻想家japaul': '63760012', '游笑天': '668015','榛美去': '814051'}

    id_name_dict = {v: k for k, v in name_id_dict.items()}

    @staticmethod
    def user_name_iuid(request_body):
        params = request_body.decode("utf-8").split("&")
        user_info = {}
        for kv in params:
            if kv.split("=")[0] == "iUid":
                user_info["iUid"] = kv.split("=")[1]
            elif kv.split("=")[0] == "user_name":
                user_info["user_name"] = kv.split("=")[1]
        return user_info

    def parse_model(self, response):
        user_info = self.user_name_iuid(response.request.body)
        json_body = json.loads(response.body.decode('gbk').encode('utf-8'))
        html = json_body["payload"]["html"]
        sel = Selector(text=html)
        note_list = sel.xpath('//div[contains(@class,"note_title")]')
        model_items = []
        for note in note_list:
            note_item = MafengwoNoteItem()
            note_info = note.xpath("div[contains(@class,'note_info')]")
            title_info = note_info.xpath("h3//a")
            note_type = "default"
            if len(title_info) == 2:
                note_type = title_info.xpath("@title").extract()[0]
                note_title = title_info.xpath("@title").extract()[1]
            else:
                note_title = title_info.xpath("@title").extract()[0]
            if note_type == "蜂首游记":
                note_href = title_info.xpath("@href").extract()[1]
            else:
                note_href = title_info.xpath("@href").extract()[0]
            note_more = note_info.xpath("div//em//text()").extract()
            pv = note_more[0].split("/")[0]
            comment = note_more[0].split("/")[1]
            collect = note_more[1]
            note_time = note_info.xpath("div//span[contains(@class,'time')]//text()").extract()[0]
            # 装配
            note_item["note_id"] = note_href.replace("http://www.mafengwo.cn", "").replace("/i/", "").replace(".html",
                                                                                                              "")
            note_item["user_name"] = self.id_name_dict[user_info["iUid"]]  # user_info["user_name"]
            note_item["user_id"] = user_info["iUid"]
            note_item["note_title"] = note_title
            note_item["note_href"] = "http://www.mafengwo.cn/i/" + note_item["note_id"] + ".html"
            note_item["pv"] = pv
            note_item["comment"] = comment
            note_item["collect"] = collect
            note_item["create_time"] = note_time
            note_item["crawl_time"] = time.time()
            if note_type != "default":
                note_item["note_type"] = note_type
            model_items.append(note_item)
        return model_items

    def start_requests(self):
        url = "http://www.mafengwo.cn/wo/ajax_post.php"
        requests = []
        user_name_iuid = self.load_user_list()
        for user_name, user_iuid in user_name_iuid.items():
            for i in range(1, 7):
                form_data = {
                    "sAction": "getArticle",
                    "iPage": str(i),
                    "iUid": user_iuid,
                    "user_name": user_name
                }
                request = FormRequest(url, callback=self.parse_model, formdata=form_data)
                requests.append(request)
        return requests
