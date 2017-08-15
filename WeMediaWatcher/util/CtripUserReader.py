data_file = "C:\PycharmProjects\WeMediaWatcher\WeMediaWatcher\data\Influencer dashboard database 0729.csv"
file = open(data_file, 'r', encoding="utf-8")
lines = tuple(file)
d = {}
for line in lines:
    content_list = line.split(",")
    if content_list[6].startswith("http://you.ctrip.com"):
        if content_list[6].endswith("/journals"):
            d[content_list[0]] = content_list[6]
        else :
            d[content_list[0]] = content_list[6] + "/journals"
print(d)
