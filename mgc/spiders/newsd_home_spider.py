# encoding: utf-8

import scrapy
from bs4 import BeautifulSoup
import time
import datetime
from mgc.items import MgcItem
import requests

class NewsdHomeSpider(scrapy.Spider):
    name = "newsd_home"

    start_urls = ['http://www.d.cn/']

    def parse(self, response):
        soup = BeautifulSoup(response.body)
        newsList = soup.find("section", "news-list")
        newsList = newsList.find_all("ul")
        index = 0
        for newsL in newsList:
            item = MgcItem()
            if 0 == index:
                item['category'] = "头条"
            elif 1 == index:
                item['category'] = "头条"
            else:
                item['category'] = "未知"
            newsL = newsL.find_all("li")
            for news in newsL:
                item['uid'] = 0
                item['sourceFrom'] = "当乐网"
                item['title'] = news.find("h4").string

                detailUrl = news.a.get("href")
                res = requests.get(detailUrl)
                res.encoding = 'utf-8'
                descSoup = BeautifulSoup(res.text, "html.parser")
                info = descSoup.find(id="content")
                item['description'] = info
                #item['description'] = ''

                item['coverPic'] = '' 
                item['banner'] = ""
                item['view'] = 0 
                item['comment'] = 0
                item['collection'] = 0
                item['source'] = detailUrl 
                item['createTime'] = (int(round(1000 * time.time())))

                author = descSoup.find("article")
                item['author'] = author.find("a", "hover").string

                item['score'] = 0

                item['tableName'] = 'o_news_dummy|o_group_post_dummy'
                item['label'] = ''

                yield item
