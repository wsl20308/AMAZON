# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class CustomPipeline(object):
    def __init__(self,host,port,user,pwd,db,table):
        self.host=host
        self.port=port
        self.user=user
        self.pwd=pwd
        self.db=db
        self.table=table

    @classmethod
    def from_crawler(cls, crawler):
        """
        Scrapy会先通过getattr判断我们是否自定义了from_crawler,有则调它来完
        成实例化
        """
        HOST = crawler.settings.get('HOST')
        PORT = crawler.settings.get('PORT')
        USER = crawler.settings.get('USER')
        PWD = crawler.settings.get('PWD')
        DB = crawler.settings.get('DB')
        TABLE = crawler.settings.get('TABLE')
        return cls(HOST,PORT,USER,PWD,DB,TABLE)

    def open_spider(self,spider):
        """
        爬虫刚启动时执行一次
        """
        self.client = MongoClient('mongodb://%s:%s@%s:%s' %(self.user,self.pwd,self.host,self.port))

    def close_spider(self,spider):
        """
        爬虫关闭时执行一次
        """
        self.client.close()


    def process_item(self, item, spider):
        # 操作并进行持久化

        d=dict(item)
        if all(d.values()):
            self.client[self.db][self.table].save(d)