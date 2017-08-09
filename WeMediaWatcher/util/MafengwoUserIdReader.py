data_file = "C:\PycharmProjects\WeMediaWatcher\WeMediaWatcher\data\Influencer dashboard database 0729.csv"

file = open(data_file, 'r', encoding="utf-8")
lines = tuple(file)
d = {}
for line in lines:
    content_list = line.split(",")
    if content_list[3].startswith("http://www.mafengwo.cn"):
        d[content_list[0]] = content_list[3].replace("http://www.mafengwo.cn/u/", "").replace(".html", "")

print(d)