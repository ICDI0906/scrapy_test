# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymongo
class SohutestPipeline(object):
    def __init__(self):
        # self.writer = open('zhengzhi.json','w',encoding='utf-8')
        self.conn = pymongo.MongoClient('localhost',27017)
        self.db = self.conn.news
    def process_item(self, item, spider):
        # content = json.dumps(dict(item),ensure_ascii=False)+',\n'
        # self.writer.write(content)
        # self.writer.flush()
        self.db.souhu.insert(dict(item))
        return item
