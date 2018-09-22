# encoding: utf-8

import scrapy
from bs4 import BeautifulSoup
import time
import datetime
from mgc.items import MgcItem
import requests
import json

class GamedogSpider(scrapy.Spider):
    name = "gamedog"

    def __init__(self, category=None, *args, **kwargs):
        super(GamedogSpider, self).__init__(*args, **kwargs)
        if category:
            self.categoryId = category
        self.start_urls = ['http://android.gamedog.cn/%s/' % self.categoryId]

    def parse(self, response):
        soup = BeautifulSoup(response.body)
        newsList = soup.find("div", "list_con").find("ul").find_all("li")
        for news in newsList:
            item = MgcItem()
            item['uid'] = 0
            item['sourceFrom'] = "游戏狗"
            item['title'] = news.find("h2").string

            detailUrl = news.find("a").get("href")
            item['description'] = ''

            if 'online' == self.categoryId:
                item['category'] = "首页安卓网游"
            elif 'game' == self.categoryId:
                item['category'] = "首页安卓单机"
            else:
                item['category'] = "未知"

            item['coverPic'] = news.find('img', 'ol_img').attrs['src']
            item['banner'] = ""
            item['view'] = 0 
            item['comment'] = 0
            item['collection'] = 0
            item['source'] = detailUrl 
            item['createTime'] = (int(time.time()))
            item['score'] = 0
            label = news.find("p", "ol_c").get_text().split("：")[0]
            item['label'] = json.dumps([label])

            item['author'] = '' 
            item['tableName'] = 'o_issue_content_dummy';

            yield item
