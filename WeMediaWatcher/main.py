import scrapy.cmdline as c

c.execute(["scrapy", "crawl", "mafengwo_note", "-o", "items.json"])
# c.execute(["scrapy", "crawl", "mafengwo_note"])
