# encoding: utf-8

import scrapy
from bs4 import BeautifulSoup
import time
import datetime
from mgc.items import MgcItem
import requests
import json

class CatpawGameSpider(scrapy.Spider):
    name = "catpaw_game"

    def __init__(self, category=None, *args, **kwargs):
        super(CatpawGameSpider, self).__init__(*args, **kwargs)
        if category:
            self.categoryId = category
        if 'jrltList' == self.categoryId:
            self.start_urls = ['https://www.maozhuar.com/find/jrltList/1/10']
        elif 'dlyxList' == self.categoryId:
            self.start_urls = ['https://www.maozhuar.com/find/dlyxList/1/10']
        elif 'zxgxList' == self.categoryId:
            self.start_urls = ['https://www.maozhuar.com/find/zxgxList']

    def parse(self, response):
        soup = BeautifulSoup(response.body)
        newsList = soup.find_all("div", "header-game game-list")
        for news in newsList:
            item = MgcItem()
            item['uid'] = 0
            item['sourceFrom'] = "猫爪"
            item['title'] = news.find("div", "game-name").find("span").string

            detailUrl = "https://www.maozhuar.com" + news.find("div", "game-name").a.get("href")
            item['description'] = ''

            item['tableName'] = 'o_issue_content_dummy';
            if 'jrltList' == self.categoryId:
                item['category'] = "发现-今日力推"
            elif 'dlyxList' == self.categoryId:
                item['category'] = "发现-独立游戏"
            elif 'zxgxList' == self.categoryId:
                item['category'] = "发现-最近更新"
                item['tableName'] = 'o_news_dummy';
            else:
                item['category'] = "未知"

            item['coverPic'] = news.find('div', 'info-photo').a.img.attrs['src']
            item['banner'] = ""
            item['view'] = 0 
            item['comment'] = 0
            item['collection'] = 0
            item['source'] = detailUrl 
            item['createTime'] = (int(round(1000 * time.time())))
            item['score'] = 0

            labels = []
            labelList = news.find("p", "game-tags wap-gameTag").find_all("a")
            for label in labelList:
                labels.append(label.string)

            item['label'] = json.dumps([label], ensure_ascii=False, encoding='utf-8')
            item['author'] = ''

            yield item
