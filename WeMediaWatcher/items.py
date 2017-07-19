# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field


class WemediawatcherItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class MafengwoUserItem(scrapy.Item):
    user_name = Field()
    user_info = Field()
    user_level = Field()
    user_location = Field()
    follow = Field()
    fans = Field()
    honey = Field()
    crawl_time = Field()


class MafengwoNoteItem(scrapy.Item):
    note_id = Field()
    user_name = Field()
    user_id = Field()
    note_title = Field()
    note_type = Field()
    note_href = Field()
    # 星级游记
    is_xj = Field()
    # 蜂首游记
    is_fs = Field()
    # 阅读数
    pv = Field()
    # 评论
    comment = Field()
    # 收藏
    collect = Field()
    # 顶
    favour = Field()
    # 创建时间
    create_time = Field()
    # 数据抓取时间
    crawl_time = Field()


class QiongyouUserItem(scrapy.Item):
    user_name = Field()
    user_id = Field()
    user_level = Field()
    user_location = Field()
    follow = Field()
    fans = Field()
    crawl_time = Field()


class QiongyouNoteItem(scrapy.Item):
    note_id = Field()
    user_name = Field()
    user_id = Field()
    note_title = Field()
    # 精华等级
    note_type = Field()
    note_href = Field()
    pv = Field()
    # 评论
    comment = Field()
    # 收藏
    collect = Field()
    # 顶
    favour = Field()
    # 创建时间
    create_time = Field()
    # 数据抓取时间
    crawl_time = Field()


class BaiduUserItem(scrapy.Item):
    user_id = Field()
    user_name = Field()
    user_info = Field()
    user_level = Field()
    user_location = Field()
    crawl_time = Field()


class BaiduNoteItem(scrapy.Item):
    pass
