# -*- coding: utf-8 -*-
# scrapy版本爬虫,只需要用scrapy genproject,然后复制到spider目录下即可,其他东西都没做修改
import scrapy
from scrapy import Request
from functools import reduce
from operator import add
import json,os


def transform(cookies):
    cookie_dict = {}
    cookies = cookies.replace(' ','')
    list = cookies.split(';')
    for i in list:
        keys = i.split('=')[0]
        values = i.split('=')[1]
        cookie_dict[keys] = values

    return cookie_dict


class GamejsonspiderSpider(scrapy.Spider):
    name = 'gamejsonspider'
    # accountId 也需要修改
    accountId = 
    start_urls = 'http://lol.sw.game.qq.com/lol/api/?c=Battle&a=matchList&areaId=1&accountId=%s&queueId=70,72,73,75,76,78,96,98,100,300,310,313,317,318,325,400,420,430,450,460,600,610,940,950,960,980,990,420,440,470,83,800,810,820,830,840,850&r1=matchList'%accountId
    Cookie = ""


    def start_requests(self):
        yield Request(url=self.start_urls,cookies=transform(self.Cookie),callback=self.parse)


    def parse(self, response):
        data = str(response.body,encoding='utf-8').strip("var matchList =")
        jsondata = json.loads(data)
        gameids = jsondata["msg"]["games"]
        gameids = reduce(add,map(lambda x: [x["gameId"]],gameids))
        for gameid in gameids:
            url = "https://lol.sw.game.qq.com/lol/api/?c=Battle&a=combatGains&areaId=1&gameId=%s&r1=combatGains"%gameid
            yield Request(url=url,cookies=transform(self.Cookie),callback=self.parsedetail,meta={'gameid':gameid})


    def parsedetail(self,response):
        if not os.path.exists("./battledetaildata"):
            os.mkdir("./battledetaildata")
        data = str(response.body).strip("var combatGains = ")
        datafile = open("./battledetaildata/%s.json" % response.meta['gameid'], 'w')
        print( response.meta['gameid'])
        datafile.write(data)
        datafile.close()



