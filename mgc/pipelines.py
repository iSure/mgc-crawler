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
            #self.db = MySQLdb.connect(host="localhost", user="root", passwd="Az%2Love-Win", port=3306, db="mgc", charset="utf8")
            self.db = MySQLdb.connect(host="rdsjx6esvsm9g2bw93www.mysql.rds.aliyuncs.com", user="jr_root", passwd="Wyj123456", port=3306, db="db_mgc_test", charset="utf8")
            self.cursor = self.db.cursor()
            print "Connect to db successfully!"
        except:
            print "Fail to connect to db!"

    def process_item(self, item, spider):
        return;
        item['coverPic'] = item['coverPic'].strip()
        if item['title']:
            param = (item['uid'], item['sourceFrom'], item['title'], item['description'], item['category'], item['coverPic'], item['banner'], item['view'], item['comment'], item['collection'], item['source'], item['createTime'], item['author'], item['score'], item['label'])
            sql = "insert into o_news_dummy (`uid`, `from`, `title`, `description`, `category`, `cover_pic`, `banner`, `view`, `comment`, `collection`, `source`, `create_time`, `author`, `score`, `label`) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            if 'o_issue_content_dummy' == item['tableName']:
                param = (item['title'], item['description'], item['coverPic'], item['category'], item['uid'], item['createTime'], item['sourceFrom'], item['source'], item['author'], item['score'], item['label'])
                sql = "insert into o_issue_content_dummy (`title`, `content`, `cover_pic`, `category`, `uid`, `create_time`, `from`, `url`, `author`, `score`, `label`) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            try:
                self.cursor.execute(sql, param)
            except:
                print "Unexpected error:", sys.exc_info()[0]
            if 'o_news_dummy|o_group_post_dummy' == item['tableName']:
                param = (item['title'], item['description'], item['coverPic'], item['uid'], item['createTime'], item['sourceFrom'], item['source'], item['author'], item['score'], item['label'])
                sql = "insert into o_group_post_dummy (`title`, `content`, `cover`, `uid`, `create_time`, `from`, `source`, `author`, `score`, `label`) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                try:
                    self.cursor.execute(sql, param)
                except:
                    print "Unexpected error:", sys.exc_info()[0]
        else:
            raise DropItem(item)

        return item

    def close_spider(self, spider):
        self.db.commit()
        self.db.close
        print("Done")
