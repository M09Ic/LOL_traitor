import requests
import time, json,os
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from operator import add
from functools import reduce



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
        "http://lol.sw.game.qq.com/lol/api/?c=Battle&a=matchList&areaId=1&accountId=2944742458&queueId=70,72,73,75,76,78,96,98,100,300,310,313,317,318,325,400,420,430,450,460,600,610,940,950,960,980,990,420,440,470,83,800,810,820,830,840,850&r1=matchList",headers=header)
    return r.text.strip("var matchList =")


def spidergamedetail(cookie):
    header = {'Cookie': cookie}
    gameidjson = spdiergameid()  # 爬比赛列表
    if not os.path.exists("./battledetaildata") :
        os.mkdir("./battledetaildata")
    gameid = getgameid(gameidjson)  # 获取gameid list
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
    spdiergameid(cookie)
    spidergamedetail(cookie)
    fl = os.listdir('/battledetaildata')
    map(delaram,fl)


def getchampionname(championid):
    hero = {"1":"Annie","2":"Olaf","3":"Galio","4":"TwistedFate","5":"XinZhao","6":"Urgot","7":"Leblanc","8":"Vladimir","9":"Fiddlesticks","10":"Kayle","11":"MasterYi","12":"Alistar","13":"Ryze","14":"Sion","15":"Sivir","16":"Soraka","17":"Teemo","18":"Tristana","19":"Warwick","20":"Nunu","21":"MissFortune","22":"Ashe","23":"Tryndamere","24":"Jax","25":"Morgana","26":"Zilean","27":"Singed","28":"Evelynn","29":"Twitch","30":"Karthus","31":"Chogath","32":"Amumu","33":"Rammus","34":"Anivia","35":"Shaco","36":"DrMundo","37":"Sona","38":"Kassadin","39":"Irelia","40":"Janna","41":"Gangplank","42":"Corki","43":"Karma","44":"Taric","45":"Veigar","48":"Trundle","50":"Swain","51":"Caitlyn","53":"Blitzcrank","54":"Malphite","55":"Katarina","56":"Nocturne","57":"Maokai","58":"Renekton","59":"JarvanIV","60":"Elise","61":"Orianna","62":"MonkeyKing","63":"Brand","64":"LeeSin","67":"Vayne","68":"Rumble","69":"Cassiopeia","72":"Skarner","74":"Heimerdinger","75":"Nasus","76":"Nidalee","77":"Udyr","78":"Poppy","79":"Gragas","80":"Pantheon","81":"Ezreal","82":"Mordekaiser","83":"Yorick","84":"Akali","85":"Kennen","86":"Garen","89":"Leona","90":"Malzahar","91":"Talon","92":"Riven","96":"KogMaw","98":"Shen","99":"Lux","101":"Xerath","102":"Shyvana","103":"Ahri","104":"Graves","105":"Fizz","106":"Volibear","107":"Rengar","110":"Varus","111":"Nautilus","112":"Viktor","113":"Sejuani","114":"Fiora","115":"Ziggs","117":"Lulu","119":"Draven","120":"Hecarim","121":"Khazix","122":"Darius","126":"Jayce","127":"Lissandra","131":"Diana","133":"Quinn","134":"Syndra","136":"AurelionSol","141":"Kayn","142":"Zoe","143":"Zyra","145":"Kaisa","150":"Gnar","154":"Zac","157":"Yasuo","161":"Velkoz","163":"Taliyah","164":"Camille","201":"Braum","202":"Jhin","203":"Kindred","222":"Jinx","223":"TahmKench","235":"Senna","236":"Lucian","238":"Zed","240":"Kled","245":"Ekko","246":"Qiyana","254":"Vi","266":"Aatrox","267":"Nami","268":"Azir","350":"Yuumi","412":"Thresh","420":"Illaoi","421":"RekSai","427":"Ivern","429":"Kalista","432":"Bard","497":"Rakan","498":"Xayah","516":"Ornn","517":"Sylas","518":"Neeko","523":"Aphelios","555":"Pyke","875":"Sett"}
    return hero[str(championid)]
def transjson( gamejson):

    gamedict = {}
    gameinfo = gamejson['gameInfo']
    gamedict["gameID"] = gameinfo['gameId']
    gamedict["gameVersion"] = gameinfo['gameVersion']
    gamedict["gametime"] = gameinfo["gameStartTimestamp"]//1000
    gamedict['gamelenth'] = gamejson['gameStats']["finalFrameTimestamp"]//1000 - gamedict["gametime"]
    for gamep in gamejson["participants"]:
        try:
            gamedict["username"] = gamep["summonerName"]
            gamedict["champion"] = getchampionname(gamep["championId"])
            gamedict["rating"] = gamep["queueRating"]
            gamedict["teamid"] = gamep["teamId"]
            gamestat = gamep["stats"]
            gamedict["win"] = gamestat["win"]
            gamedict["kills"] = gamestat["kills"]
            gamedict["deaths"] = gamestat["deaths"]
            gamedict["assists"] = gamestat["assists"]
            gamedict["minions"] = gamestat["minionsKilled"]
            gamedict["gold"] = gamestat["goldEarned"]
            gamedict["damage"] = gamestat["totalDamageDealtToChampions"]
            gamedict["wards"] = gamestat["wardsPlaced"]
            gametimeline = gamep["timeline"]
            gamedict["tenmincs"] = gametimeline["creepsPerMinDeltas"]["0-10"]
            gamedict["tenmingold"] = gametimeline["goldPerMinDeltas"]["0-10"]
            gamedict["tenminlanekill"] = gametimeline["assistedLaneKillsPerMinDeltas"]["0-10"]
            if "tinmindiffdamage" in gametimeline:
                gamedict["tinmindiffdamage"] = gametimeline["damageTakenDiffPerMinDeltas"]["0-10"]
            else:
                gamedict["tinmindiffdamage"] = 9999
            if "individualPosition" in gamestat:
                gamedict["position"] = gamestat["individualPosition"]
            else :
                if "SUPPORT" in gametimeline["role"] :
                    gamedict["position"] = "UTILITY"
                elif "CARRY" in gametimeline["role"]:
                    gamedict["position"] = "BOTTOM"
                elif gametimeline["lane"] == "MID":
                    gamedict["position"] = "MIDDLE"
                else:
                    gamedict["position"] = gametimeline["lane"]
            yield gamedict
        except:
            yield False
    return "finish"


class Db:
    def __init__(self,filename):
        self.conn = sqlite3.connect(filename)
        self.c = self.conn.cursor()
    def createtable(self):
        try:
            self.c.execute('''
            CREATE TABLE gamedata(
            ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE ,
            gameID INTEGER ,
            gametime  INTEGER,
            gamelenth INTEGER ,
            gameversion VARCHAR(100),
            username VARCHAR(100) ,
            champion VARCHAR(100),
            rating INTEGER ,
            teamid VARCHAR(10) ,
            win VARCHAR(10),
            kills INTEGER ,
            deaths INTEGER ,
            assists INTEGER ,
            minions INTEGER ,
            gold INTEGER,
            damage INTEGER,
            wards INTEGER ,
            position VARCHAR(10) ,
            tenmindamage INTEGER,
            tenmincs INTEGER ,
            tenmingold INTEGER ,
            tenminlanekill INTEGER ,
            tinmindiffdamage INTEGER 
            )
            ''')
            self.commit()
            return 1
        except:
            return 0

    def insert(self,gamedict):
        sql = "INSERT OR IGNORE INTO  gamedata (gameID,gameversion,gametime,gamelenth,username,champion,rating,teamid,win,kills,deaths,assists,minions,gold,damage,wards,position,tenmincs,tenmingold,tenminlanekill,tinmindiffdamage) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (gamedict['gameID'],gamedict['gameVersion'],gamedict['gametime'],gamedict['gamelenth'],gamedict['username'],gamedict['champion'],gamedict['rating'],gamedict['teamid'],gamedict['win'],gamedict['kills'],gamedict['deaths'],gamedict['assists'],gamedict['minions'],gamedict['gold'],gamedict['damage'],gamedict['wards'],gamedict['position'],gamedict['tenmincs'],gamedict['tenmingold'],gamedict['tenminlanekill'],gamedict['tinmindiffdamage'])
        # print("success")
        self.c.execute(sql)


    def select(self,sql):
        self.c.execute(sql)
        return self.c.fetchall()

    def commit(self):
        self.conn.commit()

    def close(self):

        self.commit()
        self.c.close()


    def run(self):
        self.createtable()
        for file in os.listdir('./battledetaildata'):
            data = json.loads(open("./battledetaildata/%s" % file).read())["msg"]
            datag = transjson(data)
            for data in datag:
                if data:
                    self.insert(data)
            self.commit()



def pad(data,p,u=1,d=1):

    if p+u>maxi:
        data[str(p)] = data[str(p-d)]
        return data
    if str(p+u) not in data:
        pad(data,p,u+1,d)
    elif str(p-d) not in data:
        pad(data,p,u,d+1)
    else:
        data[str(p)] = data[str(p-d)]+data[str(p+u)]
    return data[str(p)]


def stamp2time(stamp):
    return time.strftime("%Y-%m-%d",stamp)

map(lambda x:getindex(x,'asdf'),[1,2,3,4])

def getindex(index,indexdata):
    if index == "gamelenth":
        slices = 60
        mini = 900//slices
        maxi = 2400//slices
    elif index == "gametime":
        slices = 60*60*24*30
        mini = min(indexdata) //slices
        maxi = max(indexdata) //slices
    elif index == "rating":
        slices = 100
        mini = 1000 // slices
        maxi = 2100 // slices
    # elif index == "gameversion":
    #     version = [''.join(i.split('.')[0:2]) for i in indexdata]
    #     mini = min(version)
    #     maxi = max(version)
    #     slices = 1
    else:
        mini = min(indexdata)
        maxi = max(indexdata)
        slices = 1

    return mini,maxi,slices





def statsdata(data):
    tabledata = []
    for un in range(len(data)):
        data[un][0] = list(map(lambda x: x // slices, data[un][0]))  # 将横坐标切片分组
        tabledata.append({str(mini-1):[min(data[un][1])]})
        for i in range(len(data[un][0])): # 将数据以横坐标分段归类
            if data[un][0][i] >= mini and data[un][0][i] <= maxi:
                if str(data[un][0][i]) not in tabledata[un]:
                    tabledata[un][str(data[un][0][i])] = [data[un][1][i]]
                else:
                    tabledata[un][str(data[un][0][i])].append(data[un][1][i])
            # print(i)
        for p in range(mini, maxi + 1):
            if str(p) not in tabledata[un]:
                tabledata[un][str(p)] = pad(tabledata[un],p)
        # print(tabledata)
        tabledata[un].pop(str(mini-1))
    data = ([list(map(lambda x:sum(x)/len(x),[t[str(i)] for i in range(mini,maxi)])) for t in tabledata])
    data = np.array(data).transpose()

    return data


def linedata(data,sstd):
    data = statsdata(data)
    if sstd:

        for i in range(data.shape[1]):
            data[:,i] = data[:,i]/data[:,-1]
        print(data)
    return data


def genlinepic(data,title,pa,smooth=False,sstd=False,save=True):
    data = list(map(np.transpose,data))
    data = linedata(data,sstd=True)
    df = pd.DataFrame(data, index=pd.interval_range(0,maxi-mini, periods=len(data)), columns=users.keys())
    # print(df)
    if smooth:
        df = df.cumsum()
    df.plot(title=title)

    if not os.path.exists("img/%s" % pa) :
        os.mkdir("img/%s" % pa)
    if save:
        plt.savefig("./img/%s/%s.png" % (pa, title))
    else:
        plt.show()


def scatterdata(data):
    data = [list(map(list, d)) for d in data]
    data = list(map(np.array, data))
    return data


def genscatterpic(data,title,pa):
    data = scatterdata(data)
    fig = plt.figure()
    ax = fig.gca()
    gencolor = (x for x in colors)
    genlabel = (x for x in users.keys())
    for d in data:
        df = pd.DataFrame(data=d,columns=[need[0],need[1]])
        ax = df.plot.scatter(x=need[0],y=need[1],color=next(gencolor),label=next(genlabel),s=1,ax=ax)
    df.plot(title=title)
    if os.path.exists("img/%s"%pa) == -2:
        os.mkdir("img/%s"%pa)

    plt.savefig("./img/%s/%s.png"%(pa,title))


def addfilter(sql):
    if filters:
        for k, v in filters.items():
            sql += " AND %s = '%s'" % (k, v)
    return sql


# def gencomsql(u):
#     sql = "SELECT %s FROM gamedata WHERE win<>'Leave' AND win<>'AFK' AND username LIKE '%s'" % (','.join(need), u)
#     sql = addfilter(sql)
#     return sql
def getdbdata(gensql):
    # 工厂函数,尝试使用python新特性

    def getd(user):

        return gensql(user)
    return getd


@getdbdata
def singleuserdata(user):
    res = []
    for u in user:
        sql = "SELECT %s FROM gamedata WHERE win<>'Leave' AND win<>'AFK' AND username LIKE '%s'" % (
        ','.join(need), u)
        sql = addfilter(sql)
        res += db.select(sql)
    return res


def anay(d,user,win):
    # print(d)
    d = list(map(lambda x:x.split(';'),d))
    d[1] = list(map(int,d[1]))
    # print(d)
    if win and d[0][0] in user:
        print(d)
        return [d[1][0]/d[1][-1]]
    elif ~win and d[0][-1] in user:
        return [d[1][0]/d[1][-1]]
    else:
        return []

def getcomparedata():
    res = []
    sql = "SELECT GROUP_CONCAT(username,';'),GROUP_CONCAT(damage,';') FROM gamedata WHERE 1=1"
    sql = addfilter(sql)
    sql += "  GROUP BY gameID ORDER BY win DESC"
    print(sql)
    res = db.select(sql)
    print(len(res))
    return res




if __name__ == '__main__':
    np.set_printoptions(suppress=True)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    db = Db('data.db')
    # db.run()
    users = {'k':["i孤儿院院长i", "只要能赢做楠都行","诗与远方dEsTIny1"],'p':["新建镇镇长","可以垫刀但没必要"],'all':'%'}
    positions = ['TOP','MIDDLE','JUNGLE','BOTTOM','UTILITY']
    # positions = ['MIDDLE']
    # users = {'all':'%'}
    colors = ['b', 'g', 'r','c', 'm', 'y', 'k', 'w']
    # users = [["i孤儿院院长i", "只要能赢做楠都行"]]
    # 伤害图
    for p in ['MIDDLE']:
        need = ['gamelenth', "damage"]
        filters = {'position': p,'champion':'Yasuo'}
        # print(singleuserdata(users['pxn']))
        dataf = getdbdata(singleuserdata)
        # print(dataf)
        data = list(map(dataf,users.values()))
        # print(data)
        mini,maxi,slices = getindex(need[0],[i[0] for i in reduce(add,[i for i in data])])
        genlinepic(data,pa='damage',title="%s Yasuo场均伤害标准差 - 游戏时间图"%p,sstd=True)


    # 补刀图
    # for p in positions:
    #     need = ['gamelenth', "minions"]
    #     filters = {'position': p}
    #     data = list(map(list,getcomparedata()))
    #     # print(anay(data[0], users['pxn'], True))
    #     res = list(map(lambda x:anay(x,users['pxn'],True),data))
    #     res = list(reduce(add,res))
    #     print(res)
    #     mini,maxi,slices = getindex(need[0],[i[0] for i in reduce(add,[i for i in data])])
    #     genlinepic(data,pa='minions',title="%s 场均补刀累计 - 游戏时间图"%p,smooth=True)
        # genlinepic(data,pa='minions',title="%s 场均补刀 - 游戏时间折线图"%p)

    # 方差
    # 游戏在线人数










