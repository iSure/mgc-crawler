# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import sys
import MySQLdb
from scrapy.exceptions import DropItem

class MgcPipeline(object):
    def __init__(self):
        try:
            self.db = MySQLdb.connect(host="localhost", user="root", passwd="Az%2Love-Win", port=3306, db="mgc", charset="utf8")
            self.cursor = self.db.cursor()
            print "Connect to db successfully!"
        except:
            print "Fail to connect to db!"

    def process_item(self, item, spider):
        if item['title']:
            param = (item['uid'], item['sourceFrom'], item['title'], item['description'], item['category'], item['coverPic'], item['banner'], item['view'], item['comment'], item['collection'], item['source'], item['createTime'], item['author'])
            sql = "insert into o_news_dummy (`uid`, `from`, `title`, `description`, `category`, `cover_pic`, `banner`, `view`, `comment`, `collection`, `source`, `create_time`, `author`) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            if 'o_issue_content_dummy' == item['tableName']:
                param = (item['title'], item['description'], item['coverPic'], item['category'], item['uid'], item['createTime'], item['sourceFrom'], item['source'], item['author'])
                sql = "insert into o_issue_content_dummy (`title`, `content`, `cover_pic`, `category`, `uid`, `create_time`, `from`, `url`, `author`) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            print sql
            self.cursor.execute(sql, param)
        else:
            raise DropItem(item)

        return item

    def close_spider(self, spider):
        self.db.commit()
        self.db.close
        print("Done")
