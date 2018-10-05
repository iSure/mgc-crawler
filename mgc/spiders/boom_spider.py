# encoding: utf-8

import scrapy
from bs4 import BeautifulSoup
import time
import datetime
from mgc.items import MgcItem
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

class BoomSpider(scrapy.Spider):
    name = "boom"

    start_urls = [
        'https://xw.qq.com/m/author?aid=oCOnkjrOYvdCILtJsrehk2T3nrko',
    ]
   
    def __init__(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.browser = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=options)
        #self.browser.implicitly_wait(10)

    def __del__(self):
        self.browser.close()

    '''def start_requests(self):
        for url in self.start_urls:
            yield self.browser.get(url)'''

    def parse(self, response):
        #soup = BeautifulSoup(response.body)
        self.browser.get(response.url)
        #sleep(10)
        soup = BeautifulSoup(self.browser.page_source, 'lxml')
        newsList = soup.find_all("div", "jsx-1440870285")
        for news in newsList:
            print news
            item = MgcItem()
            item['uid'] = 0
            item['sourceFrom'] = "手游龙虎豹"
            item['title'] = news.find("div", "title-inner").string

            detailUrl = "https://xw.qq.com" + news.find("a", "link").get("href")
            '''res = requests.get(detailUrl)
            res.encoding = 'utf-8'
            descSoup = BeautifulSoup(res.text, "html.parser")
            info = descSoup.find("div", "index-info")
            item['description'] = info'''
            item['description'] = ''

            item['category'] = "公众号首条内容"

            item['coverPic'] = news.find('img').attrs['src']
            item['banner'] = ""
            item['view'] = 0 
            item['comment'] = 0
            item['collection'] = 0
            item['source'] = detailUrl 
            item['createTime'] = (int(round(1000 * time.time())))
            item['score'] = 0
            item['label'] = ''

            item['author'] = ''
            item['tableName'] = 'o_news_dummy';

            yield item
            break;
