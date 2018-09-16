# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MgcItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    uid = scrapy.Field()
    sourceFrom = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
    coverPic = scrapy.Field()
    banner = scrapy.Field()
    view = scrapy.Field()
    comment = scrapy.Field()
    collection = scrapy.Field()
    source = scrapy.Field()
    createTime = scrapy.Field()
    author = scrapy.Field()

    pass
