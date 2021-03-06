# encoding: utf-8

import scrapy
from bs4 import BeautifulSoup
import time
import datetime
from mgc.items import MgcItem
import requests
import json

class TaptapSpider(scrapy.Spider):
    name = "taptap"

    def __init__(self, category=None, *args, **kwargs):
        super(TaptapSpider, self).__init__(*args, **kwargs)
        if category:
            self.categoryId = category
        self.start_urls = ['https://www.taptap.com/category/%s' % self.categoryId]

    def parse(self, response):
        soup = BeautifulSoup(response.body)
        newsList = soup.find_all("div", "taptap-app-item")
        for news in newsList:
            item = MgcItem()
            item['uid'] = 0
            item['sourceFrom'] = "taptap"
            item['title'] = news.find("img").attrs['alt']

            detailUrl = news.a.get("href")
            '''res = requests.get(detailUrl)
            res.encoding = 'utf-8'
            descSoup = BeautifulSoup(res.text, "html.parser")
            info = descSoup.find("div", "index-info")'''
            item['description'] = '' 

            if 'e386' == self.categoryId:
                item['category'] = "发现-游戏测试"
            elif 'e420' == self.categoryId:
                item['category'] = "发现-最新更新"
            else:
                item['category'] = "未知"

            item['coverPic'] = news.a.img.attrs['data-src']
            item['banner'] = ""
            item['view'] = 0 
            item['comment'] = 0
            item['collection'] = 0
            item['source'] = detailUrl 
            item['createTime'] = (int(round(1000 * time.time())))
            item['score'] = 0

            item['author'] = '' 
            item['tableName'] = 'o_issue_content_dummy';
            if 'e420' == self.categoryId:
                item['tableName'] = 'o_news_dummy';
            
            label = news.find("span", "item-caption-label").a.string
            item['label'] = json.dumps([label], ensure_ascii=False, encoding='utf-8')

            yield item
