# encoding: utf-8

import scrapy
from bs4 import BeautifulSoup
import time
import datetime
from mgc.items import MgcItem
import requests

class GrapesSpider(scrapy.Spider):
    name = "grapes"

    '''start_urls = [
        'http://youxiputao.com/article/index/id/16',
    ]'''

    def __init__(self, category=None, *args, **kwargs):
        super(GrapesSpider, self).__init__(*args, **kwargs)
        if category:
            print 'i come in category id'
            self.categoryId = category
        self.start_urls = ['http://youxiputao.com/article/index/id/%s' % self.categoryId]

    def parse(self, response):
        soup = BeautifulSoup(response.body)
        newsList = soup.find_all("div", "news-info-box")
        for news in newsList:
            item = MgcItem()
            item['uid'] = 0
            item['sourceFrom'] = "游戏葡萄"
            item['title'] = news.div.h4.a.attrs['title']

            detailUrl = "http://youxiputao.com" + news.a.get("href")
            res = requests.get(detailUrl)
            res.encoding = 'utf-8'
            descSoup = BeautifulSoup(res.text, "html.parser")
            info = descSoup.find("div", "index-info")
            item['description'] = info 

            print self.categoryId
            if '16' == self.categoryId:
                item['category'] = "酷玩"
            elif '14' == self.categoryId:
                item['category'] = "资讯"
            elif '17' == self.categoryId:
                item['category'] = "海外"
            elif '13' == self.categoryId:
                item['category'] = "深度"
            elif '15' == self.categoryId:
                item['category'] = "demo wall"
            else:
                item['category'] = "未知"

            item['coverPic'] = news.find('img').attrs['src']
            item['banner'] = ""
            item['view'] = 0 
            item['comment'] = 0
            item['collection'] = 0
            item['source'] = 'http://youxiputao.com/article/index/id/' + self.categoryId
            item['createTime'] = (int(time.time()))

            nickSpan = news.find("span", "pull-right")
            nickTime = nickSpan.get_text()
            item['author'] = nickTime.split("·")[0]

            yield item
