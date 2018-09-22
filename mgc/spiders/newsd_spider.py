# encoding: utf-8

import scrapy
from bs4 import BeautifulSoup
import time
import datetime
from mgc.items import MgcItem
import requests

class NewsdSpider(scrapy.Spider):
    name = "newsd"

    def __init__(self, category=None, *args, **kwargs):
        super(NewsdSpider, self).__init__(*args, **kwargs)
        if category:
            self.category = category
        self.start_urls = ['http://news.d.cn/%s' % self.category + '.html']

    def parse(self, response):
        soup = BeautifulSoup(response.body)
        newsList = soup.find("ul", "list-card")
        newsList = newsList.find_all("li")
        for news in newsList:
            item = MgcItem()
            item['uid'] = 0
            item['sourceFrom'] = "当乐网"
            title = news.find("h2")
            item['title'] = title.string 

            detailUrl = "http://news.d.cn" + news.a.get("href")
            res = requests.get(detailUrl)
            res.encoding = 'utf-8'
            descSoup = BeautifulSoup(res.text, "html.parser")
            info = descSoup.find(id="content")
            item['description'] = info

            if 'special' == self.category:
                item['category'] = "专题"
            elif 'evaluation' == self.category:
                item['category'] = "评测"
            else:
                item['category'] = "未知"

            item['coverPic'] = news.find('img').attrs['data-original']
            item['banner'] = ""
            item['view'] = 0 
            item['comment'] = 0
            item['collection'] = 0
            item['source'] = detailUrl 
            item['createTime'] = (int(time.time()))

            nickSpan = news.find("div", "unit w-1-4 hide-on-middle")
            item['author'] = nickSpan.find("img").attrs['alt']

            score = news.find("div", "unit w-3-4 mid-whole")
            scoreSpan = score.find_all("span")
            item['score'] = scoreSpan[1].get_text()

            item['tableName'] = 'o_news_dummy'
            if 'demo wall' == item['category']:
                item['tableName'] = 'o_issue_content_dummy'
            item['label'] = ''

            yield item
