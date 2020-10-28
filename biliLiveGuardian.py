import os
import csv
import time
import requests

# 这地方填房间号和uid
room_id = 0
uid = 0

dir_path = os.path.dirname(os.path.realpath(__file__))

def reqGuardList(page):
    res = requests.get("https://api.live.bilibili.com/xlive/app-room/v2/guardTab/topList", {
        "roomid" : room_id,
        "page" : page,
        "ruid" : uid,
        "page_size" : 29
    })
    res.encoding = "utf-8"
    return res.json()

def storeData(li):
    with open(os.path.join(dir_path, "{roomid}_guardian.csv".format(roomid = room_id)), 'a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, delimiter = ",", 
            fieldnames = ["uid", "名字", "排名", "舰长等级", "粉丝牌等级"])
        for guard in li:
            writer.writerow({
                "uid" : guard["uid"], 
                "名字" : guard["username"], 
                "排名" : guard["rank"], 
                "舰长等级" : guardLevelConvert(guard["guard_level"]),
                "粉丝牌等级" : guard["medal_info"]["medal_level"]
            })
        f.close()

def guardLevelConvert(guard_level):
    level = {
        1 : "总督",
        2 : "提督",
        3 : "舰长"
    }
    return level.get(guard_level)

data = reqGuardList(1)
total_page = data["data"]["info"]["page"]

with open(os.path.join(dir_path, "{roomid}_guardian.csv".format(roomid = room_id)), 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, delimiter = ",", 
        fieldnames = ["uid", "名字", "排名", "舰长等级", "粉丝牌等级"])
    writer.writeheader()
    for guard in data["data"]["top3"]:
            writer.writerow({
                "uid" : guard["uid"], 
                "名字" : guard["username"], 
                "排名" : guard["rank"], 
                "舰长等级" : guardLevelConvert(guard["guard_level"]),
                "粉丝牌等级" : guard["medal_info"]["medal_level"]
            })
    f.close()

print("总共有{num}个舰长，总共{total_page}页，当前第1页"
    .format(num = data["data"]["info"]["num"], total_page = total_page))
storeData(data["data"]["list"])

for i in range(2, total_page + 1):
    time.sleep(5)
    print("当前第{page}页".format(page = i))
    data = reqGuardList(i)
    storeData(data["data"]["list"])
