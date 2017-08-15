import scrapy.cmdline as c

c.execute(["scrapy", "crawl", "ctrip_note", "-o", "items.csv"])
# c.execute(["scrapy", "crawl", "baidulvyou", "-o", "items.json"])
# c.execute(["scrapy", "crawl", "livecpt", "-o", "items.json"])
# c.execute(["scrapy", "crawl", "weiq", "-o", "items.json"])
# c.execute(["scrapy", "crawl", "qiongyou_note", "-o", "items.json"])
# c.execute(["scrapy", "crawl", "mafengwo_note"])
