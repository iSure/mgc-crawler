# encoding: utf-8

import scrapy
from bs4 import BeautifulSoup
import time
import datetime
from mgc.items import MgcItem
import requests

class CatpawSpider(scrapy.Spider):
    name = "catpaw"

    def __init__(self, category=None, *args, **kwargs):
        super(CatpawSpider, self).__init__(*args, **kwargs)
        if category:
            self.categoryId = category
        if 'topiclist' == self.categoryId:
            self.start_urls = ['https://www.maozhuar.com/topic/topiclist']

    def parse(self, response):
        soup = BeautifulSoup(response.body)
        newsList = soup.find_all("div", "themeone")
        for news in newsList:
            item = MgcItem()
            item['uid'] = 0
            item['sourceFrom'] = "猫爪"
            item['title'] = news.find("h3").string

            detailUrl = "https://www.maozhuar.com/share/zhuti/" + news.get("data-val")
            item['description'] = ''

            if 'topiclist' == self.categoryId:
                item['category'] = "热门主题-资讯趣闻"
                item['tableName'] = 'o_news_dummy';
            else:
                item['category'] = "未知"

            item['coverPic'] = news.find('div', 'gamepic').img.attrs['src']
            item['banner'] = ""
            item['view'] = 0 
            item['comment'] = 0
            item['collection'] = 0
            item['source'] = detailUrl 
            item['createTime'] = (int(time.time()))
            item['score'] = 0
            item['label'] = ''

            item['author'] = news.find("div", "displayFlex align-center").find("p").string

            yield item
