# encoding: utf-8

import scrapy
from bs4 import BeautifulSoup
import time
import datetime
from mgc.items import MgcItem
import requests
import json

class TeahouseSpider(scrapy.Spider):
    name = "teahouse"

    def __init__(self, category=None, *args, **kwargs):
        super(TeahouseSpider, self).__init__(*args, **kwargs)
        if category:
            self.categoryId = category
        self.start_urls = ['http://www.youxichaguan.com/%s.html' % self.categoryId]

    def parse(self, response):
        soup = BeautifulSoup(response.body)
        newsList = soup.find_all("li", "pbox clr")
        for news in newsList:
            item = MgcItem()
            item['uid'] = 0
            item['sourceFrom'] = "游戏茶馆"
            item['title'] = news.find("h2").a.string

            detailUrl = "http://www.youxichaguan.com/" + news.find("h2").a.get("href")
            item['description'] = ''

            if 'news-2' == self.categoryId:
                item['category'] = "新闻-快讯"
            elif 'news-4' == self.categoryId:
                item['category'] = "新闻-干货"
            elif 'news-5' == self.categoryId:
                item['category'] = "新闻-海外"
            elif 'news-6' == self.categoryId:
                item['category'] = "新闻-数据"
            elif 'news-3' == self.categoryId:
                item['category'] = "新闻-深度"
            else:
                item['category'] = "未知"

            item['coverPic'] = news.find('img').attrs['src']
            item['banner'] = ""
            item['view'] = 0 
            item['comment'] = 0
            item['collection'] = 0
            item['source'] = detailUrl 
            item['createTime'] = (int(time.time()))
            item['score'] = 0
            label = news.find("a", "sort").string
            item['label'] = json.dumps([label])

            nickSpan = news.find("div", "aut").find("span")
            item['author'] = nickSpan.get_text()
            item['tableName'] = 'o_news_dummy|o_group_post_dummy'

            yield item
