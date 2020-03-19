import os,json,requests


def getgameid(matchlist):
    gameid = []
    gameids = matchlist["msg"]["games"]
    for g in gameids:
        gameid.append(g["gameId"])
    print(len(gameid))
    return gameid


def spdiergameid(cookie):
    header = {'Cookie': cookie}
    r = requests.get(
        "http://lol.sw.game.qq.com/lol/api/?c=Battle&a=matchList&areaId=1&accountId=2978811027&queueId=70,72,73,75,76,78,96,98,100,300,310,313,317,318,325,400,420,430,450,460,600,610,940,950,960,980,990,420,440,470,83,800,810,820,830,840,850&r1=matchList",headers=header)
    return r.text.strip("var matchList =")


def spidergamedetail(cookie):
    header = {'Cookie': cookie}
    gameidjson = json.loads(spdiergameid(cookie))  # 爬比赛列表
    print(gameidjson)
    if not os.path.exists("./battledetaildata") :
        os.mkdir("./battledetaildata")
    gameid = getgameid(gameidjson) # 获取gameid list
    count = 0
    for gid in gameid:  # 爬取详细数据并保存到本地
        print(gid)
        count += 1
        print(count)
        res = requests.get(
            "https://lol.sw.game.qq.com/lol/api/?c=Battle&a=combatGains&areaId=1&gameId=%s&r1=combatGains" % gid,
            headers=header).text.strip("var combatGains = ")

        datafile = open("./battledetaildata/%s.json" % gid, 'w')
        datafile.write(res)
        datafile.close()


def delaram(filename):
    data = json.load(open("./battledetaildata/%s"%filename))
    # 删除人机
    # print([ d['queueRating'] for d in data["msg"]['participants']])

    if data["msg"]["gameInfo"]["gameMode"] == "ARAM":
        print("./battledetaildata/%s"%filename)
        os.remove("./battledetaildata/%s"%filename)
        return True

    if 0 in [ d['queueRating'] for d in data["msg"]['participants']]:
        print("./battledetaildata/%s"%filename)
        os.remove("./battledetaildata/%s"%filename)
        return True
    # 删除未完成的对局
    if data["msg"]["gameStats"]["completed"] == False:
        print("./battledetaildata/%s"%filename)
        os.remove("./battledetaildata/%s"%filename)
        return True

    return False


def runspider(cookie):
    spidergamedetail(cookie)
    fl = os.listdir('/battledetaildata')
    map(delaram,fl)


if __name__ == '__main__':
    cookie = "eas_sid=a1V568q2R454D5D229q4i8X7M4; pgv_info=ssid=s795670611; pgv_pvid=5918139850; pgv_pvi=8972125184; pgv_si=s2693123072; _qpsvr_localtk=0.835008600096897; uin=o2272617134; skey=@5IEsyjpUO; RK=jUxRDgCW+o; ptcz=ffaed72758af4ddcf58a4e2416c90737117994fa6724fff3dcc80eb61dd48233; p_uin=o2272617134; pt4_token=VtWSM6sv9sst4OSkMh02OtdUgT6DMNGonXxxFl8VJx4_; p_skey=WmdmZXetyxd7ZFxY8HrWtFT10ugdekvcOQMFGyrVE1M_; IED_LOG_INFO2=userUin%3D2272617134%26nickName%3DM90ic%26userLoginTime%3D1582445349; uin_cookie=o2272617134; ied_qq=o2272617134; LOLWebSet_AreaBindInfo_2272617134=%257B%2522areaid%2522%253A%25221%2522%252C%2522areaname%2522%253A%2522%25E8%2589%25BE%25E6%25AC%25A7%25E5%25B0%25BC%25E4%25BA%259A%2520%25E7%2594%25B5%25E4%25BF%25A1%2522%252C%2522sRoleId%2522%253A0%252C%2522roleid%2522%253A%25222272617134%2522%252C%2522rolename%2522%253A%2522%25E5%258F%25AA%25E8%25A6%2581%25E8%2583%25BD%25E8%25B5%25A2%25E5%2581%259A%25E6%25A5%25A0%25E9%2583%25BD%25E8%25A1%258C%2522%252C%2522checkparam%2522%253A%2522lol%257Cyes%257C2272617134%257C1%257C2272617134*%257C%257C%257C%257C%2525E5%25258F%2525AA%2525E8%2525A6%252581%2525E8%252583%2525BD%2525E8%2525B5%2525A2%2525E5%252581%25259A%2525E6%2525A5%2525A0%2525E9%252583%2525BD%2525E8%2525A1%25258C*%257C%257C%257C1582445354%2522%252C%2522md5str%2522%253A%252250C65EBA8E648AB9F37FFBF52155AF67%2522%252C%2522roleareaid%2522%253A%25221%2522%252C%2522sPartition%2522%253A%25221%2522%257D; lolqqcomrouteLine=index-tool_main_main_main_main_space_space"
    runspider(cookie)